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
    strings = data.get('strings')

    if not strings or not isinstance(strings, list) or len(strings) < 2:
        return jsonify({"error": "Provide a list of at least two strings to compare."}), 400

    embeddings = [encode_string(s) for s in strings]

    # Compute average similarity among all pairs
    total_similarities = 0
    num_pairs = 0
    similarities_per_string = [0] * len(strings)
    for i in range(len(embeddings)):
        for j in range(len(embeddings)):
            if i != j:
                sim = cosine_similarity(embeddings[i], embeddings[j]).item()
                total_similarities += sim
                similarities_per_string[i] += sim
                num_pairs += 1

    average_similarity = total_similarities / num_pairs

    # Identify strings with below-average similarity
    threshold = 0.9
    less_similar_strings = [strings[i] for i, sim in enumerate(similarities_per_string) if sim / (len(strings) - 1) < threshold]

    return jsonify({
        "average_similarity": average_similarity,
        "less_similar_strings": less_similar_strings
    })


if __name__ == '__main__':
    app.run(debug=True)
