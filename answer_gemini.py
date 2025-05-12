import pytesseract
from PIL import Image
import os
import google.generativeai as genai


genai.configure(api_key="")

def extract_text_from_image(image_path):
    image = Image.open(image_path)
    text = pytesseract.image_to_string(image, lang='eng')
    return text.strip()

def answer_gemini():
    files = sorted(os.listdir("screenshot"), key=lambda x: int(x.split('_')[1].split('.')[0]))
    if len(files) < 5:
        print("Pas assez de captures pour répondre.")
        return

    
    responses = [extract_text_from_image(f"screenshot/{files[i]}") for i in range(4)]
    question = extract_text_from_image(f"screenshot/{files[4]}")

    
    prompt = f"""Voici une question extraite d'un quiz, avec quatre propositions de réponse.

Question : {question}

Réponses possibles :
A. {responses[0]}
B. {responses[1]}
C. {responses[2]}
D. {responses[3]}

Quelle est la bonne réponse ? Réponds uniquement avec la lettre correspondante, et réecrit la bonne reponse."""

    model = genai.GenerativeModel('gemini-2.0-flash')
    response = model.generate_content(prompt)
    print("Réponse de Gemini :", response.text)
