import os

from flask import Flask, render_template, jsonify
import requests

ROOT_PATH = os.path.abspath(os.path.dirname(__file__))


class VueFlask(Flask):
    @property
    def static_folder(self):
        if self.debug:
            return None
        else:
            return os.path.join(ROOT_PATH, 'static')


app = VueFlask(__name__,
               static_folder=None,
               template_folder=os.path.join(ROOT_PATH, 'frontend'))


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    if app.debug:
        return requests.get('http://localhost:8080/{}'.format(path)).text
    return render_template("index.html")