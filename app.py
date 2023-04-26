from flask import Flask
from App.routes import app as routes
#import cors
from flask_cors import CORS

app: Flask = Flask(__name__)
CORS(app)

app.config.update(
    JSON_SORT_KEYS=False,
    JSON_AS_ASCII=False
)

app.logger.disabled = True
app.register_blueprint(routes)
