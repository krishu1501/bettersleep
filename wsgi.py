import os
# from main.app import create_app
from main.app import app

# app = create_app()

# app.secret_key = os.urandom(16)
if __name__ == '__main__':
	app.run(debug=True, ssl_context=('./ssl.crt', './ssl.key'))

# app.run('localhost', 5000, debug=True)
