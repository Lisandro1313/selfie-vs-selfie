# Alternative Dockerfile - simpler approach
FROM python:3.11

# Set environment to avoid display issues
ENV DISPLAY=:99
ENV QT_QPA_PLATFORM=offscreen

# Set work directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port
EXPOSE $PORT

# Run the application
CMD ["python", "rps_online/app.py"]