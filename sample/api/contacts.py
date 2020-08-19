"""
Sample RESTful model view

An example of a RESTful interface to a database model using SQLAlchemy and
Marshmallow.
"""

from flask import abort, request
from flask.views import MethodView
from flask.json import jsonify
from sqlalchemy.orm.exc import NoResultFound
from flask_jwt_extended import jwt_required
from marshmallow import ValidationError

from .. import app, db
from ..models.contact import Contact, ContactSchema


class ContactView(MethodView):

    decorators = [jwt_required]
    schema = ContactSchema()
    schema_many = ContactSchema(many=True)

    def get(self, contact_id=None):
        if contact_id is not None:
            # get a single Contact
            try:
                contact = Contact.query.filter(Contact.id == contact_id).one()
                return jsonify(ContactView.schema.dump(contact))
            except NoResultFound:
                abort(404)
        else:
            # get all contacts
            contacts = Contact.query.all()
            return jsonify(ContactView.schema_many.dump(contacts))

    def put(self):
        try:
            # create a new contact
            contact = ContactView.schema.load(request.get_json())
            db.session.add(contact)
            db.session.flush()
            contact_id = contact.id
            db.session.commit()
            return jsonify({'contact_id': contact_id, 'action': 'created'})
        except ValidationError:
            abort(400)

    def post(self, contact_id):
        # update an existing contact
        try:
            contact = Contact.query.filter(Contact.id == contact_id).one()
            contact = ContactView.schema.load(request.get_json(),
                                              instance=contact,
                                              partial=True)
            db.session.commit()
            return jsonify({'contact_id': contact_id, 'action': 'updated'})
        except NoResultFound:
            abort(404)
        except ValidationError:
            abort(400)

    def delete(self, contact_id):
        # delete a contact
        try:
            Contact.query.filter(Contact.id == contact_id).delete()
            db.session.commit()
            return jsonify({'contact_id': contact_id, 'action': 'deleted'})
        except NoResultFound:
            abort(404)


app.add_url_rule('/api/contacts', view_func=ContactView.as_view('all_contacts'))
app.add_url_rule('/api/contacts/<int:contact_id>', view_func=ContactView.as_view('contacts'))
