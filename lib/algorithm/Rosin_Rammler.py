import math

class Rosin_Ramler:
    '''
    Class Rossin_Ramler, calculating the Rossin Ramler values
    '''
    def __init__(self, stdev_drilling_accuracy, corrected_burden, fragmentation_size):
        '''
            Initiate needed variables
            params:
                fragmentation_size (x) = Ukuran fragmentasi, cm
                stdev_drilling_accuracy (W) = Standar deviasi dari keakuratan pemboran, m
                corrected_burden (Bc) = Nilai burden yang dikoreksi, m
                blasthole_diameter (D) = Diameter lubang, mm
                high_level (L) = Tinggi jenjang, m
        '''
        self.fragmentation_size = fragmentation_size
        self.stdev_drilling_accuracy = stdev_drilling_accuracy
        self.corrected_burden = corrected_burden
        self.blasthole_diameter = blasthole_diameter
        self.high_level = high_level
        
    def __calculate_uniformity_index(self):
        '''
            Calculates the uniformity index for given data
            params:
                stdev_drilling_accuracy (W) = Standar deviasi dari keakuratan pemboran, m
                corrected_burden (Bc) = Nilai burden yang dikoreksi, m
                blasthole_diameter (D) = Diameter lubang, mm
                high_level (L) = Tinggi jenjang, m
        '''
        # Calculate CC value
        t = 0.7 * self.corrected_burden         # Stemming depth, m
        j = 0.2 * self.corrected_burden         # The thickness of the rock to be crushed (subdrill), m
        cc = self.high_level - t + j
        
        # Calculate value of A
        a = self.corrected_burden / self.blasthole_diameter
        rat = self.stdev_drilling_accuracy / self.corrected_burden
        
        self.uniformity_index = (2.2 - 14 * a) * (1 - (rat)) * (1 + (a - 1) / 1) * (cc / self.high_level)
    
    def calculate_distribution(self, sieve_size):
        '''
            Calculate the distribution of x_hat presentation
            params:
                sieve_size (x_hat) = Ukuran ayakan, cm
                uniformity_index (n) = Indeks keseragaman
        '''
        # Calculate characteristic size (xc)
        xc = pow ((sieve_size / 0.683), (1 / self.uniformity_index))
        
        # Calculate the presentasional distribution
        dist = math.exp(-(pow(self.fragmentation_size / xc), self.uniformity_index)) * 100
        return dist
        
    def run(self):
        '''
            Run Rossin Ramler calculations
        '''
        # Calculate the needed parameters
        self.__calculate_uniformity_index()
        
        # Run for sieve_size from 1 - 1000
        for sieve_size in range(1, 1000):
            # Calculate the distribution
            dist = self.calculate_distribution(sieve_size)
            
            # Print the result
            print(sieve_size, dist)
    