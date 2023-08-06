import json

import tkapi

from tkapi.document import ParlementairDocument
from tkapi.zaak import Zaak


class DossierFilter(tkapi.Filter):

    def __init__(self):
        super().__init__()

    def filter_vetnummer(self, vetnummer):
        filter_str = "Vetnummer eq " + str(vetnummer)
        self.filters.append(filter_str)

    def filter_zaak(self, zaak_number):
        filter_str = 'Kamerstuk/any(ks:ks/ParlementairDocument/Zaak/any(z:z/Nummer eq ' + "'" + str(zaak_number) + "'" + '))'
        self.filters.append(filter_str)

    def filter_afgesloten(self, is_afgesloten):
        is_afgesloten_str = 'true' if is_afgesloten else 'false'
        filter_str = "Afgesloten eq " + is_afgesloten_str
        self.filters.append(filter_str)

    def filter_zaken(self, zaak_numbers):
        filter_str = 'Kamerstuk/any(ks:ks/ParlementairDocument/Zaak/any(z:'
        zaak_nummer_strs = []
        for nummer in zaak_numbers:
            zaak_nummer_strs.append('(z/Nummer eq ' + "'" + str(nummer) + "')")
        filter_str += ' or '.join(zaak_nummer_strs)
        filter_str += '))'
        self.filters.append(filter_str)


class Dossier(tkapi.TKItem):
    url = 'Kamerstukdossier'
    expand_param = 'Kamerstuk, Kamerstuk/ParlementairDocument/Zaak'

    def __init__(self, dossier_json):
        super().__init__(dossier_json)
        self.zaken_cache = []

    @staticmethod
    def create_filter():
        return DossierFilter()

    @property
    def vetnummer(self):
        return self.get_property_or_none('Vetnummer')

    @property
    def toevoeging(self):
        return self.get_property_or_none('Toevoeging')

    @property
    def afgesloten(self):
        return self.json['Afgesloten']

    @property
    def titel(self):
        return self.get_property_or_empty_string('Titel')

    @property
    def organisatie(self):
        return self.get_property_or_empty_string('Organisatie')

    @property
    def kamerstukken(self):
        from tkapi.kamerstuk import Kamerstuk
        kamerstukken = []
        for kamerstuk in self.json['Kamerstuk']:
            kamerstukken.append(tkapi.api.get_item(Kamerstuk, kamerstuk['Id']))
        return kamerstukken

    @property
    def zaken(self):
        if self.zaken_cache:
            return self.zaken_cache
        zaken = []
        for pd in self.parlementaire_documenten:
            zaken += pd.zaken
        self.zaken_cache = zaken
        return zaken

    @property
    def parlementaire_documenten(self):
        parlementair_documenten = []
        for kamerstuk in self.json['Kamerstuk']:
            if kamerstuk == '':
                continue
            pds = kamerstuk['ParlementairDocument']
            pd = ParlementairDocument(pds)
            parlementair_documenten.append(pd)
        return parlementair_documenten
