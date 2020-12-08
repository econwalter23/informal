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
    players_per_session = 20
    num_rounds = 10
    media_A = 40
    media_B = 70
    media_mayor = 0.16
    impuesto = 0.18
    instructions_template = 'informal/instructions.html'
    rho = 0.7

        
    




class Subsession(BaseSubsession):
    
     def creating_session(self):
        for p in self.get_players():
            
            p.asignar_grupo = random.randint(1, Constants.players_per_session+1)
    


class Group(BaseGroup):
    decision_A = models.BooleanField(label='¿ Le gustaría continuar en su grupo actual o cambiar al grupo B?'.
                                    choices=[ 
                                        [True,'Continuar']
                                        [False, 'Cambiar']
                                    ]
                                    )
    
    decision_B = models.BooleanField(label='¿ Le gustaría continuar en su grupo actual o cambiar al grupo A?'.
                                    choices=[ 
                                        [True,'Continuar']
                                        [False, 'Cambiar']
                                    ]
                                    )

class Player(BasePlayer):
    
    def role(self):
        if self.asignar_grupo <= (0,60)*Constants.players_per_session:
            return 'grupo A'
        else:
            return 'grupo B'