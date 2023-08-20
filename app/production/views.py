from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required
from . import production
from .forms import AddNewProductForm, AddNewProductionRunForm, AddNewIngredient, AddNewSupplier, RecipeForm
from .. import db
from ..models import Product, ProductionRun, Ingredient, Supplier, SupplierIngredient, Recipe, RecipeIngredient, Permission
from ..decorators import admin_required, permission_required
from datetime import datetime


@production.route('/')
def production_home():
    return render_template("production/production.html")

# Add a new product in the database
@production.route('/new_product', methods=["GET", "POST"])
@permission_required(Permission.MANAGE_PRODUCTS)
def new_product():
    title = "Add Product"
    product_form = AddNewProductForm()
    if product_form.validate_on_submit():
        # check if a similar product exists
        product = Product.query.filter_by(name=product_form.name.data).first()
        if product is not None:
            flash("A product with this name already exists.", category="error")
        new_product = Product(
            name=product_form.name.data, 
            price=product_form.price.data, 
            description=product_form.description.data
            )
        db.session.add(new_product)
        db.session.commit()
        flash("Product added successfully", category="success")
        return redirect(url_for("production.view_products"))
    return render_template("production/products/create_product.html", product_form=product_form, title=title)

# View the products in the database
@production.route('/view_products', methods=["GET", "POST"])
def view_products():
    products = Product.query.all()
    return render_template("production/products/view_products.html", products=products)

@production.route('/view_product/<int:id>')
def view_product(id):
    product = Product.query.get_or_404(id)
    production_runs = product.production_runs.all()
    return render_template("production/products/view_product.html", product=product, production_runs=production_runs)

# Edit values of the products in the database
@production.route('/product/<int:id>', methods=["GET", "POST"])
@permission_required(Permission.MANAGE_PRODUCTS)
def update_product(id):
    title = "Edit Product"
    product = Product.query.get_or_404(id)
    product_form = AddNewProductForm()
    if product_form.validate_on_submit():
        product.name = product_form.name.data
        product.price = product_form.price.data
        product.description = product_form.description.data
        db.session.add(product)
        db.session.commit()
        flash("Product Updated Successfully", category="success")
        return redirect(url_for("production.view_products"))
    product_form.name.data = product.name
    product_form.price.data = product.price
    product_form.description.data = product.description
    return render_template("production/products/create_product.html", product_form=product_form, title=title)

# Delete products in the database
@production.route('/product_delete/<int:id>', methods=["GET", "POST"])
@permission_required(Permission.MANAGE_PRODUCTS)
def delete_product(id):
    product = Product.query.get_or_404(id)
    db.session.delete(product)
    db.session.commit()
    return redirect(url_for("production.view_products"))

# New production run
@production.route('/new_productionrun', methods=["GET", "POST"])
@admin_required 
def new_productionrun():
    title="New Production Run"
    production_run_form = AddNewProductionRunForm()
    if production_run_form.validate_on_submit():
        new_productionrun = ProductionRun(
            product_id=production_run_form.product_id.data, 
            quantity=production_run_form.quantity.data, 
            flour_kneaded=production_run_form.flour_kneaded.data, 
            oil_used=production_run_form.oil_used.data
            )
        db.session.add(new_productionrun)
        db.session.commit()
        flash("Production run added successfully", category="success")
        return redirect(url_for("production.view_productionruns"))
    return render_template("production/production_run/create_productionrun.html", production_run_form=production_run_form, title=title)

# View production runs
@production.route('/view_productionruns', methods=["GET", "POST"])
@admin_required
def view_productionruns():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    query = db.session.query(ProductionRun, Product.name).\
                        join(Product, ProductionRun.product_id == Product.id).\
                        order_by(ProductionRun.created_at.desc())
    pagination = query.paginate(page=page, per_page=per_page)
    productionruns = pagination.items
    return render_template("production/production_run/view_productionruns.html", productionruns=productionruns, pagination=pagination)

@production.route('/view_productionrun/<int:id>', methods=["GET"])
@admin_required
def view_productionrun(id):
    productionrun = ProductionRun.query.get_or_404(id)
    product = Product.query.get(productionrun.product_id)
    return render_template("production/production_run/view_productionrun.html", productionrun=productionrun, product=product)

# Edit production runs
@production.route('/productionrun/<int:id>', methods=["GET", "POST"])
@admin_required
def update_productionrun(id):
    title="Edit Production Run"
    productionrun = ProductionRun.query.get_or_404(id)
    production_run_form = AddNewProductionRunForm()
    if production_run_form.validate_on_submit():
        productionrun.product_id = production_run_form.product_id.data
        productionrun.quantity = production_run_form.quantity.data
        productionrun.flour_kneaded = production_run_form.flour_kneaded.data
        productionrun.oil_used = production_run_form.oil_used.data
        db.session.add(productionrun)
        db.session.commit()
        flash("Production run updated successfully", category="success")
        return redirect(url_for("production.view_productionruns"))
    production_run_form.product_id.data = productionrun.product_id
    production_run_form.quantity.data = productionrun.quantity
    production_run_form.flour_kneaded.data = productionrun.flour_kneaded
    production_run_form.oil_used.data = productionrun.oil_used
    return render_template("production/production_run/create_productionrun.html", production_run_form=production_run_form, title=title)

# Delete products in the database
@production.route('/delete_productionrun/<int:id>', methods=["GET", "POST"])
@admin_required
def delete_productionrun(id):
    productionrun = ProductionRun.query.get_or_404(id)
    db.session.delete(productionrun)
    db.session.commit()
    return redirect(url_for("production.view_productionruns"))

# Add ingredients used in production
@production.route('/new_ingredient', methods=["GET", "POST"])
@permission_required(Permission.MANAGE_RECIPE_DETAILS)
def new_ingredient():
    title="New Ingredient"
    ingredient_form = AddNewIngredient()
    if ingredient_form.validate_on_submit():
        ingredient = Ingredient(
            name=ingredient_form.name.data, 
            unit_of_measurement=ingredient_form.measurement.data
            )
        db.session.add(ingredient)
        db.session.commit()
        flash("Ingredient added successfully", category="success")
        return redirect(url_for("production.view_ingredients"))
    return render_template("production/ingredients/create_ingredient.html", ingredient_form=ingredient_form, title=title)

@production.route("/view_ingredients")
@permission_required(Permission.MANAGE_RECIPE_DETAILS)
def view_ingredients():
    ingredients = Ingredient.query.all()
    return render_template("production/ingredients/view_ingredients.html", ingredients=ingredients)

@production.route("/view_ingredient/<int:id>", methods=["GET"])
@permission_required(Permission.MANAGE_RECIPE_DETAILS)
def view_ingredient(id):
    ingredient = Ingredient.query.get_or_404(id)
    suppliers = Supplier.query.join(Supplier.supplier_ingredients)\
                                .join(Ingredient, SupplierIngredient.ingredient)\
                                .filter(Ingredient.name == ingredient.name)\
                                .all()
    return render_template("production/ingredients/view_ingredient.html", ingredient=ingredient, suppliers=suppliers)

@production.route('/update_ingredient/<int:id>', methods=["GET", "POST"])
@permission_required(Permission.MANAGE_RECIPE_DETAILS)
def update_ingredient(id):
    title="Update Ingredient"
    ingredient_form = AddNewIngredient()
    ingredient = Ingredient.query.get_or_404(id)
    if ingredient_form.validate_on_submit():
        ingredient.name = ingredient_form.name.data
        ingredient.unit_of_measurement = ingredient_form.measurement.data
        db.session.add(ingredient)
        db.session.commit()
        flash("Ingredient updated successfully", category="success")
        return redirect(url_for("production.view_ingredient", id=ingredient.id))
    ingredient_form.name.data = ingredient.name
    ingredient_form.measurement.data = ingredient.unit_of_measurement
    return render_template("production/ingredients/create_ingredient.html", ingredient_form=ingredient_form, title=title)

@production.route('/delete_ingredient/<int:id>', methods=["GET", "POST"])
@permission_required(Permission.MANAGE_RECIPE_DETAILS)
def delete_ingredient(id):
    ingredient = Ingredient.query.get_or_404(id)
    db.session.delete(ingredient)
    db.session.commit()
    return redirect(url_for("production.view_ingredients"))

@production.route('/new_supplier', methods=["GET", "POST"])
@permission_required(Permission.MANAGER)
def new_supplier():
    title="New Supplier"
    supplier_form = AddNewSupplier()
    if supplier_form.validate_on_submit():
        if 'add_ingredient' in request.form:
            supplier_form.add_empty_ingredient()
        elif 'submit' in request.form:
            supplier = Supplier(
                name=supplier_form.name.data, 
                phone_no=supplier_form.phone_no.data, 
                email=supplier_form.email.data
                )
            db.session.add(supplier)
            db.session.commit()

            for ingredient_form in supplier_form.ingredients:
                if ingredient_form.ingredient_id != 0:
                    supplier_ingredient = SupplierIngredient(
                        supplier_id = supplier.id,
                        ingredient_id = ingredient_form.ingredient_id.data,
                        unit_cost = ingredient_form.unit_cost.data,
                    )
                    db.session.add(supplier_ingredient)
            db.session.commit()
            flash("Supplier added successfully", category="success")
            return redirect(url_for("production.view_suppliers"))
    return render_template("production/suppliers/create_supplier.html", supplier_form=supplier_form, title=title)

@production.route('/view_suppliers')
@permission_required(Permission.MANAGER)
def view_suppliers():
    suppliers = Supplier.query.all()
    return render_template("production/suppliers/view_suppliers.html", suppliers=suppliers)

@production.route('/view_supplier/<int:id>')
@permission_required(Permission.MANAGER)
def view_supplier(id):
    supplier = Supplier.query.get_or_404(id)
    supplier_ingredients = db.session.query(Ingredient, SupplierIngredient.unit_cost).\
                            join(SupplierIngredient).\
                            filter(SupplierIngredient.supplier_id == supplier.id).\
                            all()
    return render_template("production/suppliers/view_supplier.html", supplier=supplier, supplier_ingredients=supplier_ingredients)

@production.route('/update_supplier/<int:id>', methods=["GET", "POST"])
@permission_required(Permission.MANAGER)
def update_supplier(id):
    title = "Update Supplier"
    supplier = Supplier.query.get_or_404(id)

    supplier_form = AddNewSupplier(obj=supplier)

    if supplier_form.validate_on_submit():
        supplier_form.populate_obj(supplier)

        supplier.name = supplier_form.name.data
        supplier.phone_no = supplier_form.phone_no.data
        supplier.email = supplier_form.email.data
        # Call the update_timestamp method to update the updated_at
        supplier.update_timestamp()

        for ingredient_form in supplier_form.ingredients:
            ingredient_id = ingredient_form.ingredient_id.data
            ingredient = Ingredient.query.get(ingredient_id)

            if ingredient:
                supplier_ingredient = SupplierIngredient.query.filter_by(supplier_id=supplier.id, ingredient_id=ingredient.id).first()
                supplier_ingredient.unit_cost = ingredient_form.unit_cost.data
    
        db.session.commit()
        flash("Supplier updated successfully", category="success")
        return redirect(url_for("production.view_suppliers"))
    return render_template("production/suppliers/create_supplier.html", supplier_form=supplier_form, title=title)

@production.route('/delete_supplier/<int:id>', methods=["GET", "POST"])
@permission_required(Permission.MANAGER)
def delete_supplier(id):
    supplier = Supplier.query.get_or_404(id)
    db.session.delete(supplier)
    db.session.commit()
    return redirect(url_for("production.view_suppliers"))

@production.route("/create_recipe", methods=["GET", "POST"])
@permission_required(Permission.MANAGE_RECIPE_DETAILS)
def create_recipe():
    recipe_form = RecipeForm()

    if recipe_form.validate_on_submit():
        if 'add_ingredient' in request.form:
            recipe_form.add_empty_ingredient()
        elif 'submit_recipe' in request.form:
            recipe = Recipe(
                name = recipe_form.name.data,
                description = recipe_form.description.data,
                yield_amount = recipe_form.yield_amount.data
            )
            db.session.add(recipe)
            db.session.commit()

            for ingredient_form in recipe_form.recipe_ingredients:
                if ingredient_form.ingredient_id.data != 0:
                    ingredient = RecipeIngredient(
                        recipe_id = recipe.id,
                        ingredient_id = ingredient_form.ingredient_id.data,
                        quantity = ingredient_form.quantity.data,
                        unit_of_measurement = ingredient_form.unit_of_measurement.data
                    )
                    db.session.add(ingredient)
            db.session.commit()
            return redirect(url_for("production.view_recipe"))
    return render_template("production/recipes/create_recipe.html", recipe_form=recipe_form)


@production.route("/view_recipes", methods=["GET", "POST"])
@permission_required(Permission.VIEW_RECIPE_DETAILS)
def view_recipes():
    recipes = Recipe.query.all()
    return render_template("production/recipes/view_recipes.html", recipes=recipes)

@production.route("/view_recipe/<int:recipe_id>", methods=["GET", "POST"])
@permission_required(Permission.VIEW_RECIPE_DETAILS)
def view_recipe(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    return render_template("production/recipes/view_recipe.html", recipe=recipe)

@production.route("/update_recipe/<int:recipe_id>", methods=["GET", "POST"])
@permission_required(Permission.MANAGE_RECIPE_DETAILS)
def update_recipe(recipe_id):
    title = "Update Recipe"
    recipe = Recipe.query.get(recipe_id)
    if recipe is None:
        # Handle case where recipe is not found
        return "Recipe not found", 404

    # populates the form fields with data fetched from recipe query
    recipe_form = RecipeForm(obj=recipe)

    if recipe_form.validate_on_submit():
        recipe_form.populate_obj(recipe)
          # Update recipe data
        recipe.created_at = datetime.utcnow()
        recipe.name = recipe_form.name.data
        recipe.description = recipe_form.description.data
        recipe.yield_amount = recipe_form.yield_amount.data

        # Update recipe details
        for index, recipe_ingredient_form in enumerate(recipe_form.recipe_ingredients):
            recipe_details = recipe.recipe_ingredients[index]
            if recipe_ingredient_form and recipe_ingredient_form.ingredient_id.data != 0:
                recipe_details.ingredient_id = recipe_ingredient_form.ingredient_id.data
                recipe_details.quantity = recipe_ingredient_form.quantity.data
                recipe_ingredient_form.unit_of_measurement.data = recipe_details.unit_of_measurement

        db.session.commit()
        return redirect(url_for("production.view_recipe", recipe_id=recipe.id))
    return render_template("production/recipes/create_recipe.html", recipe_form=recipe_form, title=title)

@production.route("/delete_recipe/<int:recipe_id>", methods=["GET", "POST"])
@permission_required(Permission.MANAGE_RECIPE_DETAILS)
def delete_recipe(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)

    # Delete corresponding recipe details
    for recipe_ingredient in recipe.recipe_ingredients:
        db.session.delete(recipe_ingredient)

    db.session.delete(recipe)
    db.session.commit()
    return redirect(url_for("production.view_recipes"))