from app.main import app, config


def create_app(config_name):
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    return app
