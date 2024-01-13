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
        
    def get_powder_factor(self):
        '''
            Getter of powder factor
        '''
        return self.powder_factor
    
    def get_holes_number(self):
        '''
            Getter of holes number
        '''
        return self.holes_number 

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

    def get_rock_breaker_time(self):
        '''
            Getter of rock breaker time
        '''
        return self.rock_breaker_time  

    def __calculate_rock_breaker_time(self):
        '''
            Calculate the rock breaker time
            params:
                daily target = Jumlah volume batuan yang diledakkan per hari, m^3
        '''
        self.rock_breaker_time = self.daily_target * 0.8 / 5    # Caterpillar 320D2: 582 joules per blow, significantly higher than the JCB 3DX, translates to a potential breaking capacity of 2 - 5 cubic meters per hour under ideal conditions.

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
            Calculate the blasting cost
            params:
                rock_volume = Volume batuan yang diledakkan per lubang ledak, m^3
        '''
        self.blasting_cost = self.rock_volume * 18253   # 18253 adalah cost per m^3 batuan yang diledakkan
    
    def __calculate_rock_breaker_cost(self):
        '''
            Calculate the rock breaker cost
            params:
                rock_breaker_time = Waktu yang dibutuhkan untuk Rrock breaker menghancurkan batuan dari fragmentasi batuan yang melebihi Kuz Ram Fragmentation (jam)
        '''
        self.rock_breaker_cost = self.rock_breaker_time * 4000000   # Based on these factors, the rental rate for a Caterpillar 320D2 rock breaker in Indonesia can range from approximately Rp 3,000,000 to Rp 5,000,000 per hour.
    
    def run(self):
        '''
            Run the cost calculation
        '''
        # Calculate the parameters
        self.__calculate_powder_factor()
        self.__calculate_holes_number()
        self.__calculate_rock_breaker_time()
        self.__calculate_drilling_cost()
        self.__calculate_blasting_cost()
        self.__calculate_rock_breaker_cost()

        # Calculate cost
        cost1 = self.drilling_cost + self.blasting_cost
        cost2 = self.rock_breaker_cost
        cost = cost1 + cost2
        
        # Return the value
        return round(cost, 3)
    