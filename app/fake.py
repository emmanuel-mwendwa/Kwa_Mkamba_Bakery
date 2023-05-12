from random import randint
from faker import Faker
from sqlalchemy.exc import IntegrityError
from . import db
from .models import User, Product, ProductionRun

def users(count=100):
    fake = Faker()

    i = 0
    #Generate fake users
    while i < count:
        u = User(email=fake.email(),
                 username=fake.user_name(),
                 password="asdf",
                 confirmed=True,
                 name=fake.name(),
                 phone_no=fake.random_number(digits=9),
                 member_since=fake.past_date()
                 )
        db.session.add(u)
        i += 1
    with db.session.no_autoflush:
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()



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