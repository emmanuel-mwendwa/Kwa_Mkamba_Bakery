from app import create_app, db
from flask_migrate import Migrate
from app.models import Role, User, Permission, Product, ProductionRun, Supplier, SupplierIngredient, Ingredient, Recipe, RecipeIngredient, Route, Customer, Dispatch, DispatchDetails, PaymentMethod, Order, OrderDetail
import os

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
migrate = Migrate(app, db)

@app.shell_context_processor
def make_shell_processor():
    return dict(
        db=db, 
        User=User, 
        Role=Role, 
        Permission=Permission, 
        Product=Product, 
        ProductionRun=ProductionRun,
        Supplier=Supplier,
        SupplierIngredient=SupplierIngredient,
        Ingredient=Ingredient,
        Recipe=Recipe,
        RecipeIngredient=RecipeIngredient,
        Route=Route,
        Customer=Customer,
        Dispatch=Dispatch,
        DispatchDetails=DispatchDetails,
        Order=Order,
        OrderDetail=OrderDetail,
        PaymentMethod=PaymentMethod
    )
