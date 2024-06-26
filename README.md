# Flask-Blog (WIP)

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Routes](#routes)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Usage](#usage)
- [Dependencies](#dependencies)
- [Docker](#Docker)
- [Configuration](#configuration)
- [Contributors](#contributors)


## Introduction

This repository contains a Flask-based web application designed for blogging and user interactions. It supports user authentication using AWS Cognito, forms handling with Flask-WTF, and database interactions via SQLAlchemy.

## Features

- User authentication and authorization with AWS Cognito
- Form validations with Flask-WTF
- Data persistence using SQLAlchemy with a SQLite backend
- Bootstrap 5 for responsive front-end design

## Routes

- /: The home page displaying posts.
- /about: Static about page.
- /contact: Contact form for sending messages.
- /awslogin: AWS Cognito integrated login page.
- /new_password: Handle new password requirements for Cognito.
- /awslogout: Logout route that clears session data.
- /secure_area: Example secure area that requires authentication.

## Project Structure

- /flask:
    - server.py: Main Flask application setup and routes.
    - /templates: HTML templates for the application.
    - /static: Static files like images and CSS.
    - /instance: Contains the local db for testing. In production use cloud db.
- requirements.txt: List of packages required to run the application.

## Installation

To get started with this project, follow these steps:

1. Clone the repository:
   ```
   git clone https://github.com/Paramvir12121/Flask-Blog.git
    ```
2. Change directory to the cloned repository:
    ```
    cd your-repository-name
    ```
3. Install required Python packages:
    ```
    pip install -r requirements.txt
    ```
4. Usage
    To run the application locally:
    Set environment variables for AWS Cognito in your .env file:
    ```
    COGNITO_REGION=your_cognito_region
    USER_POOL_ID=your_user_pool_id
    APP_CLIENT_ID=your_app_client_id
    ```
4. Run the Flask server:
    ```
    python flask/server.py
    ```
The build and run the image of the project, follow the following steps:
1. Building the Docker Image
    Navigate to the root directory of the project where the Dockerfile is located and run the following command to build the Docker image:

    ```
    docker build -t flask-blog:0.0.1 .
    ```
    This command builds a Docker image named flask-blog with the tag 0.0.1.

2. Running the Container
    To run your Docker container with the environment configurations from the .env file, use the following command:

    ```
    docker run -d -p 5000:5000 --env-file ./flask/.env --name my-flask-app flask-blog:0.0.1
    ```
    This command will:

    - Run the container in detached mode (-d).
    - Map port 5000 of the host to port 5000 of the container, allowing access to the Flask application via http://localhost:5000.
    - Use the .env file located in the flask directory to configure the environment variables.
    - Name the container my-flask-app for easy reference.

3. Verifying the Application
    After running the container, you can verify that the application is up and running by accessing:

    ```
    http://localhost:5000
    ```
    in your web browser. This should load the Flask Blog application hosted inside your Docker container.



## Dependencies
All dependencies are listed in requirements.txt. Major Dependencies are:
- Flask: Flask is used as the core framework for your web application. It is responsible for creating the app instance, defining routes, and handling requests. For instance, app  Flask(__name__) initializes the Flask application, and the decorators @app.route are used to map URLs to Python functions.

- Flask-WTF: This extension is utilized for handling forms. You use FlaskForm to define forms such as LoginForm, SignupForm, and PostForm. These forms handle user input for authentication, signing up, and posting messages. It integrates seamlessly with your templates to validate user input against specified criteria.

- WTForms: While part of Flask-WTF, WTForms alone is responsible for defining form fields and validation rules. It’s used extensively in defining forms like LoginForm, where fields and validation rules are specified (e.g., StringField, PasswordField with validators such as DataRequired()).

- Flask-SQLAlchemy: This is used to interact with the SQLite database. It manages the creation of database models and handles all database transactions. For example, db = SQLAlchemy(model_class=Base) initializes the SQLAlchemy object, and models like User and UserPost inherit from db.Model, making them part of the ORM.

- Flask-Bootstrap: Flask-Bootstrap is used to integrate Bootstrap into Flask easily. It is initialized with bootstrap = Bootstrap5(app), which enables Bootstrap templates and forms to render with Bootstrap styling by default, enhancing the UI design and responsiveness without additional CSS.

- Boto3: Boto3 is the AWS SDK used primarily for AWS Cognito authentication. Functions like sign_in utilize Boto3 to interact with AWS Cognito services, handling user authentication processes such as signing in and responding to authentication challenges.

- python-dotenv: Used to load environment variables from a .env file at the start of your application with load_dotenv(). This approach is used to manage sensitive information such as AWS access keys and your Flask application's secret key without hardcoding them into the source code.

- Flask-Cognito: This extension enables your application to use AWS Cognito for user authentication. It helps manage session tokens and user authentication states with decorators like @cognito_auth_required, which you use to protect routes that require a user to be logged in.

- SQLAlchemy: SQLAlchemy, which is integrated into Flask through Flask-SQLAlchemy, is used for defining the ORM models and handling the SQL transactions transparently. It is pivotal in operations that involve creating, querying, updating, or deleting records from your SQLite database.



## Docker
Docker allows for easier orchestration and cross platform compatibility. 
The Docker setup uses python:3.8-slim as the base image and includes environment configurations for integrating with AWS Cognito.


- Structure
    Dockerfile: Defines the Docker image.
    flask/: Directory containing Flask application code.
    requirements.txt: Lists all Python dependencies.

- Environment Variables
    The Dockerfile configures several environment variables for AWS Cognito integration:
    ```
    COGNITO_REGION: AWS region for Cognito services (default us-east-1).
    COGNITO_USERPOOL_ID: The user pool ID.
    COGNITO_APP_CLIENT_ID: The app client ID associated with your Cognito user pool.
    COGNITO_CHECK_TOKEN_EXPIRATION: Boolean to enable token expiration checking.
    ```

    But it is not recommended to not expose the environment variables in the repository.

    - Instead of setting environment variables directly in the Dockerfile, you can use an environment file (.env). Eg:
        ```
        COGNITO_REGION=us-east-1
        COGNITO_USERPOOL_ID=user_pool_id
        COGNITO_APP_CLIENT_ID=app_client_ID
        COGNITO_CHECK_TOKEN_EXPIRATION=true
        ```
        
        This file can then be used with Docker without hardcoding secrets into your Dockerfile or image:
        
        ```
        docker run --env-file .env myimage
        ```

    OR
    - Modify the environment variables in the Docker run command to match your AWS Cognito setup during runtime:
    ```
    docker run -d -p 5000:5000 -e COGNITO_REGION='your-region' -e COGNITO_USERPOOL_ID='your-userpool-id' -e COGNITO_APP_CLIENT_ID='your-app-client-id' -e COGNITO_CHECK_TOKEN_EXPIRATION='true' --name my-flask-app flask-blog
    ```

- Building the Docker Image
    To build the Docker image, navigate to the directory containing the Dockerfile and run:
    ```
    docker build -t flask-blog .
    ```

- Running the Container
    Run your Docker container using the following command:

    ```
    docker run -d -p 5000:5000 --name my-flask-app flask-blog
    ```
    This command will start the Flask application in a Docker container named my-flask-app and expose it on port 5000.

- Accessing the Application
    Once the container is running, access the Flask application by navigating to http://localhost:5000 in your web browser.

- Custom Configuration
    




## Configuration
The application uses environment variables stored in a .env file for configuration. These include keys for AWS Cognito and the Flask app's secret key.

## Contributors
To contribute to this project, please fork the repository, make changes, and submit a pull request.
