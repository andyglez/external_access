from settings import database as db, email

def init_app(app):
    db.initial_setup()
    email.set_mail(app.config)
