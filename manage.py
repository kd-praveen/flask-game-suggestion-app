from flask.cli import FlaskGroup

from web.app import app, db

cli = FlaskGroup(app)

# Create db cli command
@cli.command("create_db")
def create_db():
    db.drop_all()
    db.create_all()
    db.session.commit()

if __name__ == "__main__":
    cli()