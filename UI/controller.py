import flet as ft
from UI.view import View
from model.model import DepositoStrumenti

'''
    CONTROLLER:
    - Funziona da intermediario tra MODELLO e VIEW
    - Gestisce la logica del flusso dell'applicazione
'''

class Controller:
    def __init__(self, view: View, model: DepositoStrumenti):
        self._model = model
        self._view = view

    def get_nome(self):
        return self._model.nome

    def get_responsabile(self):
        return self._model.responsabile

    def set_responsabile(self, responsabile):
        self._model.responsabile = responsabile

    def conferma_responsabile(self, e):
        self._model.responsabile = self._view.input_responsabile.value
        self._view.txt_responsabile.value = f"Responsabile: {self._model.responsabile}"
        self._view.update()

    # Altre Funzioni Event Handler
    def mostra_tutti_strumenti(self,e):
        # chiediamo al model tutti gli strumenti dal DB
        lista_strumenti = self._model.get_strumenti()
        # controllo errori / lista vuota
        if lista_strumenti is None:
            self._view.show_alert("Errore nel recupero degli strumenti")
            return
        # svuoto la listview esistente
        self._view.lista_strumenti.controls.clear()
        if len(lista_strumenti) == 0:
            self._view.lista_strumenti.controls.append(ft.Text("Nessuno strumento presente nel database"))
        else:
            for strumento in lista_strumenti:
                self._view.lista_strumenti.controls.append(ft.Text(str(strumento)))

        self._view.update()
    def cerca_strumenti_per_tipo(self,e):
        # leggo il tipo digitato dall'utente
        tipo_cercato = self._view.input_tipo_strumento.value.strip()

        # controllo che l'utente abbia digitato qualcosa
        if tipo_cercato == "":
            self._view.show_alert("Inserisci un tipo di strumento da cercare")
            return

        # chiedo al model gli strumenti filtrati per quel tipo
        lista_ricerca = self._model.cerca_strumenti_per_tipo(tipo_cercato)

        # controllo errori
        if lista_ricerca is None:
            self._view.show_alert("Errore durante la ricerca nel database.")
            return

        # svuoto la listview dedicata alla ricerca
        self._view.lista_strumenti_ricerca.controls.clear()

        if len(lista_ricerca) == 0:
            self._view.lista_strumenti_ricerca.controls.append(
                ft.Text(f"Nessuno strumento trovato per il tipo: {tipo_cercato}")
            )
        else:
            for strumento in lista_ricerca:
                self._view.lista_strumenti_ricerca.controls.append(ft.Text(str(strumento)))

        # pulisco il campo di input e aggiorno
        self._view.input_tipo_strumento.value = ""
        self._view.update()

