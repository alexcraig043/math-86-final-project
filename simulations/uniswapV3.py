import numpy as np
import matplotlib.pyplot as plt

## In a liquidity position (x,y), x is amount of USDC, y is amount of ETH

class UniswapV3:
    def __init__(self, fee_rate, current_price):
        self.fee_rate = fee_rate # assumes a constant fee rate
        self.price = current_price
        self.liquidity_positions = {}

        self.ticks = []
        self.intervals = []
        # initialize ticks between 0 and approx 4700
        for i in range(1500):
            self.ticks.append(1.01**i)

    def instantiate_initial_liquidity_distribution(self, total_liquidity):
        ## for each tick, start with a certain amount of liquidity
        for i in range(len(self.ticks)-1):
            interval = (self.ticks[i], self.ticks[i+1])
            self.intervals.append(interval)
            self.liquidity_positions[interval] = [0,0,0] # stands for token 1, 2, and total volume in thus position
        center = self.match_position(self.price)

        ## Assign Liquidity
        self.liquidity_positions[self.intervals[center]][2] = total_liquidity/2
        for j in range(center+1, len(self.intervals)):
           self.liquidity_positions[self.intervals[j]][2] = self.liquidity_positions[self.intervals[j-1]][2]/4
           self.liquidity_positions[self.intervals[j]][0] = 0.5*self.liquidity_positions[self.intervals[j]][2]
           self.liquidity_positions[self.intervals[j]][1] = 0.5*self.liquidity_positions[self.intervals[j]][2]/self.intervals[j][0]
        
        for j in range(center-1, -1, -1):
            self.liquidity_positions[self.intervals[j]][2] = self.liquidity_positions[self.intervals[j+1]][2]/4
            self.liquidity_positions[self.intervals[j]][0] = 0.5*self.liquidity_positions[self.intervals[j]][2]
            self.liquidity_positions[self.intervals[j]][1] = 0.5*self.liquidity_positions[self.intervals[j]][2]/self.intervals[j][0]
    
    def swap(self, token_from, amount):
        # Assumes there is enough liquidity for current range
        # Simplified swap logic, not accounting for slippage or price impact
        current_interval = self.match_position(self.price)
        if token_from == "USDC":
            ## in this case, amount of y increases
            root_price = np.sqrt(self.price)
            delta_root_price = amount/self.liquidity_positions[self.intervals[current_interval]][2]
            self.price += delta_root_price**2
            if self.price > self.intervals[current_interval][1]:
                delta_x = self.liquidity_positions[self.intervals[current_interval]][2]/root_price
                delta_y = self.liquidity_positions[self.intervals[current_interval]][2]*root_price
                self.liquidity_positions[self.intervals[current_interval]][0] += delta_x
                self.liquidity_positions[self.intervals[current_interval]][1] += delta_y
            else:
                print("Not enough liquidity in current space, we move to another tick interval")
                proper_tick = self.match_position(self.price)
                delta_x = self.liquidity_positions[self.intervals[proper_tick]][2]/root_price
                delta_y = self.liquidity_positions[self.intervals[proper_tick]][2]*root_price
                self.liquidity_positions[self.intervals[proper_tick]][0] += delta_x
                self.liquidity_positions[self.intervals[proper_tick]][1] += delta_y
            fee = amount*self.fee_rate
            effective_amount = amount-fee
            swapped_to = effective_amount/self.price
            print(f"You have swapped for {swapped_to} ETHs, at the price of {self.price}")
            return delta_y, self.price
    
    # ---------------------------- HELPERS -----------------------------------
    def match_position(self, price):
        for i in range(len(self.intervals)-1):
            if self.intervals[i][0] <= price <= self.intervals[i+1][1]:
                return i
        return -1


## As of March 3rd, Uniswap has a TVL of 3.2b
## Assuming it follows a normal distribution
## As for now, price of ETH is 3478.16, say it is 3478
## It is in between tick 819 and tick 820
## Since we initialized to have 851 intervals, gets progressives more as it goes to interval (819,820)
    ## Suppose the current interval is most likely for liquid providers to put money in
    ## Let it be 1/2 of total pool, next interval be (1/2)^(2+1), summing both side, we get 1
    ## Suppose it goes to infinity and range becomes (0,+infty)

test = UniswapV3(0.0003, 3478)
test.instantiate_initial_liquidity_distribution(3.2*10**9)
test.swap("USDC", 100000)


    # def add_liquidity(self, lower_price, upper_price, amount):
    #     # Unique ID for the NFT representing the position
    #     position_id = len(self.liquidity_positions) + 1
    #     self.liquidity_positions[position_id] = {
    #         'lower_price': lower_price,
    #         'upper_price': upper_price,
    #         'amount': amount
    #     }
    #     return position_id

    # do we actually need this part?
    # def remove_liquidity(self, position_id):
    #     if position_id in self.liquidity_positions:
    #         removed_liquidity = self.liquidity_positions[position_id]['amount']
    #         del self.liquidity_positions[position_id]
    #         self.total_liquidity -= removed_liquidity
    #         return removed_liquidity
    #     else:
    #         return 0


