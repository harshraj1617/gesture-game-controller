# 🎮 Gesture Game Controller  

Hey everyone! 👋  

I’ve built a **gesture-controlled game controller** using **Python, OpenCV, and MediaPipe**.  
With just your body movements, you can play many types of games that use basic keyboard controls.  

Currently, the controller maps:  
- 👊 **Punch** → `X` (Attack)  
- ⬅️ **Turn Left** → `A` (Move Left)  
- ➡️ **Turn Right** → `D` (Move Right)  
- ⬆️ **Jump** → `Space`  

So, any game that accepts these keyboard inputs can be played using this system.  



## 🚀 Features
- Real-time gesture tracking using **MediaPipe Pose**  
- Maps body gestures directly to keyboard inputs  
- Simple, lightweight, and works on most systems  
- Can be extended for more complex controls  



## 🧠 Future Improvements
This is the **first version**, and it’s purely **rule-based** (no ML yet).  
If you want to improve accuracy for your setup:  
1. Use the provided scripts to collect gesture data from your own webcam.  
2. Train a custom ML model on your dataset.  
3. Replace the rule-based system with the trained model for better robustness.  

This way, the controller adapts to your environment and gives much higher accuracy.  



## 🎥 Inspiration
The idea comes from my fascination with the movie **Real Steel 🤖** (2011).  
As a teenager, I was amazed at the concept of controlling robots through human gestures.  
Now, more than 14 years later, technologies like **Computer Vision** and **MediaPipe** make it possible to simulate that dream with just a few lines of code.  

What once looked like “alien tech” now runs on my laptop..and that’s fascinating!  
One of my favourite movie though...


## 🛠️ Technologies Used
- [Python](https://www.python.org/)  
- [OpenCV](https://opencv.org/)  
- [MediaPipe](https://developers.google.com/mediapipe)  
- [pynput](https://pypi.org/project/pynput/)  



## ⚡ Getting Started  

### 1. Clone this repository
```bash
git clone https://github.com/your-username/gesture-game-controller.git
cd gesture-game-controller
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the controller
```bash
python controller.py
```



## 📌 Notes
- Works best in a well-lit environment with clear body visibility.  
- Games must accept `X`, `A`, `D`, and `Space` as inputs.  
- You can tweak thresholds in the code to suit your movements.  



## 📜 License
This project is licensed under the **MIT License** — feel free to use, modify, and share with credit.  


## 🤝 Contributing
Pull requests are welcome! For major changes, please open an issue first to discuss what you’d like to change.  



## ✨ Demo  
added in the repo feel free tocheck thast
