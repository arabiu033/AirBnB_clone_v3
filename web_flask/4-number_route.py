#!/usr/bin/python3
""" Script that starts a Flask web application """
from flask import Flask

app = Flask(__name__)
app.url_map.strict_slashes = False


@app.route('/')
def hello_hbnb():
    """ Print Hello HBNB"""
    return 'Hello HBNB!'


@app.route('/hbnb')
def hbnb():
    """ Print HBNB """
    return 'HBNB'


@app.route('/c/<text>')
def variable(text):
    """ Print variable """
    return 'C {}'.format(text.replace('_', ' '))


@app.route('/python')
@app.route('/python/<text>')
def pytext(text='is cool'):
    """ Print python text """
    return 'Python {}'.format(text.replace('_', ' '))


@app.route('/number/<int:n>')
def num(n):
    """ number route"""
    return '{:d} is a number'.format(n)


if __name__ == '__main__':
    app.run(debug=True)
    app.run(host='0.0.0.0', port=5000)
