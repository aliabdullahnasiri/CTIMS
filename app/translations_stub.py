from flask_babel import gettext as _


def dummy_navbar_strings():
    """
    This function is never executed. It only exists so pybabel extract
    can find dynamic database strings and add them to the .pot file.
    """

    # Top-level items
    _("Dashboard")
    _("Users")
    _("Permissions")
    _("Roles")

    # CTI Management Section
    _("CTI Management")
    _("Times")
    _("Departments")
    _("Semesters")
    _("Jobs")
    _("Employees")
    _("Teacher")
    _("Subjects")
    _("Classes")
    _("Students")
    _("Exams")
    _("Results")
    _("Teachers Attendances")
    _("Students Attendances")

    # Account Section
    _("Account")
    _("Profile")
