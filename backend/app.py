from flask import Flask, request, jsonify
from flask_cors import CORS
import pymongo
from bson.objectid import ObjectId
import time
from dataclasses import dataclass, asdict
import json
import traceback

app = Flask(__name__)
CORS(app)

try:
    print("Attempting to connect to MongoDB...")
    client = pymongo.MongoClient("mongodb://localhost:27017/", serverSelectionTimeoutMS=5000)
  
    client.server_info()
    print("MongoDB connection successful!")
    
    db = client["user_database"]
    collection = db["users"]
    doc_count = collection.count_documents({})
    print(f"Number of documents in collection: {doc_count}")
except Exception as e:
    print(f"ERROR connecting to MongoDB: {e}")
    print("Continuing with limited functionality...")
    client = None
    db = None
    collection = None

@dataclass
class UserPreferences:
    timezone: str

@dataclass
class User:
    username: str
    password: str
    roles: list
    preferences: UserPreferences
    created_ts: float
    active: bool = True
    updated_ts: float = None

def serialize_user(user):
    if "_id" in user:
        user["_id"] = str(user["_id"])
    return user

@app.route('/api/test', methods=['GET'])
def test_route():
    """Rota de teste para verificar se a API está funcionando"""
    return jsonify({"message": "API is working!"})

@app.route('/api/mongodb-status', methods=['GET'])
def mongodb_status():
    """Verifica o status da conexão com MongoDB"""
    try:
        if client is None:
            return jsonify({"status": "disconnected", "message": "MongoDB is not connected"})
        
        
        db_names = client.list_database_names()
        
      
        doc_count = 0
        if collection is not None:
            doc_count = collection.count_documents({})
            
        return jsonify({
            "status": "connected", 
            "databases": db_names,
            "current_db": "user_database",
            "document_count": doc_count
        })
    except Exception as e:
        print(f"Error in MongoDB status: {e}")
        traceback.print_exc()
        return jsonify({"status": "error", "message": str(e)})

@app.route('/api/users', methods=['GET'])
def get_users():
    """Obtém todos os usuários"""
    if collection is None:
       
        return jsonify([
            {"_id": "test1", "username": "test_user", "roles": ["tester"], 
             "preferences": {"timezone": "UTC"}, "active": True, "created_ts": time.time()}
        ])
    
    try:
        users = list(collection.find())
        print(f"Found {len(users)} users in database")
        
        
        for user in users:
            if 'user' in user and 'username' not in user:
                user['username'] = user['user']
            
    
            if 'preferences' not in user or not isinstance(user['preferences'], dict):
                user['preferences'] = {'timezone': user.get('user_timezone', 'UTC')}
            elif 'timezone' not in user['preferences']:
                user['preferences']['timezone'] = user.get('user_timezone', 'UTC')
        
        serialized_users = [serialize_user(user) for user in users]
        return jsonify(serialized_users)
    except Exception as e:
        print(f"Error fetching users: {e}")
        traceback.print_exc()
        return jsonify([]), 500

@app.route('/api/users/<id>', methods=['GET'])
def get_user(id):
    user = collection.find_one({"_id": ObjectId(id)})
    if not user:
        return jsonify({"error": "User not found"}), 404
    return jsonify(serialize_user(user))

@app.route('/api/users', methods=['POST'])
def create_user():
    data = request.json
    
    preferences = UserPreferences(timezone=data.get('timezone', 'UTC'))
    
    user = User(
        username=data['username'],
        password=data['password'],
        roles=data['roles'],
        preferences=preferences,
        created_ts=time.time()
    )
    
    result = collection.insert_one(asdict(user))
    user_id = str(result.inserted_id)
    
    return jsonify({"id": user_id, "message": "User created successfully"}), 201

@app.route('/api/users/<id>', methods=['PUT'])
def update_user(id):
    data = request.json
    
    update_data = {
        "username": data['username'],
        "password": data['password'],
        "roles": data['roles'],
        "preferences": {
            "timezone": data['timezone']
        },
        "active": data.get('active', True),
        "updated_ts": time.time()
    }
    
    result = collection.update_one(
        {"_id": ObjectId(id)},
        {"$set": update_data}
    )
    
    if result.matched_count == 0:
        return jsonify({"error": "User not found"}), 404
    
    return jsonify({"message": "User updated successfully"})

@app.route('/api/users/<id>', methods=['DELETE'])
def delete_user(id):
    result = collection.delete_one({"_id": ObjectId(id)})
    
    if result.deleted_count == 0:
        return jsonify({"error": "User not found"}), 404
    
    return jsonify({"message": "User deleted successfully"})

if __name__ == '__main__':
    print("Starting Flask server on port 5000...")
    print("You can test the server by accessing: http://localhost:5000/api/test")
    print("To check MongoDB status: http://localhost:5000/api/mongodb-status")
    app.run(debug=True, host='0.0.0.0') 