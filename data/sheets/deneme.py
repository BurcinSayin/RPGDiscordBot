import gspread

from data.sheets.UserData import UserData
from data.sheets.CharacterData import CharacterData


def runme():
    gc = gspread.service_account(filename='../../sheet-auth.json')
    sh = gc.open("Settings")

    udb = UserData(sh)
    cdb = CharacterData(gc.open("Characters"))

    target = cdb.get_character_obj("Hantalas")

    target.name = "Zanor"

    cdb.save_data_obj(target)
    # cdb.add_character( "user_id", "entity_name")

    print(changes)


if __name__ == '__main__':
    try:
        runme()
    except Exception as e:
        print(f"Something went wrong with the demo! Here's what: {e}")
