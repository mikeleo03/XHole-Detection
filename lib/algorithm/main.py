from Rock_Factor import Rock_Factor
from KuzRam_Fragmentation import KuzRam_Fragmentation
from Rosin_Rammler import Rosin_Rammler
from Cost_Calculation import Cost_Calculation

if __name__ == '__main__':
    # Setup some initial data needed
    # 0. Setup rock and explosives
    # Let the rock - Basalt
    specific_gravity = 2.9
    hardness = 6.09
    rock_density = 181.0412
    # Let the explosives - ANFO
    explosives_density = 1.7
    detonation_speed = 12000
    blasting_energy = 100
    
    # 1. Rock Factor
    rock_mass_description = 1       # Powdery / Friable
    joint_plane_spacing = 2         # Intermediate (0.1 - 1m)
    joint_plane_orientation = 4     # Dip into Face  
    
    # Calculating the rock factor
    rock_factor_class = Rock_Factor(rock_mass_description, joint_plane_spacing, joint_plane_orientation, specific_gravity, hardness)
    rock_factor = rock_factor_class.run()
    
    # 2. Kuz Ram Fragmentation
    high_level = 10
    ignition_method = True          # Serentak
    
    rock_deposition = 1             # steeply dipping into cut
    geologic_structure = 3          # massive intact rock
    number_of_rows = 2              # Jumlah baris lubang ledak = 2
    gap_jaw_crusher = 30
    x_kuzram = 0.8 * gap_jaw_crusher
    print("x_kuzram:", x_kuzram)
    stdev_drilling_accuracy = 0   
    
    # Calculating the fragmentation size
    blasthole_diameter = 0.05    # Minimum diameter, m
    fragmentation_size = 0       # Initial fragmentation size, m
    while (fragmentation_size < x_kuzram):
        # Kuz-Ram Calculations
        kuzram_class = KuzRam_Fragmentation(explosives_density, detonation_speed, blasting_energy, rock_density, blasthole_diameter, high_level)
        fragmentation_size = kuzram_class.run(rock_factor, rock_deposition, geologic_structure, number_of_rows, ignition_method)
        print("diameter, size:", blasthole_diameter, fragmentation_size)
        if (fragmentation_size < x_kuzram):
            blasthole_diameter += 0.01
        
    print("Expected diameter:", round(blasthole_diameter, 2))
    
    good_diameter = False
    while (not good_diameter):
        # Rosin-Rammler Calculations
        corrected_burden = kuzram_class.get_corrected_burden()
        rossin_rammler_class = Rosin_Rammler(stdev_drilling_accuracy, corrected_burden, fragmentation_size, blasthole_diameter, high_level)
        rossin_rammler_class.calculate_rossin(int(2.25 * x_kuzram))
        sieve_size_data, percent_data = rossin_rammler_class.get_rossin_data()
    
        # Doing reggression with all those data and get the sieve_size_data when percent_data = 80
        pos = len(sieve_size_data) - 1
        x_val1 = sieve_size_data[pos]
        y_val1 = percent_data[pos]
        print("Init value, pos:", x_val1, y_val1, pos)
        while (y_val1 > 80):
            y_val1 = percent_data[pos]
            x_val1 = sieve_size_data[pos]
            pos -= 1
        
        # Gather the larger one
        y_val2 = percent_data[pos+2]
        x_val2 = sieve_size_data[pos+2]
        
        # Normalize values
        y_nom2 = y_val2 - 80
        y_nom1 = 80 - y_val1
        y_fix2 = y_nom2 / (y_nom1 + y_nom2)
        y_fix1 = y_nom1 / (y_nom1 + y_nom2)
        
        # Weighting process
        x_val = x_val1 * y_fix1 + x_val2 * y_fix2
        print(x_val1, y_fix1, x_val2, y_fix2)
        print("X Val:", x_val)
        
        # Conditions
        if (x_val >= x_kuzram):
            good_diameter = True
        else:
            blasthole_diameter -= 0.01
        
    print("Final expected diameter:", round(blasthole_diameter, 2))
    rossin_rammler_class.run(int(2.25 * x_kuzram), round(x_val, 3), 80, x_kuzram)
    
    # 4. Cost_Calculation
    rock_volume = kuzram_class.get_rock_volume()
    explosive_mass = kuzram_class.get_explosive_mass()
    daily_target = 25000 # bcm/day
    coloumn_charge = rossin_rammler_class.get_coloumn_charge()
    cost_calculation_class = Cost_Calculation(rock_volume, explosive_mass, daily_target, coloumn_charge)
    cost_calculation = cost_calculation_class.run()
    print("Cost calc:", cost_calculation)
    