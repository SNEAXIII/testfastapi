# openssl rand -hex 128
from json import dumps
from fastapi import FastAPI
from sqlmodel import Field, SQLModel, Relationship, select, Session
from sqlalchemy.exc import OperationalError, NoResultFound
from time import sleep
from QueryStorer import QueryStorer, ENGINE
from tools.db_security import bulk_insert_decorator
from tools.minilogger import ml
from tools.secrets import BULK_INSERT_NUMBER, CSV_PATH, DB_CONNECTION_RETRY, DB_CONNECTION_TIMEOUT
import csv


class Status(SQLModel):
    success: bool = True

    def __init__(self, success=True):
        self.success: bool = success


class Voie(SQLModel, table=True):
    ID: int = Field(primary_key=True)
    Nom: str = Field(max_length=50)
    lieux: list["Lieux"] = Relationship(back_populates="voie")


class CodePostal(SQLModel, table=True):
    ID: int = Field(primary_key=True)
    Numero: str = Field(max_length=5)
    lieux: list["Lieux"] = Relationship(back_populates="codepostal")


class Commune(SQLModel, table=True):
    ID: int = Field(primary_key=True)
    Nom: str = Field(max_length=50)
    lieux: list["Lieux"] = Relationship(back_populates="commune")


class Lieux(SQLModel, table=True):
    ID: int = Field(primary_key=True)
    ID_STR: str = Field(max_length=50)
    Numero: str = Field(default=None, max_length=50)
    ID_VOIE: int = Field(foreign_key="voie.ID")
    ID_CP: int = Field(foreign_key="codepostal.ID")
    ID_Commune: int = Field(foreign_key="commune.ID")
    x: str = Field(max_length=15)
    y: str = Field(max_length=15)
    voie: Voie = Relationship(back_populates="lieux")
    codepostal: CodePostal = Relationship(back_populates="lieux")
    commune: Commune = Relationship(back_populates="lieux")


DATATYPE = {
    "voie": Voie,
    "cp": CodePostal,
    "commune": Commune,
    "lieu": Lieux
}


@bulk_insert_decorator
def populate_db():
    store = QueryStorer(bulk_size=BULK_INSERT_NUMBER)
    with open(CSV_PATH) as f:
        for index, ligne in enumerate(csv.reader(f)):
            store.add_lieu(ligne)
        store.flush()
    return "done"


app = FastAPI()


@app.get("/log")
def get_log():
    return ml.get_log()


@app.delete("/log")
def get_log():
    ml.clear_log()
    return "succes"


@app.post("/create_db", response_model=Status)
def create_db():
    for essai in range(DB_CONNECTION_RETRY):
        try:
            SQLModel.metadata.drop_all(ENGINE)
            SQLModel.metadata.create_all(ENGINE)
            ml.log("Création du schéma réussie")
            return Status()
        except OperationalError:
            ml.log(f"Erreur lors de la création du shéma de la BDD, essai numéro {essai + 1}")
            sleep(DB_CONNECTION_TIMEOUT)
    return Status(False)


@app.get("/get/lieux/{id_lieux}", response_model=Lieux)
def get_voie(id_lieux: int):
    with Session(ENGINE) as session:
        try:
            return session.get(Lieux, id_lieux)
        except NoResultFound:
            return "no result found"


@app.post("/populate_db")
def post_populate_db():
    create_db()
    populate_db()
