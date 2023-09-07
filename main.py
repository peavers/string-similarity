from flask import Flask, request, jsonify
from transformers import BertTokenizer, BertModel
import torch
from torch.nn.functional import cosine_similarity

app = Flask(__name__)

# Load pre-trained BERT model and tokenizer
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = BertModel.from_pretrained('bert-base-uncased')


def encode_string(s):
    tokens = tokenizer(s, return_tensors='pt', padding=True, truncation=True, max_length=128)
    with torch.no_grad():
        embeddings = model(**tokens).last_hidden_state
    return embeddings.mean(dim=1)


@app.route('/similarity', methods=['POST'])
def similarity():
    data = request.get_json()
    string1 = data.get('string1')
    string2 = data.get('string2')

    if not string1 or not string2:
        return jsonify({"error": "Both 'string1' and 'string2' are required."}), 400

    string1_embedding = encode_string(string1)
    string2_embedding = encode_string(string2)
    similarity_score = cosine_similarity(string1_embedding, string2_embedding).item()

    return jsonify({"similarity": similarity_score})


if __name__ == '__main__':
    app.run(debug=True)
