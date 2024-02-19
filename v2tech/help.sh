#!/bin/bash

# Set the path to your virtual environment
VENV_PATH="./venv"

# Check if the first argument is "activate"
if [ "$1" == "venv" ]; then
    # Activate the virtual environment
    source "${VENV_PATH}/Scripts/activate"
elif [ "$1" == "install" ]; then
    # Install dependencies
    pip install -r requirement.txt
elif [ "$1" == "server" ]; then
    # Run the development server
    python manage.py runserver "$2"
elif [ "$1" == "migrate" ]; then
    # Apply database migrations
    python manage.py makemigrations
    python manage.py migrate
elif [ "$1" == "superuser" ]; then
    # Create a superuser
    python manage.py createsuperuser
elif [ "$1" == "-venv" ]; then
    # Deactivate the virtual environment
    deactivate
elif [ "$1" == "init" ]; then
    # Initialize the virtual environment
    virtualenv venv
elif [ "$1" == "first" ]; then
    # Install virtualenv, create venv, activate, install requirements, and run server
    pip install virtualenv
    virtualenv venv
    source "${VENV_PATH}/Scripts/activate"
    pip install -r requirement.txt
    python manage.py runserver
elif [ "$1" == "run" ]; then
    # Activate and run the development server
    source "${VENV_PATH}/Scripts/activate"
    python manage.py runserver
elif [ "$1" == "shell" ]; then
    # Open Django shell
    python manage.py shell
else
    # Handle unrecognized command
    echo "Unrecognized command: $1"
    echo "Instead, you can use the following commands:"
    echo "./script.sh first"
    echo "./script.sh run"
    echo "./script.sh migrate"
    echo "./script.sh superuser"
    echo "./script.sh venv"
    echo "./script.sh shell"
fi
