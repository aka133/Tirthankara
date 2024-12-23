FROM python:3.12-slim

# Set working directory in the container
WORKDIR /app

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy only the src directory contents to /app
COPY src/ .

# Expose the application port
EXPOSE 5001

# Set environment variables if needed
ENV FLASK_APP=webapp.py
ENV FLASK_RUN_HOST=0.0.0.0

# Run the application
CMD ["python", "webapp.py"]