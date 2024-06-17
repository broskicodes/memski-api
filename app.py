from dotenv import load_dotenv
from mem0 import Memory
from flask import Flask, request

load_dotenv()
app = Flask(__name__)

# config = {
#   "vector_store": {
#     "provider": "qdrant",
#     "config": {
#       "host": "localhost",
#       "port": 6333
#     }
#   }
# }

# mem_store = Memory.from_config(config)

@app.route('/')
def hello():
    return 'Hello, World!'

# @app.route("/save", methods=["POST"])
# def save_memory():
#     json_data = request.get_json()
#     user_id = json_data.get("user_id")
#     memory = json_data.get("memory")

#     print(user_id)
#     print(memory)

#     return "ok"


if __name__ == '__main__':
    app.run(debug=False)



