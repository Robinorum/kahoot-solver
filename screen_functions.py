import cv2
import numpy as np


def rgb_to_hsv(rgb_color):
    """Convertit une couleur RGB en HSV."""
    rgb_np = np.uint8([[rgb_color]])
    hsv_np = cv2.cvtColor(rgb_np, cv2.COLOR_RGB2HSV)
    return hsv_np[0][0]

def detect_color_areas(image, lower_color, upper_color, min_size=(100, 100)):
    """Détecte une zone dans une image correspondant à une couleur spécifique."""
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv_image, lower_color, upper_color)
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Filtrer les petits objets
    min_width, min_height = min_size
    rectangles = [
        cv2.boundingRect(contour)
        for contour in contours
        if cv2.boundingRect(contour)[2] >= min_width and cv2.boundingRect(contour)[3] >= min_height
    ]
    return rectangles

def save_detected_area(image, rect, filename):
    """Enregistre une zone spécifique de l'image."""
    x, y, w, h = rect
    cropped = image[y:y+h, x:x+w]
    cv2.imwrite(filename, cropped)


def save_question_band(image, filename):
    """
    Enregistre une bande horizontale partant du milieu de l'écran jusqu'à 300 pixels en dessous.
    
    Args:
        image: L'image source (capture d'écran complète).
        filename: Le nom du fichier pour enregistrer la bande.
    """
    height, width, _ = image.shape

    # Calculer les dimensions de la bande
    x = 0
    y = height // 2
    w = width
    h = min(300, height - y)  # S'assurer de ne pas dépasser les limites de l'écran

    # Découper la bande
    cropped = image[y:y+h, x:x+w]

    # Sauvegarder l'image découpée
    cv2.imwrite(filename, cropped)
    print(f"Bande enregistrée dans {filename}")







