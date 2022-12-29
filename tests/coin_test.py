from utils.coin import parse_coin_string, create_coin_string


def parse_coin():
    res = parse_coin_string("10gp 5sp")
    assert res == 10500, "10gp 5sp should be 1050 coins"


def create_coin():
    res = create_coin_string(843563)
    assert res == "843pp 5gp 6sp 3cp", "10gp 5sp should be 1050 coins"


if __name__ == '__main__':
    create_coin()
