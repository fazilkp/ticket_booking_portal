## main.py
from flask import Flask
from app import create_app

# Entry point for the Flask application
if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
