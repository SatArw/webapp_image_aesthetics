from website import create_app
from flask import Flask
from flask_mail import Mail
app = create_app()

if __name__ == '__main__':
    app.run(host = "0.0.0.0")
