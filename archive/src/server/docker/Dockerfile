FROM python:3.10

# Add metadata to the image
LABEL maintainer="haorui.peng@eit.lth.se"
LABEL version="1.0"

RUN pip install zmq numpy

# Make a directory for the server script
WORKDIR /usr/src/server
RUN mkdir data

# Copy the Python script into the container
COPY ./central_server.py ./central_server.py

# Specify the default command to run when the container starts
CMD ["python", "-u", "./central_server.py"]