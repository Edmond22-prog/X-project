FROM python:3.10

LABEL author="Edmond Makolle"

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file in the working directory
COPY requirements.txt .

# Update pip
RUN pip install --no-cache-dir --upgrade pip

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install gunicorn server for running the app
RUN pip install gunicorn

# Copy the current directory the working directory
COPY . .

# COPY the start.sh script to the root directory of the container
COPY ./start /start

# Give execute permission to the start.sh script
RUN chmod +x /start

# Expose the port the app runs on
EXPOSE 8000
