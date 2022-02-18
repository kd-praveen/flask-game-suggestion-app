from web.models import Game


def test_new_game():
    """
    GIVEN a Game model
    WHEN a new Game is created
    THEN check the name, price and space fields are defined correctly
    """
    game = Game('Call of duty: MW3', '9999.99', '453456789')
    assert game.name == 'Call of duty: MW3'
    assert game.price == '9999.99'
    assert game.space == '453456789'