# Imports
from project import create_app
from flask import Flask

# Entry point
app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
