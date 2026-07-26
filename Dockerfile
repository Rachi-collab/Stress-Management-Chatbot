# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set environmental variables to prevent Python from writing pyc files and buffering stdout
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory in the container
WORKDIR /code

# Copy the requirements file and install dependencies
COPY requirements.txt /code/
RUN pip install --no-cache-dir -r requirements.txt

# Create cache directories for Hugging Face hub and LlamaIndex and grant write permissions
RUN mkdir -p /code/.cache && chmod -R 777 /code/.cache
ENV HF_HOME=/code/.cache

# Copy the rest of the application code
COPY . /code/

# Expose port 7860 (Hugging Face Spaces routes requests to port 7860 by default)
EXPOSE 7860

# Run the FastAPI server
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7860"]
