import cv2
import mediapipe as mp
from pynput.keyboard import Key, Controller
from collections import deque

#this is beta version ths dosent include combo attacks made for fun (cuz i enjoyed the movie robo boxing so much)havefun!
# - Punch  -> tap 'x'
# - Jump   -> tap space
# - Turn   -> hold 'a' (left) / 'd' (right)

# ---------- Config ----------
PUNCH_THRESH_X = 0.20        # wrist-shoulder horizontal distance
JUMP_DELTA_Y   = 0.20        # upward change of shoulder-center
TURN_ON_Z      = 0.40        # z diff to engage left/right
TURN_OFF_Z     = 0.20        # z diff to disengage (hysteresis)
SMOOTH_N       = 5           # moving window size for smoothing
PUNCH_COOLDOWN = 10          # frames
JUMP_COOLDOWN  = 20          # frames

#used mediapipe for body points detection and open cv to take live input
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)
mp_draw = mp.solutions.drawing_utils

keyboard = Controller()

cap = cv2.VideoCapture(0)
if not cap.isOpened():
    raise RuntimeError("Webcam not found.")

# Smoothing buffers
shoulder_y_buf = deque(maxlen=SMOOTH_N)
z_diff_buf = deque(maxlen=SMOOTH_N)

# States
punch_cd = 0
jump_cd = 0
turn_state = "center"  # left/right/center
last_shoulder_y = None

def moving_avg(buf):
    return sum(buf) / len(buf) if buf else 0.0

def press_and_release(key):
    keyboard.press(key)
    keyboard.release(key)

def release_turn_keys():
    try:
        keyboard.release('a')
    except: pass
    try:
        keyboard.release('d')
    except: pass
print("ESC to exit. ")

try:
    while True:
        ok, frame = cap.read()
        if not ok:
            continue

        # Mirror + RGB
        image = cv2.cvtColor(cv2.flip(frame, 1), cv2.COLOR_BGR2RGB)
        image.flags.writeable = False
        results = pose.process(image)
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        if results.pose_landmarks:
            # Draw landmarks
            mp_draw.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

            lms = results.pose_landmarks.landmark
            r_wrist = lms[mp_pose.PoseLandmark.RIGHT_WRIST]
            l_wrist = lms[mp_pose.PoseLandmark.LEFT_WRIST]
            r_sh = lms[mp_pose.PoseLandmark.RIGHT_SHOULDER]
            l_sh = lms[mp_pose.PoseLandmark.LEFT_SHOULDER]

            # ----- Smoothing inputs -----
            shoulder_center_y = (r_sh.y + l_sh.y) / 2.0
            shoulder_y_buf.append(shoulder_center_y)
            shoulder_y_sm = moving_avg(shoulder_y_buf)

            z_diff = r_sh.z - l_sh.z  # +ve => right shoulder deeper
            z_diff_buf.append(z_diff)
            z_diff_sm = moving_avg(z_diff_buf)

            # ----- Punch (single tap) -----
            if punch_cd == 0:
                right_dx = abs(r_wrist.x - r_sh.x)
                left_dx = abs(l_wrist.x - l_sh.x)
                if right_dx > PUNCH_THRESH_X or left_dx > PUNCH_THRESH_X:
                    cv2.putText(image, "PUNCH", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)
                    press_and_release('x')
                    punch_cd = PUNCH_COOLDOWN

            # ----- Jump (single tap when shoulder moves up) -----
            if last_shoulder_y is not None and jump_cd == 0:
                delta_up = last_shoulder_y - shoulder_y_sm
                if delta_up > JUMP_DELTA_Y:
                    cv2.putText(image, "JUMP", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)
                    press_and_release(Key.space)
                    jump_cd = JUMP_COOLDOWN
            last_shoulder_y = shoulder_y_sm

            # ----- Turn (held a/d with hysteresis) -----
            new_state = turn_state
            if turn_state == "center":
                if z_diff_sm < -TURN_ON_Z:
                    new_state = "left"
                elif z_diff_sm > TURN_ON_Z:
                    new_state = "right"
            elif turn_state == "left":
                if abs(z_diff_sm) < TURN_OFF_Z or z_diff_sm > TURN_ON_Z:
                    new_state = "center"
            elif turn_state == "right":
                if abs(z_diff_sm) < TURN_OFF_Z or z_diff_sm < -TURN_ON_Z:
                    new_state = "center"

            if new_state != turn_state:
                # release previous
                if turn_state == "left":
                    keyboard.release('a')
                elif turn_state == "right":
                    keyboard.release('d')

                # press new
                if new_state == "left":
                    keyboard.press('a')
                    cv2.putText(image, "TURN LEFT", (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)
                elif new_state == "right":
                    keyboard.press('d')
                    cv2.putText(image, "TURN RIGHT", (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)
                else:
                    cv2.putText(image, "CENTER", (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)

                turn_state = new_state

            # ----- cooldowns -----
            if punch_cd > 0: punch_cd -= 1
            if jump_cd > 0: jump_cd -= 1

        # UI overlay
        cv2.putText(image, "ESC to quit", (10, image.shape[0]-10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,255,255), 1)
        cv2.imshow("Gesture Controller", image)

        if cv2.waitKey(5) & 0xFF == 27:
            break

finally:
    # Cleanup
    release_turn_keys()
    cap.release()
    cv2.destroyAllWindows()
