import os
from flask_migrate import Migrate
from flask.cli import FlaskGroup
from dotenv import load_dotenv
from app import app, db

load_dotenv()
app.config.from_object(os.getenv('APP_SETTINGS'))

migrate = Migrate(app, db)
cli = FlaskGroup(app)

if __name__ == '__main__':
    cli()



