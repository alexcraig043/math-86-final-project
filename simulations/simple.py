class Simple:
    def __init__(self, x, y, x_val=1, y_val=1):
        self.x = x  # Quantity of asset x
        self.y = y  # Quantity of asset y
        self.x_val = x_val  # Value of one unit of x in USD
        self.y_val = y_val  # Value of one unit of y in USD
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

    def set_x_val(self, new_x_val):
        """
        Set the USD value of one unit of x.

        :param new_x_val: New value of one unit of x in USD.
        """
        self.x_val = new_x_val

    def set_y_val(self, new_y_val):
        """
        Set the USD value of one unit of y.

        :param new_y_val: New value of one unit of y in USD.
        """
        self.y_val = new_y_val

    def get_x_value_in_usd(self):
        """
        Calculate the total USD value of x in the pool.

        :return: The total value of x in USD.
        """
        return self.x * self.x_val

    def get_y_value_in_usd(self):
        """
        Calculate the total USD value of y in the pool.

        :return: The total value of y in USD.
        """
        return self.y * self.y_val
