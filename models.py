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
    num_rounds = 7
    
    #endowments y parámetros iniciales 
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
    contact_template = "informal/Contactenos.html"
    

class Subsession(BaseSubsession):

    def creating_session(self):
        """Calculo algunas variables que se usan en cada ronda"""
        x = range(1,Constants.num_rounds+1)
        lendow_B = []
        lendow_A = []
        lb_star = [] 
        la_star = []
        ls_minAsolo = []
        ls_maxAsolo = []
        ls_maxAcompa = []
        ls_minAcompa = []
        lelemAsolo = []
        lelemAcompa = []

        lp_tAtBmin = []
        lp_tAtBmax = []
        lp_nAnBmin = []
        lp_nAnBmax = []
        lp_tAnBmin = []
        lp_tAnBmax = []

        lp_tBtAmin = []
        lp_tBtAmax = []
        lp_nBnAmin = []
        lp_nBnAmax = []
        lp_nBtAmin = []
        lp_nBtAmax = []

        lprodAsolo = []
        lprodAcompa = []
        lprodBsolo = []
        lprodBcompa = []

        for i in x:
                
            self.session.vars[f'endow_B_{i}'] = float(200)*i
            self.session.vars[f'endow_A_{i}'] = float(self.session.vars[f'endow_B_{i}']*0.25)

            lendow_B.append(self.session.vars[f'endow_B_{i}'])
            self.session.vars['endow_B']= lendow_B

            lendow_A.append(self.session.vars[f'endow_A_{i}'])
            self.session.vars['endow_A']= lendow_A

            #a_star y b_Star que se usan para calcular los pagos
            self.session.vars[f'b_star_{i}'] = float((1/((1-Constants.impuesto)**(2)-(Constants.q_like*Constants.impuesto*Constants.impuesto)*(1-Constants.p_like)))*( (1-Constants.impuesto)**(2) + (Constants.q_like*(1-Constants.impuesto))*( (self.session.vars[f'endow_A_{i}']/self.session.vars[f'endow_B_{i}'])+Constants.impuesto*(1-Constants.p_like) ) ))
            self.session.vars[f'a_star_{i}'] = float(1 + (((1-Constants.p_like)/(1-Constants.impuesto))*(1-Constants.impuesto + (Constants.impuesto*self.session.vars[f'b_star_{i}']))*(self.session.vars[f'endow_B_{i}'] / self.session.vars[f'endow_A_{i}'])))
            
            lb_star.append(self.session.vars[f'b_star_{i}'])
            self.session.vars['b_star']= lb_star

            la_star.append(self.session.vars[f'a_star_{i}'])
            self.session.vars['a_star'] = la_star

            # rangos de la empresa informal si se queda sola o comparte
            self.session.vars[f's_minAsolo_{i}'] = -(Constants.A_solo*self.session.vars[f'endow_A_{i}'])
            self.session.vars[f's_maxAsolo_{i}'] = float( ((self.session.vars[f'a_star_{i}']*Constants.impuesto/(1-Constants.impuesto))*(self.session.vars[f'endow_A_{i}'])/(Constants.alto_solo))-((1-Constants.alto_solo)/Constants.alto_solo)*self.session.vars[f's_minAsolo_{i}'] )
            self.session.vars[f's_maxAcompa_{i}'] = (Constants.A_compa*self.session.vars[f'endow_A_{i}'])
            self.session.vars[f's_minAcompa_{i}'] = float( (self.session.vars[f'a_star_{i}']*Constants.impuesto/((1-Constants.impuesto)*(1-Constants.alto_compa)))*self.session.vars[f'endow_A_{i}'] - (Constants.alto_compa/(1-Constants.alto_compa))*self.session.vars[f's_maxAcompa_{i}'] )    

            ls_minAsolo.append(self.session.vars[f's_minAsolo_{i}'])
            self.session.vars['s_minAsolo'] = ls_minAsolo

            ls_maxAsolo.append(self.session.vars[f's_maxAsolo_{i}'])
            self.session.vars['s_maxAsolo'] = ls_maxAsolo

            ls_maxAcompa.append(self.session.vars[f's_maxAcompa_{i}'])
            self.session.vars['s_maxAcompa'] = ls_maxAcompa

            ls_minAcompa.append(self.session.vars[f's_minAcompa_{i}'])
            self.session.vars['s_minAcompa'] = ls_minAcompa

            self.session.vars[f'elemAsolo_{i}'] = [self.session.vars[f's_minAsolo_{i}'] , self.session.vars[f's_maxAsolo_{i}']]
            self.session.vars[f'elemAcompa_{i}'] = [self.session.vars[f's_minAcompa_{i}'], self.session.vars[f's_maxAcompa_{i}']]

            lelemAsolo.append(self.session.vars[f'elemAsolo_{i}'])
            self.session.vars['elemAsolo'] = lelemAsolo

            lelemAcompa.append(self.session.vars[f'elemAcompa_{i}'])
            self.session.vars['elemAcompa'] = lelemAcompa

            # rangos de la empresa formal si se queda sola o comparte
            self.session.vars[f's_minBsolo_{i}'] = -(Constants.B_solo*self.session.vars[f'endow_B_{i}'])
            self.session.vars[f's_maxBcompa_{i}'] = (Constants.B_compa*self.session.vars[f'endow_B_{i}'])
            self.session.vars[f's_maxBsolo_{i}'] = float( ((self.session.vars[f'b_star_{i}']*Constants.impuesto/(1-Constants.impuesto))*self.session.vars[f'endow_B_{i}']/(Constants.alto_solo))-((1-Constants.alto_solo)/(Constants.alto_solo))*self.session.vars[f's_minBsolo_{i}'] )
            self.session.vars[f's_minBcompa_{i}'] = float( ((self.session.vars[f'b_star_{i}']*Constants.impuesto/(1-Constants.impuesto))*self.session.vars[f'endow_B_{i}']/(1-Constants.alto_compa))-(Constants.alto_compa/(1-Constants.alto_compa))*self.session.vars[f's_maxBcompa_{i}'] )

            self.session.vars[f'elemBsolo_{i}'] = [self.session.vars[f's_minBsolo_{i}'], self.session.vars[f's_maxBsolo_{i}']]
            self.session.vars[f'elemBcompa_{i}'] = [self.session.vars[f's_minBcompa_{i}'], self.session.vars[f's_maxBcompa_{i}']]

            # pagos minimos y máximos de la informal
            self.session.vars[f'p_tAtBmin_{i}'] = round((1-Constants.impuesto)*(self.session.vars[f'endow_A_{i}'] + self.session.vars[f's_minAsolo_{i}']),0)
            self.session.vars[f'p_tAtBmax_{i}'] = round((1-Constants.impuesto)*(self.session.vars[f'endow_A_{i}'] + self.session.vars[f's_maxAsolo_{i}']),0)
            self.session.vars[f'p_nAnBmin_{i}'] = round(self.session.vars[f'endow_A_{i}'] + (self.session.vars[f'endow_B_{i}'] + self.session.vars[f's_minBsolo_{i}'])*Constants.impuesto,0)
            self.session.vars[f'p_nAnBmax_{i}'] = round(self.session.vars[f'endow_A_{i}'] + (self.session.vars[f'endow_B_{i}'] + self.session.vars[f's_maxBsolo_{i}'])*Constants.impuesto,0)
            self.session.vars[f'p_tAnBmin_{i}'] = round((1-Constants.impuesto)*(self.session.vars[f'endow_A_{i}'] + self.session.vars[f's_minAcompa_{i}']),0)
            self.session.vars[f'p_tAnBmax_{i}'] = round((1-Constants.impuesto)*(self.session.vars[f'endow_A_{i}'] + self.session.vars[f's_maxAcompa_{i}']),0)

            lp_tAtBmin.append(self.session.vars[f'p_tAtBmin_{i}'])
            self.session.vars['p_tAtBmin'] = lp_tAtBmin

            lp_tAtBmax.append(self.session.vars[f'p_tAtBmax_{i}'])
            self.session.vars['p_tAtBmax'] = lp_tAtBmax

            lp_nAnBmin.append(self.session.vars[f'p_nAnBmin_{i}'])
            self.session.vars['p_nAnBmin'] = lp_nAnBmin

            lp_nAnBmax.append(self.session.vars[f'p_nAnBmax_{i}'])
            self.session.vars['p_nAnBmax'] = lp_nAnBmax

            lp_tAnBmin.append(self.session.vars[f'p_tAnBmin_{i}'])
            self.session.vars['p_tAnBmin'] = lp_tAnBmin

            lp_tAnBmax.append(self.session.vars[f'p_tAnBmax_{i}'])
            self.session.vars['p_tAnBmax'] = lp_tAnBmax

            # pagos minimos y máximos de la formal

            self.session.vars[f'p_tBtAmin_{i}'] = round(self.session.vars[f'endow_B_{i}'] + Constants.impuesto*(self.session.vars[f'endow_A_{i}'] + self.session.vars[f's_minAsolo_{i}']),0)
            self.session.vars[f'p_tBtAmax_{i}'] = round(self.session.vars[f'endow_B_{i}'] + Constants.impuesto*(self.session.vars[f'endow_A_{i}'] + self.session.vars[f's_maxAsolo_{i}']),0)
            self.session.vars[f'p_nBnAmin_{i}'] = round((1-Constants.impuesto)*(self.session.vars[f'endow_B_{i}'] + self.session.vars[f's_minBsolo_{i}']),0)
            self.session.vars[f'p_nBnAmax_{i}'] = round((1-Constants.impuesto)*(self.session.vars[f'endow_B_{i}'] + self.session.vars[f's_maxBsolo_{i}']),0)
            self.session.vars[f'p_nBtAmin_{i}'] = round((1-Constants.impuesto)*(self.session.vars[f'endow_B_{i}'] + self.session.vars[f's_minBcompa_{i}']),0)
            self.session.vars[f'p_nBtAmax_{i}'] = round((1-Constants.impuesto)*(self.session.vars[f'endow_B_{i}'] + self.session.vars[f's_maxBcompa_{i}']),0)

            lp_tBtAmin.append(self.session.vars[f'p_tBtAmin_{i}'])
            self.session.vars['p_tBtAmin'] = lp_tBtAmin

            lp_tBtAmax.append(self.session.vars[f'p_tBtAmax_{i}'])
            self.session.vars['p_tBtAmax'] = lp_tBtAmax

            lp_nBnAmin.append(self.session.vars[f'p_nBnAmin_{i}'])
            self.session.vars['p_nBnAmin'] = lp_nBnAmin

            lp_nBnAmax.append(self.session.vars[f'p_nBnAmax_{i}'])
            self.session.vars['p_nBnAmax'] = lp_nBnAmax

            lp_nBtAmin.append(self.session.vars[f'p_nBtAmin_{i}'])
            self.session.vars['p_nBtAmin'] = lp_nBtAmin

            lp_nBtAmax.append(self.session.vars[f'p_nBtAmax_{i}'])
            self.session.vars['p_nBtAmax'] = lp_nBtAmax

            for p in self.get_players():
                if p.id_in_group == 1:
                    p.participant.vars[f'prodAsolo_{i}'] = random.choices(self.session.vars[f'elemAsolo_{i}'],Constants.probAsolo,k=1)
                    p.participant.vars[f'prodAcompa_{i}'] = random.choices(self.session.vars[f'elemAcompa_{i}'],Constants.probAcompa,k=1)
                
                    lprodAsolo.append(p.participant.vars[f'prodAsolo_{i}'] )
                    p.participant.vars['prodAsolo'] = lprodAsolo     

                    lprodAcompa.append(p.participant.vars[f'prodAcompa_{i}'])
                    p.participant.vars['prodAcompa'] = lprodAcompa            
                
                else:
                    p.participant.vars[f'prodBcompa_{i}'] = random.choices(self.session.vars[f'elemBcompa_{i}'],Constants.probBcompa,k=1)
                    p.participant.vars[f'prodBsolo_{i}'] = random.choices(self.session.vars[f'elemBsolo_{i}'],Constants.probBsolo,k=1)

                    lprodBsolo.append(p.participant.vars[f'prodBsolo_{i}'])
                    p.participant.vars['prodBsolo'] = lprodBsolo     

                    lprodBcompa.append( p.participant.vars[f'prodBcompa_{i}'] )
                    p.participant.vars['prodBcompa'] = lprodBcompa            
                
                
class Group(BaseGroup):

    
    def set_payoffs(self):
        '''Calcula el pago de los participantes tomando en cuenta la decision del otro'''
        p1 = self.get_player_by_id(1)
        p2 = self.get_player_by_id(2)

        if p1.decision == True:
            
            if p2.decision == True:
                p1.payoff = round(float((1-Constants.impuesto)*(self.session.vars[f'endow_A_{self.round_number}'] + p1.participant.vars[f'prodAsolo_{self.round_number}'][0])),1)/self.session.vars[f'endow_A_{self.round_number}']
                p2.payoff = round(float(self.session.vars[f'endow_B_{self.round_number}'] + Constants.impuesto*(self.session.vars[f'endow_A_{self.round_number}']+p1.participant.vars[f'prodAsolo_{self.round_number}'][0])),1)/ self.session.vars[f'endow_B_{self.round_number}']
            else:
                        
                p1.payoff = round(float((1-Constants.impuesto)*(self.session.vars[f'endow_A_{self.round_number}'] + p1.participant.vars[f'prodAcompa_{self.round_number}'][0])),1)/self.session.vars[f'endow_A_{self.round_number}']
                p2.payoff = round(float((1-Constants.impuesto)*(self.session.vars[f'endow_B_{self.round_number}'] + p2.participant.vars[f'prodBcompa_{self.round_number}'][0])),1)/self.session.vars[f'endow_B_{self.round_number}']
        else:    
            if p2.decision == True:
                p1.payoff = 1
                p2.payoff = 1
            else:
                p1.payoff = round((self.session.vars[f'endow_A_{self.round_number}'] + Constants.impuesto*(self.session.vars[f'endow_B_{self.round_number}'] + p2.participant.vars[f'prodBsolo_{self.round_number}'][0])),1)/ self.session.vars[f'endow_A_{self.round_number}']
                p2.payoff = round(((1-Constants.impuesto)*(self.session.vars[f'endow_B_{self.round_number}'] + p2.participant.vars[f'prodBsolo_{self.round_number}'][0])),1)/ self.session.vars[f'endow_B_{self.round_number}']
    
    def set_ratios(self):
        '''Calcula el ratio de los participantes tomando en cuenta la decision del otro'''
        p1 = self.get_player_by_id(1)
        p2 = self.get_player_by_id(2)

        if p1.decision == True:
            
            if p2.decision == True:
                p1.ratio = round(float((1-Constants.impuesto)*(self.session.vars[f'endow_A_{self.round_number}'] + p1.participant.vars[f'prodAsolo_{self.round_number}'][0])),0)
                p2.ratio = round(float(self.session.vars[f'endow_B_{self.round_number}'] + Constants.impuesto*(self.session.vars[f'endow_A_{self.round_number}']+p1.participant.vars[f'prodAsolo_{self.round_number}'][0])),0)
            else:
                        
                p1.ratio = round(float((1-Constants.impuesto)*(self.session.vars[f'endow_A_{self.round_number}'] + p1.participant.vars[f'prodAcompa_{self.round_number}'][0])),0)
                p2.ratio = round(float((1-Constants.impuesto)*(self.session.vars[f'endow_B_{self.round_number}'] + p2.participant.vars[f'prodBcompa_{self.round_number}'][0])),0)
        else:    
            if p2.decision == True:
                p1.ratio = self.session.vars[f'endow_A_{self.round_number}']
                p2.ratio = self.session.vars[f'endow_B_{self.round_number}']
            else:
                p1.ratio = round((self.session.vars[f'endow_A_{self.round_number}'] + Constants.impuesto*(self.session.vars[f'endow_B_{self.round_number}'] + p2.participant.vars[f'prodBsolo_{self.round_number}'][0])),0)
                p2.ratio = round(((1-Constants.impuesto)*(self.session.vars[f'endow_B_{self.round_number}'] + p2.participant.vars[f'prodBsolo_{self.round_number}'][0])),0)

    def after_all_players_arrive_method(self):
        self.set_payoffs()
        self.set_ratios()

class Player(BasePlayer):

    def role(self):
        '''Asigna el sector al que pertenecera cada jugador'''
        if self.id_in_group == 1:
            return 'Informal'
        else:
            return 'Formal'


    # aqui defino un booleano tq' a cada jugador le sale dos posibilidades de transitar o no.
    decision = models.BooleanField(label='¿ Le gustaría continuar en su sector actual o transitar al otro sector?',
                                    choices=[ 
                                        [True,'Transitar'],
                                        [False, 'No transitar']
                                    ]
                                    )
    
    ratio = models.FloatField()

    

    



    



