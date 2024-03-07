import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

## In a liquidity position (x,y), x is amount of ETH, y is amount of USDC

class UniswapV3:
    def __init__(self, fee_rate, low_mean = 3400, high_mean = 4000, num_lp = 3200, vl_per_lp = 100000):
        self.fee_rate = fee_rate # assumes a constant fee rate
        self.liquidity_positions = {}

        self.ticks = []
        self.intervals = []
        # initialize ticks between 0 and approx 4700
        for i in range(10000):
            self.ticks.append(1.001**i)

        self.instantiate_initial_liquidity_distribution(low_mean, high_mean, num_lp, vl_per_lp)
    
    def instantiate_initial_liquidity_distribution(self, low_mean, high_mean, num_lp, vl_per_lp):
        ## for each tick, start with a certain amount of liquidity
        for i in range(len(self.ticks)-1):
            interval = (self.ticks[i], self.ticks[i+1])
            self.intervals.append(interval)
            self.liquidity_positions[interval] = [0,0,0] # stands for token x, y, and L in this interval

        self.generate_distribution(low_mean, high_mean, num_lp, vl_per_lp)
        for interval in self.intervals:
            vl = self.liquidity_positions[interval][2]
            self.liquidity_positions[interval][0] = 0.5*vl/interval[0]
            self.liquidity_positions[interval][1] = 0.5*vl
            self.liquidity_positions[interval][2] = self.liquidity_positions[interval][0]*self.liquidity_positions[interval][1]


    def swap_y_for_x(self, amount, current_price = 3800):
        #determining which pool to use based on the current price
        current_interval = self.match_position(current_price)
        price = self.intervals[current_interval][0]  # x to y swap ratio
        # print(f"current price of x to y is {price}")

        # calculate price change if we do it within the current interval
        delta_y = (1-self.fee_rate)*amount  # y_in
        delta_root_price = delta_y/self.liquidity_positions[self.intervals[current_interval]][2]
        if price + delta_root_price**2 < self.intervals[current_interval][1]:
            ## swapping within a tick, only root_p changes, L is constant
            x_end = self.liquidity_positions[self.intervals[current_interval]][2]/(self.liquidity_positions[self.intervals[current_interval]][1]+delta_y)
            delta_x = self.liquidity_positions[self.intervals[current_interval]][0] - x_end
            self.liquidity_positions[self.intervals[current_interval]][0] += delta_x
            self.liquidity_positions[self.intervals[current_interval]][1] += delta_y
            # print(f"You have swapped for {delta_x} token x, at the price of {price}, the change of price is {delta_root_price**2}")
            return (delta_x, delta_root_price**2)
        else:
            # print("Not enough liquidity in current space, we move to another tick interval")
            proper_tick = self.match_position(price + delta_root_price**2)
            # print(self.liquidity_positions[self.intervals[proper_tick]])
            new_price = self.intervals[proper_tick][0]
            x_end = self.liquidity_positions[self.intervals[proper_tick]][2]/(self.liquidity_positions[self.intervals[proper_tick]][1]+delta_y)
            delta_x = self.liquidity_positions[self.intervals[proper_tick]][0] - x_end
            self.liquidity_positions[self.intervals[proper_tick]][0] += delta_x
            self.liquidity_positions[self.intervals[proper_tick]][1] += delta_y
            # print(f"You have swapped for {delta_x} token x, at the price of {new_price}, the change of price is {new_price-price}")
            return (delta_x, new_price-price)
        
    def swap_x_for_y(self, amount, current_price = 3800):
        #determining which pool to use based on the current price
        current_interval = self.match_position(current_price)
        price = 1/self.intervals[current_interval][0]  # x to y swap ratio
        # print(f"current price of y to x is {price}")

        # calculate price change if we do it within the current interval
        delta_x = (1-self.fee_rate)*amount  # x_in
        delta_root_price = delta_x/self.liquidity_positions[self.intervals[current_interval]][2]
        if price + (delta_root_price)**2 > 1/self.intervals[current_interval][1]:
            ## swapping within a tick, only root_p changes, L is constant
            y_end = self.liquidity_positions[self.intervals[current_interval]][2]/(self.liquidity_positions[self.intervals[current_interval]][0]+delta_x)
            delta_y = self.liquidity_positions[self.intervals[current_interval]][1] - y_end
            self.liquidity_positions[self.intervals[current_interval]][0] += delta_x
            self.liquidity_positions[self.intervals[current_interval]][1] += delta_y
            # print(f"You have swapped for {delta_y} token y, at the price of {price}, the change of price is {(delta_root_price)**2}")
            return delta_y, (delta_root_price)**2
        else:
            # print("Not enough liquidity in current space, we move to another tick interval")
            proper_tick = self.match_position(price + delta_root_price**2)
            # print(self.liquidity_positions[self.intervals[proper_tick]])
            new_price = self.intervals[proper_tick][0]
            x_end = self.liquidity_positions[self.intervals[proper_tick]][2]/(self.liquidity_positions[self.intervals[proper_tick]][1]+delta_y)
            delta_x = self.liquidity_positions[self.intervals[proper_tick]][0] - x_end
            self.liquidity_positions[self.intervals[proper_tick]][0] += delta_x
            self.liquidity_positions[self.intervals[proper_tick]][1] += delta_y
            # print(f"You have swapped for {delta_y} token y, at the price of {new_price}, the change of price is {new_price-price}")
            return delta_y, new_price-price
    
    # ---------------------------- HELPERS -----------------------------------
    def match_position(self, price):
        for i in range(len(self.intervals)-1):
            if self.intervals[i][0] <= price <= self.intervals[i+1][1]:
                return i
        return -1
    
    def match_2_position(self, a, b):
        rl = [-1, -1]
        for i in range(len(self.intervals)-1):
            if self.intervals[i][0] <= a <= self.intervals[i+1][1]:
                rl[0] = i
            elif self.intervals[i][0] <= b <= self.intervals[i+1][1]:
                rl[1] = i
                break
        return rl[0], rl[1]
    
    def generate_distribution(self, low_mean, high_mean, num_lp, vl_per_lp):
        # arbitrary assumption
        # intuition: aggregating LPs

        ## Set each LP to provide liquidity on a interval [a,b]
        ## let a be 2-week low, max be 2-week high, and a b are points on normal distribiutions centering at a and b
        ## Choose a 5% std for each normal distribution
        for i in range(num_lp):
            low = 1
            high = 0
            # make sure after the loop, low <= high
            while low > high:
                # choose a
                low = np.random.normal(loc=low_mean, scale=low_mean*0.05)
                # choose b
                high = np.random.normal(loc=high_mean, scale=high_mean*0.05)

            # map to ticks
            low_tick, high_tick = self.match_2_position(low, high)
            for j in range(low_tick, high_tick+1):
                self.liquidity_positions[self.intervals[j]][2] += vl_per_lp



## As of March 3rd, Uniswap has a TVL of 3.2b
## Assuming it follows a normal distribution
## As for now, price of ETH is 3478.16, say it is 3478
## It is in between tick 819 and tick 820
## Since we initialized to have 851 intervals, gets progressives more as it goes to interval (819,820)
    ## Suppose the current interval is most likely for liquid providers to put money in
    ## Let it be 1/2 of total pool, next interval be (1/2)^(2+1), summing both side, we get 1
    ## Suppose it goes to infinity and range becomes (0,+infty)

# test = UniswapV3(0.0003)
# test.swap_y_for_x(10000)[1]
# test.swap_x_for_y(20)