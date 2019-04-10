from settings import database as db

def init_app():
    db.initial_setup()
