# Sentence Transformer String Grouping Service

This repository offers a Flask-based API service to group semantically similar strings using the Sentence Transformer
model. The code is designed for ease of understanding and integration into projects that require text grouping based on
semantic similarity.

---

### Features

- Utilizes the Sentence Transformer for generating dense vector representations of text strings.
- Groups similar strings based on a specified similarity threshold.
- Returns groups of similar strings.

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

After setup, run the service using:

```bash
python main.py
```

This starts the Flask server, making the API endpoint accessible at `http://localhost:5000/similarity`.

---

## Using Docker

For those favoring containerization, a Docker image is available that wraps all dependencies and setup, offering a
seamless method to run the string grouping service.

### Pulling the Docker Image

Fetch the Docker image with:

```bash
docker pull peavers/string-similarity
```

### Running the Service with Docker

After downloading the image, execute the service with:

```bash
docker run -p 5000:5000 peavers/string-similarity
```

This command routes port `5000` within the container to port `5000` on your machine. The service is then accessible
at `http://localhost:5000/similarity`.

### Notes for Docker Users

- Ensure Docker is properly installed and operational. For Docker beginners, consult
  the [official documentation](https://docs.docker.com/get-started/).
- Ensure Docker has adequate resources, given that Sentence Transformer models can be memory-intensive.

---

## How to Use

To group similar strings, make a POST request to the `/similarity` endpoint with a JSON payload listing the strings. An
example using `curl`:

```bash
curl -X POST http://localhost:5000/similarity?threshold=0.98 -H "Content-Type: application/json" -d '{"strings": ["Hello world", "Greetings earth", "Hi there"]}'
```

Expected Response:

```json
{
  "groups": [
    [
      "Hello world",
      "Greetings earth"
    ],
    [
      "Hi there"
    ]
  ]
}
```

## How it Works

1. **Sentence Transformer Embedding:** Text strings are transformed into embeddings via the Sentence Transformer model.
   These embeddings are dense vectors reflecting the text's semantic information.

2. **Grouping Similar Strings:** Using the cosine similarity, strings are grouped based on a specified threshold.

3. **Response:** The service returns groups of similar strings.

### Future Enhancements

- Potential support for other transformer models.
- Batch processing for efficiently managing high volumes of text.
- More metrics and methods for text comparison.

### Contributing

Contributions are welcome! Open an issue for any problems, or submit pull requests for enhancements.

---

**Note**: Make sure you have adequate computational resources when running the Sentence Transformer model. For
production deployment, consider dedicated hardware or cloud solutions.

---

For questions, feedback, or issues, open an issue in this repository.