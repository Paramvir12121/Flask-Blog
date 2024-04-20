# Use an official Python runtime as a parent image
FROM python:3.8-slim

RUN mkdir /app
# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY ./flask /app

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 5000 available to the world outside this container
EXPOSE 5000

# # Define environment variable
ENV COGNITO_REGION us-east-1
ENV COGNITO_USERPOOL_ID userid
ENV COGNITO_APP_CLIENT_ID app-client
ENV COGNITO_CHECK_TOKEN_EXPIRATION token-exp-check 

# Run app.py when the container launches
CMD ["python", "server.py"]