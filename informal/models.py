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

    name_in_url = 'Informal Game'
    players_per_group = 2
    num_rounds = 5
    endow_B = c(70)
    endow_A = c(endow_B*0.25)
    s_minB = -5
    s_maxB = 5
    s_minA = -3
    s_maxA = 3
    p_like = 0.5
    q_like = 0.5

    impuesto = 0.18

    e_payment_ntA_ntB = endow_A + impuesto*(endow_B + (s_minB+s_maxB)*0.5)
    e_payment_tA = (1-impuesto)*(endow_A + (s_minA + s_maxA)*0.5)

    e_payment_ntB = (1-impuesto)*(endow_B + (s_minB + s_maxB)*0.5)
    e_payment_tB_tA = endow_B + impuesto*(endow_A + (s_minA + s_maxA)*0.5)


    instructions_template = 'informal/instructions.html'
    instructions_template_A = 'informal/instructionsA.html'
    

class Subsession(BaseSubsession):
    pass

class Group(BaseGroup):

    def set_payoffs(self):
        p1 = self.get_player_by_id(1)
        p2 = self.get_player_by_id(2)
        
        p1.prod = random.uniform(Constants.s_minA,Constants.s_maxA)
        p2.prod = random.uniform(Constants.s_minB,Constants.s_maxB)    

        if p1.decision == 'Transitar':
            if p2.decision == 'Transitar':
                p1.payoff = (1-Constants.impuesto)*(Constants.endow_A + p1.prod)
                p2.payoff = Constants.endow_B + Constants.impuesto*(Constants.endow_A + p1.prod)
            
            else:
                
                p1.payoff = (1-Constants.impuesto)*(Constants.endow_A + p1.prod)
                p2.payoff = (1-Constants.impuesto)*(Constants.endow_B + p2.prod)
        else:    
            if p2.decision == 'Transitar':
                p1.payoff = Constants.endow_A
                p2.payoff = Constants.endow_B
            else:
                p1.payoff = Constants.endow_A + Constants.impuesto*(Constants.endow_B + p2.prod)
                p2.payoff = (1-Constants.impuesto)*(Constants.endow_B + p2.prod)

class Player(BasePlayer):
    
    decision = models.BooleanField(label='¿ Le gustaría continuar en su grupo actual o transitar al otro grupo?',
                                    choices=[ 
                                        [True,'Transitar'],
                                        [False, 'No transitar']
                                    ]
                                    )
    
