from math import exp, log


class Catalyst:
    def __init__(self, asset_balances, weights):
        """
        Initializes the Catalyst AMM with given asset balances and weights.
        :param asset_balances: A dictionary mapping asset symbols to their initial balances.
        :param weights: A dictionary mapping asset symbols to their weights in the pool.
        """
        self.asset_balances = asset_balances
        self.weights = weights

    def _calculate_units(self, delta, asset):
        """
        Calculates the units for a given delta of an asset.
        """
        weight = self.weights[asset]
        balance = self.asset_balances[asset]
        units = weight * log(balance + delta / balance)
        return units

    def swap(self, delta_alpha, alpha, beta):
        """
        Performs a swap from asset alpha to asset beta.
        """
        units = self._calculate_units(delta_alpha, alpha)
        weight_beta = self.weights[beta]
        balance_beta = self.asset_balances[beta]
        delta_beta = balance_beta * (1 - exp(-units / weight_beta))

        # Update balances
        self.asset_balances[alpha] += delta_alpha
        self.asset_balances[beta] -= delta_beta

        return delta_beta

    def get_balances(self):
        """
        Returns the current balances of all assets in the pool.
        """
        return self.asset_balances
