# INITIAL COLLECTIONS FOR DATABASE
# RUN SCRIPT: python initial_db_and_collections.py
import json
from tqdm import tqdm
from pymongo import MongoClient


client = MongoClient('mongodb://localhost:27017/')


db = client['fortuna']


collections = [
    'users'
]

logs = []
for collection_name in tqdm(collections, desc='Processing collections'):
    if collection_name not in db.list_collection_names():
        db.create_collection(collection_name)
        logs.append(
            f"Collection '{collection_name}' was successfully added.")
    else:
        logs.append(
            f"Collection '{collection_name}' already exists in the database.")

logs = json.dumps(logs, indent=2)

print()

print(f"Status: {logs}")
