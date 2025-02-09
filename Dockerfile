# Use the official Python base image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements.txt file into the container
COPY requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application into the container
COPY . .

# Expose the port the app will run on
EXPOSE 5000

# Command to run the app
CMD ["python3", "main.py"]
