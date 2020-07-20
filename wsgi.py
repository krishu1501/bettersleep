import os
from main.app import app
app.secret_key = os.urandom(16)
app.run(debug=True, ssl_context=('./ssl.crt', './ssl.key'))

# app.run('localhost', 5000, debug=True)
