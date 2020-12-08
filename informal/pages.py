from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants
import random

class Introduction(Page):
    def is_displayed(self):
        return self.round_number == 1

class MyPageB(Page):
    
    def before_next_page(self):
        for p in self.group.get_players():
            if p.role() == 'grupo B':
                if self.round_number == 1: 
                    p.product = random.randint(-10,10)
                    if p.product > 0:
                        p.transfer_B = (Constants.media_B + p.product)*Constants.impuesto
                        p.endowment_B = (Constants.media_B + p.product)*(1 - Constants.impuesto)
                    else:
                        p.transfer_B = 0 
                        p.endowment_B = Constants.media_B + p.product
                else:
                    p.product = Constants.rho*p.product + random.randint(-10,10)
                    if p.product > 0:
                        p.transfer_B = (p.endowment_B + p.product)*(Constants.impuesto)
                        p.endowment_B = (p.endowment_B + p.product)*(1 - Constants.impuesto)
                    else:
                        p.transfer_B = 0
                        p.endowment_B = p.endowment_B + (1 + Constants.rho)*p.product
            pass   
    
    def is_displayed(self):
        return self.p.role() == 'grupo B' 

class MyPageB2(Page):
    
    form_model ='group'
    form_fields = ['decision_B']
    
    def is_displayed(self):
        return self.p.role() == 'grupo B' 

class WaitForB(WaitPage):
    
    def is_displayed(self):
        return self.p.role() == 'grupo A' 

class MyPageA(Page):
    
    def before_next_page(self):
        for p in self.group.get_players():
            if p.role() == 'grupo A':
                if self.round_number == 1: 
                    p.transfer_A = p.transfer_B
                    p.endowment_A = Constants.media_A + p.transfer_A
                else:
                    p.endowment_A = p.endowment_A + p.transfer_A
            pass

    def is_displayed(self):
        return self.p.role() == 'grupo A'

class MyPageA2(Page):
    
    form_model ='group'
    form_fields = ['decision_A']
    
    def is_displayed(self):
        return self.p.role() == 'grupo A' 



class ResultsWaitPage(WaitPage):
    pass


class Results(Page):
    pass


page_sequence = [Introduction, MyPageB, MyPageA, MyPageB2, ResultsWaitPage, Results]
