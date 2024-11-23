from sqlmodel import Session, text
from .minilogger import ml
from .connector import ENGINE

ALL_TABLE = [
    "codepostal",
    "commune",
    "lieux",
    "voie"
]

STATE = {
    "DISABLE": 0,
    "ENABLE": 1,
}


def disable_security():
    executor("DISABLE")


def enable_security():
    executor("ENABLE")


def executor(action: str):
    ml.log(f"Essai de {action} la sécurité")
    if (action := action.upper()) not in STATE:
        raise ValueError(f"Invalid action {action}!")
    bin_action = STATE[action]
    with Session(ENGINE) as session:
        for table in ALL_TABLE:
            ml.log(f"{action} les clés de la table {table}")
            session.exec(text(f"ALTER TABLE {table} {action} KEYS;"))
        session.exec(text(f"SET foreign_key_checks = {bin_action};"))
        session.exec(text(f"SET unique_checks = {bin_action};"))
    ml.log(f"Succès de {action} la sécurité")


def bulk_insert_decorator(func):
    def wrapper(*args, **kwargs):
        disable_security()
        try:
            result = func(*args, **kwargs)
        finally:
            enable_security()
        return result

    return wrapper
