from flask import Flask

# Create an instance of the class for our use
app = Flask(__name__)

# If we need to enable debug for futire dev
app.debug = False
# Enable pretty print for easier to read dev
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True