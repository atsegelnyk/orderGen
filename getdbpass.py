from getpass import getpass


def get_db_pass():
    db_pass = getpass(prompt='Please, enter db password: ', stream=None)
    return db_pass

