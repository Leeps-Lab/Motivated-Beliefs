from otree_markets.pages import BaseMarketPage
from django.contrib.staticfiles.templatetags.staticfiles import static
from ._builtin import Page, WaitPage

class grouping(WaitPage):
    wait_for_all_groups = True
    after_all_players_arrive = 'grouping'

class Wait_for_trading(WaitPage):
    wait_for_all_groups = True

class Pre_Trading_Survey_1(Page):
    def get_timeout_seconds(self):
        return 60
    def before_next_page(self):
        if self.timeout_happened:
            if self.player.Question_1_pre_ns == '':
                self.player.Question_1_pre_ns = '-1'
            if self.player.Question_2_pre_ns == '':
                self.player.Question_2_pre_ns = '-1'
            if self.player.Question_3_pre_ns == 0:
                self.player.Question_3_pre_ns = -1
            self.player.save()

    def vars_for_template(self):
            
            def before_next_page(self):
                self.player.save()

            img_url = '/static/Motivated_Beliefs/Balls2/balls_{}.jpg'.format(self.player.signal1_black)
            if self.player.hi==1:
                color = "Green"
                hi = True
            elif self.player.hi==0:
                color = "Red"
                hi = False
            else:
                color = None

            if self.player.treatment==2:
                # for Intense 
                img_sig_url = '/static/Motivated_Beliefs/signal_pre_trading_1_i.PNG'
                divident_range = "(between 0 and 1000)"
                group_assignment = [
                'The Computer assigned you into group', 
                'H if your IQ rank is higher than your paired player', 
                'L if your IQ rank is lower than your paired player'
                ]
            elif self.player.treatment== 1: 
                # for Treatment 1 
                img_sig_url = '/static/Motivated_Beliefs/signal_pre_trading_1.PNG'
                divident_range = "(between 400 and 600)"
                group_assignment = [
                'The Computer assigned you into group', 
                'H if your IQ rank is higher than your paired player', 
                'L if your IQ rank is lower than your paired player'
                ]
            else: 
                # for control 0 
                img_sig_url = '/static/Motivated_Beliefs/signal_pre_trading_1.PNG'
                divident_range = "(between 400 and 600)"
                group_assignment = [
                'The Computer assigned you into group',
                'H or L by random.'
                ]
            
            return {
                'signal1black': self.player.signal1_black,
                'signal1white': self.player.signal1_white,
                'img_url': img_url,
                'img_sig_url': img_sig_url,
                'color':color,
                'hi': hi,
                'divident_range': divident_range,
                'group_assignment': group_assignment
            }
    form_model = 'player'
    form_fields = ['Question_1_pre_ns', 'Question_2_pre_ns', 'Question_3_pre_ns']

class Pre_Trading_Survey_2(Page):
    def get_timeout_seconds(self):
        return 60

    def before_next_page(self):
        if self.timeout_happened:
            if self.player.Question_1_pre_s == '':
                self.player.Question_1_pre_s = '-1'
            if self.player.Question_2_pre_s == '':
                self.player.Question_2_pre_s = '-1'
            if self.player.Question_3_pre_s == 0:
                self.player.Question_3_pre_s = -1
            self.player.save()

    def vars_for_template(self):
            def before_next_page(self):
                self.player.save()
            
            img_url = '/static/Motivated_Beliefs/Balls2/balls_{}.jpg'.format(self.player.signal1_black)
            if self.player.hi==1:
                color = "Green"
                hi = True
            elif self.player.hi==0:
                color = "Red"
                hi = False
            else:
                color = None
            
            if self.player.treatment==2:
                # for Intense 
                img_sig_url = '/static/Motivated_Beliefs/signal_i.PNG'
                divident_range = "(between 0 and 1000)"
                group_assignment = [
                'The Computer assigned you into group', 
                'H if your IQ rank is higher than your paired player', 
                'L if your IQ rank is lower than your paired player'
                ]
            elif self.player.treatment== 1: 
                # for Treatment 1 
                img_sig_url = '/static/Motivated_Beliefs/signal.PNG'
                divident_range = "(between 400 and 600)"
                group_assignment = [
                'The Computer assigned you into group', 
                'H if your IQ rank is higher than your paired player', 
                'L if your IQ rank is lower than your paired player'
                ]
            else: 
                # for control 0 
                img_sig_url = '/static/Motivated_Beliefs/signal.PNG'
                divident_range = "(between 400 and 600)"
                group_assignment = [
                'The Computer assigned you into group',
                'H or L by random.'
                ]
            
            return {
                'signal1black': self.player.signal1_black,
                'signal1white': self.player.signal1_white,
                'img_url': img_url,
                'img_sig_url': img_sig_url,
                'color':color,
                'hi': hi,
                'divident_range': divident_range,
                'group_assignment': group_assignment
            }

    form_model = 'player'
    form_fields = ['Question_1_pre_s', 'Question_2_pre_s', 'Question_3_pre_s']


class Market(BaseMarketPage): 
    #def get_timeout_seconds(self):
     #   return self.group.get_remaining_time()
    
    def vars_for_template(self):
        
        # img_sig_url = '/static/Motivated_Beliefs/signal.PNG'
        img_url = '/static/Motivated_Beliefs/Balls2/balls_{}.jpg'.format(self.player.signal1_black)

        r_num = self.subsession.round_number 
        output = "Period Number"
        if r_num>2:
            r_num = r_num -2
        else:
            output = "Practice Period"
        if self.player.hi==1:
             color = "Green"
             hi = True
        elif self.player.hi==0:
            color = "Red"
            hi =False
        else:
            color = None

        if self.player.treatment==2:
                # for Intense 
                img_sig_url = '/static/Motivated_Beliefs/signal_i.PNG'
                divident_range = "(between 0 and 1000)"
                group_assignment = [
                'The Computer assigned you into group', 
                'H if your IQ rank is higher than your paired player', 
                'L if your IQ rank is lower than your paired player'
                ]
        elif self.player.treatment== 1: 
            # for Treatment 1 
            img_sig_url = '/static/Motivated_Beliefs/signal.PNG'
            divident_range = "(between 400 and 600)"
            group_assignment = [
            'The Computer assigned you into group', 
            'H if your IQ rank is higher than your paired player', 
            'L if your IQ rank is lower than your paired player'
            ]
        else: 
            # for control 0 
            img_sig_url = '/static/Motivated_Beliefs/signal.PNG'
            divident_range = "(between 400 and 600)"
            group_assignment = [
            'The Computer assigned you into group',
            'H or L by random.'
            ]

        return {
            'round_num_display_string': output, 
            'round_num':r_num,
            'signal1black': self.player.signal1_black,
            'signal1white': self.player.signal1_white,
            'img_url': img_url,
            'color': color,
            'img_sig_url': img_sig_url,
            'hi':hi,
            'divident_range': divident_range,
            'group_assignment': group_assignment
        }

        
class Post_Trading_Survey(BaseMarketPage):
    def get_timeout_seconds(self):
        return 60
    def before_next_page(self):
        if self.timeout_happened:
            if self.player.Question_1_post == '':
                self.player.Question_1_post = '-1'
            if self.player.Question_2_post == '':
                self.player.Question_2_post= '-1'
            if self.player.Question_3_post == 0:
                self.player.Question_3_post = -1
            self.player.save()


    def vars_for_template(self):

            def before_next_page(self):
                self.player.save()

            img_url = '/static/Motivated_Beliefs/Balls2/balls_{}.jpg'.format(self.player.signal1_black)
            if self.player.hi==1:
                color = "Green"
                hi =True
            elif self.player.hi==0:
                color = "Red"
                hi =False
            else:
                color = None

            if self.player.treatment==2:
                # for Intense 
                img_sig_url = '/static/Motivated_Beliefs/signal_i.PNG'
                divident_range = "(between 0 and 1000)"
                group_assignment = [
                'The Computer assigned you into group', 
                'H if your IQ rank is higher than your paired player', 
                'L if your IQ rank is lower than your paired player'
                ]
            elif self.player.treatment== 1: 
                # for Treatment 1 
                img_sig_url = '/static/Motivated_Beliefs/signal.PNG'
                divident_range = "(between 400 and 600)"
                group_assignment = [
                'The Computer assigned you into group', 
                'H if your IQ rank is higher than your paired player', 
                'L if your IQ rank is lower than your paired player'
                ]
            else: 
                # for control 0 
                img_sig_url = '/static/Motivated_Beliefs/signal.PNG'
                divident_range = "(between 400 and 600)"
                group_assignment = [
                'The Computer assigned you into group',
                'H or L by random.'
                ]
            
            return {
                'signal1black': self.player.signal1_black,
                'signal1white': self.player.signal1_white,
                'img_url': img_url,
                'img_sig_url': img_sig_url,
                'color':color,
                'hi': hi,
                'divident_range': divident_range,
                'group_assignment': group_assignment
            }

    form_model = 'player'
    form_fields = ['Question_1_post', 'Question_2_post', 'Question_3_post']

class Wait(WaitPage):
    wait_for_all_groups = True
    
    after_all_players_arrive = 'set_payoffs'

class Results_trading(Page):
    def get_timeout_seconds(self):
        return 15
    def vars_for_template(self): 
        if self.player.treatment==2:
                # for Intense 
            min_l = 0
            max_l = 1000
        else: 
            min_l = 400
            max_l = 600

        return{
            'shares': self.player.shares,
#            'profit': self.player.profit,
#            'asset_value': self.player.asset_value,
             'cash_flow': self.player.settled_cash,
#            'payoff_from_trading': self.player.payoff_from_trading,
            'contingent_trading_profit_G': self.player.contingent_trading_profit_G,
            'contingent_trading_profit_B': self.player.contingent_trading_profit_B,
            'min_l' : min_l,
            'max_l' : max_l, 
        }
class Results_survey(Page):
    def get_timeout_seconds(self):
        return 15
    def vars_for_template(self): 
        return{
            'Question_1_pay_post': self.player.Question_1_payoff_post,
            'Question_2_pay_post': self.player.Question_2_payoff_post,
            'Question_3_pay_post': self.player.Question_3_payoff_post,
            'Question_1_pay_pre_ns': self.player.Question_1_payoff_pre_ns,
            'Question_2_pay_pre_ns': self.player.Question_2_payoff_pre_ns,
            'Question_3_pay_pre_ns': self.player.Question_3_payoff_pre_ns,
            'Question_1_pay_pre_s': self.player.Question_1_payoff_pre_s,
            'Question_2_pay_pre_s': self.player.Question_2_payoff_pre_s,
            'Question_3_pay_pre_s': self.player.Question_3_payoff_pre_s,
            'payoff_from_survey': self.player.survey_avg_pay, 
        }
class Results_total(Page):
    def get_timeout_seconds(self):
        return 15
    def vars_for_template(self): 
        return{
#            'total_pay':self.player.total_payoff,
            'payoff_from_survey': self.player.survey_avg_pay, 
#            'payoff_from_trading': self.player.payoff_from_trading,
            'contingent_trading_profit_G': self.player.contingent_trading_profit_G,
            'contingent_trading_profit_B': self.player.contingent_trading_profit_B,
            'contingent_total_payoff_G': self.player.contingent_total_payoff_G,
            'contingent_total_payoff_B': self.player.contingent_total_payoff_B,
        }
class Results_sum(Page):
    def get_timeout_seconds(self):
        if self.subsession.round_number==2:
            return 1000
        else:
            return 15
    def before_next_page(self):
        if self.timeout_happened:
            self.player.save()

    def vars_for_template(self): 
        if self.player.world_state==1:
            state="G"
        elif self.player.world_state==0:
            state="B"
        if self.player.treatment==2:
                # for Intense 
            min_l = 0
            max_l = 1000
        else: 
            min_l = 400
            max_l = 600
        return {
            'Question_1_pay_post': self.player.Question_1_payoff_post,
            'Question_2_pay_post': self.player.Question_2_payoff_post,
            'Question_3_pay_post': self.player.Question_3_payoff_post,
            'Question_1_pay_pre_ns': self.player.Question_1_payoff_pre_ns,
            'Question_2_pay_pre_ns': self.player.Question_2_payoff_pre_ns,
            'Question_3_pay_pre_ns': self.player.Question_3_payoff_pre_ns,
            'Question_1_pay_pre_s': self.player.Question_1_payoff_pre_s,
            'Question_2_pay_pre_s': self.player.Question_2_payoff_pre_s,
            'Question_3_pay_pre_s': self.player.Question_3_payoff_pre_s,
#            'profit': self.player.profit,
#            'asset_value': self.player.asset_value,
            'cash_flow': self.player.settled_cash,
            'payoff_from_survey': self.player.survey_avg_pay, 
#            'payoff_from_trading': self.player.payoff_from_trading,
#            'total_pay':self.player.total_payoff,
            'shares': self.player.shares,
            'contingent_trading_profit_G': self.player.contingent_trading_profit_G,
            'contingent_trading_profit_B': self.player.contingent_trading_profit_B,
            'contingent_total_payoff_G': self.player.contingent_total_payoff_G,
            'contingent_total_payoff_B': self.player.contingent_total_payoff_B,
            'min_l' : min_l,
            'max_l' : max_l, 
        }


page_sequence = [grouping, Wait_for_trading, Pre_Trading_Survey_1, Pre_Trading_Survey_2, Wait_for_trading, Market, Post_Trading_Survey, Wait, Results_trading, Results_survey, Results_total, Results_sum]
