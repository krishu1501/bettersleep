from .app import db
db.create_all()

# from werkzeug.serving import make_ssl_devcert
# make_ssl_devcert('./ssl', host='localhost')