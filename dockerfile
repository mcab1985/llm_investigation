# Select base image for Python
FROM python:3.11-slim

# Set working directory 
WORKDIR /app

# Copy dependencies 
COPY requirements.txt . 

# Insall python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . . 

# Port 
EXPOSE 6001

CMD ["python", "classifier_app.py"]
