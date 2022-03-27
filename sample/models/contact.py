"""
Sample Database Model Definition
"""
# pylint: disable=too-few-public-methods,too-many-ancestors

from marshmallow_sqlalchemy import field_for
from ..db import db, ma


class Contact(db.Model):
    """Contact object"""

    __tablename__ = "contacts"
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    email = db.Column(db.String(120))
    phone = db.Column(db.String(30))
    created = db.Column(db.DateTime)


class ContactSchema(ma.SQLAlchemyAutoSchema):
    """Contact schema"""

    class Meta:
        """Schema metadata"""

        model = Contact
        load_instance = True

    id = field_for(Contact, "id", dump_only=True)
