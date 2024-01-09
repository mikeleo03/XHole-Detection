import math

class KuzRam_Fragmentation:
    '''
    Class KuzRam_Fragmentation, implementing KuzRam Fragmentation calculations
    '''
    def __init__(self, explosives_density, detonation_speed, rock_density, blasthole_diameter, high_level, ignition_method):
        '''
            Initiate needed variables
            params:
                rock_factor (A) = Faktor batuan, diperoleh dari pembobotan batuan berdasarkan nilai blasting index
                explosive_mass (Qe) = massa bahan peledak per lubang tembak
                rock_volume (Vo) = volume batuan pecah per lubang tembak
            args:
                explosives_density (rho1) = Massa jenis peledak, gr/cc
                detonation_speed (VoD) = Kecepatan detonasi batuan, ft/s
                blasting_energy (E) = Relatif weight strength bahan peledak, ANFO = 100, TNT = 115, kJ
                rock_density (rho2) = Massa jenis batuan, pond cubic ft
                blasthole_diameter (D) = Diameter lubang, mm
                high_level (L) = Tinggi jenjang, m
                ignition_method = Metode penyalaan, bisa "serentak" (true) atau "tunda" (false)
        '''
        self.rock_factor = 0
        self.explosives_density = explosives_density
        self.detonation_speed = detonation_speed
        self.blasting_energy = blasting_energy
        self.rock_density = rock_density
        self.blasthole_diameter = blasthole_diameter
        self.high_level = high_level
        self.ignition_method = ignition_method
        
    def __calculate_rock_volume(self):
        '''
            Calculate the rock volume
            params:
                corrected_burden (Bc) = Nilai burden yang dikoreksi, m
                stiffness (s)
                high_level (L) = Tinggi jenjang, m
        '''
        self.rock_volume = self.corrected_burden * self.stiffness * self.high_level
        
    def __calculate_burden(self):
        '''
            Calculate the burden (R. L. Ash)
            params:
                explosives_density (rho1) = Massa jenis peledak, gr/cc
                detonation_speed (VoD) = Kecepatan detonasi batuan, ft/s
                rock_density (rho2) = Massa jenis batuan, pond cubic ft
                blasthole_diameter (D) = Diameter lubang, mm
        '''
        af1 = (self.explosives_density * pow(self.detonation_speed, 2) / 1.2 * pow(pow(1200, 2)), (1/3))     # Calculate explosives adjustment
        af2 = pow((160 / self.rock_density), (1/3))     # Calculate rock adjustment
        Kbstd = 30
        self.burden = self.blasthole_diameter * Kbstd * af1 * af2
        
    def __calculate_corrected_burden(self):
        '''
            Calculate the corrected burden by considering correction factors
            params:
                burden (B) = Burden, m
                rock_deposition = Kondisi sedimentasi batuan, ['steeply dipping into cut' (1), 'steeply dipping into face' (2), atau lainnya (3)]
                geologic_structure = Struktur geologi batuan, ['heavily cracked' (1), 'thin well cemented layers' (2), atau 'massive intact rock' (3)]
                number_of_rows = Jumlah baris lubang ledak, [1, 2, atau lebih]
        '''
        # Set the initial values
        Kd = 0; Ks = 0; Kr = 0
        
        # Calculating the value of Kd
        if rock_deposition == 1: Kd = 1.18
        elif rock_deposition == 2: Kd = 0.95
        else: Kd = 1.0

        # Menentukan faktor koreksi Ks
        if geologic_structure == 1: Ks = 1.30
        elif geologic_structure == 2: Ks = 1.1
        else: Ks = 0.95

        # Menentukan faktor koreksi Kr
        if number_of_rows <= 2: Kr = 1.0
        else: Kr = 0.95

        # Menghitung corrected burden
        self.corrected_burden = Kd * Ks * Kr * self.burden
        
    def __calculate_stifness(self):
        '''
            Calculate stiffness
            params:
                high_level (L) = Tinggi jenjang, m
                corrected_burden (Bc) = Nilai burden yang dikoreksi, m
                ignition_method = Metode penyalaan, bisa 'serentak' (true) atau 'tunda' (false)
        '''
        # Calculate stiffness ratio
        stiffness_ratio = self.high_level / self.corrected_burden

        # Calculate the stifness value
        s = 0
        if stiffness_ratio < 4:
            if ignition_method:
                s = (self.high_level + 2 * self.corrected_burden) / 3
            else:
                s = (self.high_level + 7 * self.corrected_burden) / 8
        else:
            if ignition_method:
                s = 2 * self.corrected_burden
            else:
                s = 1.4 * self.corrected_burden

        self.stiffness = s

    def __calculate_explosive_mass(self):
        '''
            Calculate the corrected burden by considering correction factors
            params:
                blasthole_diameter (D) = Diameter lubang, mm
                corrected_burden (Bc) = Nilai burden yang dikoreksi, m
                high_level (L) = Tinggi jenjang, m
        '''
        r = 1/2 * self.blasthole_diameter
        t = 0.7 * self.corrected_burden         # Stemming depth, m
        j = 0.2 * self.corrected_burden         # The thickness of the rock to be crushed (subdrill), m
        self.explosive_mass = math.pi * pow(r, 2) * (self.high_level - t + j)
    
    def run(self):
        '''
            Run KuzRam Fragmentation calculations
            params:
                explosives_density (rho1) = Massa jenis peledak, gr/cc
                detonation_speed (VoD) = Kecepatan detonasi batuan, ft/s
                rock_density (rho2) = Massa jenis batuan, pond cubic ft
                blasthole_diameter (D) = Diameter lubang, mm
                high_level (L) = Tinggi jenjang, m
                ignition_method = Metode penyalaan, bisa'serentak' (true) atau 'tunda' (false)
                blasting_energy (E) = Relatif weight strength bahan peledak, ANFO = 100, TNT = 115, kJ
        '''
        # Calculate the needed parameters
        self.__calculate_rock_volume()
        self.__calculate_burden()
        self.__calculate_corrected_burden()
        self.__calculate_stifness()
        self.__calculate_explosive_mass()
        
        # Calculate the fragmentation size
        x = self.rock_factor * (self.rock_volume / self.explosive_mass) ** 0.8 * self.explosive_mass ** (1 / 6) / (self.blasting_energy / 115) ** (-19 / 30)
        x *= 100  # Convert into mm
        
        # Return the rounded value
        return round(x, 2)
    