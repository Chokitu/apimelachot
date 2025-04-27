from flask import Flask, request, jsonify, send_from_directory, redirect
from flask_cors import CORS
from pymongo import MongoClient
from bson.objectid import ObjectId
import threading
from populate_db import populate_database
import os
import signal
import sys

app = Flask(__name__)
CORS(app)

# Connect to MongoDB
try:
    # Try connecting with default settings
    client = MongoClient('mongodb://localhost:27017/', serverSelectionTimeoutMS=5000)
    # Force a connection to verify it works
    client.admin.command('ping')
    print("Connected to MongoDB successfully!")
except Exception as e:
    print(f"MongoDB connection error: {e}")
    print("Please make sure MongoDB is installed and running.")

db = client['melachot_db']  # Database name
collection = db['melachot']  # Collection name

# Initialize the database - but it also checks if the collection is empty before populating. 
# This prevents overwriting existing data.
populate_database()

# Routes

# Add a root route to the API that redirects to the frontend
@app.route('/', methods=['GET'])
def redirect_to_frontend():
    # Redirect to the frontend service
    return redirect("http://localhost:3001/", code=302)

# Optional: Add a catch-all route to redirect any non-API paths to the frontend
@app.route('/<path:path>', methods=['GET'])
def api_catch_all(path):
    # Only redirect if the path isn't one of our API paths
    if not path.startswith('api/'):
        return redirect(f"http://localhost:3001/{path}", code=302)
    else:
        return jsonify({"error": f"API endpoint /{path} not found"}), 404

# GET all melachot
@app.route('/api/melachot', methods=['GET'])
def get_all_melachot():
    melachot = list(collection.find({}, {'_id': 0}))
    return jsonify(melachot)

# GET a specific melacha by ID
@app.route('/api/melachot/<int:melacha_id>', methods=['GET'])
def get_melacha(melacha_id):
    melacha = collection.find_one({"id": melacha_id}, {'_id': 0})
    if melacha:
        return jsonify(melacha)
    return jsonify({"error": "Melacha not found"}), 404

# GET melachot by category
@app.route('/api/categories/<category>', methods=['GET'])
def get_by_category(category):
    results = list(collection.find({"category": {"$regex": category, "$options": "i"}}, {'_id': 0}))
    if results:
        return jsonify(results)
    return jsonify({"error": "Category not found"}), 404

# GET list of all categories
@app.route('/api/categories', methods=['GET'])
def get_categories():
    categories = collection.distinct("category")
    return jsonify(categories)

# POST - Add a new melacha
@app.route('/api/melachot', methods=['POST'])
def add_melacha():
    new_melacha = request.json
    
    # Validate required fields
    if not all(key in new_melacha for key in ['name', 'category', 'description']):
        return jsonify({"error": "Missing required fields"}), 400
    
    # Generate new ID
    max_id = collection.find_one(sort=[("id", -1)])
    new_id = 1 if not max_id else max_id["id"] + 1
    new_melacha['id'] = new_id
    
    # Insert into MongoDB
    collection.insert_one(new_melacha)
    
    # Return the new melacha (without MongoDB's _id field)
    new_melacha.pop('_id', None)
    return jsonify(new_melacha), 201

# PUT - Update a melacha
@app.route('/api/melachot/<int:melacha_id>', methods=['PUT'])
def update_melacha(melacha_id):
    update_data = request.json
    
    # Ensure id remains unchanged
    update_data['id'] = melacha_id
    
    # Update in MongoDB
    result = collection.update_one({"id": melacha_id}, {"$set": update_data})
    
    if result.matched_count > 0:
        # Return the updated melacha
        updated_melacha = collection.find_one({"id": melacha_id}, {'_id': 0})
        return jsonify(updated_melacha)
    
    return jsonify({"error": "Melacha not found"}), 404

# DELETE - Remove a melacha
@app.route('/api/melachot/<int:melacha_id>', methods=['DELETE'])
def delete_melacha(melacha_id):
    melacha = collection.find_one({"id": melacha_id})
    if melacha:
        collection.delete_one({"id": melacha_id})
        return jsonify({"message": f"Melacha '{melacha['name']}' deleted successfully"})
    
    return jsonify({"error": "Melacha not found"}), 404

# Search melachot by name or description
@app.route('/api/search', methods=['GET'])
def search_melachot():
    query = request.args.get('q', '').lower()
    if not query:
        return jsonify({"error": "Search query is required"}), 400
    
    results = list(collection.find({
        "$or": [
            {"name": {"$regex": query, "$options": "i"}},
            {"description": {"$regex": query, "$options": "i"}}
        ]
    }, {'_id': 0}))
    
    return jsonify(results)

# Search melachot by keywords
@app.route('/api/search/keywords', methods=['GET'])
def search_by_keyword():
    keyword = request.args.get('keyword', '').lower()
    if not keyword:
        return jsonify({"error": "Keyword is required"}), 400
    
    results = list(collection.find(
        {"keywords": {"$regex": keyword, "$options": "i"}},
        {'_id': 0}
    ))
    
    return jsonify(results)

# GET all keywords
@app.route('/api/keywords', methods=['GET'])
def get_all_keywords():
    pipeline = [
        {"$unwind": "$keywords"},
        {"$group": {"_id": None, "keywords": {"$addToSet": "$keywords"}}},
        {"$project": {"_id": 0, "keywords": 1}}
    ]
    
    result = list(collection.aggregate(pipeline))
    if result:
        return jsonify(sorted(result[0]["keywords"]))
    return jsonify([])

# Create a second Flask app for serving the frontend
frontend_app = Flask(__name__, static_folder='../frontend')

# Serve the frontend
@frontend_app.route('/', defaults={'path': ''})
@frontend_app.route('/<path:path>')
def serve_frontend(path):
    if path != "" and os.path.exists(os.path.join(frontend_app.static_folder, path)):
        return send_from_directory(frontend_app.static_folder, path)
    else:
        return send_from_directory(frontend_app.static_folder, 'index.html')

def run_api():
    app.run(debug=True, port=3000, use_reloader=False)

def run_frontend():
    frontend_app.run(debug=True, port=3001, use_reloader=False)

def signal_handler(sig, frame):
    print("Shutting down servers...")
    sys.exit(0)

if __name__ == '__main__':
    # Register signal handler
    signal.signal(signal.SIGINT, signal_handler)
    
    # Start both servers in separate threads
    api_thread = threading.Thread(target=run_api, daemon=True)  # Set daemon=True
    frontend_thread = threading.Thread(target=run_frontend, daemon=True)  # Set daemon=True
    
    api_thread.start()
    frontend_thread.start()
    
    try:
        # Keep the main thread alive while allowing keyboard interrupts
        while True:
            api_thread.join(0.1)
            frontend_thread.join(0.1)
            if not api_thread.is_alive() or not frontend_thread.is_alive():
                break
    except KeyboardInterrupt:
        print("Shutting down servers...")
        sys.exit(0)