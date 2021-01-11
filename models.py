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
empresas del sector formal al informal y viceversa.
"""

class Constants(BaseConstants):

    name_in_url = 'informal_game'
    players_per_group = 2
    players_per_session = 10
    num_rounds = 10
    
    #endowments y parámetros iniciales 
    endow_B = float(100)
    endow_A = float(endow_B*0.25)

    impuesto = float(0.18)
    p_like = float(0.5)
    q_like = float(0.5)
        
    #rango de las choques de productividad
    A_solo = 1
    A_compa = 2 
    B_solo = float(0.5)
    B_compa = 2
    alto_solo = float(0.9)
    alto_compa = float(0.1)

    # prob de los choques empresa informal
    probAsolo = [0.1, 0.9]
    probAcompa = [0.9, 0.1]

    # prob de los choques empresa formal
    probBsolo = [0.1, 0.9]
    probBcompa = [0.9, 0.1]

    # intrucciones
    instructions_template = 'informal/instructions.html'
    instructions_button = "informal/Instructions_Button.html"
    instructions_template_A = 'informal/instructionsA.html'
    instructions_buttonA = "informal/Instructions_ButtonA.html"
    

class Subsession(BaseSubsession):

    def creating_session(self):
        """Calculo algunas variables que se usan en cada ronda"""
        x = range(1,Constants.num_rounds+1)
        for self.round_number in x:

            self.session.vars['endow_B'] = float(100)*self.round_number
            self.session.vars['endow_A'] = float(self.session.vars['endow_B']*0.25)

            #a_star y b_Star que se usan para calcular los pagos
            self.session.vars['b_star'] = float((1/((1-Constants.impuesto)**(2)-(Constants.q_like*Constants.impuesto*Constants.impuesto)*(1-Constants.p_like)))*( (1-Constants.impuesto)**(2) + (Constants.q_like*(1-Constants.impuesto))*( (Constants.endow_A/Constants.endow_B)+Constants.impuesto*(1-Constants.p_like) ) ))
            self.session.vars['a_star'] = float(1 + (((1-Constants.p_like)/(1-Constants.impuesto))*(1-Constants.impuesto + (Constants.impuesto*self.session.vars['b_star']))*(self.session.vars['endow_B']/self.session.vars['endow_A'])))
            
            # rangos de la empresa informal si se queda sola o comparte
            self.session.vars['s_minAsolo'] = -(Constants.A_solo*self.session.vars['endow_A'])
            self.session.vars['s_maxAsolo'] = float( ((self.session.vars['a_star']*Constants.impuesto/(1-Constants.impuesto))*(self.session.vars['endow_A'])/(Constants.alto_solo))-((1-Constants.alto_solo)/Constants.alto_solo)*self.session.vars['s_minAsolo'] )
            self.session.vars['s_maxAcompa'] = (Constants.A_compa*self.session.vars['endow_A'])
            self.session.vars['s_minAcompa'] = float( (self.session.vars['a_star']*Constants.impuesto/((1-Constants.impuesto)*(1-Constants.alto_compa)))*self.session.vars['endow_A'] - (Constants.alto_compa/(1-Constants.alto_compa))*self.session.vars['s_maxAcompa'] )    

            self.session.vars['elemAsolo'] = [self.session.vars['s_minAsolo'] , self.session.vars['s_maxAsolo']]
            self.session.vars['elemAcompa'] = [self.session.vars['s_minAcompa'], self.session.vars['s_maxAcompa']]

            # rangos de la empresa formal si se queda sola o comparte
            self.session.vars['s_minBsolo'] = -(Constants.B_solo*self.session.vars['endow_B'])
            self.session.vars['s_maxBcompa'] = (Constants.B_compa*self.session.vars['endow_B'])
            self.session.vars['s_maxBsolo'] = float( ((self.session.vars['b_star']*Constants.impuesto/(1-Constants.impuesto))*self.session.vars['endow_B']/(Constants.alto_solo))-((1-Constants.alto_solo)/(Constants.alto_solo))*self.session.vars['s_minBsolo'] )
            self.session.vars['s_minBcompa'] = float( ((self.session.vars['b_star']*Constants.impuesto/(1-Constants.impuesto))*self.session.vars['endow_B']/(1-Constants.alto_compa))-(Constants.alto_compa/(1-Constants.alto_compa))*self.session.vars['s_maxBcompa'] )

            self.session.vars['elemBsolo'] = [self.session.vars['s_minBsolo'], self.session.vars['s_maxBsolo']]
            self.session.vars['elemBcompa'] = [self.session.vars['s_minBcompa'], self.session.vars['s_maxBcompa']]

            # pagos minimos y máximos de la informal
            self.session.vars['p_tAtBmin'] = round((1-Constants.impuesto)*(self.session.vars['endow_A'] + self.session.vars['s_minAsolo']),1)
            self.session.vars['p_tAtBmax'] = round((1-Constants.impuesto)*(self.session.vars['endow_A'] + self.session.vars['s_maxAsolo']),1)
            self.session.vars['p_nAnBmin'] = round(self.session.vars['endow_A'] + (self.session.vars['endow_B'] + self.session.vars['s_minBsolo'])*Constants.impuesto,1)
            self.session.vars['p_nAnBmax'] = round(self.session.vars['endow_A'] + (self.session.vars['endow_B'] + self.session.vars['s_maxBsolo'])*Constants.impuesto,1)
            self.session.vars['p_tAnBmin'] = round((1-Constants.impuesto)*(self.session.vars['endow_A'] + self.session.vars['s_minAcompa']),1)
            self.session.vars['p_tAnBmax'] = round((1-Constants.impuesto)*(self.session.vars['endow_A'] + self.session.vars['s_maxAcompa']),1)

            # pagos minimos y máximos de la formal

            self.session.vars['p_tBtAmin'] = round(self.session.vars['endow_B'] + Constants.impuesto*(self.session.vars['endow_A'] + self.session.vars['s_minAsolo']),1)
            self.session.vars['p_tBtAmax'] = round(self.session.vars['endow_B'] + Constants.impuesto*(self.session.vars['endow_A'] + self.session.vars['s_maxAsolo']),1)
            self.session.vars['p_nBnAmin'] = round((1-Constants.impuesto)*(self.session.vars['endow_B'] + self.session.vars['s_minBsolo']),1)
            self.session.vars['p_nBnAmax'] = round((1-Constants.impuesto)*(self.session.vars['endow_B'] + self.session.vars['s_maxBsolo']),1)
            self.session.vars['p_nBtAmin'] = round((1-Constants.impuesto)*(self.session.vars['endow_B'] + self.session.vars['s_minBcompa']),1)
            self.session.vars['p_nBtAmax'] = round((1-Constants.impuesto)*(self.session.vars['endow_B'] + self.session.vars['s_maxBcompa']),1)

            for p in self.get_players():
                if p.id_in_group == 1:
                    p.participant.vars['prodAsolo'] = random.choices(self.session.vars['elemAsolo'],Constants.probAsolo,k=1)
                    p.participant.vars['prodAcompa'] = random.choices(self.session.vars['elemAcompa'],Constants.probAcompa,k=1)
                else:
                    p.participant.vars['prodBcompa'] = random.choices(self.session.vars['elemBcompa'],Constants.probBcompa,k=1)
                    p.participant.vars['prodBsolo'] = random.choices(self.session.vars['elemBsolo'],Constants.probBsolo,k=1)
                
class Group(BaseGroup):

      
    def set_payoffs(self):
        '''Calcula el pago de los participantes tomando en cuenta la decision del otro'''
        p1 = self.get_player_by_id(1)
        p2 = self.get_player_by_id(2)
        
        if p1.decision == 'Transitar':
            if p2.decision == 'Transitar':
                p1.payoff = round(float((1-Constants.impuesto)*(self.session.vars['endow_A'][0] + p1.participant.vars['prodAsolo'][0])),1)
                p2.payoff = round(float(Constants.endow_B + Constants.impuesto*(self.session.vars['endow_A'][0]
            else:    
                p1.payoff = round(float((1-Constants.impuesto)*(self.session.vars['endow_A'][0] + p1.participant.vars['prodAcompa'][0])),1)
                p2.payoff = round(float((1-Constants.impuesto)*(self.session.vars['endow_B'][0] + p2.participant.vars['prodBcompa'][0])),1)
        else:    
            if p2.decision == 'Transitar':
                p1.payoff = self.session.vars['endow_A'][0]
                p2.payoff = self.session.vars['endow_B'][0]
            else:
                p1.payoff = round(float(self.session.vars['endow_A'][0] + Constants.impuesto*(self.session.vars['endow_B'][0] + p2.participant.vars['prodBsolo'][0])),1)
                p2.payoff = round(float((1-Constants.impuesto)*(self.session.vars['endow_B'][0] + p2.participant.vars['prodBsolo'][0])),1)
    
    def set_ratio(self):
        '''Calcula el ratio de los participantes'''
        p1 = self.get_player_by_id(1)  
        p2 = self.get_player_by_id(2)
        # Aquí en  Group class calculo los ratios de cada jugador. Pero luego no se como podria sumar
        #  los obtenidos en cada ronda.
        p1.ratio = round(float(p1.payoff/self.session.vars['endow_A'][0]),1)
        p2.ratio = round(float(p2.payoff/self.session.vars['endow_B'][0]),1)
    

class Player(BasePlayer):

    # aqui defino un booleano tq' a cada jugador le sale dos posibilidades de transitar o no.
    decision = models.BooleanField(label='¿ Le gustaría continuar en su sector actual o transitar al otro sector?',
                                    choices=[ 
                                        [True,'Transitar'],
                                        [False, 'No transitar']
                                    ]
                                    )

    

    



    



