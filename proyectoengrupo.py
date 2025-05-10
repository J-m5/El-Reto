import cv2
import base64
import requests
import json

# Paso 1: Capturar una imagen con la cámara web
def capture_image():
    # Inicializar la cámara
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: No se pudo abrir la cámara.")
        return None

    # Capturar una imagen
    ret, frame = cap.read()
    if not ret:
        print("Error: No se pudo capturar la imagen.")
        cap.release()
        return None

    # Guardar la imagen en un archivo
    image_path = "captured_image.jpg"
    cv2.imwrite(image_path, frame)
    cap.release()
    return image_path

# Paso 2: Utilizar la API de Clarifai para la detección de personas
def detect_person(image_path, api_key):
    # URL de la API de Clarifai
    url = "https://api.clarifai.com/v2/models/aaa03c23b3724a16a56b629203edc62c/versions/aa7f35c01e0642fda5cf400f54367208/outputs"

    # Preparar los datos para la solicitud
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    data = {
        "inputs": [
            {
                "data": {
                    "image": {
                        "base64": ""
                    }
                }
            }
        ]
    }

    # Leer la imagen y codificarla en base64
    with open(image_path, "rb") as image_file:
        encoded_image = base64.b64encode(image_file.read()).decode("utf-8")
        data["inputs"][0]["data"]["image"]["base64"] = encoded_image

    # Realizar la solicitud a la API
    response = requests.post(url, headers=headers, data=json.dumps(data))
    response_data = response.json()

    # Procesar la respuesta
    if response.status_code == 200:
        concepts = response_data["outputs"][0]["data"]["concepts"]
        for concept in concepts:
            if concept["name"] == "person" and concept["value"] > 0.5:
                return True
        return False
    else:
        print(f"Error en la solicitud a Clarifai: {response.status_code}")
        print(response_data)
        return None

# Paso 3: Mostrar el resultado de la detección
def main():
    # Capturar una imagen
    image_path = capture_image()
    if image_path is None:
        print("No se pudo capturar la imagen.")
        return

    # API key de Clarifai (reemplaza con tu propia API key)
    api_key = "geofrey1822"

    # Detectar personas en la imagen
    person_detected = detect_person(image_path, api_key)
    if person_detected is None:
        print("No se pudo determinar si hay una persona en la imagen.")
    elif person_detected:
        print("Se detectó una persona en la imagen.")
    else:
        print("No se detectó ninguna persona en la imagen.")

if __name__ == "__main__":
    main()
