from flask_babel import gettext as _


def dummy_navbar_strings():
    """
    This function is never executed. It only exists so pybabel extract
    can find dynamic database strings and add them to the .pot file.
    """

    # Top-level items
    _("DASHBOARD_LABEL")
    _("USERS_LABEL")
    _("PERMISSIONS_LABEL")
    _("ROLES_LABEL")

    # CTI Management Section
    _("CTI_MANAGEMENT_LABEL")
    _("TIMES_LABEL")
    _("DEPARTMENTS_LABEL")
    _("SEMESTERS_LABEL")
    _("JOBS_LABEL")
    _("EMPLOYEES_LABEL")
    _("TEACHER_LABEL")
    _("SUBJECTS_LABEL")
    _("CLASSES_LABEL")
    _("STUDENTS_LABEL")
    _("EXAMS_LABEL")
    _("RESULTS_LABEL")
    _("TEACHERS_ATTENDANCES_LABEL")
    _("STUDENTS_ATTENDANCES_LABEL")

    # Account Section
    _("ACCOUNT_LABEL")
    _("PROFILE_LABEL")

    # Name
    _("CTI")
    _("Computer Technology Institute")
    _("Ali Abdullah Nasiri")

    # Languages
    _("PS_LABEL")
    _("FA_LABEL")
    _("EN_LABEL")
