"""
this is the "secret sauce" -- a single entry-point that resolves the
import dependencies.  If you're using blueprints, you can import your
blueprints here too.

then when you want to run your app, you point to main.py or `main.app`
"""
import os

from app import db
from app import app
from models import Connection
from views import *

if __name__ == "__main__":
    Connection.create_table(fail_silently=True)
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
