from flask import Flask, request, jsonify
from sentence_transformers import SentenceTransformer, util

app = Flask(__name__)

# Load the sentence-transformer model
model = SentenceTransformer('all-MiniLM-L6-v2')


def encode_string(s):
    return model.encode(s, convert_to_tensor=True)


@app.route('/similarity', methods=['POST'])
def similarity():
    data = request.get_json()
    strings = data.get('strings')

    # Default if none is provided.
    threshold = float(request.args.get('threshold', 0.98))

    if not strings or not isinstance(strings, list) or len(strings) < 2:
        return jsonify({"error": "Provide a list of at least two strings to compare."}), 400

    embeddings = [encode_string(s) for s in strings]

    grouped = []
    while embeddings:
        current_embedding = embeddings.pop(0)
        current_string = strings.pop(0)

        group = [current_string]
        other_indices = []

        for idx, other_embedding in enumerate(embeddings):
            sim = util.pytorch_cos_sim(current_embedding, other_embedding).item()
            if sim >= threshold:
                group.append(strings[idx])
                other_indices.append(idx)

        for idx in reversed(other_indices):
            embeddings.pop(idx)
            strings.pop(idx)

        grouped.append(group)

    return jsonify({
        "groups": grouped
    })


if __name__ == '__main__':
    app.run(debug=True)
