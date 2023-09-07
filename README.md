# BERT String Similarity Service

This repository provides a Flask-based API service for computing semantic similarity between a list of strings using the
BERT (Bidirectional Encoder Representations from Transformers) model. The code is designed to be straightforward to
understand and can be easily integrated into various projects requiring similarity measurement among text strings.

---

### Features

- Uses BERT for generating dense vector representations of text strings.
- Computes pairwise cosine similarity to measure how close two vectors are.
- Returns average similarity and identifies strings that have below-average similarity.

## Installation and Setup

1. Clone this repository.
   ```bash
   git clone https://github.com/peavers/string-similarity
   cd string-similarity
   ```

2. Install the required packages.
   ```bash
   pip install -r requirements.txt
   ```

### Running the Service

After setting up, you can run the service by executing:

```bash
python main.py
```

This will start the Flask server, and you can access the API endpoint at `http://localhost:5000/similarity`.

---

## Using Docker

For those who prefer containerization, we provide a Docker image that encapsulates all the dependencies and setup,
offering a straightforward way to run the string similarity service.

### Pulling the Docker Image

To get the Docker image, use the following command:

```bash
docker pull peavers/string-similarity
```

### Running the Service with Docker

After pulling the image, you can run the service with:

```bash
docker run -p 5000:5000 peavers/string-similarity
```

This command maps port `5000` inside the container to port `5000` on your machine. Once executed, the service will be
accessible at `http://localhost:5000/similarity`.

### Notes for Docker Users

- Ensure Docker is properly installed and running on your machine. If new to Docker, refer to
  the [official documentation](https://docs.docker.com/get-started/) to get started.
- Running BERT inside a Docker container will require a sufficient amount of memory. Ensure the Docker engine has enough
  resources allocated.

---

## How to Use

To compute similarity among a set of strings, make a POST request to the `/similarity` endpoint with a JSON payload
containing the list of strings. Here's an example using `curl`:

```bash
curl -X POST http://localhost:5000/similarity -H "Content-Type: application/json" -d '{"strings": ["Hello world", "Greetings earth", "Hi there"]}'
```

Expected Response:

```json
{
  "average_similarity": 0.9421,
  "less_similar_strings": [
    "Hi there"
  ]
}
```

## How it Works

1. **BERT Tokenization and Embedding:** Strings are tokenized using the BERT tokenizer, and embeddings are generated
   using the BERT model. The embeddings are dense vectors that capture the contextual information of the text.

2. **Computing Similarity:** The cosine similarity between all pairs of strings is computed. This metric ranges from
   -1 (completely dissimilar) to 1 (completely similar), with 0 indicating orthogonality.

3. **Response:** The service computes an average similarity across all pairs and also identifies any string that has a
   below-average similarity against the others.

### Future Enhancements

- Support for other transformer models.
- Batch processing for handling large volumes of text efficiently.
- Additional metrics for comparing text strings.

### Contributing

We welcome contributions! Please open an issue if you find any, or submit a pull request if you have improvements.

---

**Note**: Ensure you have enough memory and computational power to run BERT, as it's a large model. If you're planning
to deploy this in a production environment, consider using dedicated hardware or cloud services.

---

For any issues, questions, or feedback, please open an issue in this repository.