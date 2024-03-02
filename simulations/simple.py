class Simple:
    def __init__(self, x, y):
        self.x = x  # Quantity of asset x
        self.y = y  # Quantity of asset y
        self.k = x * y  # Constant product

    def add_liquidity(self, delta_x, delta_y):
        """
        Add liquidity to the pool.

        :param delta_x: Amount of x added to the pool.
        :param delta_y: Amount of y added to the pool.
        """
        self.x += delta_x
        self.y += delta_y
        self.k = self.x * self.y  # Recalculate constant product

    def remove_liquidity(self, delta_x, delta_y):
        """
        Remove liquidity from the pool.

        :param delta_x: Amount of x removed from the pool.
        :param delta_y: Amount of y removed from the pool.
        """
        if delta_x <= self.x and delta_y <= self.y:
            self.x -= delta_x
            self.y -= delta_y
            self.k = self.x * self.y  # Recalculate constant product
        else:
            print("Cannot remove more liquidity than available")

    def swap_x_for_y(self, delta_x):
        """
        Swap x for y using the AMM model.

        :param delta_x: Amount of x being swapped.
        :return: The amount of y received in the swap.
        """
        new_x = self.x + delta_x
        new_y = self.k / new_x
        delta_y = self.y - new_y
        self.x = new_x
        self.y = new_y
        return delta_y

    def swap_y_for_x(self, delta_y):
        """
        Swap y for x using the AMM model.

        :param delta_y: Amount of y being swapped.
        :return: The amount of x received in the swap.
        """
        new_y = self.y + delta_y
        new_x = self.k / new_y
        delta_x = self.x - new_x
        self.x = new_x
        self.y = new_y
        return delta_x
