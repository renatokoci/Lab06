from database.DB_connect import get_connection
from model.strumento import Strumento
from model.prestito import Prestito

'''
    MODELLO:
    - Rappresenta la struttura dati
    - Si occupa di gestire lo stato dell'applicazione
    - Interagisce con il database
'''

class DepositoStrumenti:
    def __init__(self, nome, responsabile):
        self._nome = nome
        self._responsabile = responsabile

    @property
    def nome(self):
        return self._nome

    @nome.setter
    def nome(self, nome):
        self._nome = nome

    @property
    def responsabile(self):
        return self._responsabile

    @responsabile.setter
    def responsabile(self, responsabile):
        self._responsabile = responsabile

    def get_strumenti(self) -> list[Strumento] | None:
        """
            Funzione che legge tutti gli strumenti nel database
            :return: una lista con tutti gli strumenti presenti oppure None
        """
        cnx = get_connection()
        if cnx is None:
            print("Errore connessione database")
            return None
        cursore = cnx.cursor(dictionary=True)
        query = "SELECT * FROM strumento"
        lista_strumenti = []
        try:
            cursore.execute(query)
            for row in cursore:
                # Modifica i nomi delle chiavi 'id', 'tipo', ecc. nel DB
                strumento = Strumento(
                row["codice"],
                row["tipo"],
                row["marca"],
                row["anno_acquisto"],
                row["valore"]
                )
                lista_strumenti.append(strumento)
        except Exception as e:
            print(e)
            return None
        finally:
            cursore.close()
            cnx.close()
        return lista_strumenti

    def cerca_strumenti_per_tipo(self, tipo) -> list[Strumento] | None:
        """
            Funzione che recupera una lista con tutti gli strumenti presenti nel database di un certo tipo
            :param tipo: il tipo dello strumento (es. "Chitarra")
            :return: una lista con tutti gli strumenti del tipo indicato oppure None
        """
        cnx = get_connection()
        if cnx is None:
            return None

        cursore = cnx.cursor(dictionary=True)
        # Il %s serve a evitare l'sql injection
        query = "SELECT * FROM strumento WHERE tipo = %s"
        lista_strumenti = []
        try:
            # Passiamo la variabile 'tipo' come tupla: (tipo,)
            cursore.execute(query, (tipo,))
            for row in cursore:
                strumento = Strumento(
                    row["codice"],
                    row["tipo"],
                    row["marca"],
                    row["anno_acquisto"],
                    row["valore"]
                )
                lista_strumenti.append(strumento)
        except Exception as e:
            print(e)
            return None
        finally:
            cursore.close()
            cnx.close()

        return lista_strumenti
