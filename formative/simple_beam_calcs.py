"""
Script to find the number of brackets required to support the helicopter load.
"""

import numpy as np
import matplotlib.pyplot as plt
import math

#### Material Properties####
materials_dict = {
    "A36Steel": {
        "E": 200E9,        # Pa
        "v": 0.26,         # Poisson's Ratio
        "dens": 7850,      # kg/m³
        "yield_strength": 250E6  # Pa (250 MPa)
    },
    "S355Steel": {
        "E": 210E9,        # Pa
        "v": 0.30,         # Poisson's Ratio
        "dens": 7850,      # kg/m³
        "yield_strength": 355E6  # Pa (355 MPa)
    },
    "1045Steel": {
        "E": 205E9,        # Pa
        "v": 0.29,         # Poisson's Ratio
        "dens": 7870,      # kg/m³
        "yield_strength": 530E6  # Pa (530 MPa)
    },
    "316StainlessSteel": {
        "E": 193E9,        # Pa
        "v": 0.30,         # Poisson's Ratio
        "dens": 8000,      # kg/m³
        "yield_strength": 290E6  # Pa (290 MPa)
    },
    "4340Steel": {
        "E": 210E9,        # Pa
        "v": 0.29,         # Poisson's Ratio
        "dens": 7850,      # kg/m³
        "yield_strength": 470E6  # Pa (470 MPa)
    },
    "AISI8620Steel": {
        "E": 205E9,        # Pa
        "v": 0.29,         # Poisson's Ratio
        "dens": 7850,      # kg/m³
        "yield_strength": 620E6  # Pa (620 MPa)
    }
}
#### Bracket Dimensions and properties #####
w = 0.3
t = 0.3
l = 8
V = w*t*l #volume
I = (w * t**3) / 12 #second moment of intertia

#### Other Parameters ####
SF = 2.5 #safety factor
g = 9.81
heli_weight = 0.7E3 * g
heli_weight_sf = heli_weight*SF 

def find_max_bracket_load(E, density)-> int:
    self_load_perm = (density*V*g) / l
    d_self = (self_load_perm * l**4) / (8 * E * I)
    max_allowable_def = 0.001 + d_self
    max_w = (max_allowable_def * 8 * E * I) / (l**3)  # Adjusted to include length of bracket for overall load
    return max_w

def find_min_num_brackets(E, density)-> int:
    min_num = (heli_weight_sf) / (find_max_bracket_load(E, density) - (density*V*g))
    return math.ceil(min_num) #returns rounded up to the next whole number

def find_spacing(num_br)-> int:
    plat_width = 8
    space = plat_width - (num_br * w)
    spacing = space / (num_br - 1)
    return spacing

def calculate_expected_deflection(num_brackets,E, density)-> int:
    bracket_weight = V * density * g
    heli_load = heli_weight_sf
    load_perm = ((heli_load / num_brackets)/l) + (bracket_weight/l)
    d_overall = (load_perm * l**4) / (8 * E * I)
    d_self = ((bracket_weight/l) * l**4) / (8 * E * I)
    d_add_simple = (((heli_load / num_brackets)/l) * l**4) / (8 * E * I)
    d_additional = d_overall- d_self
    return d_overall, d_additional, d_add_simple

def calculate_shear(num_brackets:list, E:int, density:int)-> int:
    max_shear_force = (heli_weight_sf/num_brackets)+ (density * V * g)
    max_shear_stress = (3*max_shear_force*3)/(2*t*w)
    return max_shear_stress

def main():
    for material, properties in materials_dict.items():
        E = properties["E"]
        density = properties["dens"]
        yield_strength = properties["yield_strength"]
        num_brackets = find_min_num_brackets(E, density)
        expected_shear = calculate_shear(num_brackets, E, density)
        expected_deflection, additional_deflection, additional_simple = calculate_expected_deflection(num_brackets, E,density)
        model_load = (heli_weight_sf/num_brackets) / (l*w)

        # print results for each material
        print(f"\nMaterial: {material}")
        print(f"Number of brackets: {num_brackets}")
        # Tresca Criterion
        if expected_shear < (yield_strength/2):
            print(f"Under Tresca criterion, a maximum shear stress of {expected_shear:.1E}Pa will not cause the beam to yield")
        else:
            print("Material will yield.")
        print(f"Expected additional deflection: {additional_deflection:.1E}m")
        print(f"Expected overall deflection: {expected_deflection:.1E}m")

        print(f"Model Load Magnitude: {round(model_load,5)}")
        
        spacing = (8 - (w*(num_brackets-1))) / (num_brackets -1)
        print(f"Bracket spacing: {round(spacing,2)}")

if __name__ == "__main__":    
    main()

