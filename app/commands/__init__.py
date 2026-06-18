from .seed import seed_provinces_and_districts


def register_commands(app):
    app.cli.add_command(seed_provinces_and_districts)
