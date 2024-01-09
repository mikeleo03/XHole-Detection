class Rock_Factor:
    '''
    Class Rock_Factor, calculating the rock factor values
    '''
    def __init__(self, rock_mass_description, joint_plane_spacing, joint_plane_orientation, specific_gravity, hardness):
        '''
            Initiate needed variables
            params:
                rock_mass_description (RMD)
                joint_plane_spacing (JPS)
                joint_plane_orientation (JPO)
                specific_gravity (SG)
                hardness (H)
        '''
        self.rock_mass_description = rock_mass_description
        self.joint_plane_spacing = joint_plane_spacing
        self.joint_plane_orientation = joint_plane_orientation
        self.specific_gravity= specific_gravity
        self.hardness = hardness
        
    def __calculate_blasting_index(self):
        '''
            Calculate the blasting index
            params:
                rock_mass_description (RMD)
                joint_plane_spacing (JPS)
                joint_plane_orientation (JPO)
                specific_gravity_influence (SGI)
                hardness (H)
        '''
        # Get initial values
        rmd = 0; jps = 0; jpo = 0; sgi = 0; h = 0
        # Rock Mass Description value (RMD)
        # Powdery / Friable [1]     10
        # Blocky [2]                20
        # Totally Massive [3]       50
        if self.rock_mass_description == 1: rmd = 10
        elif self.rock_mass_description == 2: rmd = 20
        elif self.rock_mass_description == 3: rmd = 50
        
        # Joint Plane Spacing value (JPS)
        # Close (< 0.1m) [1]            10
        # Intermediate (0.1 - 1m) [2]   20
        # Wide (> 1m)[3]                50
        if self.joint_plane_spacing == 1: jps = 10
        elif self.joint_plane_spacing == 2: jps = 20
        elif self.joint_plane_spacing == 3: jps = 50
        
        # Joint Plane Orientation value (JPO)
        # Horizontal [1]                10
        # Dip out of Face [2]           20
        # Strike Normal to Face [3]     30
        # Dip into Face [4]             40
        if self.joint_plane_orientation == 1: jpo = 10
        elif self.joint_plane_orientation == 2: jpo = 20
        elif self.joint_plane_orientation == 3: jpo = 30
        elif self.joint_plane_orientation == 4: jpo = 40
        
        # Specific Gravity Influence value (SGI)
        sgi = 25 * self.specific_gravity - 50
        
        # Hardness value (H)
        h = self.hardness
        
        # Calculate the rock factor
        self.blasting_index = 0.5 * (rmd + jps + jpo + sgi + h)
        
    def run(self):
        '''
            Run Rock Factor calculations
        '''
        # Calculate the needed parameters
        self.__calculate_blasting_index()
        
        # Return the rounded value
        return round(self.blasting_index * 0.15, 3)
        