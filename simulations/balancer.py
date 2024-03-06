class Balancer:
    def __init__(self, x, y, weight_x, weight_y):
        self.x = x  # Quantity of asset x
        self.y = y  # Quantity of asset y
        self.weight_x = weight_x  # Weight of asset x
        self.weight_y = weight_y  # Weight of asset y

    def swap_x_for_y(self, delta_x):
        """
        Swap x for y using the Balancer AMM model.

        :param delta_x: Amount of x being swapped.
        :return: The amount of y received in the swap.
        """
        # Calculate new balance of x after adding delta_x
        new_x = self.x + delta_x
        # Calculate the invariant before the swap
        invariant_before = (self.x**self.weight_x) * (self.y**self.weight_y)
        # Calculate the new balance of y to maintain the invariant
        new_y = (invariant_before / (new_x**self.weight_x)) ** (1 / self.weight_y)
        # Calculate delta_y
        delta_y = self.y - new_y
        # Update balances
        self.x = new_x
        self.y = new_y
        return delta_y

    def swap_y_for_x(self, delta_y):
        """
        Swap y for x using the Balancer AMM model.

        :param delta_y: Amount of y being swapped.
        :return: The amount of x received in the swap.
        """
        # Calculate new balance of y after adding delta_y
        new_y = self.y + delta_y
        # Calculate the invariant before the swap
        invariant_before = (self.x**self.weight_x) * (self.y**self.weight_y)
        # Calculate the new balance of x to maintain the invariant
        new_x = (invariant_before / (new_y**self.weight_y)) ** (1 / self.weight_x)
        # Calculate delta_x
        delta_x = self.x - new_x
        # Update balances
        self.x = new_x
        self.y = new_y
        return delta_x
