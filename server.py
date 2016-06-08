from datetime import datetime
from functools import wraps
from flask import Flask, request, Response

import os

from config import Config

app = Flask(__name__)
app.config.from_object(Config)


def check_auth(username, password):
    """This function is called to check if a username /
    password combination is valid.
    """
    return username == app.config['USERNAME'] and (
           password == app.config['PASSWORD'])


def authenticate():
    """Sends a 401 response that enables basic auth"""
    return Response(
    'Could not verify your access level for that URL.\n'
    'You have to login with proper credentials', 401,
    {'WWW-Authenticate': 'Basic realm="Login Required"'})


def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated


@app.route("/", methods=['GET'])
@requires_auth
def hello():
    return """
<form action="/" method="post"
enctype="multipart/form-data">
<input type="file" name="uploadedfile" id="uploadedfile" /> 
<br />
<input type="submit" name="submit" value="Submit" />
</form>
"""


@app.route("/", methods=['POST'])
@requires_auth
def get_form():
    if 'uploadedfile' not in request.files:
        return "No file selected"
    f = request.files['uploadedfile']
    f.save(os.path.join(app.config['UPLOAD_FOLDER'], datetime.now().strftime('%Y-%m-%d-%H-%m.json')))
    return 'Success'


if __name__ == "__main__":
    app.run()
