# -*- coding: utf-8 -*-

from openfisca_france.model.base import *  # noqa analysis:ignore


class indemnites_journalieres_maternite(Variable):
    column = FloatCol
    entity = Individu
    label = u"Indemnités journalières de maternité"
    definition_period = MONTH
    set_input = set_input_divide_by_period


class indemnites_journalieres_paternite(Variable):
    column = FloatCol
    entity = Individu
    label = u"Indemnités journalières de paternité"
    definition_period = MONTH
    set_input = set_input_divide_by_period


class indemnites_journalieres_adoption(Variable):
    column = FloatCol
    entity = Individu
    label = u"Indemnités journalières d'adoption"
    definition_period = MONTH
    set_input = set_input_divide_by_period


class indemnites_journalieres_maladie(Variable):
    column = FloatCol
    entity = Individu
    label = u"Indemnités journalières de maladie"
    definition_period = MONTH
    set_input = set_input_divide_by_period


class indemnites_journalieres_accident_travail(Variable):
    column = FloatCol
    entity = Individu
    label = u"Indemnités journalières d'accident du travail"
    definition_period = MONTH
    set_input = set_input_divide_by_period


class indemnites_journalieres_maladie_professionnelle(Variable):
    column = FloatCol
    entity = Individu
    label = u"Indemnités journalières de maladie professionnelle"
    definition_period = MONTH
    set_input = set_input_divide_by_period


class indemnites_journalieres(Variable):
    column = FloatCol
    label = u"Total des indemnités journalières"
    entity = Individu
    definition_period = MONTH

    def formula(self, simulation, period):
        ressources = [
            'indemnites_journalieres_maternite',
            'indemnites_journalieres_paternite',
            'indemnites_journalieres_adoption',
            'indemnites_journalieres_maladie',
            'indemnites_journalieres_accident_travail',
            'indemnites_journalieres_maladie_professionnelle',
            ]
        total = sum(simulation.calculate(ressource, period) for ressource in ressources)

        return total


class indemnites_journalieres_imposables(Variable):
    column = FloatCol
    label = u"Total des indemnités journalières imposables"
    entity = Individu
    reference = "http://vosdroits.service-public.fr/particuliers/F3152.xhtml"
    definition_period = MONTH

    def formula(self, simulation, period):
        indemnites_journalieres = simulation.calculate('indemnites_journalieres', period)
        indemnites_journalieres_accident_travail = simulation.calculate('indemnites_journalieres_accident_travail', period)
        indemnites_journalieres_maladie_professionnelle = simulation.calculate('indemnites_journalieres_accident_travail', period)
        result = indemnites_journalieres - 0.5 * (
            indemnites_journalieres_accident_travail + indemnites_journalieres_maladie_professionnelle
        )

        return result

class date_arret_de_travail(Variable):
    column = DateCol(default = date.min)
    entity = Individu
    label = u"Date depuis laquelle la personne est en arrêt de travail"
    definition_period = ETERNITY
