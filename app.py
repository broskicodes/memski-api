import os
from dotenv import load_dotenv
from mem0 import Memory
from flask import Flask, request

load_dotenv()
app = Flask(__name__)

config = {
  "vector_store": {
    "provider": "qdrant",
    "config": {
      # "host": "localhost",
      # "port": 6333
      "url": f"{os.getenv('QDRANT_API_ENDPOINT', 'localhost')}:6333",
      "api_key": os.getenv("QDRANT_API_KEY")
    }
  }
}

mem_store = Memory.from_config(config)

@app.route('/')
def hello():
    return mem_store.get_all()

@app.route("/save", methods=["POST"])
def save_memory():
    json_data = request.get_json()
    user_id = json_data.get("user_id")
    memory = json_data.get("memory")
    metadata = json_data.get("metadata") if json_data.get("metadata") else None

    mem_store.add(memory, user_id=user_id, metadata=metadata)

    return "memory added successfully"

if __name__ == '__main__':
    app.run()
    # app.run(debug=True)



