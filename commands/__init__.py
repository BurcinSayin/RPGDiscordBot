from . import Status
from . import Char
from . import Coin
from . import Item


# And so on.
commands_list = {
    "status": Status.Status(),
    "char": Char.Char(),
    "coin": Coin.Coin(),
    "item": Item.Item()
}
