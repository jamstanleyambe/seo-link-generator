from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

app.config['UPLOAD_FOLDER'] = "app/uploads"
app.config['OUTPUT_FOLDER'] = "app/seo_output"

from app import routes  # Import API routes
