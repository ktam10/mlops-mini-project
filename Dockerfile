# Base image
FROM python:3.13-slim

# Set working directory
WORKDIR /app

#Install ffmpeg 
RUN apt-get update && apt-get install -y ffmpeg && rm -rf /var/lib/apt/lists/*

# Cp requirements
COPY requirements.txt .

# Install py dependencies
RUN pip install --no-cache-dir -r requirements.txt

# copy app code
COPY . .

#Expose port 8000
EXPOSE 8000

# MLflow and AWS config
ENV MLFLOW_TRACKING_URI=http://18.223.143.16:5000
ENV AWS_DEFAULT_REGION=us-east-2

#Start server
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

