from .app import db,app
app.app_context().push()
db.create_all()

# from werkzeug.serving import make_ssl_devcert
# make_ssl_devcert('./ssl', host='localhost')