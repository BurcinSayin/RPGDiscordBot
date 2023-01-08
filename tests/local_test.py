import json
import os
from dotenv import load_dotenv
import lambda_function


def get_event(event_name):
    f = open(f"testJson/{event_name}.json")
    retval = json.load(f)
    # Closing file
    f.close()
    return retval


if __name__ == '__main__':
    load_dotenv()

    # lambda_function.lambda_handler(get_event("status_event"), "")
    # lambda_function.lambda_handler(get_event("char_create_event"), "")
    # lambda_function.lambda_handler(get_event("char_list_event"), "")
    # res = lambda_function.lambda_handler(get_event("char_switch_event"), "")
    # lambda_function.lambda_handler(get_event("coin_add_event"), "")
    # lambda_function.lambda_handler(get_event("coin_give_event"), "")
    # lambda_function.lambda_handler(get_event("ping_event"), "")
    res = lambda_function.lambda_handler(get_event("item_add_event"), "")
    print(res)
