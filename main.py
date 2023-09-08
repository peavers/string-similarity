from flask import Flask, request, jsonify
from transformers import BertTokenizer, BertModel
import torch
from torch.nn.functional import cosine_similarity

app = Flask(__name__)

# Load pre-trained BERT model and tokenizer
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = BertModel.from_pretrained('bert-base-uncased')


def encode_string(s):
    s = s.replace('.', ' ')  # Replace periods with spaces for better matching
    tokens = tokenizer(s, return_tensors='pt', padding=True, truncation=True, max_length=128)
    with torch.no_grad():
        embeddings = model(**tokens).last_hidden_state

    return embeddings.mean(dim=1)


@app.route('/similarity', methods=['POST'])
def similarity():
    data = request.get_json()
    strings = data.get('strings')

    # Get threshold from query parameters. Default to 0.9 if not provided.
    threshold = float(request.args.get('threshold', 0.9))

    if not strings or not isinstance(strings, list) or len(strings) < 2:
        return jsonify({"error": "Provide a list of at least two strings to compare."}), 400

    embeddings = [encode_string(s) for s in strings]

    # Compute similarity matrix
    sim_matrix = [[0 for _ in range(len(embeddings))] for _ in range(len(embeddings))]
    for i in range(len(embeddings)):
        for j in range(len(embeddings)):
            if i != j:
                sim_matrix[i][j] = cosine_similarity(embeddings[i], embeddings[j]).item()

    # Group similar strings based on similarity matrix
    visited = set()
    groups = []

    for i in range(len(strings)):
        if i not in visited:
            current_group = [strings[i]]
            visited.add(i)
            for j in range(i + 1, len(strings)):
                if j not in visited and sim_matrix[i][j] >= threshold:
                    current_group.append(strings[j])
                    visited.add(j)
            groups.append(current_group)

    return jsonify({"groups": groups})


if __name__ == '__main__':
    app.run(debug=True)
