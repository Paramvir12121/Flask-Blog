# Flask-Blog (WIP)

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Dependencies](#dependencies)
- [Configuration](#configuration)
- [Contributors](#contributors)
- [License](#license)

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
   ```bash
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
## Dependencies
All dependencies are listed in requirements.txt. Major dependencies include Flask, SQLAlchemy, Flask-WTF, and Boto3.

## Configuration
The application uses environment variables stored in a .env file for configuration. These include keys for AWS Cognito and the Flask app's secret key.

## Contributors
To contribute to this project, please fork the repository, make changes, and submit a pull request.
