import pyautogui
import cv2
import numpy as np
import keyboard
from ultralytics import YOLO
import tempfile
import os
from answer_gemini import answer_gemini



model_path = 'yolov8s_best.pt'
model = YOLO(model_path)

def take_screenshot():
    screenshot = pyautogui.screenshot()
    screenshot = np.array(screenshot)
    screenshot = cv2.cvtColor(screenshot, cv2.COLOR_RGB2BGR)
    return screenshot

def main():
    print("en attente de ctrl+alt+a")
    
    while True:
        try:
            if keyboard.is_pressed("ctrl+alt+a"):

                if os.path.exists("screenshot"):
                    for file in os.listdir("screenshot"):
                        os.remove(os.path.join("screenshot", file))

                screenshot = take_screenshot()

                with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as tmp:
                    cv2.imwrite(tmp.name, screenshot)
                    tmp_path = tmp.name

                results = model.predict(tmp_path)
                result = results[0]

                os.makedirs("screenshot", exist_ok=True)

                for i, box in enumerate(result.boxes):
                    x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
                    cropped_box = screenshot[int(y1):int(y2), int(x1):int(x2)]
                    cv2.imwrite(f'screenshot/box_{i}.jpg', cropped_box)

                os.remove(tmp_path)

                answer_gemini()



        except KeyboardInterrupt:
            break



if __name__ == "__main__":
    main()
