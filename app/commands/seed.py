import json

import click
from flask.cli import with_appcontext

from app.extensions.console import console
from app.extensions.db import db
from app.models.district import District
from app.models.province import Province


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
