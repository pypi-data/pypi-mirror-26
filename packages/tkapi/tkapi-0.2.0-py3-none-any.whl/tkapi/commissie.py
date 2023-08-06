import tkapi
from tkapi.persoon import Persoon


class CommissieFilter(tkapi.SoortFilter):

    def __init__(self):
        super().__init__()

    def filter_naam(self, naam):
        filter_str = "NaamNL eq " + "'" + naam.replace("'", "''") + "'"
        self.filters.append(filter_str)


class Commissie(tkapi.TKItem):
    url = 'Commissie'
    expand_param = 'Organisatie, Lid/VastPersoon'

    def __init__(self, commissie_json):
        super().__init__(commissie_json)
        self.leden_cache = []

    @staticmethod
    def create_filter():
        return CommissieFilter()

    @property
    def afkorting(self):
        return self.get_property_or_empty_string('Afkorting')

    @property
    def naam(self):
        return self.get_property_or_empty_string('NaamNL')

    @property
    def naam_web(self):
        return self.get_property_or_empty_string('NaamWebNL')

    @property
    def soort(self):
        return self.get_property_or_empty_string('Soort')

    @property
    def leden(self):
        if self.leden_cache:
            return self.leden_cache
        if 'Lid' not in self.json:
            return []
        leden = []
        for lid in self.json['Lid']:
            leden.append(CommissieLid(lid))
        self.leden_cache = leden
        return leden

    def __str__(self):
        pretty_print = self.id + ': '
        pretty_print += self.naam
        if self.afkorting:
            pretty_print += ' (' + self.afkorting + ')'
        return pretty_print


class CommissieLid(tkapi.TKItem):
    def __init__(self, lid_json):
        super().__init__(lid_json)

    @property
    def vast_van(self):
        return self.get_date_or_none('VastVan')

    @property
    def vast_tot_en_met(self):
        return self.get_date_or_none('VastTotEnMet')

    @property
    def persoon(self):
        if self.json['VastPersoon']:
            return Persoon(self.json['VastPersoon'])
        return None

    def __str__(self):
        pretty_print = ''
        if self.persoon:
            pretty_print = str(self.persoon)
        if self.vast_van:
            pretty_print += ': ' + str(self.vast_van)
        if self.vast_tot_en_met:
            pretty_print += ' - ' + str(self.vast_tot_en_met)
        else:
            pretty_print += ' - heden'
        return pretty_print

