from .app import db, ma

# Game Model
class Game(db.Model):
    __tablename__ = 'games'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=False, unique=True, nullable=False)
    price = db.Column(db.Float())
    space = db.Column(db.BigInteger())

    def __init__(self, name, price, space):
        self.name = name
        self.price = price
        self.space = space

    def __repr__(self):
        return '<id {}>'.format(self.id)

# Game Schema for Game Model
class GameSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Game

    name = ma.auto_field()
    price = ma.auto_field()
    space = ma.auto_field()
