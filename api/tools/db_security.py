from sqlmodel import Session, text

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
    if (action := action.upper()) not in STATE:
        raise ValueError(f"Invalid action {action}!")
    bin_action = bin(STATE[action])
    with Session(ENGINE) as session:
        for table in ALL_TABLE:
            session.exec(text(f"ALTER TABLE {table} {action} KEYS;"))
        session.exec(text(f"SET foreign_key_checks = {bin_action};"))
        session.exec(text(f"SET unique_checks = {bin_action};"))

def bulk_insert_decorator(func):
    def wrapper(*args, **kwargs):
        disable_security()
        try:
            result = func(*args, **kwargs)
        finally:
            enable_security()
        return result
    return wrapper