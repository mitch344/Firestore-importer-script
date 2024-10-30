import json
import tkinter as tk
from tkinter import filedialog
import firebase_admin
from firebase_admin import credentials, firestore
import uuid

# Initialize Firebase with selected certificate
def initialize_firebase():
    global db
    if firebase_admin._apps:
        print("Firebase already initialized.")
        return firestore.client()
        
    cert_path = filedialog.askopenfilename(
        title="Select Firebase Service Account JSON",
        filetypes=[("JSON files", "*.json")]
    )
    if not cert_path:
        print("Error: No certificate selected. Initialization aborted.")
        return None

    try:
        cred = credentials.Certificate(cert_path)
        firebase_admin.initialize_app(cred)
        db = firestore.client()
        print("Firebase initialized successfully.")
    except Exception as e:
        print(f"Error: Failed to initialize Firebase: {e}")

# Function to open JSON file and upload to Firestore
def upload_json_to_firestore():
    if not db:
        print("Error: Firebase not initialized. Please select a valid certificate.")
        return

    file_path = filedialog.askopenfilename(title="Select JSON File", filetypes=[("JSON files", "*.json")])
    if not file_path:
        return  # If no file selected, return

    try:
        with open(file_path, 'r') as file:
            data = json.load(file)

        collection_name = collection_entry.get()
        if not collection_name:
            print("Error: Please enter a collection name.")
            return

        document_id = str(uuid.uuid4())

        # Upload to Firestore
        db.collection(collection_name).document(document_id).set(data)
        print(f"Success: Data uploaded to {collection_name}/{document_id}")

    except Exception as e:
        print(f"Error: Failed to upload data: {e}")

# Create GUI using tkinter
root = tk.Tk()
root.title("Firestore JSON Importer")
root.geometry("400x250")

# Collection Name Input
tk.Label(root, text="Collection Name:").pack(pady=5)
collection_entry = tk.Entry(root, width=30)
collection_entry.pack(pady=5)

# Initialize Firebase Button
initialize_button = tk.Button(root, text="Select Firebase Certificate and Initialize", command=initialize_firebase)
initialize_button.pack(pady=10)

# Upload Button
upload_button = tk.Button(root, text="Select JSON and Upload", command=upload_json_to_firestore)
upload_button.pack(pady=20)

# Run the GUI loop
db = None
root.mainloop()
