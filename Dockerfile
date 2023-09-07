FROM pytorch/pytorch:1.9.0-cpu

# Set the working directory in the container
WORKDIR /app

# Copy the local package files to the container
COPY . .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Define environment variable for Flask to run in production mode
ENV FLASK_ENV=production

# Run the Flask app when the container launches
CMD ["flask", "run", "--host=0.0.0.0"]
