from . import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, AnonymousUserMixin
from flask import current_app
from sqlalchemy import event
from sqlalchemy.ext.declarative import declarative_base
import jwt
import datetime


Base = declarative_base()

class Permission:
    VIEW_PRODUCTS = 1
    VIEW_INVENTORY = 2
    VIEW_PRODUCTION_RUN = 4
    MANAGE_PRODUCTS = 8
    MANAGE_INVENTORY = 16
    MANAGE_PRODUCTION_RUN = 32
    VIEW_SALES_REPORT = 64
    MANAGE_SALES_REPORT = 128
    VIEW_RECIPE_DETAILS = 256
    MANAGE_RECIPE_DETAILS = 512
    MANAGER = 1024
    ADMINISTRATOR = 2048


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

            'Baker': [Permission.VIEW_RECIPE_DETAILS, Permission.MANAGE_RECIPE_DETAILS, Permission.VIEW_PRODUCTS],

            'Sales_Associate': [Permission.VIEW_SALES_REPORT, Permission.MANAGE_SALES_REPORT, Permission.VIEW_INVENTORY, Permission.VIEW_PRODUCTS],

            'Production_Supervisor': [Permission.VIEW_PRODUCTS, Permission.VIEW_PRODUCTION_RUN, Permission.VIEW_INVENTORY, Permission.MANAGE_PRODUCTS, Permission.MANAGE_INVENTORY, Permission.MANAGE_PRODUCTION_RUN],

            'Manager': [Permission.VIEW_PRODUCTS, Permission.VIEW_INVENTORY, Permission.VIEW_PRODUCTION_RUN, Permission.VIEW_SALES_REPORT, Permission.MANAGE_PRODUCTS, Permission.MANAGE_INVENTORY, Permission.MANAGE_PRODUCTION_RUN, Permission.MANAGE_SALES_REPORT, Permission.MANAGER],

            'Administrator': [Permission.VIEW_PRODUCTS, Permission.VIEW_INVENTORY, Permission.VIEW_PRODUCTION_RUN, Permission.MANAGE_PRODUCTS, Permission.MANAGE_INVENTORY, Permission.MANAGE_PRODUCTION_RUN, Permission.VIEW_SALES_REPORT, Permission.MANAGE_SALES_REPORT, Permission.VIEW_RECIPE_DETAILS, Permission.MANAGE_RECIPE_DETAILS, Permission.MANAGER, Permission.ADMINISTRATOR]
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
    username = db.Column(db.String(64), unique=True, index=True, nullable=False)
    email = db.Column(db.String(64), unique=True, index=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    confirmed = db.Column(db.Boolean, default=False)
    name = db.Column(db.String(64))
    phone_no = db.Column(db.String(13))
    member_since = db.Column(db.DateTime(), default=datetime.datetime.utcnow())
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    sales_assoc = db.relationship("Route", backref="sales_assoc", lazy="dynamic")

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


# production management tables for my system 
class Product(db.Model):
    __tablename__ = "products"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime(), default=datetime.datetime.utcnow())
    updated_at = db.Column(db.DateTime(), default=datetime.datetime.utcnow())
    production_runs = db.relationship('ProductionRun', backref='production', lazy='dynamic')


class ProductionRun(db.Model):
    __tablename__ = "production_runs"

    id = db.Column(db.Integer, primary_key=True)
    flour_kneaded = db.Column(db.Integer, nullable=False)
    oil_used = db.Column(db.Integer, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'))
    created_at = db.Column(db.DateTime(), default=datetime.datetime.utcnow())
    updated_at = db.Column(db.DateTime(), default=datetime.datetime.utcnow())


class SupplierIngredient(db.Model):
    __tablename__ = "supplier_ingredients"

    supplier_id = db.Column(db.Integer, db.ForeignKey('suppliers.id'), primary_key=True)
    ingredient_id = db.Column(db.Integer, db.ForeignKey('ingredients.id'), primary_key=True)
    unit_cost = db.Column(db.Float, nullable=False)

    supplier = db.relationship('Supplier', backref=db.backref('supplier_ingredients', cascade='all, delete-orphan'))
    ingredient = db.relationship('Ingredient', backref=db.backref('supplier_ingredients', cascade='all, delete-orphan'))


class Supplier(db.Model):
    __tablename__ = "suppliers"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    phone_no = db.Column(db.String(13), nullable=False)
    email = db.Column(db.String(50))
    created_at = db.Column(db.DateTime(), default=datetime.datetime.utcnow())
    updated_at = db.Column(db.DateTime(), default=datetime.datetime.utcnow())

    @staticmethod
    def update_timestamp(mapper, connection, target):
        target.updated_at = datetime.datetime.utcnow()

    @classmethod
    def register_event_listeners(cls):
        event.listen(cls, 'before_update', cls.update_timestamp)

Supplier.register_event_listeners()


class Ingredient(db.Model):
    __tablename__ = "ingredients"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    unit_of_measurement = db.Column(db.String(12))
    created_at = db.Column(db.DateTime(), default=datetime.datetime.utcnow())
    updated_at = db.Column(db.DateTime(), default=datetime.datetime.utcnow())

    # insert ingredients
    @staticmethod
    def insert_ingredients():
        ingredients = {
            "Flour": ["Kilograms"],
            "Saccharin": ["grams"],
            "Yeast": ["grams"],
            "Salt": ["grams"],
            "Baking Powder": ["grams"],
            "Cooking Oil": ["Litres"],
            "Water": ["litres"],
            "Electricity": ["KiloWatts"],
            "Packing Papers": ["Packets"]
        }
        try:
            # iterate over the dictionary to add the ingredients
            for name, values in ingredients.items():
                ingredient = Ingredient.query.filter_by(name=name).first()
                if ingredient is not None: 
                    print(f"Ingredient '{name}' already exists.")
                else:
                    ingredient = Ingredient(
                        name=name,
                        unit_of_measurement=values[0]
                        )
                    db.session.add(ingredient)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(f"Error occured: {e}")


class Recipe(db.Model):
    __tablename__ = "recipes"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.Text)
    yield_amount = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime(), default=datetime.datetime.utcnow())
    updated_at = db.Column(db.DateTime(), default=datetime.datetime.utcnow())
    recipe_ingredients = db.relationship('RecipeIngredient', backref="recipe")


class RecipeIngredient(db.Model):
    __tablename__ = "recipe_ingredients"

    id = db.Column(db.Integer, primary_key=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey("recipes.id"))
    ingredient_id = db.Column(db.Integer, db.ForeignKey("ingredients.id"))
    quantity = db.Column(db.Float, nullable=False)
    unit_of_measurement = db.Column(db.String(12))
    created_at = db.Column(db.DateTime(), default=datetime.datetime.utcnow())
    updated_at = db.Column(db.DateTime(), default=datetime.datetime.utcnow())

    recipe_ingredients = db.relationship('Ingredient', backref='recipe')


# sales management tables for my bakery system 
class Route(db.Model):
    __tablename__ = "routes"

    route_id = db.Column(db.Integer, primary_key=True)
    route_name = db.Column(db.String(26))
    sales_assoc_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    customers = db.relationship('Customer', lazy="dynamic", backref="cust_route")
    dispatch_route = db.relationship('Dispatch', lazy="dynamic", backref="dispatch_route")


class Customer(db.Model):
    __tablename__ = "customers"

    cust_id = db.Column(db.Integer, primary_key=True)
    cust_name = db.Column(db.String(128))
    cust_email = db.Column(db.String(128))
    cust_phone_no = db.Column(db.Integer)
    cust_mpesa_agent_name = db.Column(db.String(128))
    route_id = db.Column(db.Integer, db.ForeignKey("routes.route_id"))


class Dispatch(db.Model):
    __tablename__ = "dispatch"

    dispatch_id = db.Column(db.Integer, primary_key=True)
    dispatch_date = db.Column(db.DateTime())
    route_id = db.Column(db.Integer, db.ForeignKey("routes.route_id"))
    dispatch_details = db.relationship('DispatchDetails', lazy='dynamic', backref='dispatch_details')


class DispatchDetails(db.Model):
    __tablename__ = "dispatch_details"

    id = db.Column(db.Integer, primary_key=True)
    dispatch_id = db.Column(db.Integer, db.ForeignKey("dispatch.dispatch_id"))
    product_id = db.Column(db.Integer, db.ForeignKey("products.id"))
    quantity = db.Column(db.Float)
    returns = db.Column(db.Float)

    product = db.relationship('Product', backref='dispatch_details')


class PaymentMethod(db.Model):
    __tablename__ = "payment_methods"

    method_id = db.Column(db.Integer, primary_key=True)
    method_name =  db.Column(db.String(28))
    method_details = db.Column(db.String(56))

    # insert payment methods
    @staticmethod
    def insert_payment_methods():
        methods = {
            "Cash": "Cash",
            "M-PESA": "M-Pesa Code"
        }
        try:
            # iterate over the dictionary to add the payment methods
            for name, values in methods.items():
                method = PaymentMethod.query.filter_by(method_name=name).first()
                if method is not None: 
                    print(f"Payment method '{name}' already exists.")
                else:
                    method = PaymentMethod(
                        method_name=name,
                        method_details=values
                        )
                    db.session.add(method)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(f"Error occured: {e}")



class Order(db.Model):
    __tablename__ = "orders"

    order_id = db.Column(db.Integer, primary_key=True)
    order_date = db.Column(db.DateTime())
    order_notes = db.Column(db.Text)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.cust_id'))
    payment_method_id = db.Column(db.Integer, db.ForeignKey('payment_methods.method_id'))

    order_details = db.relationship('OrderDetail', backref="orderdetail")
    customer = db.relationship('Customer', backref="customer")
    payment = db.relationship('PaymentMethod', backref="payment")


class OrderDetail(db.Model):
    __tablename__ = "order_details"

    order_detail_id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.order_id'))
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'))
    quantity = db.Column(db.Float)

    product = db.relationship('Product', backref="orderdetail")
