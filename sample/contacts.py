"""
Flask Sample blueprint - Contacts View
"""

from datetime import datetime
from flask import Blueprint, redirect, request, abort, render_template, url_for, flash
from flask.views import MethodView
from flask.json import jsonify
from flask_jwt_extended import jwt_required
from sqlalchemy.orm.exc import NoResultFound
from marshmallow import ValidationError
from .auth import auth_required
from .db import db
from .models.contact import Contact, ContactSchema


blueprint = Blueprint("contacts", __name__)


# Page-Oriented Views
# Delete these if you don't plan to serve HTML


@blueprint.route("/contacts", methods=["GET"])
@auth_required()
def list_contacts():
    """
    List all contacts
    """
    contacts = list(Contact.query.all())
    return render_template("contacts/contacts.html", contacts=contacts)


@blueprint.route("/contact/<int:contact_id>", methods=["GET"])
@auth_required()
def get_contact(contact_id):
    """
    Get a contact
    """
    try:
        contact = Contact.query.filter(Contact.id == contact_id).one()
        return render_template("contacts/contact.html", contact=contact)
    except NoResultFound:
        abort(404, "Contact not found")


@blueprint.route("/contact/new", methods=["GET", "POST"])
@auth_required()
def new_contact():
    """
    Create a new contact
    """
    if request.method == "GET":
        return render_template("contacts/new_contact.html")
    else:
        try:
            # create a new contact
            contact = Contact()
            contact.first_name = request.form["first_name"]
            contact.last_name = request.form["last_name"]
            contact.email = request.form["email"]
            contact.phone = request.form["phone"]
            contact.created = datetime.now()
            db.session.add(contact)
            db.session.commit()
            flash('Contact created')
            return redirect(url_for("contacts.list_contacts"))
        except ValidationError:
            abort(400)


@blueprint.route("/contact/edit/<int:contact_id>", methods=["GET", "POST"])
@auth_required()
def update_contact(contact_id):
    """
    Update a contact
    """
    try:
        contact = Contact.query.filter(Contact.id == contact_id).one()
        if request.method == "GET":
            return render_template("contacts/edit_contact.html", contact=contact)
        else:
            contact.first_name = request.form["first_name"]
            contact.last_name = request.form["last_name"]
            contact.email = request.form["email"]
            contact.phone = request.form["phone"]
            db.session.commit()
            flash('Contact updated')
            return redirect(url_for("contacts.list_contacts"))
    except NoResultFound:
        abort(404, "Contact not found")


@blueprint.route("/contact/delete/<int:contact_id>", methods=["GET", "POST"])
@auth_required()
def delete_contact(contact_id):
    """
    Delete a contact
    """
    try:
        contact = Contact.query.filter(Contact.id == contact_id).one()
        if request.method == "GET":
            return render_template("contacts/delete_contact.html", contact=contact)
        else:
            Contact.query.filter(Contact.id == contact_id).delete()
            db.session.commit()
            flash("Contact deleted")
            return redirect(url_for("contacts.list_contacts"))
    except NoResultFound:
        abort(404, "Contact not found")


# API-Oriented View
# Delete this if you don't need to provide RESTful APIs


class ContactView(MethodView):
    """
    RESTful Contacts Resource
    """

    decorators = [jwt_required()]
    schema = ContactSchema()
    schema_many = ContactSchema(many=True)

    def get(self, contact_id=None):
        """Get a contact or all contacts"""
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
        """Create a contact"""
        try:
            contact = ContactView.schema.load(request.get_json())
            db.session.add(contact)
            db.session.flush()
            contact_id = contact.id
            db.session.commit()
            return jsonify({"contact_id": contact_id, "action": "created"})
        except ValidationError:
            abort(400)

    def post(self, contact_id):
        """Update a contact"""
        try:
            contact = Contact.query.filter(Contact.id == contact_id).one()
            contact = ContactView.schema.load(
                request.get_json(), instance=contact, partial=True
            )
            db.session.commit()
            return jsonify({"contact_id": contact_id, "action": "updated"})
        except NoResultFound:
            abort(404)
        except ValidationError:
            abort(400)

    def delete(self, contact_id):
        """Delete a contact"""
        try:
            Contact.query.filter(Contact.id == contact_id).delete()
            db.session.commit()
            return jsonify({"contact_id": contact_id, "action": "deleted"})
        except NoResultFound:
            abort(404)


blueprint.add_url_rule(
    "/api/contacts", view_func=ContactView.as_view("all_contacts_api")
)
blueprint.add_url_rule(
    "/api/contacts/<int:contact_id>", view_func=ContactView.as_view("contacts_api")
)
