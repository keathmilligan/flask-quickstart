"""
Sample RESTful model view

An example of a RESTful interface to a database model using SQLAlchemy and
Marshmallow.
"""

from flask import abort, request
from flask.views import MethodView
from flask.json import jsonify
from sqlalchemy.orm.exc import NoResultFound
from flask_jwt import jwt_required

from .. import app, db
from ..models.contact import Contact, ContactSchema


class ContactView(MethodView):

    decorators = [jwt_required()]
    schema = ContactSchema()
    schema_many = ContactSchema(many=True)

    def get(self, id=None):
        if id is not None:
            # get a single Contact
            try:
                contact = Contact.query.filter(Contact.id == id).one()
                return jsonify(ContactView.schema.dump(contact).data)
            except NoResultFound:
                abort(404)
        else:
            # get all contacts
            contacts = Contact.query.all()
            return jsonify(ContactView.schema_many.dump(contacts).data)

    def put(self):
        # create a new contact
        result = ContactView.schema.load(request.get_json())
        # check for marshalling errors
        if len(result.errors):
            abort(400)
        else:
            contact = result.data
            db.session.add(contact)
            db.session.flush()
            id = contact.id
            db.session.commit()
            return jsonify({'id': id, 'action': 'created'})

    def post(self, id):
        # update an existing contact
        try:
            contact = Contact.query.filter(Contact.id == id).one()
            result = ContactView.schema.load(request.get_json(),
                                             instance=contact,
                                             partial=True)
            # check for marshalling errors
            if len(result.errors):
                abort(400)
            else:
                db.session.commit()
                return jsonify({'id': id, 'action': 'updated'})
        except NoResultFound:
            abort(404)

    def delete(self, id):
        # delete a contact
        try:
            Contact.query.filter(Contact.id == id).delete()
            db.session.commit()
            return jsonify({'id': id, 'action': 'deleted'})
        except NoResultFound:
            abort(404)


app.add_url_rule('/api/contacts', view_func=ContactView.as_view('all_contacts'))
app.add_url_rule('/api/contacts/<int:id>', view_func=ContactView.as_view('contacts'))
