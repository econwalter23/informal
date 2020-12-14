from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants

#import random

class Introduction(Page):
    
    def is_displayed(self):
        return self.round_number == 1

class MyPage(Page):

    form_model ='player'
    form_fields = ['decision']
    
    def is_displayed(self):
        return self.round_number == 1

class MyPage2(Page):

    form_model ='player'
    form_fields = ['decision']
    
    def is_displayed(self):
        return self.round_number > 1    
    
class ResultsWaitPage(WaitPage):
    after_all_players_arrive = 'set_payoffs'

class Results(Page):
    pass
        


page_sequence = [Introduction, MyPage, MyPage2, ResultsWaitPage, Results]
