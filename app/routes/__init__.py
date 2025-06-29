from . import auth, admin, user

def register_blueprints(app):
    return app.register_blueprint(auth.bp), app.register_blueprint(admin.bp), app.register_blueprint(user.bp)