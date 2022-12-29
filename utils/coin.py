def parse_coin_string(coin_string):
    ret_val = 0
    coin_parts = coin_string.split()
    multiplier = 1
    for coin_str in coin_parts:
        if coin_str.endswith("cp"):
            coin_str = coin_str.replace("cp", "")
        elif coin_str.endswith("sp"):
            multiplier = 10
            coin_str = coin_str.replace("sp", "")
        elif coin_str.endswith("gp"):
            multiplier = 100
            coin_str = coin_str.replace("gp", "")
        elif coin_str.endswith("pp"):
            multiplier = 1000
            coin_str = coin_str.replace("pp", "")

        try:
            ret_val += int(coin_str) * multiplier
        except:
            print("cannot parse" + coin_str)

    return ret_val


def create_coin_string(coin_value):
    ret_val = "This guy is bankrupt!!!"
    if coin_value > 0:
        current_coins = coin_value
        pp_part, current_coins = _get_coin_part(current_coins, 1000, "pp")
        gp_part, current_coins = _get_coin_part(current_coins, 100, "gp")
        sp_part, current_coins = _get_coin_part(current_coins, 10, "sp")
        cp_part, current_coins = _get_coin_part(current_coins, 1, "cp")
        ret_val = f"{pp_part} {gp_part} {sp_part} {cp_part}"
    return ret_val

def _get_coin_part(current_coins, multiplier, coin_string):
    coin_part_remain = current_coins % multiplier
    coin_part_val = int((current_coins - coin_part_remain) / multiplier)
    current_coins = current_coins - (coin_part_val * multiplier)
    if coin_part_val > 0:
        return f"{coin_part_val}{coin_string}", current_coins
    else:
        return "", current_coins
