from random import randint
from faker import Faker
from . import db
from .models import Product, ProductionRun

def products(num_products=10, num_production_runs=50):
    fake = Faker()
    
    # Generate fake products
    for i in range(num_products):
        p = Product(
            name=fake.word(),
            description = fake.sentence(),
            price=randint(100, 1000)
        )
        db.session.add(p)

    # Generate fake production runs
    product_ids = [p.id for p in Product.query.all()]
    for i in range(num_production_runs):
        pr = ProductionRun(
            product_id = fake.random_element(elements=product_ids),
            quantity=randint(1, 100),
            flour_kneaded=randint(1, 100),
            oil_used=randint(1, 4),
            created_at=fake.date_time_between(start_date='-1y', end_date='now')
        )
        db.session.add(pr)

    db.session.commit()