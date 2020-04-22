FROM python:3.8-slim-buster as build

# Set the working directory to /dockerapi
WORKDIR /src

# Copy the current directory contents into the container at /DockerAPI
ADD ./src /src

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r /src/requirements.txt

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Define Environment Variables
ENV PATH=$PATH:/src/
ENV PYTHONPATH /src/

# Run the Application
RUN chmod u+x /src/run.sh
CMD /src/run.sh
