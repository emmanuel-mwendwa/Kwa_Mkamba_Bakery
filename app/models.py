from . import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, AnonymousUserMixin
from flask import current_app
import jwt
import datetime


class Permission:
    VIEW_PRODUCTS = 1
    VIEW_INVENTORY = 2
    VIEW_PRODUCTION_RUN = 4
    MANAGE_INVENTORY = 8
    MANAGE_PRODUCTION_RUN = 16
    VIEW_SALES_REPORT = 32
    MANAGE_SALES_REPORT = 64
    VIEW_RECIPE_DETAILS = 128
    MANAGE_RECIPE_DETAILS = 256
    MANAGER = 512
    ADMINISTRATOR = 1024


class Role(db.Model):
    __tablename__ = "roles"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    # role assigned to new users upon registration
    default = db.Column(db.Boolean, default=False, index=True)
    # permissions allowed for different users
    permissions = db.Column(db.Integer)
    users = db.relationship('User', backref='role', lazy='dynamic')

    # set the value of permissions to 0 if no initial value is given
    def __init__(self, **kwargs):
        super(Role, self).__init__(**kwargs)
        if self.permissions is None:
            self.permissions = 0

    # add permission
    def add_permission(self, perm):
        if not self.has_permission(perm):
            self.permissions += perm

    # remove permission
    def remove_permission(self, perm):
        if self.has_permission(perm):
            self.permissions -= perm

    # reset permission
    def reset_permissions(self):
        self.permissions = 0

    # check if user has permission
    def has_permission(self, perm):
        return self.permissions & perm == perm
    
    # adding roles to the database
    @staticmethod
    def insert_roles():
        roles = {
            'User': [Permission.VIEW_PRODUCTS],

            'Baker': [Permission.VIEW_RECIPE_DETAILS, Permission.MANAGE_RECIPE_DETAILS],

            'Sales_Associate': [Permission.VIEW_SALES_REPORT, Permission.MANAGE_SALES_REPORT, Permission.VIEW_INVENTORY, Permission.VIEW_PRODUCTS],

            'Production_Supervisor': [Permission.VIEW_PRODUCTS, Permission.VIEW_PRODUCTION_RUN, Permission.VIEW_INVENTORY, Permission.MANAGE_INVENTORY, Permission.MANAGE_PRODUCTION_RUN],

            'Manager': [Permission.VIEW_PRODUCTS, Permission.VIEW_INVENTORY, Permission.VIEW_PRODUCTION_RUN, Permission.VIEW_SALES_REPORT, Permission.MANAGE_INVENTORY, Permission.MANAGE_PRODUCTION_RUN, Permission.MANAGE_SALES_REPORT, Permission.MANAGER],

            'Administrator': [Permission.VIEW_PRODUCTS, Permission.VIEW_INVENTORY, Permission.VIEW_PRODUCTION_RUN, Permission.MANAGE_INVENTORY, Permission.MANAGE_PRODUCTION_RUN, Permission.VIEW_SALES_REPORT, Permission.MANAGE_SALES_REPORT, Permission.VIEW_RECIPE_DETAILS, Permission.MANAGE_RECIPE_DETAILS, Permission.MANAGER, Permission.ADMINISTRATOR]
        }
        default_role = 'User'
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.reset_permissions()
            for perm in roles[r]:
                role.add_permission(perm)
            role.default = (role.name == default_role)
            db.session.add(role)
        db.session.commit()

class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    email = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    confirmed = db.Column(db.Boolean, default=False)
    name = db.Column(db.String(64))
    phone_no = db.Column(db.String(13))
    member_since = db.Column(db.DateTime(), default=datetime.datetime.utcnow())
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    @property
    def password(self):
        raise AttributeError('Password is not a readable attribute')
    
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)
    

    def generate_confirmation_token(self, expiration=3600):
        confirmation_token = jwt.encode({
            "confirm": self.id,
            "exp": datetime.datetime.now(tz=datetime.timezone.utc) + datetime.timedelta(seconds=expiration)
        },
        current_app.config['SECRET_KEY'],
        algorithm="HS256"
        )
        return confirmation_token
    
    def confirm(self, token):
        try:
            data = jwt.decode(
                token,
                current_app.config['SECRET_KEY'],
                leeway=datetime.timedelta(seconds=10),
                algorithms=["HS256"]
            )
        except:
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        db.session.add(self)
        return True
    
    def generate_reset_token(self, expiration=3600):
        reset_password_token = jwt.encode({
            "reset": self.id,
            "exp": datetime.datetime.now(tz=datetime.timezone.utc) + datetime.timedelta(seconds=expiration)
        },
        current_app.config['SECRET_KEY'],
        algorithm="HS256"
        )
        return reset_password_token

    @staticmethod
    def reset_password(token, new_password):
        try:
            data = jwt.decode(
                token,
                current_app.config['SECRET_KEY'],
                leeway=datetime.timedelta(seconds=10),
                algorithms=["HS256"]
            )
        except:
            return False
        user = User.query.get(data.get('reset'))
        if user is None:
            return False
        user.password = new_password
        db.session.add(user)
        return True


    def generate_email_change_token(self, new_email, expiration=3600):
        change_email_token = jwt.encode({
            "change_email": self.id,
            "new_email": new_email,
            "exp": datetime.datetime.now(tz=datetime.timezone.utc) + datetime.timedelta(seconds=expiration)
        },
        current_app.config['SECRET_KEY'],
        algorithm="HS256"
        )
        return change_email_token

    def change_email(self, token):
        try:
            data = jwt.decode(
                    token,
                    current_app.config['SECRET_KEY'],
                    leeway=datetime.timedelta(seconds=10),
                    algorithms=["HS256"]
                )
        except:
            return False
        if data.get('change_email') != self.id:
            return False
        new_email = data.get('new_email')
        if new_email is None:
            return False
        if self.query.filter_by(email=new_email).first() is not None:
            return False
        self.email = new_email
        db.session.add(self)
        return True

    # assigning roles to users
    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.role is None:
            if self.email == current_app.config['APP_ADMIN']:
                self.role = Role.query.filter_by(name='Administrator').first()
            if self.role is None:
                self.role = Role.query.filter_by(default=True).first()

    # role verification
    def can(self, perm):
        return self.role is not None and self.role.has_permission(perm)
    
    def is_administrator(self):
        return self.can(Permission.ADMINISTRATOR)
    

class AnonymousUser(AnonymousUserMixin):
    def can(self, permissions):
        return False
    
    def is_administrator(self):
        return False
    
login_manager.anonymous_user = AnonymousUser

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Product(db.Model):
    __tablename__ = "products"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(24))
    price = db.Column(db.Integer)
    description = db.Column(db.Text)
    date_created = db.Column(db.DateTime(), index=True, default=datetime.datetime.utcnow())
    product = db.relationship('Production_Run', backref='role', lazy='dynamic')


class Production_Run(db.Model):
    __tablename__ = "production_runs"

    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey("products.id"))
    quantity = db.Column(db.Integer)
    flour_kneaded = db.Column(db.Integer)
    date_created = db.Column(db.DateTime(), index=True, default=datetime.datetime.utcnow())