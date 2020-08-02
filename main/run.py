import os
# from .app import create_app
from main.app import app

# app = create_app()
# app.app_context().push()

# app.secret_key = os.urandom(16)
if __name__ == '__main__':
	app.run(debug=True, ssl_context=('./ssl.crt', './ssl.key'))
	# app.run(debug=True, ssl_context=('./ssl.crt', './ssl.key'), host='0.0.0.0')

# app.run('localhost', 5000, debug=True)
