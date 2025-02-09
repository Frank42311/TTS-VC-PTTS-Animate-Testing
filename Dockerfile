# Use the slim version of Python 3.11
FROM python:3.11-slim

# Set the working directory to /app
WORKDIR /app

# Copy the dependency file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project code into the container (including the TTS folder)
COPY . .

# Default to starting bash so PyCharm can run specified scripts via Docker remote interpreter
CMD [ "bash" ]
