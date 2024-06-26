import os
from dotenv import load_dotenv
from mem0 import Memory
from flask import Flask, request
import requests
import json


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

wordware_api_key = os.getenv("WORDWARE_API_KEY")
mem_store = Memory.from_config(config)

@app.route('/memory/query', methods=["POST"])
def query_memories():
    json_data = request.get_json()
    user_id = json_data.get("user_id")
    query = json_data.get("query")


    memories = mem_store.search(query, user_id=user_id, limit=5)

    return [{'text': memory['text'], 'score': memory['score']} for memory in memories]

@app.route("/memory/save", methods=["POST"])
def save_memory():
    json_data = request.get_json()
    user_id = json_data.get("user_id")
    memory = json_data.get("memory")
    metadata = json_data.get("metadata") if json_data.get("metadata") else None

    mem_store.add(memory, user_id=user_id, metadata=metadata)

    return "memory added successfully"

@app.route("/prompt", methods=["POST"])
def rewrite_prompt():
    prompt_id = "5b95a4a2-5092-4b71-9276-ece797bc195f"

    json_data = request.get_json()
    agent_sys_prompt = json_data.get("agent_sys_prompt")
    convo = json_data.get("convo")
    prompt = json_data.get("prompt")
    user_id = json_data.get("user_id") 

    r = requests.post(f"https://app.wordware.ai/api/prompt/{prompt_id}/run",
        json={
            "inputs": {
                "agent_sys_prompt": agent_sys_prompt,
                "convo": convo,
                "prompt": prompt,
                "user_id": user_id,
            }
        },
        headers={"Authorization": f"Bearer {wordware_api_key}"},
        stream=False
    )

    for line in r.iter_lines():
        if line:
            content = json.loads(line.decode('utf-8'))
            value = content['value']
            # We can print values as they're generated
            # if value['type'] == 'generation':
            #     if value['state'] == "start":
            #         print("\nNEW GENERATION -", value['label'])
            #     else:
            #         print("\nEND GENERATION -", value['label'])
            # elif value['type'] == "chunk":
            #     print(value['value'], end="")
            if value['type'] == "outputs":
                # Or we can read from the outputs at the end
                # Currently we include everything by ID and by label - this will likely change in future in a breaking
                # change but with ample warning
                # print("\nFINAL OUTPUTS:")
                # print(json.dumps(value, indent=4))
                # output = json.loads(line.decode('utf-8'))
                # print(value["values"].keys())
                return value["values"]["new_prompt"]

    # print(r.text)

    return "ok"

if __name__ == '__main__':
    # app.run(host="0.0.0.0", port=os.getenv("PORT", 5000))
    app.run(debug=True)



