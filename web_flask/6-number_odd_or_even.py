#!/usr/bin/python3
""" Script that starts a Flask web application """
from flask import Flask, render_template

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


@app.route('/number_template/<int:n>')
def num_template(n):
    """Displays HTML page is n is an integer"""
    return render_template('5-number.html', n=n)


@app.route('/number_odd_or_even/<int:n>')
def num_even_or_odd(n):
    """ Display number even or odd"""
    return render_template('6-number_odd_or_even.html', n=n)


if __name__ == '__main__':
    app.run(debug=True)
    app.run(host='0.0.0.0', port=5000)
