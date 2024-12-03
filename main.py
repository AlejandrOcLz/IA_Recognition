import os
import base64
import face_recognition
from flask import Flask, request, jsonify

app = Flask(__name__)

# Ruta donde se guardarán las imágenes
IMAGE_STORAGE_PATH = "./user_images/"
os.makedirs(IMAGE_STORAGE_PATH, exist_ok=True)

PROPERTIES_FILE = "./user_data.properties"

# Función para guardar los datos en un archivo .properties
def save_user_data(user_id, image_filename):
    with open(PROPERTIES_FILE, 'a') as file:
        file.write(f"{user_id}={image_filename}\n")

# Función para cargar las imágenes y codificarlas en características faciales
def load_face_encodings(image_path):
    image = face_recognition.load_image_file(image_path)
    face_encoding = face_recognition.face_encodings(image)
    return face_encoding[0] if face_encoding else None

@app.route('/', methods=['GET'])
def Acceso():
    return jsonify({
        "message": "Welcome to the IA FaceRecognition From Alejandro"
    }), 200

@app.route('/register', methods=['POST'])
def register_user():
    try:
        # Obtener los datos del cuerpo de la solicitud en formato JSON
        data = request.get_json()

        # Extraer user_id e imagen (en formato base64) del JSON
        user_id = data.get("user_id")
        image_data = data.get("image")

        # Validar que ambos campos están presentes
        if not user_id or not image_data:
            return jsonify({"error": "user_id or image is missing"}), 400

        # Decodificar la imagen base64 (ignora encabezado como 'data:image/jpeg;base64,')
        image_bytes = base64.b64decode(image_data.split(",")[1])

        # Crear un nombre de archivo único usando el user_id, sin extensión en el nombre
        image_filename = f"{user_id}.jpg"
        image_path = os.path.join(IMAGE_STORAGE_PATH, image_filename)

        # Guardar la imagen en el servidor
        with open(image_path, "wb") as image_file:
            image_file.write(image_bytes)

        # Guardar los datos en el archivo .properties
        save_user_data(user_id, image_filename)

        # Responder con un mensaje de éxito
        return jsonify({
            "message": "User registered successfully",
            "user_id": user_id,
            "image_path": image_path
        }), 200

    except Exception as e:
        # Manejo de errores
        return jsonify({"error": str(e)}), 500

@app.route('/identify', methods=['POST'])
def identify_user():
    try:
        # Obtener los datos del cuerpo de la solicitud en formato JSON
        data = request.get_json()

        # Extraer la imagen de la solicitud
        image_data = data.get("image")

        if not image_data:
            return jsonify({"error": "No image provided"}), 400

        # Decodificar la imagen base64 (ignora encabezado como 'data:image/jpeg;base64,')
        image_bytes = base64.b64decode(image_data.split(",")[1])

        # Guardar la imagen temporalmente
        temp_image_path = "./temp_image.jpg"
        with open(temp_image_path, "wb") as image_file:
            image_file.write(image_bytes)

        # Codificar las características faciales de la imagen recibida
        unknown_face_encoding = load_face_encodings(temp_image_path)

        if unknown_face_encoding is None:
            return jsonify({"error": "No face found in the provided image"}), 400

        # Leer los datos del archivo .properties
        with open(PROPERTIES_FILE, 'r') as file:
            lines = file.readlines()

        # Comparar la imagen con las imágenes guardadas
        for line in lines:
            user_id, saved_image_filename = line.strip().split('=')

            saved_image_path = os.path.join(IMAGE_STORAGE_PATH, saved_image_filename)

            # Cargar la imagen guardada y codificar sus características faciales
            saved_face_encoding = load_face_encodings(saved_image_path)

            if saved_face_encoding is None:
                continue  # Si no se encuentra rostro en la imagen guardada, saltar

            # Comparar las características faciales
            face_match = face_recognition.compare_faces([saved_face_encoding], unknown_face_encoding)

            if face_match[0]:
                return jsonify({"message": f"{user_id}"}), 200

        return jsonify({"message": "No match found"}), 404

    except Exception as e:
        # Manejo de errores
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    #app.run(debug=True)
    app.run(host="0.0.0.0", port=5000, debug=True)
