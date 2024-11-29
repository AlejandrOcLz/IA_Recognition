# IA_Recognition

# ---------------------------------------Dependencias---------------------------------------------------------------
Python: 3.8
PIP: 22.3.1
dlib: 19.24.6
pillow: 10.4.0
opencv-python: 4.10.0.84
flask: 3.0.3
face_recognition: 1.3.0
face-recognition-util: 0.1.2
face-recognition-model: 0.3.0


# --------------------------------------------API--------------------------------------------------------------------

# Registro
post: http://url/register
Example: 
{
    "user_id": "user_ID", 
    "image": "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD/2wCEAAYGBgYHBgcICAcKCwoLCg8ODAwODxYQERAREBYiFRkVFRkVIh4kHhweJB42Ki..."
}

Request 200:
{
    "image_path": "./user_images/user_ID.jpg",
    "message": "User registered successfully",
    "user_id": "user_ID"
}



# Identificar
post: http://url/identify
Example:
{
    "image": "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD/2wCEAAYGBgYHBgcICAcKCwoLCg8ODAwODxYQERAREBYiFRkVFRkVIh4kHhweJB42Ki..."
}

Request 200:
{
    "message": "user_ID"
}

