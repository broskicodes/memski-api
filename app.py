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

@app.route("/", methods=["GET"])
def hello():
  return "hello"

@app.route('/query', methods=["POST"])
def query_memories():
    json_data = request.get_json()
    user_id = json_data.get("user_id")
    query = json_data.get("query")


    memories = mem_store.search(query, user_id=user_id, limit=5)

    return [{'text': memory['text'], 'score': memory['score']} for memory in memories]

@app.route("/save", methods=["POST"])
def save_memory():
    json_data = request.get_json()
    user_id = json_data.get("user_id")
    memory = json_data.get("memory")
    metadata = json_data.get("metadata") if json_data.get("metadata") else None

    mem_store.add(memory, user_id=user_id, metadata=metadata)

    return "memory added successfully"

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=os.getenv("PORT", 5000))
    # app.run(debug=True)



