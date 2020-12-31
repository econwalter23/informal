from otree.api import (
    models,
    widgets,
    BaseConstants,
    BaseSubsession,
    BaseGroup,
    BasePlayer,
    Currency as c,
    currency_range,
)

import random

author = 'Richard Asto & Walter Ruelas'

doc = """
Este es un juego que busca contrastar los resultados de un modelo de teoria de juegos en la que transitan
empresas del sector formal al informal
"""

class Constants(BaseConstants):

    name_in_url = 'informal_game'
    players_per_group = 2
    num_rounds = 5
    
    #endowments y parámetros iniciales 
    endow_B = c(100)
    endow_A = c(endow_B*0.25)
    impuesto = 0.18
    p_like = 0.5
    q_like = 0.5
    b_star = (1/((1-impuesto)**(2)-q_like*impuesto*impuesto*(1-p_like)))*( (1-impuesto)**(2) + q_like*(1-impuesto)*( (endow_A/endow_B)+impuesto*(1-p_like) ) )
    a_star = 1 + (((1-p_like)/(1-impuesto))*(1-impuesto + impuesto*b_star)*(endow_B/endow_A))
    
    #rango de las choques de productividad
    A_solo = 1
    A_compa = 2 
    B_solo = 0.5
    B_compa = 2
    alto_solo = 0.9
    alto_compa = 0.1

    # rangos de la empresa informal si se queda sola o comparte
    s_minAsolo = -c(A_solo*endow_A)
    s_maxAsolo = c( ((a_star*impuesto/(1-impuesto))*endow_A/(alto_solo))-((1-alto_solo)/alto_solo)*s_minAsolo )
    s_maxAcompa = c(A_compa*endow_A)
    s_minAcompa = c( (a_star*impuesto/((1-impuesto)*(1-alto_compa)))*endow_A - (alto_compa/(1-alto_compa))*s_maxAcompa )

    # rangos de la empresa formal si se queda sola o comparte
    s_minBsolo = -c(B_solo*endow_B)
    s_maxBcompa = c(B_compa*endow_B)
    s_maxBsolo = c( ((b_star*impuesto/(1-impuesto))*endow_B/(alto_solo))-((1-alto_solo)/alto_solo)*s_minBsolo )
    s_minBcompa = c( ((b_star*impuesto/(1-impuesto))*endow_B/(1-alto_compa))-(alto_compa/(1-alto_compa))*s_maxBcompa )
    

    # pagos esperados minimos y máximos de la informal
    p_nAtB = c(endow_A)
    p_tAtBmin = c((1-impuesto)*(endow_A + s_minAsolo))
    p_tAtBmax = c((1-impuesto)*(endow_A + s_maxAsolo))
    p_nAnBmin = c(endow_A + (endow_B + s_minBsolo)*impuesto)
    p_nAnBmax = c(endow_A + (endow_B + s_maxBsolo)*impuesto)
    p_tAnBmin = c((1-impuesto)*(endow_A + s_minAcompa))
    p_tAnBmax = c((1-impuesto)*(endow_A + s_maxAcompa))

    # pagos esperados minimos y máximos de la formal
    p_tBnA = c(endow_B)
    p_tBtAmin = c(endow_B + impuesto*(endow_A + s_minAsolo))
    p_tBtAmax = c(endow_B + impuesto*(endow_A + s_maxAsolo))
    p_nBnAmin = c((1-impuesto)*(endow_B + s_minBsolo))
    p_nBnAmax = c((1-impuesto)*(endow_B + s_maxBsolo))
    p_nBtAmin = c((1-impuesto)*(endow_B + s_minBcompa))
    p_nBtAmax = c((1-impuesto)*(endow_B + s_maxBcompa))

    # intrucciones
    instructions_template = 'informal/instructions.html'
    instructions_button = "informal/Instructions_Button.html"
    instructions_template_A = 'informal/instructionsA.html'
    instructions_buttonA = "informal/Instructions_ButtonA.html"
    

class Subsession(BaseSubsession):
    pass

class Group(BaseGroup):

    def set_prod(self):
        '''Calcula los choques de productividad de cada participante dependiendo si esta solo en un sector o acompañado'''
        p1 = self.get_player_by_id(1)
        p2 = self.get_player_by_id(2)
        
        p1.prodsolo = random.uniform(Constants.s_minAsolo,Constants.s_maxAsolo)
        p1.prodcompa = random.uniform(Constants.s_minAcompa,Constants.s_maxAcompa)
        p2.prodsolo = random.uniform(Constants.s_minBsolo,Constants.s_maxBsolo)
        p2.prodcompa = random.uniform(Constants.s_minBcompa,Constants.s_maxBcompa)

    def set_payoffs(self):
        '''Calcula el pago de los participantes tomando en cuenta la decision del otro'''
        p1 = self.get_player_by_id(1)
        p2 = self.get_player_by_id(2)
        

        if p1.decision == 'Transitar':
            if p2.decision == 'Transitar':
                p1.payoff = (1-Constants.impuesto)*(Constants.endow_A + p1.prodsolo)
                p2.payoff = Constants.endow_B + Constants.impuesto*(Constants.endow_A + p1.prodsolo)
            
            else:
                
                p1.payoff = (1-Constants.impuesto)*(Constants.endow_A + p1.prodcompa)
                p2.payoff = (1-Constants.impuesto)*(Constants.endow_B + p2.prodcompa)
        else:    
            if p2.decision == 'Transitar':
                p1.payoff = Constants.endow_A
                p2.payoff = Constants.endow_B
            else:
                p1.payoff = Constants.endow_A + Constants.impuesto*(Constants.endow_B + p2.prodsolo)
                p2.payoff = (1-Constants.impuesto)*(Constants.endow_B + p2.prodsolo)

class Player(BasePlayer):
    
    def role(self):
        '''Asigna el sector al que pertenecera cada jugador'''
        if self.id_in_group == 1:
            return 'Informal'
        else:
            return 'Formal'

    decision = models.BooleanField(label='¿ Le gustaría continuar en su grupo actual o transitar al otro grupo?',
                                    choices=[ 
                                        [True,'Transitar'],
                                        [False, 'No transitar']
                                    ]
                                    )
    
