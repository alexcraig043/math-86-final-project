class Balancer:
    def __init__(self, initial_tokens, initial_weights, initial_balances):
        """
        Initialize a Balancer pool with multiple tokens.
        :param initial_tokens: List of tokens in the pool.
        :param initial_weights: Corresponding weights of the tokens.
        :param initial_balances: Initial balance of each token.
        """
        self.tokens = initial_tokens
        self.weights = {
            token: weight for token, weight in zip(initial_tokens, initial_weights)
        }
        self.balances = {
            token: balance for token, balance in zip(initial_tokens, initial_balances)
        }
        self.total_weight = sum(initial_weights)

    def swap(self, token_in, token_out, amount_in):
        """
        Simulate a token swap in the pool.
        :param token_in: Token being swapped in.
        :param token_out: Token being swapped out.
        :param amount_in: Amount of token_in being swapped.
        :return: Amount of token_out received.
        """
        # Simplified swap logic, ignoring fees and slippage for demonstration.
        weight_in = self.weights[token_in]
        weight_out = self.weights[token_out]
        balance_in = self.balances[token_in] + amount_in
        balance_out = self.balances[token_out]

        # Balancer's formula to determine amount out, simplified for illustration
        amount_out = (balance_out * amount_in * weight_in) / (balance_in * weight_out)

        # Update balances
        self.balances[token_in] = balance_in
        self.balances[token_out] -= amount_out

        return amount_out

    def add_liquidity(self, token, amount):
        """
        Add liquidity to the pool for a specific token.
        :param token: Token for which liquidity is added.
        :param amount: Amount of token added.
        """
        if token in self.balances:
            self.balances[token] += amount
        else:
            print("Token not in pool.")

    def remove_liquidity(self, token, amount):
        """
        Remove liquidity from the pool for a specific token.
        :param token: Token for which liquidity is removed.
        :param amount: Amount of token removed.
        """
        if token in self.balances and self.balances[token] >= amount:
            self.balances[token] -= amount
        else:
            print("Insufficient balance or token not in pool.")
