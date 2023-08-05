# Flask-Stride

## Introduction
Flask-Stride is a [Flask](http://flask.pocoo.org/) extension that lets you easily create [Atlassian Stride](https://www.stride.com/) apps (a.k.a bots)

## Installation
Using Pip: `pip install flask-stride`

## Example

```
from flask import Flask
from flask_stride import Stride

app = Flask(__name__)

s = Stride(key='My Bot')

@s.chat_bot('my_bot', '/mention', '/direct-message')
def chat_f():
    # Do Stuff
    return ('',203)

# This needs to be called after defining all of your bot code
s.init_app(a)
```
The above code will create a simple bot called "My Bot" and setups all of the endpoints required.
Whenver your bot is mentioned in a conversation or directly, the `chat_f()` function will be executed.

As an added bonus, the App Descriptor endpoint is automatically configured for you. By default, it is located at [/app-descriptor.json]() of your web server.