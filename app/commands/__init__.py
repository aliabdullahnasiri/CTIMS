from .seed import seed_provinces_and_districts, seed_school_grades_and_subjects


def register_commands(app):
    app.cli.add_command(seed_provinces_and_districts)
    app.cli.add_command(seed_school_grades_and_subjects)
