from app import create_app, db
from flask_migrate import Migrate
from app.models import Role, User
import os

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
migrate = Migrate(app, db)

@app.shell_context_processor
def make_shell_processor():
    return dict(db=db, User=User, Role=Role)
