# Use the official Python image from the Docker Hub
# FROM python:3.9.19-slim
FROM dpokidov/imagemagick:latest


# Install ImageMagick
RUN apt-get update && \
    apt-get install -y wget ffmpeg fuse python3 python3-pip  && \
    apt-get install -y wget ffmpeg fuse python3 python3-pip fonts-courier-prime fonts-dejavu fonts-dejavu-extra fonts-dejavu-core && \
    rm -rf /var/lib/apt/lists/*


# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt /app/

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code to /app
COPY . /app

#RUN ./magick --appimage-extract

# Expose the port your app runs on (if applicable)
EXPOSE 8000

ENV OPENAI_API_KEY=''
ENV unsplash_ID=''
ENV unsplash_Access_Key=''
ENV unsplash_Secret_Key=''
#ENV IMAGEMAGICK_BINARY='/usr/local/bin/magick'
ENV IMAGEMAGICK_BINARY='/usr/local/bin/magick'
ENV IMAGICK_FONT_PATH='/usr/share/fonts/truetype/dejavu'


# Define the command to run the application
ENTRYPOINT [ "python3", "/app/app.py" ]
