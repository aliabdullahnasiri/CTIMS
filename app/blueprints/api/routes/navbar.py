from typing import Dict, List

from flask import jsonify, url_for
from flask_login import current_user, login_required

from app.blueprints.api import bp
from app.models.permission import Permission
from app.models.role import Role
from flask_babel import _

ITEMS: List[Dict] = [
    {
        "type": "item",
        "title": _("DASHBOARD_LABEL"),
        "icon": "dashboard",
        "endpoint": "admin.dashboard",
        "permissions": Permission.get("VIEW_DASHBOARD"),
    },
    {
        "type": "item",
        "title": _("USERS_LABEL"),
        "icon": "groups",
        "endpoint": "admin.users",
        "permissions": Permission.get("FETCH_USERS") | Permission.get("FETCH_USER"),
    },
    {
        "type": "item",
        "title": _("PERMISSIONS_LABEL"),
        "icon": "lock_open_circle",
        "endpoint": "admin.permissions",
        "permissions": Permission.get("FETCH_PERMISSIONS")
        | Permission.get("FETCH_PERMISSION"),
    },
    {
        "type": "item",
        "title": _("ROLES_LABEL"),
        "icon": "supervised_user_circle",
        "endpoint": "admin.roles",
        "permissions": Permission.get("FETCH_ROLES") | Permission.get("FETCH_ROLE"),
    },
    {
        "type": "section",
        "title": _("CTI_MANAGEMENT_TITLE"),
        "items": [
            {
                "type": "item",
                "title": _("TIMES_TITLE"),
                "icon": None,
                "endpoint": "admin.times",
                "permissions": Permission.get("FETCH_TIMES")
                | Permission.get("FETCH_TIME"),
            },
            {
                "type": "item",
                "title": _("DEPARTMENTS_LABEL"),
                "icon": None,
                "endpoint": "admin.departments",
                "permissions": Permission.get("FETCH_DEPARTMENTS")
                | Permission.get("FETCH_DEPARTMENT"),
            },
            {
                "type": "item",
                "title": _("SEMESTERS_LABEL"),
                "icon": None,
                "endpoint": "admin.semesters",
                "permissions": Permission.get("FETCH_SEMESTERS")
                | Permission.get("FETCH_SEMESTER"),
            },
            {
                "type": "item",
                "title": _("JOBS_LABEL"),
                "icon": None,
                "endpoint": "admin.jobs",
                "permissions": Permission.get("FETCH_JOBS")
                | Permission.get("FETCH_JOB"),
            },
            {
                "type": "item",
                "title": _("EMPLOYEES_LABEL"),
                "icon": None,
                "endpoint": "admin.employees",
                "permissions": Permission.get("FETCH_EMPLOYEES")
                | Permission.get("FETCH_EMPLOYEE"),
            },
            {
                "type": "item",
                "title": _("TEACHER_LABEL"),
                "icon": None,
                "endpoint": "admin.teachers",
                "permissions": Permission.get("FETCH_TEACHERS")
                | Permission.get("FETCH_TEACHER"),
            },
            {
                "type": "item",
                "title": _("SUBJECTS_LABEL"),
                "icon": None,
                "endpoint": "admin.subjects",
                "permissions": Permission.get("FETCH_SUBJECTS")
                | Permission.get("FETCH_SUBJECT"),
            },
            {
                "type": "item",
                "title": _("CLASSES_LABEL"),
                "icon": None,
                "endpoint": "admin.classes",
                "permissions": Permission.get("FETCH_CLASSES")
                | Permission.get("FETCH_CLASS"),
            },
            {
                "type": "item",
                "title": _("STUDENTS_LABEL"),
                "icon": None,
                "endpoint": "admin.students",
                "permissions": Permission.get("FETCH_STUDENTS")
                | Permission.get("FETCH_STUDENT"),
            },
            {
                "type": "item",
                "title": _("EXAMS_LABEL"),
                "icon": None,
                "endpoint": "admin.exams",
                "permissions": Permission.get("FETCH_EXAMS")
                | Permission.get("FETCH_EXAM"),
            },
            {
                "type": "item",
                "title": _("RESULTS_LABEL"),
                "icon": None,
                "endpoint": "admin.results",
                "permissions": Permission.get("FETCH_RESULTS")
                | Permission.get("FETCH_RESULT"),
            },
            {
                "type": "item",
                "title": _("TEACHERS_ATTENDANCES_LABEL"),
                "icon": None,
                "endpoint": "admin.teachers_attendances",
                "permissions": Permission.get("FETCH_TEACHERS_ATTENDANCES")
                | Permission.get("FETCH_TEACHER_ATTENDANCE"),
            },
            {
                "type": "item",
                "title": _("STUDENTS_ATTENDANCES_LABEL"),
                "icon": None,
                "endpoint": "admin.students_attendances",
                "permissions": Permission.get("FETCH_STUDENTS_ATTENDANCES")
                | Permission.get("FETCH_STUDENT_ATTENDANCE"),
            },
        ],
    },
    {
        "type": "section",
        "title": _("ACCOUNT_TITLE"),
        "items": [
            {
                "type": "item",
                "title": _("PROFILE_TITLE"),
                "icon": "person",
                "endpoint": "admin.profile",
            },
        ],
    },
]


def build_navbar(current_user) -> List:
    return list(
        filter(
            lambda f_item: (
                type(f_item["for"]) is str
                and current_user.primary_role_uid
                == getattr(Role.get(f_item["for"]), "uid")
                if f_item and f_item.get("for")
                else True
            ),
            [
                (
                    {
                        "type": item.get("type"),
                        "title": item.get("title"),
                        "for": item.get("for"),
                        "icon": item.get("icon"),
                        "items": list(
                            map(
                                lambda m_item: {
                                    "type": m_item.get("type"),
                                    "title": m_item.get("title"),
                                    "icon": m_item.get("icon"),
                                    "url": url_for(m_item.get("endpoint")),
                                    "for": item.get("for"),
                                },
                                filter(
                                    lambda i: current_user.can(i.get("permissions", 0)),
                                    item.get("items", []),
                                ),
                            )
                        ),
                    }
                    if item.get("type") == "section"
                    else (
                        {
                            "type": item.get("type"),
                            "title": item.get("title"),
                            "for": item.get("for"),
                            "icon": item.get("icon"),
                            "url": url_for(item["endpoint"]),
                        }
                        if current_user.can(item.get("permissions", 0))
                        else None
                    )
                )
                for item in ITEMS
            ],
        )
    )


@bp.route("/navbar")
@login_required
def navbar():
    return jsonify(build_navbar(current_user))