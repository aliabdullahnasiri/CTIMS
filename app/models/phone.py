from operator import call

from app.extensions.db import db


class Phone(db.Model):
    __tablename__ = "phones"

    user_id = db.Column(db.String(8), db.ForeignKey("users.uid"), nullable=False)
    number = db.Column(db.String(20), unique=True, nullable=False)

    user = db.relationship("User", back_populates="phones")

    def to_dict(self) -> dict:
        return {
            "number": self.number,
            "user_id": self.user_id,
            **call(getattr(super(), "to_dict")),
        }

    def __repr__(self):
        return f"<Phone {self.number} Employee={self.user_id}>"
