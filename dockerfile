# Select base image for Python
FROM python:3.11-slim

# Set working directory 
WORKDIR /app

# Copy dependencies 
COPY requirements.txt . 
COPY classifier_app.py .
COPY finetune.py . 
COPY dataset_handler.py .
COPY text_classifier.py .

# Insall python dependencies
RUN pip install --no-cache-dir -r requirements.txt && \
    # Finetune destilbert model
    python3 finetune.py

# Copy application
COPY . . 

# Port 
EXPOSE 6001

CMD ["python", "classifier_app.py"]
