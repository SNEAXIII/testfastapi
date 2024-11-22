# openssl rand -hex 128
from fastapi import FastAPI
from sqlmodel import Field, SQLModel, Relationship, select, Session
from sqlalchemy.exc import OperationalError, NoResultFound
from time import sleep
from QueryStorer import QueryStorer,ENGINE
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
    ID: str = Field(primary_key=True, max_length=50)
    Numero: str = Field(default=None, max_length=50)
    ID_VOIE: int = Field(foreign_key="voie.ID")
    ID_CP: int = Field(foreign_key="codepostal.ID")
    ID_Commune: int = Field(foreign_key="commune.ID")
    x: str = Field(max_length=15)
    y: str = Field(max_length=15)
    voie: "Voie" = Relationship(back_populates="lieux")
    codepostal: "CodePostal" = Relationship(back_populates="lieux")
    commune: "Commune" = Relationship(back_populates="lieux")


DATATYPE = {
    "voie": Voie,
    "cp": CodePostal,
    "commune": Commune,
    "lieu": Lieux
}
app = FastAPI()


@app.post("/create_db/", response_model=Status)
def create_db():
    for essai in range(15):
        try:
            SQLModel.metadata.drop_all(ENGINE)
            SQLModel.metadata.create_all(ENGINE)
            print("Création du schéma réussie")
            return Status()
        except OperationalError:
            print(f"Erreur lors de la création du shéma de la BDD, essai numéro {essai + 1}")
            sleep(1)
    return Status(False)


@app.get("/{type_donnee}/{id}/")
def get_first(type_donnee: str, id: int):
    if not (classe_choisie := DATATYPE.get(type_donnee.lower())):
        return "no go"
    with (Session(ENGINE) as session):
        try:
            return session.exec(select(classe_choisie).where(classe_choisie.ID == id)).one()
        except NoResultFound:
            return "curl ko"

@app.post("/populate_db/")
def populate_db():
    store = QueryStorer(bulk_size=50000)
    with open("data/bano.csv") as f:
        for index, ligne in enumerate(csv.reader(f)):
            store.add_lieu(ligne)
        store.flush()
    return "done"
