import os


def config_path(app):
    """
    returns the full config path for the application
    :param app
    :return :full config path
    """
    return os.path.join(app.root_path,"config.env")