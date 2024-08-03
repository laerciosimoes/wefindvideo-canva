# Use the official Python image from the Docker Hub
FROM python:3.9.19-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt /app/

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code to /app
COPY . /app

# Expose the port your app runs on (if applicable)
EXPOSE 8000

ENV OPENAI_API_KEY=''
ENV unsplash_ID=''
ENV unsplash_Access_Key=''
ENV unsplash_Secret_Key=''


# Define the command to run the application
CMD ["python", "app.py"]