from Rock_Factor import Rock_Factor
from KuzRam_Fragmentation import KuzRam_Fragmentation
from Rosin_Rammler import Rosin_Rammler

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
    print("Rock factor:", rock_factor)
    
    # 2. Kuz Ram Fragmentation
    blasthole_diameter = 0.03       # Minimum diameter, m
    high_level = 10
    ignition_method = True          # Serentak
    
    rock_deposition = 1             # steeply dipping into cut
    geologic_structure = 3          # massive intact rock
    number_of_rows = 2              # Jumlah baris lubang ledak = 2      
    
    # Calculating the fragmentation size
    kuzram_class = KuzRam_Fragmentation(explosives_density, detonation_speed, blasting_energy, rock_density, blasthole_diameter, high_level)
    fragmentation_size = kuzram_class.run(rock_factor, rock_deposition, geologic_structure, number_of_rows, ignition_method)
    print("Fragmentation size:", fragmentation_size)
    
    # 3. Rosin-Rammler Calculations
    stdev_drilling_accuracy = 5
    corrected_burden = kuzram_class.get_corrected_burden()
    print("Corrected Burden:", corrected_burden)
    rossin_rammler_class = Rosin_Rammler(stdev_drilling_accuracy, corrected_burden, fragmentation_size, blasthole_diameter, high_level)
    rossin_rammler_class.run()
    