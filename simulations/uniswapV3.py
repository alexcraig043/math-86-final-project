class UniswapV3:
    def __init__(self, fee_rate):
        self.liquidity_positions = {}
        self.fee_rate = fee_rate
        self.total_liquidity = 0
        self.price = 1  # Assume initial price of 1 for simplicity

    def add_liquidity(self, lower_price, upper_price, amount, owner_id):
        # Unique ID for the NFT representing the position
        position_id = len(self.liquidity_positions) + 1
        self.liquidity_positions[position_id] = {
            'lower_price': lower_price,
            'upper_price': upper_price,
            'amount': amount,
            'owner_id': owner_id
        }
        self.total_liquidity += amount  # Simplified liquidity tracking
        return position_id

    def remove_liquidity(self, position_id):
        if position_id in self.liquidity_positions:
            removed_liquidity = self.liquidity_positions[position_id]['amount']
            del self.liquidity_positions[position_id]
            self.total_liquidity -= removed_liquidity
            return removed_liquidity
        else:
            return 0

    def swap(self, is_buy, amount):
        # Simplified swap logic, not accounting for slippage or price impact
        fee = amount * self.fee_rate
        effective_amount = amount - fee
        if is_buy:
            # Simplify: assume price increases by a fixed rate per unit bought
            self.price += effective_amount * 0.001
        else:
            # Simplify: assume price decreases by a fixed rate per unit sold
            self.price -= effective_amount * 0.001
        return effective_amount, self.price

# Example usage
pool = UniswapV3(0.003)  # 0.3% fee rate
position_id = pool.add_liquidity(0.9, 1.1, 1000, 'LP1')
print(f"Added liquidity with position ID: {position_id}")
removed_liquidity = pool.remove_liquidity(position_id)
print(f"Removed liquidity: {removed_liquidity}")
swap_amount, new_price = pool.swap(True, 500)
print(f"Swapped 500 tokens. Effective amount: {swap_amount}, New price: {new_price}")
