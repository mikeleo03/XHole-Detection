import math
import matplotlib.pyplot as plt

class Rosin_Rammler:
    '''
    Class Rossin_Ramler, calculating the Rossin Ramler values
    '''
    def __init__(self, stdev_drilling_accuracy, corrected_burden, fragmentation_size, blasthole_diameter, high_level):
        '''
            Initiate needed variables
            params:
                fragmentation_size (x) = Ukuran fragmentasi, cm
                stdev_drilling_accuracy (W) = Standar deviasi dari keakuratan pemboran, m
                corrected_burden (Bc) = Nilai burden yang dikoreksi, m
                blasthole_diameter (D) = Diameter lubang, mm
                high_level (L) = Tinggi jenjang, m
        '''
        self.stdev_drilling_accuracy = stdev_drilling_accuracy
        self.corrected_burden = corrected_burden
        self.fragmentation_size = fragmentation_size
        self.blasthole_diameter = blasthole_diameter
        self.high_level = high_level
        
    def __calculate_uniformity_index(self, stiffness):
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
        val = 1 - (self.stdev_drilling_accuracy / self.corrected_burden)
        big_a = stifness / self.corrected_burden
        self.uniformity_index = (2.2 - 14 * a / 1000) * val * (1 + (big_a - 1) / 2) * (cc / self.high_level)
    
    def calculate_distribution(self, sieve_size):
        '''
            Calculate the distribution of x_hat presentation
            params:
                sieve_size (x_hat) = Ukuran ayakan, cm
                uniformity_index (n) = Indeks keseragaman
        '''
        # Calculate characteristic size (xc)
        xc = self.fragmentation_size / pow(0.693, (1 / self.uniformity_index))
        
        # Calculate the presentasional distribution
        dist = math.exp(-((sieve_size / xc) ** self.uniformity_index)) * 100
        return dist
        
    def run(self, stiffness):
        '''
            Run Rossin Ramler calculations
        '''
        # Calculate the needed parameters
        self.__calculate_uniformity_index(stiffness)
        print(self.uniformity_index)
        sieve_size_data = []
        percent_data = []
        
        # Run for sieve_size from 1 - 1000
        for sieve_size in range(1, 1000):
            # Calculate the distribution
            dist = self.calculate_distribution(sieve_size)
            
            # Print the result
            sieve_size_data.append(sieve_size)
            percent_data.append(dist)
            print(sieve_size, dist)
        
        # Plot the data
        plt.plot(sieve_size_data, percent_data)
        plt.xlabel("Fragmentasi (cm)")                          # add X-axis label 
        plt.ylabel("Presentase Lolos (%)")                      # add Y-axis label 
        plt.title("Estimasi Hasil Fragmentasi Peledakan")       # add title 
        plt.show()