from operator import call

from flask_babel import gettext as _

from app.extensions.db import db


class District(db.Model):
    __tablename__ = "district"

    province_uid = db.Column(db.String(8), db.ForeignKey("province.uid"))
    name = db.Column(db.String(100))

    province = db.relationship(
        "Province",
        back_populates="districts",
    )

    def to_dict(self) -> dict:
        return {
            "name": _(self.name),
            "province_uid": self.province_uid,
            **call(getattr(super(), "to_dict")),
        }

    def __repr__(self):
        return f"<District name={self.name!r}>"
