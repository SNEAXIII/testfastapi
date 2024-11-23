import csv

from ordered_set import OrderedSet
from sqlmodel import Session, text
from tools.connector import ENGINE
from tools.minilogger import ml

TEMPLATE_LIEUX = "INSERT INTO lieux (ID_STR, Numero, ID_VOIE, ID_CP, ID_Commune, x, y) VALUES %s;"
TEMPLATE_VOIE = "INSERT INTO voie (Nom) VALUES %s;"
TEMPLATE_CP = "INSERT INTO codepostal (Numero) VALUES %s;"
TEMPLATE_COMMUNE = "INSERT INTO commune (Nom) VALUES %s;"


class QueryStorer:
    def __init__(self, bulk_size=1000):
        self.total = 0
        self.bulk_size = bulk_size
        self.reset_lignes()
        self.voies = OrderedSet()
        self.cps = OrderedSet()
        self.communes = OrderedSet()
        self.index_to_exec = {
            "voie": [0, self.voies, TEMPLATE_VOIE],
            "codepostal": [0, self.cps, TEMPLATE_CP],
            "commune": [0, self.communes, TEMPLATE_COMMUNE]
        }

    # def __str__(self)->str:
    #     def trunk(_str:str)->str:
    #         return _str[:72] + '...' if len(_str) > 75 else _str
    #     eol = "\n"
    #     tab = "    "
    #     return f"self.index_to_exec={eol+tab}{eol+tab.join()}"

    def reset_lignes(self):
        self.lignes = []

    @staticmethod
    def trim_50(_str: str) -> str:
        return (_str if len(_str) <= 50 else f"{_str[:47]}...").replace("\"", "")

    def add_voie(self, voie: str) -> int:
        return self.voies.add(self.trim_50(voie))

    def add_cp(self, cp: str) -> int:
        return self.cps.add(cp[:5])

    def add_commune(self, commune: str) -> int:
        return self.communes.add(self.trim_50(commune))

    def add_lieu(self, ligne: list) -> None:
        id_str, numero, voie, cp, commune, _, x, y = ligne
        data = (
            self.trim_50(id_str),
            self.trim_50(numero),
            str(self.add_voie(voie) + 1),
            str(self.add_cp(cp) + 1),
            str(self.add_commune(commune) + 1),
            x, y
        )
        self.lignes.append(self.convert_line_to_lieu(data))
        if len(self.lignes) >= self.bulk_size:
            self.flush()

    @staticmethod
    def convert_line_to_lieu(data) -> str:
        separator = '","'
        return f'("{separator.join(data)}")'

    def get_merged_lieux(self):
        return ",".join(self.lignes)

    @staticmethod
    def get_sql_request(template: str, data):
        return template % data

    def flush(self):
        self.total += len(self.lignes)
        ml.log(f"Nombre de lieux à ajouter = {len(self.lignes)}")
        with Session(ENGINE) as session:
            for table, contenu in self.index_to_exec.items():
                raw_data = contenu[1][contenu[0]:len(contenu[1])]
                if not raw_data:
                    continue
                contenu[0] = len(contenu[1])
                separator = '"),("'
                data = f'("{separator.join(raw_data)}")'
                sql = text(contenu[2] % data)
                session.exec(sql)
            if self.lignes:
                sql = text(TEMPLATE_LIEUX % self.get_merged_lieux())
                self.reset_lignes()
                session.exec(sql)
            # try :
            session.commit()
            ml.log(f"Total ajouté = {self.total}")


if __name__ == "__main__":
    store = QueryStorer()
    with open("data/minibano.csv") as f:
        for index, ligne in enumerate(csv.reader(f)):
            store.add_lieu(ligne)
            store.flush()
    ml.log(store.lignes)
