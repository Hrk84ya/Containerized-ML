# Use Python base image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy files
COPY model.pkl app.py requirements.txt ./

# Install dependencies
RUN pip install -r requirements.txt

# Expose port
EXPOSE 5050

# Run Flask app
CMD ["python", "app.py"]