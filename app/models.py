from flask import current_app
from . import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import datetime
import time
import jwt


class Role(db.Model):
    __tablename__ = "roles"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(28), unique=True)
    users = db.relationship('User', backref='role', lazy='dynamic')


class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(64))
    username = db.Column(db.String(64), unique=True, index=True)
    email = db.Column(db.String(128), unique=True)
    password_hash = db.Column(db.String(128))
    confirmed = db.Column(db.Boolean, default=False)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    @property
    def password(self):
        raise AttributeError('Password is not a readable object')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def generate_confirmation_token(self, expiration=3600):
        confirmation_token = jwt.encode({
            'confirm': self.id,
            'exp': datetime.datetime.now(tz=datetime.timezone.utc) + datetime.timedelta(seconds=expiration)
        },
        current_app.config['SECRET_KEY'],
        algorithm='HS256'
        )
        return confirmation_token

    def confirm(self, token):
        try:
            data = jwt.decode(
                token,
                current_app.config['SECRET_KEY'],
                leeway = datetime.timedelta(seconds=10),
                algorithms = ["HS256"]
            )
        except:
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        db.session.add(self)
        return True

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# Production tables
# Table to store products
class Product(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(13), unique=True)
    name = db.Column(db.String(20), unique=True)
    description = db.Column(db.String(56))
    price = db.Column(db.Integer)
    date_created = db.Column(db.DateTime,  default=datetime.datetime.utcnow())
    date_updated = db.Column(db.DateTime, default=datetime.datetime.utcnow(), onupdate=datetime.datetime.utcnow())
    production = db.relationship('ProductionRun', backref='product', lazy='dynamic')


# Table to store daily production
class ProductionRun(db.Model):
    __tablename__ = 'production_run'

    id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Integer)
    date_created = db.Column(db.DateTime, default=datetime.datetime.utcnow())
    date_updated = db.Column(db.DateTime, default=datetime.datetime.utcnow(), onupdate=datetime.datetime.utcnow())
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'))
    

# Ingredients table
class Ingredient(db.Model):
    __tablename__ = 'ingredients'

    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(13), unique=True)
    name = db.Column(db.String(30))
    supplier = db.Column(db.String(56))
    unit_cost = db.Column(db.Integer)
    date_created = db.Column(db.DateTime, default=datetime.datetime.utcnow())
    date_updated = db.Column(db.DateTime, default=datetime.datetime.utcnow(), onupdate=datetime.datetime.utcnow())


# Supplier table
class Supplier(db.Model):
    __tablename__ = 'suppliers'

    id = db.Column(db.Integer, primary_key=True)
    supplier_name = db.Column(db.String(56))
    contact_person = db.Column(db.String(56))
    contact_number = db.Column(db.Integer)
    contact_email = db.Column(db.String(56))
    address = db.Column(db.String(56))
    date_created = db.Column(db.DateTime, default=datetime.datetime.utcnow())
    date_updated = db.Column(db.DateTime, default=datetime.datetime.utcnow(), onupdate=datetime.datetime.utcnow())
    inventories = db.relationship('Inventory', backref='supplier', lazy='dynamic')

class Inventory(db.Model):
    __tablename__ = 'inventory'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(56))
    current_quantity = db.Column(db.Integer)
    reorder_level = db.Column(db.Integer)
    cost_per_unit = db.Column(db.Integer)
    total_cost = db.Column(db.Integer)
    date_created = db.Column(db.DateTime, default=datetime.datetime.utcnow())
    date_updated = db.Column(db.DateTime, default=datetime.datetime.utcnow(), onupdate=datetime.datetime.utcnow())
    supplier_id = db.Column(db.Integer, db.ForeignKey('suppliers.id'))