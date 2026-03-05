# Imports
from project import create_app, login_manager
from flask import Flask

# Entry point
app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
