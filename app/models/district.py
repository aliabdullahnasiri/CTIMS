from operator import call

from app.extensions.db import db


class District(db.Model):
    __tablename__ = "district"

    province_uid = db.Column(db.String(8), db.ForeignKey("province.uid"))
    name = db.Column(db.String(100))

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "province_uid": self.province_uid,
            **call(getattr(super(), "to_dict")),
        }

    def __repr__(self):
        return f"<District name={self.name!r}>"
