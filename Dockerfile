FROM python:3.11-slim  # Use a simple Python base image.  

WORKDIR /code  # Place the project inside the container at /code.  

COPY requirements.txt /code/requirements.txt  # Copy Python dependencies first.  

RUN pip install --no-cache-dir -r /code/requirements.txt  # Install dependencies.  

COPY app /code/app  # Copy the application folder.  
COPY schemas /code/schemas  # Copy schemas for reference.  
COPY .env.example /code/.env.example  # Copy the sample env file.  

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]  # Start the API server.
