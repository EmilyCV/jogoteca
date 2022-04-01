import os
from flask import Flask

app = Flask(__name__)
app.config.from_pyfile('config.py')

from views import *

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
