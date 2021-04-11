from otree.api import (
    models, BaseConstants
)
from otree_markets import models as markets_models
from otree_markets.exchange.base import Order
from .configmanager import ConfigManager

import random
import itertools
import numpy as np
import math

class Constants(BaseConstants):
    name_in_url = 'Motivated_Beliefs'
    players_per_group = None
    num_rounds = 16
    # the columns of the config CSV and their types
    # this dict is used by ConfigManager
    config_fields = {
        'period_length': int,
        'asset_endowment': int,
        'cash_endowment': int,
        'allow_short': bool,
        'state': int,
        'player_1_pair': int, 
        'player_2_pair': int, 
        'player_3_pair': int, 
        'player_4_pair': int, 
        'player_5_pair': int, 
        'player_6_pair': int, 
        'player_7_pair': int, 
        'player_8_pair': int,
        'treat': int, 
        'player_1_treat': int, 
        'player_2_treat': int, 
        'player_3_treat': int, 
        'player_4_treat': int, 
        'player_5_treat': int, 
        'player_6_treat': int, 
        'player_7_treat': int, 
        'player_8_treat': int, 
        'player_1_con': int, 
        'player_2_con': int, 
        'player_3_con': int, 
        'player_4_con': int, 
        'player_5_con': int, 
        'player_6_con': int, 
        'player_7_con': int, 
        'player_8_con': int,
        'player_1_hi': int, 
        'player_2_hi': int, 
        'player_3_hi': int, 
        'player_4_hi': int, 
        'player_5_hi': int, 
        'player_6_hi': int, 
        'player_7_hi': int, 
        'player_8_hi': int
    }


class Subsession(markets_models.Subsession):

    @property
    def config(self):
        config_addr = Constants.name_in_url + '/configs/' + self.session.config['config_file']
        return ConfigManager(config_addr, self.round_number, Constants.config_fields)  
    def allow_short(self):
        return self.config.allow_short
    def creating_session(self):
        for player in self.get_players():
        ## set the world state for each player equal to the global state
            player.world_state = self.config.state

        if self.round_number > self.config.num_rounds:
            return
        return super().creating_session()

    def grouping(self):
        self.set_player_id()
        self.set_balls_signal(self.config.treat)
        self.make_pairs(self.config.treat, self.config.state)
         ### get totals 
        total_black = self.get_black_balls()
        total_white = self.get_white_balls()
        total_black_low = self.get_black_balls_low()
        total_black_high= self.get_black_balls_high()
        for player in self.get_players():
            player.total_black = total_black
            player.total_white = total_white
            player.total_black_low = total_black_low
            player.total_black_high = total_black_high

    ######################################################################
    ## sets player id based on IQ Ranking
    ##
    ######################################################################
    def set_player_id(self):
        rank = []
        for player in self.get_players():
            #print(player.participant.vars['ranking'])
            #rank.append((player, player.participant.vars['ranking']))
            player.iqranking = player.participant.vars['ranking']
            ### sort by rankinng
            ## set playing id in group useing tupple..
        #print(rank)
    #######################################################################
    ### sets the players signals 
    ### treat, player
    #######################################################################
    def set_balls_signal(self,treat):
            player_bb = self.get_bb_array(treat)
            i=0
            for p in self.get_players():
                print(p.iqranking)
                i=p.iqranking-1
                p.signal1_black = player_bb[i]
                p.signal1_white = 1-p.signal1_black
    #######################################################################
    ### sets the pairs for player and color
    ### treat, player
    #######################################################################
    def make_pairs(self,treat,state):
        player_pairs = self.get_pairs_array()
        random_colors = self.get_random_pp()
        i=0
        for p in self.get_players():
            p.pair = player_pairs[i]
            if treat == 1:  
                if state == 1:
                    if p.iqranking > p.pair:
                        p.hi = 1
                    else:
                        p.hi = 0
                else:
                    if p.iqranking > p.pair:
                        p.hi = 0
                    else:
                        p.hi = 1
            else:
                p.hi = random_colors[i]
            i=i+1
    ######################################################################
    ######################################################################
    def get_random_pp(self):
        return [self.config.player_1_hi,self.config.player_2_hi, self.config.player_3_hi, self.config.player_4_hi, 
                self.config.player_5_hi, self.config.player_6_hi,self.config.player_7_hi, self.config.player_8_hi]
    #######################################################################
    ### get group array
    ### 
    #######################################################################
    def get_pairs_array(self):
        return [self.config.player_1_pair,self.config.player_2_pair, self.config.player_3_pair, self.config.player_4_pair, 
                self.config.player_5_pair, self.config.player_6_pair,self.config.player_7_pair, self.config.player_8_pair]
    #######################################################################
    ### creates an array of player private signals  
    ### 
    #######################################################################
    def get_bb_array(self, treat):
        if treat==1:
            return [self.config.player_1_treat,self.config.player_2_treat, self.config.player_3_treat, self.config.player_4_treat, 
                    self.config.player_5_treat, self.config.player_6_treat,self.config.player_7_treat, self.config.player_8_treat]
        else:
            return [self.config.player_1_con,self.config.player_2_con, self.config.player_3_con, self.config.player_4_con, 
                    self.config.player_5_con, self.config.player_6_con,self.config.player_7_con, self.config.player_8_con]

    #######################################################################
    ### sets all profits players 
    ### player
    #######################################################################
    def set_profits(self):
         for player in self.get_players():
            player.set_profit()
    #######################################################################
    ### sets the payoff for each player and assigns a profit ranking
    ### player
    #######################################################################
    def set_payoffs(self):
        ############
        self.set_profits()
        ##sort profit to get ranking 
        rank = []
        for player in self.get_players():
            rank.append(player)
        rank.sort(reverse = True, key = lambda x: x.profit)
        n=1

        for i in range(len(rank)):
            if i>0 and rank[i].profit == rank[i-1].profit:
                rank[i].pranking = rank[i-1].pranking
            else:
                rank[i].pranking = n
            n=n+1

        for p in self.get_players():
            p.set_total_payoff()
    #######################################################################
    ### retuns the total black and white balls in the systems 
    ### player
    #######################################################################
    def get_black_balls(self):
        total_black =0
        for p in self.get_players():
            total_black = total_black+p.signal1_black
        return total_black

    def get_white_balls(self):
        total_white =0
        for p in self.get_players():
            total_white = total_white+p.signal1_white
        return total_white
    #######################################################################
    ### retuns the total black balls when signal low
    ### player
    #######################################################################
    def get_black_balls_low(self):
        total_black =0
        for p in self.get_players():
            if p.signal_nature==0:
                    total_black = total_black + p.signal1_black
        return total_black
    #######################################################################
    ### retuns the total black balls when signal high
    ### player
    #######################################################################
    def get_black_balls_high(self):
        total_black =0
        for p in self.get_players():
            if p.signal_nature==1:
                    total_black = total_black + p.signal1_black
        return total_black

class Group(markets_models.Group):
    def period_length(self):
        return self.subsession.config.period_length

    def _on_enter_event(self, event):
        '''handle an enter message sent from the frontend
        
        first check to see if the new order would cross your own order, sending an error if it does.
        this isn't a proper check to see whether it would cross your own order, as it only checks the best
        opposite-side order.
        '''

        enter_msg = event.value
        asset_name = enter_msg['asset_name'] if enter_msg['asset_name'] else markets_models.SINGLE_ASSET_NAME

        exchange = self.exchanges.get(asset_name=asset_name)
        if enter_msg['is_bid']:
            best_ask = exchange._get_best_ask()
            if best_ask and best_ask.pcode == enter_msg['pcode'] and enter_msg['price'] >= best_ask.price:
                self._send_error(enter_msg['pcode'], 'Cannot enter a bid that crosses your own ask')
                return
        else:
            best_bid = exchange._get_best_bid()
            if best_bid and best_bid.pcode == enter_msg['pcode'] and enter_msg['price'] <= best_bid.price:
                self._send_error(enter_msg['pcode'], 'Cannot enter an ask that crosses your own bid')
                return
        if enter_msg['price'] >300 or enter_msg['price'] <100:
            return
        
        super()._on_enter_event(event)
        
    def confirm_enter(self, order):
        player = self.get_player(order.pcode)
        player.refresh_from_db()
        exchange = self.exchanges.get()

        if order.is_bid:
            if player.current_bid:
                exchange.cancel_order(player.current_bid.id)
            player.current_bid = order
            player.save()
        else:
            if player.current_ask:
                exchange.cancel_order(player.current_ask.id)
            player.current_ask = order
            player.save()

        super().confirm_enter(order)

    def confirm_trade(self, trade):
        exchange = self.exchanges.get()
        for order in itertools.chain(trade.making_orders.all(), [trade.taking_order]):
            player = self.get_player(order.pcode)
            player.refresh_from_db()

            # if the order from this trade is the current order for that player, update their current order to None.
            # if the order from this trade is NOT the current order for that player, cancel it.
            # the exception to this is if the price on the trade order and current order are the same, we assume the current
            # order is a partially completed order from this trade and don't cancel it
            if order.is_bid and player.current_bid:
                if order.id == player.current_bid.id:
                    player.current_bid = None
                    player.save()
                elif order.price != player.current_bid.price:
                    exchange.cancel_order(player.current_bid.id)

            if not order.is_bid and player.current_ask:
                if order.id == player.current_ask.id:
                    player.current_ask = None
                    player.save()
                elif order.price != player.current_ask.price:
                    exchange.cancel_order(player.current_ask.id)

        super().confirm_trade(trade)
    
    def confirm_cancel(self, order):
        player = self.get_player(order.pcode)
        player.refresh_from_db()
        if order.is_bid:
            player.current_bid = None
        else:
            player.current_ask = None
        player.save()

        super().confirm_cancel(order)
    

class Player(markets_models.Player):

    current_bid = models.ForeignKey(Order, null=True, on_delete=models.CASCADE, related_name="+")
    current_ask = models.ForeignKey(Order, null=True, on_delete=models.CASCADE, related_name="+")

    def check_available(self, is_bid, price, volume, asset_name):
        '''instead of checking available assets, just check settled assets since there can
        only ever be one bid/ask on the market from each player
        '''
        if not is_bid and self.settled_assets[asset_name] < volume:
            return False
        return True
       
    def update_holdings_trade(self, price, volume, is_bid, asset_name):
        if is_bid:
            self.settled_cash -= price * volume

            self.available_assets[asset_name] += volume
            self.settled_assets[asset_name] += volume
        else:
            self.settled_cash += price * volume

            self.available_assets[asset_name] -= volume
            self.settled_assets[asset_name] -= volume

    def asset_endowment(self):
        return self.subsession.config.asset_endowment
    
    def cash_endowment(self):
        return self.subsession.config.cash_endowment

    def update_holdings_available(self, order, removed):
        sign = 1 if removed else -1
        if not order.is_bid:
            self.available_assets[order.exchange.asset_name] += order.volume * sign
            

## Bayes methods
    def BU_low(self, k, m ):
        return (math.pow(0.6,k) + math.pow(.4,m))/((math.pow(.6,k) + math.pow(.4,m)) +(math.pow(.4,k) + math.pow(.6,m)))
    def BU_hi(self, k, m ):
        return (math.pow(0.8,k) + math.pow(.2,m))/((math.pow(.8,k) + math.pow(.2,m)) +(math.pow(.2,k) + math.pow(.8,m)))
    def BU_env_b(self, l, h ):
        return (((math.pow(0.6,l) * math.pow(.4,8-l))*(math.pow(.8,h)*math.pow(.2,8-h)))/(((math.pow(.6,l)*math.pow(.4,8-l)*math.pow(.8,h)*math.pow(.2,8-h)) +(math.pow(.4,l)*math.pow(.6,8-l)*math.pow(.2,h)*math.pow(.8,8-h)))))
## defined Variables 
    pranking = models.IntegerField()
    iqranking = models.IntegerField()
    profit = models.IntegerField()
    total_payoff = models.IntegerField()
    payment_signal1 = models.IntegerField()
    world_state = models.IntegerField()
    signal1_black = models.IntegerField()
    signal1_white = models.IntegerField()
    signal_nature = models.IntegerField()
    total_black = models.IntegerField()
    total_white = models.IntegerField()
    Question_1_pre_int_ns = models.IntegerField()
    Question_1_pre_int_s = models.IntegerField()
    Question_1_post_int = models.IntegerField()
    total_black_low = models.IntegerField()
    total_black_high = models.IntegerField()
    Question_1_payoff_pre_ns = models.IntegerField(initial=0)
    Question_2_payoff_pre_ns = models.IntegerField(initial=0)
    Question_3_payoff_pre_ns = models.IntegerField(initial=0)
    Question_1_payoff_pre_s = models.IntegerField(initial=0)
    Question_2_payoff_pre_s = models.IntegerField(initial=0)
    Question_3_payoff_pre_s = models.IntegerField(initial=0)
    Question_1_payoff_post = models.IntegerField(initial=0)
    Question_2_payoff_post = models.IntegerField(initial=0)
    Question_3_payoff_post = models.IntegerField(initial=0)
    survey_avg_pay = models.IntegerField()
    profit = models.IntegerField()
    asset_value = models.IntegerField()
    payoff_from_trading = models.IntegerField()
    shares = models.IntegerField()
    average_payoff = models.IntegerField()
    hi = models.IntegerField()
    color = models.IntegerField()
    pair = models.IntegerField()
## Questions Pre
    Question_1_pre_ns = models.StringField(
        label='''
        Your answer:'''
    )
    Question_1_pre_s = models.StringField(
        label='''
        Your answer:'''
    )
    Question_1_post = models.StringField(
        label='''
        Your answer:'''
    )
    Question_2_pre_ns = models.IntegerField(min=100, max=300,
        label='''
        Enter a number between 100 and 300.'''
    )
    Question_2_pre_s = models.IntegerField(min=100, max=300,
        label='''
        Enter a number between 100 and 300.'''
    )
    Question_2_post = models.IntegerField(min=100, max=300,
        label='''
        Enter a number between 100 and 300.'''
    )
    Question_3_pre_ns = models.IntegerField(
        choices=[1,2,3,4,5,6,7,8],
        label='''
         Please choose one of the following.
        '''
    )
    Question_3_pre_s = models.IntegerField(
        choices=[1,2,3,4,5,6,7,8],
        label='''
         Please choose one of the following.
        '''
    )
    Question_3_post = models.IntegerField(
        choices=[1,2,3,4,5,6,7,8],
        label='''
         Please choose one of the following.
        '''
    )
    #######################################################################
    ### sets the proft for an indivdual player 
    #######################################################################
    def set_profit(self):
        self.shares = self.settled_assets['A']
        old_asset_value = 0
        if self.world_state==1:
            self.asset_value = self.shares*300
            self.profit = self.asset_value + self.settled_cash
             ## bad state
        else:
            self.asset_value = self.shares*100
            self.profit =  self.asset_value + self.settled_cash
    #######################################################################
    ### sets the proft for an indivdual player 
    #######################################################################
    def get_profit(self):
        return self.profit
    #######################################################################
    ### calculates payoff
    #######################################################################
    def set_total_payoff(self):
        ###################question 1 post#####################################
        p_n_pre = random.randint(0,99)
        n_asset_binomail_pre = np.random.binomial(1, p_n_pre/100)
        n_asset_value_pre = n_asset_binomail_pre*200 +100
        #######################################################################
        p_n_post = random.randint(0,99)
        n_asset_binomail_post = np.random.binomial(1, p_n_post/100)
        n_asset_value_post = n_asset_binomail_post*200 +100
         ################question 1 post#########################################
        try:
            self.Question_1_post_int = int(self.Question_1_post)
        except ValueError: 
            self.Question_1_post_int = -2

        if self.Question_1_post_int > 100:
            self.Question_1_payoff_post = 0
        elif self.Question_1_post_int < 0:
            self.Question_1_payoff_post = 0

        elif self.Question_1_post_int>p_n_post:
            self.Question_1_payoff_post = self.world_state*200 +100
        else:
            self.Question_1_payoff_post = n_asset_value_post

        ################question 1 pre#########################################
        try:
            self.Question_1_pre_int_ns = int(self.Question_1_pre_ns)
        except ValueError: 
            self.Question_1_pre_int_ns = -2

        if self.Question_1_pre_int_ns > 100:
            self.Question_1_payoff_post = 0
        elif self.Question_1_pre_int_ns < 0:
            self.Question_1_payoff_post = 0

        if self.Question_1_pre_int_ns>p_n_pre:
            self.Question_1_payoff_pre_ns = self.world_state*200 +100
        else:
            self.Question_1_payoff_pre_ns = n_asset_value_pre
        try:
            self.Question_1_pre_int_s = int(self.Question_1_pre_s)
        except ValueError: 
            self.Question_1_pre_int_s = -2

        if self.Question_1_pre_int_s > 100:
            self.Question_1_payoff_post = 0
        elif self.Question_1_pre_int_s < 0:
            self.Question_1_payoff_post = 0

        if self.Question_1_pre_int_s>p_n_pre:
            self.Question_1_payoff_pre_s = self.world_state*200 +100
        else:
            self.Question_1_payoff_pre_s = n_asset_value_pre
        ################### ### question 2 post###################################
        p_n = random.randint(100,300)
        if self.Question_2_post>p_n:
            self.Question_2_payoff_post = self.world_state*200 +100
        else:
            self.Question_2_payoff_post = p_n
        ################### ### question 2 pre###################################
        p_n = random.randint(100,300)
        if self.Question_2_pre_s>p_n:
            self.Question_2_payoff_pre_s = self.world_state*200 +100
        else:
            self.Question_2_payoff_pre_s = p_n

        p_n = random.randint(100,300)
        if self.Question_2_pre_ns>p_n:
            self.Question_2_payoff_pre_ns = self.world_state*200 +100
        else:
            self.Question_2_payoff_pre_ns = p_n
        ################### ### question 3 pre###################################
        ##C correct profit ranking
        C = self.pranking
        ##R is the reported belief
        R = self.Question_3_pre_ns
        self.Question_3_payoff_pre_ns= (int) (100 - (math.pow((C - R),2)))

        R = self.Question_3_pre_s
        self.Question_3_payoff_pre_s= (int) (100 - (math.pow((C - R),2)))
        ################### ### question 3 post###################################
        ##C correct profit ranking
        C = self.pranking
        ##R is the reported belief
        R = self.Question_3_post
        self.Question_3_payoff_post= (int) (100 - (math.pow((C - R),2)))
        ### set to zero if did not answer survye questions
        if self.Question_1_pre_ns==-1:
            self.Question_1_payoff_pre_ns = 0
        if self.Question_1_pre_s==-1:
            self.Question_1_payoff_pre_s = 0
        if self.Question_1_post==-1:
            self.Question_1_payoff_post = 0
        if self.Question_2_pre_ns==-1:
            self.Question_2_payoff_pre_ns = 0
        if self.Question_2_pre_s==-1:
            self.Question_2_payoff_pre_s = 0
        if self.Question_2_post==-1:
            self.Question_2_payoff_post = 0
        if self.Question_3_pre_ns==-1:
            self.Question_3_payoff_pre_ns= 0
        if self.Question_3_pre_s==-1:
            self.Question_3_payoff_pre_s = 0
        if self.Question_3_post==-1:
            self.Question_3_payoff_post = 0
        ## set total payoff ###############################
        self.payoff_from_trading = self.profit

        self.survey_avg_pay  = (int)((self.Question_1_payoff_pre_s+self.Question_1_payoff_pre_ns + self.Question_2_payoff_pre_s + 
            self.Question_2_payoff_pre_ns+  self.Question_3_payoff_pre_s + self.Question_3_payoff_pre_ns + self.Question_1_payoff_post+
            self.Question_2_payoff_post+ self.Question_3_payoff_post)/9) 
        
        self.total_payoff = self.survey_avg_pay + self.payoff_from_trading

        ## sets payoff to best payoff per round 
        conversion_rate = .0017
        if self.subsession.round_number > 2:
                self.payoff = self.payoff + (self.total_payoff * conversion_rate)