import numpy as np


class Board:
    def __init__(self, dimX, dimY, cell_features,  alpha=0, beta=0, gamma=0, init_random=True,):
        # cell features should be a list of tuples
        self.dimX = dimX
        self.dimY = dimY
        self.alpha = alpha
        self.beta = beta
        self.gamma = gamma
        self.cell_features = cell_features
        self.cells = np.empty((dimX, dimY), np.dtype(self.cell_features))
        self.history = []

        if init_random:
            self.initialize_cells()

    def initialize_cells(self):

        for x in range(self.dimX):
            for y in range(self.dimY):
                self.cells[x, y]["H"] = np.random.choice([0, 1])
                self.cells[x, y]["PP"] = np.random.choice([0, 1, 2])
                self.cells[x, y]["D"] = np.random.choice([0, 1, 2, 3])
                self.cells[x, y]["VS"] = round(np.random.uniform(0.0, 1.0), 2)

            
    def set_cell_feature(self, x, y, feature, value):
        self.cells[x, y][feature] = value

    def get_cell(self, x, y):
        return self.cells[x, y]

    def get_cells_feature(self, feature, history_index = None):
        print(history_index)
        if(history_index is None):
            return self.cells[:,:][feature]
        else:
            return self.history[history_index][:,:][feature]

    def get_cells(x, y):
        return self.cells

    def update(self):
        self.history.append(np.copy(self.cells))
        new_cells = np.empty((self.dimX, self.dimY),  dtype=self.cell_features) 
        for x in range(self.dimX):
            for y in range(self.dimY):
                cell = self.cells[x, y]
                neighborhood = self.get_neighborhood(x, y) 
                new_state = self.property_price_update(cell, neighborhood)
                new_state = self.desirability_update(new_state, neighborhood)
                new_state = self.vacancy_update(new_state, neighborhood)
                new_cells[x, y] = new_state
                
        self.cells = new_cells

    def property_price_update(self, cell, neighborhood):
        income = cell["H"]
        property_price = cell["PP"]
        desirability = cell["D"]

        # Income factor based on income level
        income_factor = 0.3 if income == 1 else 0
        new_property_price = int(property_price * (1 + self.alpha * (income_factor + self.beta * desirability)))
        new_property_price = max(1, new_property_price)  # Ensure a minimum property price
        
        new_cell = cell.copy()
        new_cell["PP"] = new_property_price
        return new_cell

    def desirability_update(self, cell, neighborhood):
        new_cell = cell.copy()
        property_price = cell["PP"]
        desirability = cell["D"]

        masked_pp = np.where(neighborhood["VS"] < 1, neighborhood["PP"], 0)
        if np.count_nonzero(masked_pp) > 0:
            avg_nearby_price = np.mean(masked_pp)
        else:
            avg_nearby_price = 0.5  # Default small value

        if property_price > 0:
            new_desirability = desirability + self.gamma * ((avg_nearby_price / (property_price + 1)) - 1)
            new_desirability = min(max(new_desirability, 0), 3.5)  # Allow slight overflows
        else:
            new_desirability = desirability

        new_cell["D"] = new_desirability
        return new_cell


    def vacancy_update(self, cell, neighborhood):
        income = cell['H']
        property_price = cell['PP']
        desirability = cell['D']
        vacancy_status = cell['VS']

        # Change income based on desirability and property price
        if vacancy_status == 0 and desirability >= 2 and property_price >= 1:
            income = 1  # Attract higher income households
        elif vacancy_status == 0 and desirability < 1:
            income = 0  # Lower desirability leads to lower income

        # Update vacancy status
        if income == 0 and property_price > 2:  # Example threshold
            new_vacancy_status = 1
        else:
            new_vacancy_status = 0

        new_cell = cell.copy()
        new_cell['H'] = income
        new_cell['VS'] = new_vacancy_status
        return new_cell


        

    def get_neighborhood(self, x, y):
        return self.cells[max(0, x - 1):min(self.dimX, x + 2), max(0,y-1):min(self.dimY, y + 2)]

    def terminate(self):
        self.history.append(np.copy(self.cells))
