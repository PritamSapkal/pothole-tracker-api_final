from flask import Flask, jsonify
import firebase_admin
from firebase_admin import credentials, firestore
from flask_cors import CORS
import os
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Initialize Firebase
cred = credentials.Certificate("C:\\Users\\prita\\OneDrive\\Desktop\\pthhole_tracker\\SERVER_AND_MAP_CODE\\potholes-tracker-6de66-firebase-adminsdk-fbsvc-88d9710f35.json")  # Update with your Firebase JSON key
firebase_admin.initialize_app(cred)
db = firestore.client()

def get_pothole_data():
    """Fetch pothole data from Firebase."""
    try:
        potholes_ref = db.collection("potholes_database").stream()
        data = [{
            "latitude": float(doc.to_dict().get("latitude", 0)),
            "longitude": float(doc.to_dict().get("longitude", 0)),
            "size": str(doc.to_dict().get("size", "")).strip().lower()
        } for doc in potholes_ref if doc.to_dict().get("latitude") and doc.to_dict().get("longitude")]

        return data
    except Exception as e:
        print(f"Firebase Error: {str(e)}")
        return []

@app.route('/api/potholes', methods=['GET'])
def potholes():
    """API endpoint to fetch pothole data."""
    try:
        data = get_pothole_data()
        if not data:
            return jsonify({
                "success": True,
                "message": "No pothole data found",
                "data": []
            })
        return jsonify({
            "success": True,
            "count": len(data),
            "data": data
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": "Server error",
            "details": str(e)
        }), 500

if __name__ == "__main__":
    if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
