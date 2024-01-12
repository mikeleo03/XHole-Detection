import math

class Cost_Calculation:
    '''
    Class Cost_Calculation, calculating the cost of drilling and blasting values
    '''
    def __init__(self, rock_volume, explosive_mass, daily_target, coloumn_charge):
        '''
            Initiate needed variables
            params:
                rock_volume = Volume batuan yang diledakkan per lubang ledak, m^3
                explosive_mass =  Massa bahan peledak per lubang ledak, kg
                daily_target = target volume batuan harian yang diledakkan, m^3
        '''
        self.rock_volume = rock_volume
        self.explosive_mass = explosive_mass
        self.daily_target = daily_target
        self.coloumn_charge = coloumn_charge

    def __calculate_powder_factor(self):
        '''
            Calculate the powder factor
            params:
                rock_volume = Volume batuan yang diledakkan per lubang ledak, m^3
                explosive_mass =  Massa bahan peledak per lubang ledak, kg
        '''
        self.powder_factor = self.explosive_mass / self.rock_volume

    def __calculate_holes_number(self):
        '''
            Calculate the number of holes
            params:
                daily target = Jumlah volume batuan yang diledakkan per hari, m^3
                rock_volume = Volume batuan yang diledakkan per lubang ledak, m^3
        '''
        self.holes_number = self.daily_target / self.rock_volume

    def __calculate_drilling_cost(self):
        '''
            Calculate the number of holes
            params:
                holes_number = Jumlah lubang ledak sekali peledakan (dianggap peledakan sehari sekali), m^3
                coloumn_charge = tinggi lubang yang terisi bahan peledak per lubang, m^3
        '''
        self.drilling_cost = self.holes_number * self.coloumn_charge * 50059  # 500059 adalah cost per meter drilling

    def __calculate_blasting_cost(self):
        '''
            Calculate the number of holes
            params:
                holes_number = Jumlah lubang ledak sekali peledakan (dianggap peledakan sehari sekali), m^3
                coloumn_charge = tinggi lubang yang terisi bahan peledak per lubang, m^3
        '''
        self.blasting_cost = self.rock_volume * 18253   # 18253 adalah cost per m^3 batuan yang diledakkan
    
    def run(self):
        '''
            Run the cost calculation
        '''
        # Calculate the parameters
        self.__calculate_powder_factor()
        self.__calculate_holes_number()
        self.__calculate_drilling_cost()
        self.__calculate_blasting_cost()

        # Calculate cost
        cost = self.drilling_cost + self.blasting_cost
        
        # Return the value
        return round(cost, 3)
    