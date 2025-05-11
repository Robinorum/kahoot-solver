import os
import tkinter as tk
from tkinter import messagebox
import cv2
import pytesseract
import openai


def extract_text_from_screenshots():
    """Extrait le texte de toutes les images dans le dossier 'screenshots' et retourne les réponses sous un format structuré."""
    
    folder = "screenshots"
    responses = {}

    # Lister tous les fichiers dans le dossier 'screenshots'
    screenshot_files = [f for f in os.listdir(folder) if f.endswith('.png')]
    
    # Extraire et afficher le texte pour chaque image
    for filename in screenshot_files:
        # Charger l'image
        image_path = os.path.join(folder, filename)
        image = cv2.imread(image_path)
        
        # Utiliser pytesseract pour extraire le texte
        extracted_text = pytesseract.image_to_string(image, config='--psm 6')  # Utilisation du mode adapté pour une seule zone de texte
        
        # Identifier la couleur à partir du nom du fichier
        if "red" in filename.lower():
            responses["Red answer"] = extracted_text.strip()
        elif "blue" in filename.lower():
            responses["Blue answer"] = extracted_text.strip()
        elif "yellow" in filename.lower():
            responses["Yellow answer"] = extracted_text.strip()
        elif "green" in filename.lower():
            responses["Green answer"] = extracted_text.strip()

    # Retourner les réponses sous forme structurée
    return responses




def extract_question_from_screenshot():
    """Extrait le texte de l'image 'question.png' et retourne le texte extrait."""
    
    image_path = os.path.join("screenshots", "question.png")
    
    # Vérifier si le fichier existe
    if not os.path.exists(image_path):
        return "Le fichier 'question.png' n'existe pas dans le dossier 'screenshots'."
    
    # Charger l'image
    image = cv2.imread(image_path)
    
    # Utiliser pytesseract pour extraire le texte
    extracted_text = pytesseract.image_to_string(image, config='--psm 6')  # Utilisation du mode adapté pour une seule zone de texte
    
    return extracted_text.strip()




def send_to_chatgpt(question, extracted_answers):
    """Envoie le prompt à ChatGPT avec la question et les réponses extraites."""
    # Construire le prompt pour l'API ChatGPT
    prompt = f"I have a Kahoot with software engineering questions. This is the question: {question}.\n"
    prompt += f"And these are the choices I have: {extracted_answers}"
    prompt += f"What is the correct answer?"

    # Utiliser l'API OpenAI pour envoyer le prompt
    try:
        openai.api_key = ""
        
        reponse = openai.chat.completions.create(
            messages=[{
                "role": "user",
                "content": prompt,
            }],
            model="gpt-4",  # Ou "gpt-3.5-turbo" si vous préférez
        )
        
        print("ChatGPT answer:")
        print(reponse.choices[0].message.content)
        #tk.messagebox.showinfo(reponse.choices[0].message.content)

    except Exception as e:
        print(f"Erreur lors de l'envoi à ChatGPT: {e}")