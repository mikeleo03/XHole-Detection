import math
import matplotlib.pyplot as plt
from io import BytesIO
import base64

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
        self.img_data = None  # to store the plot image data

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
        self.coloumn_charge = self.high_level - t + j

        # Calculate value of A
        a = self.corrected_burden / (self.blasthole_diameter)
        A = 4 / self.corrected_burden
        val = 1 - (self.stdev_drilling_accuracy / self.corrected_burden)
        self.uniformity_index = (2.2 - 14 * a / 1000) * val * (1 + (A - 1) / 2) * (self.coloumn_charge / self.high_level)

    def get_coloumn_charge(self):
        '''
            Getter of coloumn charge
        '''
        return self.coloumn_charge
    
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

    def calculate_rossin(self, value):
        '''
            Run Rossin Ramler calculations
        '''
        # Calculate the needed parameters
        self.__calculate_uniformity_index()
        self.sieve_size_data = []
        self.percent_data = []

        # Run for sieve_size from 1 - 1000
        for sieve_size in range(1, value + 1):
            # Calculate the distribution
            dist = 100 - self.calculate_distribution(sieve_size)

            # Print the result
            self.sieve_size_data.append(sieve_size)
            self.percent_data.append(dist)
                
    def get_rossin_data(self):
        '''
            Getter of rossin data
        '''
        return self.sieve_size_data, self.percent_data
            
    def get_image_data(self):
        '''
            Getter of image data
        '''
        return self.img_data

    def run(self, value, x_highlight, y_highlight, x_kuzram):
        '''
            Plot Rossin Ramler calculations
        '''
        # Run the calculation
        self.calculate_rossin(value)
        
        # Plot the data
        plt.plot(self.sieve_size_data, self.percent_data)
        plt.xlabel("Fragmentation Size (cm)")  # add X-axis label
        plt.ylabel("Pass Precentage (%)")  # add Y-axis label
        plt.title("Estimation of Blast Fragmentation Results")  # add title
        # Highlight the specific point in red using plt.scatter
        plt.scatter(x_highlight, y_highlight, color='red', label='Highlighted Point')
        # Add text annotation next to the highlighted point
        plt.text(x_highlight + 1, y_highlight + 3, f'80% Rossin = {x_highlight}', color='red', fontsize=9, ha='left')
        plt.text(1, 4, f'X Kuz-Ram = {x_kuzram}', color='orange', fontsize=9, ha='left', va='bottom')
        plt.show()

        """ # Save the plot to a BytesIO object
        img_buf = BytesIO()
        plt.savefig(img_buf, format='png')
        img_buf.seek(0)

        # Encode the image as base64 to embed it in the HTML
        self.img_data = base64.b64encode(img_buf.read()).decode('utf-8')

        # Clear the plot
        plt.clf() """