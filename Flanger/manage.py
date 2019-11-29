from flanger.app import FlangerApp
from flask import  request

app = FlangerApp(__name__)


@app.route('/')
def hello():
    a = request
    return {}


if __name__ == '__main__':
    app.run(debug=True, port=8080)
