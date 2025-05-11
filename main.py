import pyautogui
import cv2
import numpy as np
import keyboard
from screen_functions import rgb_to_hsv, detect_color_areas, save_detected_area, save_question_band
from ai_answering import extract_text_from_screenshots, send_to_chatgpt, extract_question_from_screenshot

def take_screenshot():
    """Capture l'écran entier."""
    screenshot = pyautogui.screenshot()
    return np.array(screenshot)

def main():
    # Attendre pour ouvrir l'application
    while True:
        try:
            if keyboard.is_pressed("ctrl+alt+a"):
    
    # Capture l'écran
                screenshot = take_screenshot()
                screenshot_bgr = cv2.cvtColor(screenshot, cv2.COLOR_RGB2BGR)
                
                # Vos couleurs exactes en RGB
                colors_rgb = {
                    "red": (208, 53, 66),
                    "yellow": (207, 160, 53),
                    "blue": (48, 102, 199),
                    "green": (70, 135, 41)
                }
                
                # Convertir les couleurs RGB en HSV avec une tolérance
                tolerance = 10
                colors_hsv = {
                    name: {
                        "lower": np.array(rgb_to_hsv(rgb) - np.array([tolerance, 40, 40]), dtype=np.uint8),
                        "upper": np.array(rgb_to_hsv(rgb) + np.array([tolerance, 40, 40]), dtype=np.uint8)
                    }
                    for name, rgb in colors_rgb.items()
                }
                
                # Détection et sauvegarde
                for color_name, hsv_range in colors_hsv.items():
                    rectangles = detect_color_areas(screenshot_bgr, hsv_range["lower"], hsv_range["upper"], min_size=(50, 50))
                    
                    for i, rect in enumerate(rectangles):
                        filename = f"screenshots/{color_name}_{i}.png"
                        save_detected_area(screenshot_bgr, rect, filename)
                        print(f"Zone {color_name} enregistrée dans {filename}")


                save_question_band(screenshot_bgr, "screenshots/question.png")

                question_text_raw = extract_question_from_screenshot()
                question_text = question_text_raw.split('?')[0] + '?'
                print(f"Question extraite: {question_text}")
                        
                
                extracted_answers = extract_text_from_screenshots()

                # Si des réponses sont extraites, envoyer le prompt à ChatGPT
                if extracted_answers:
                    #question_text = "Which architectural style is best for organizing a system into layers, with each layer providing a set of services ?"
                    send_to_chatgpt(question_text, extracted_answers)
        except KeyboardInterrupt:
            break



if __name__ == "__main__":
    main()
