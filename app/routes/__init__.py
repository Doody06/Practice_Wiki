from . import auth, admin

def register_blueprints(app):
    return app.register_blueprint(auth.bp), app.register_blueprint(admin.bp)