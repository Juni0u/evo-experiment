# Use a base image
FROM python:3.12.3

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install dependencies from requirements.txt (if you're using Python)
RUN pip install -r requirements.txt

# Define the command to run your app
CMD ["python", "main.py"]
