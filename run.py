from flask import Flask
from app import create_app
app = create_app()

from app.routes.admin import *

if __name__ == "__main__":
    app.run(debug=True)
    