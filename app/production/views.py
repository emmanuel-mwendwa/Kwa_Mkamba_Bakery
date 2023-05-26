from flask import render_template, redirect, url_for, flash, request
from . import production
from .forms import AddNewProductForm, AddNewProductionRunForm, EditProductionRunForm, AddNewIngredient, AddNewSupplier, EditIngredient, EditSupplier, AddSupplierIngredientForm, RecipeForm, RecipeIngredientForm
from .. import db
from ..models import Product, ProductionRun, Ingredient, Supplier, SupplierIngredient, Recipe, RecipeIngredient
from ..decorators import admin_required

# Add a new product in the database
@production.route('/new_product', methods=["GET", "POST"])
@admin_required
def new_product():
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
    return render_template("production/products/create_product.html", product_form=product_form)

# View the products in the database
@production.route('/view_products', methods=["GET", "POST"])
def view_products():
    products = Product.query.all()
    return render_template("production/products/view_products.html", products=products)

@production.route('/view_product/<int:id>')
def view_product(id):
    product = Product.query.get_or_404(id)
    return render_template("production/products/view_product.html", product=product)

# Edit values of the products in the database
@production.route('/product/<int:id>', methods=["GET", "POST"])
@admin_required
def edit_product(id):
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
    return render_template("production/products/edit_product.html", product_form=product_form)

# Delete products in the database
@production.route('/product_delete/<int:id>', methods=["GET", "POST"])
@admin_required
def delete_product(id):
    product = Product.query.get_or_404(id)
    db.session.delete(product)
    db.session.commit()
    return redirect(url_for("production.view_products"))

# New production run
@production.route('/new_productionrun', methods=["GET", "POST"])
@admin_required 
def new_productionrun():
    title="New ProductionRun"
    form = AddNewProductionRunForm()
    if form.validate_on_submit():
        new_productionrun = ProductionRun(
            product_id=form.product_id.data, 
            quantity=form.quantity.data, 
            flour_kneaded=form.flour_kneaded.data, 
            oil_used=form.oil_used.data
            )
        db.session.add(new_productionrun)
        db.session.commit()
        flash("Production run added successfully", category="success")
        return redirect(url_for("production.view_productionruns"))
    return render_template("production/new_items.html", form=form, title=title)

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
    return render_template("production/view_productionruns.html", productionruns=productionruns, pagination=pagination)

# Edit production runs
@production.route('/productionrun/<int:id>', methods=["GET", "POST"])
@admin_required
def edit_productionrun(id):
    title="Edit Items"
    productionrun = ProductionRun.query.get_or_404(id)
    form = EditProductionRunForm()
    if form.validate_on_submit():
        productionrun.product_id = form.product_id.data
        productionrun.quantity = form.quantity.data
        productionrun.flour_kneaded = form.flour_kneaded.data
        productionrun.oil_used = form.oil_used.data
        db.session.add(productionrun)
        db.session.commit()
        flash("Production run edited successfully", category="success")
        return redirect(url_for("production.view_productionruns"))
    form.product_id.data = productionrun.product_id
    form.quantity.data = productionrun.quantity
    form.flour_kneaded.data = productionrun.flour_kneaded
    form.oil_used.data = productionrun.oil_used
    return render_template("production/edit_items.html", form=form, title=title)

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
@admin_required
def new_ingredient():
    title="New Ingredient"
    form = AddNewIngredient()
    if form.validate_on_submit():
        ingredient = Ingredient(
            name=form.name.data, 
            unit_of_measurement=form.measurement.data, 
            unit_cost=form.unit_cost.data)
        db.session.add(ingredient)
        db.session.commit()
        flash("Ingredient added successfully", category="success")
        return redirect(url_for("production.view_ingredients"))
    return render_template("production/new_items.html", form=form, title=title)

@production.route("/view_ingredients")
@admin_required
def view_ingredients():
    ingredients = Ingredient.query.all()
    return render_template("production/view_ingredients.html", ingredients=ingredients)

@production.route('/edit_ingredient/<int:id>', methods=["GET", "POST"])
@admin_required
def edit_ingredient(id):
    title="Edit Ingredient"
    form = EditIngredient()
    ingredient = Ingredient.query.get_or_404(id)
    if form.validate_on_submit():
        ingredient.name = form.name.data
        ingredient.unit_of_measurement = form.measurement.data
        ingredient.unit_cost = form.unit_cost.data
        db.session.add(ingredient)
        db.session.commit()
        flash("Ingredient updated successfully", category="success")
        return redirect(url_for("production.view_ingredients"))
    form.name.data = ingredient.name
    form.measurement.data = ingredient.unit_of_measurement
    form.unit_cost.data = ingredient.unit_cost
    return render_template("production/edit_items.html", form=form, title=title)

@production.route('/delete_ingredient/<int:id>', methods=["GET", "POST"])
@admin_required
def delete_ingredient(id):
    ingredient = Ingredient.query.get_or_404(id)
    db.session.delete(ingredient)
    db.session.commit()
    return redirect(url_for("production.view_ingredients"))

@production.route('/new_supplier', methods=["GET", "POST"])
@admin_required
def new_supplier():
    title="New Supplier"
    form = AddNewSupplier()
    if form.validate_on_submit():
        supplier = Supplier(
            name=form.name.data, 
            phone_no=form.phone_no.data, 
            email=form.email.data
            )
        db.session.add(supplier)
        db.session.commit()
        flash("Supplier added successfully", category="success")
        return redirect(url_for("production.view_suppliers"))
    return render_template("production/new_items.html", form=form, title=title)

@production.route('/view_suppliers')
@admin_required
def view_suppliers():
    suppliers = Supplier.query.all()
    return render_template("production/view_suppliers.html", suppliers=suppliers)

@production.route('/view_supplier/<int:id>')
@admin_required
def view_supplier(id):
    supplier = Supplier.query.get_or_404(id)
    supplier_ingredients = db.session.query(Ingredient, SupplierIngredient.unit_cost).\
                            join(SupplierIngredient).\
                            filter(SupplierIngredient.supplier_id == supplier.id).\
                            all()
    return render_template("production/view_supplier.html", supplier=supplier, supplier_ingredients=supplier_ingredients)

@production.route('/edit_supplier/<int:id>', methods=["GET", "POST"])
@admin_required
def edit_supplier(id):
    title = "Edit Supplier"
    form = EditSupplier()
    supplier = Supplier.query.get_or_404(id)
    if form.validate_on_submit():
        supplier.name = form.name.data
        supplier.phone_no = form.phone_no.data
        supplier.email = form.email.data
        # Call the update_timestamp method to update the updated_at
        Supplier.update_timestamp(None, None, supplier)
        db.session.add(supplier)
        db.session.commit()
        flash("Supplier updated successfully", category="success")
        return redirect(url_for("production.view_suppliers"))
    form.name.data = supplier.name
    form.phone_no.data = supplier.phone_no
    form.email.data = supplier.email
    return render_template("production/edit_items.html", form=form, title=title)

@production.route('/delete_supplier/<int:id>', methods=["GET", "POST"])
@admin_required
def delete_supplier(id):
    supplier = Supplier.query.get_or_404(id)
    db.session.delete(supplier)
    db.session.commit()
    return redirect(url_for("production.view_suppliers"))

@production.route('/new_supplier_ingredient', methods=["GET", "POST"])
@admin_required
def new_supplier_ingredient():
    title = "New Supplier Ingredient"
    form = AddSupplierIngredientForm()

    if form.validate_on_submit():
        supplier_ingredient = SupplierIngredient(
                            supplier_id=form.supplier_id.data,
                            ingredient_id=form.ingredient_id.data,
                            unit_cost = form.unit_cost.data
                            ) 
        db.session.add(supplier_ingredient)
        db.session.commit()
        flash("Supplier Ingredient added successfully", category="success")
        return redirect(url_for('production.view_suppliers'))
    
    return render_template('production/new_items.html', form=form)

@production.route("/create_recipe", methods=["GET", "POST"])
@admin_required
def create_recipe():
    recipe_form = RecipeForm()
    ingredient_forms = [RecipeIngredientForm()]

    
    if recipe_form.validate_on_submit():
        # Create recipe and recipe ingredients
        if 'add_ingredient' in request.form:
            ingredient_forms.append(RecipeIngredientForm())
        elif 'submit_recipe' in request.form:
            if all(form.validate() for form in ingredient_forms):
                recipe = Recipe(
                    name = recipe_form.name.data,
                    description = recipe_form.description.data,
                    yield_amount = recipe_form.yield_amount.data
                )
                db.session.add(recipe)
                db.session.commit()

                db.session.refresh(recipe)

                for form in ingredient_forms:
                    # if form.ingredient_id.data:
                    recipe_ingredient = RecipeIngredient(
                        recipe_id = recipe.id,
                        ingredient_id = form.ingredient_id.data,
                        quantity = form.quantity.data,
                        unit_of_measurement = form.unit_of_measurement.data
                    )
                    db.session.add(recipe_ingredient)
                db.session.commit()

                return redirect(url_for("main.index"))
    
    return render_template("production/create_recipe.html", recipe_form=recipe_form, ingredient_forms=ingredient_forms)