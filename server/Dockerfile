# Grab Python 3.x image
FROM python:3

# Let Python output be sent to the host computer
ENV PYTHONUNBUFFERED 1

# Define/create a working directory for the RUN/CMD/COPY commands
WORKDIR /app

# Copy the requirements.txt file into the container
COPY ./src/requirements.txt .

# Install the required dependencies
RUN pip install -r requirements.txt

# Tell Docker to listen to traffic on this port inside the container
EXPOSE 80
