from operator import call

from app.extensions.db import db


class Province(db.Model):
    __tablename__ = "province"

    name = db.Column(db.String(100), unique=True)

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            **call(getattr(super(), "to_dict")),
        }

    def __repr__(self):
        return f"<Province name={self.name!r}>"
