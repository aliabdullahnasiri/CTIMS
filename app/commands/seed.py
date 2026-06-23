import json
from typing import List, Union

import click
from flask.cli import with_appcontext

from app.extensions.console import console
from app.extensions.db import db
from app.models.district import District
from app.models.province import Province
from app.models.subject import SchoolGrade, SchoolSubject


@click.command("seed-provinces-and-districts")
@with_appcontext
def seed_provinces_and_districts():
    with open("data/provinces-and-districts.json", encoding="utf-8") as f:
        provinces = json.load(f)

        for p in provinces:
            province: Province = Province()
            province.name = p["name"]

            db.session.add(province)
            db.session.commit()

            for d in p["districts"]:
                district: District = District()
                district.name = d["name"]
                setattr(district, "province", province)

                db.session.add(district)
                db.session.commit()

            console.print(province)


@click.command("seed-school-grades-and-subjects")
@with_appcontext
def seed_school_grades_and_subjects():
    with open("data/school-grades.json", encoding="utf-8") as f:
        for g in json.load(f):
            if not SchoolGrade.query.filter_by(name=g).count():
                grade = SchoolGrade()
                grade.name = g

                db.session.add(grade)
                db.session.commit()

    with open("data/school-subjects.json", encoding="utf-8") as f:
        subjects = json.load(f)

        for s in subjects:
            label = s
            grades: Union[List[str], None] = None
            subject: Union[SchoolSubject, None] = None

            if type(s) is dict:
                label = s["name"]
                grades = s["grades"]

            if not (subject := SchoolSubject.query.filter_by(label=label).scalar()):
                subject = SchoolSubject()
                subject.label = label

                db.session.add(subject)
                db.session.commit()

            for g in SchoolGrade.query.all():
                if grades and g.name not in grades:
                    continue

                if subject not in g.subjects:
                    g.subjects.add(subject)
                    db.session.commit()
