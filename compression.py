import math
from utils import partial_factor_of_safety_for_materials, beta_for_solid_timber

def calculate_design_compressive_stress(design_action, width, depth):
    area = width * depth
    compressive_stress = design_action / area
    return round(compressive_stress, 3)

def calculate_design_compressive_strength(xTic_compressive_strength, Kmod, Ksys):
    design_strength = (xTic_compressive_strength * Kmod * Ksys) / partial_factor_of_safety_for_materials
    return round(design_strength, 3)

def calculate_radius_of_gyration(b, h):
    Area = b * h
    second_moment_of_area = (b * (h ** 3)) / 12
    i = math.sqrt(second_moment_of_area / Area)
    return i

def calculate_relative_slenderness_ratio(slenderness_ratio, xTic_compressive_strength, E005):
    relative_slenderness_ratio = (slenderness_ratio / math.pi) * math.sqrt(xTic_compressive_strength / E005)
    return relative_slenderness_ratio

def calculate_relative_slenderness_ratios_for_both_axes(effective_length, y, z, xTic_compressive_strength, E005):
    # calculate slenderness ratios for y-y

    radius_of_gyration_for_y = calculate_radius_of_gyration(y, z)
    slenderness_ratio_y = effective_length / radius_of_gyration_for_y

    # calculate slenderness ratio for z-z
    radius_of_gyration_for_z = calculate_radius_of_gyration(z, y)
    slenderness_ratio_z = effective_length / radius_of_gyration_for_z

    # calculate relative slenderness ratios
    relative_slenderness_ratio_y = calculate_relative_slenderness_ratio(slenderness_ratio_y, xTic_compressive_strength, E005)
    relative_slenderness_ratio_z = calculate_relative_slenderness_ratio(slenderness_ratio_z, xTic_compressive_strength, E005)

    return round(relative_slenderness_ratio_y, 3), round(relative_slenderness_ratio_z, 3)

def check_for_compression(design_action, width, depth, length, support_condition, E005, xTic_compressive_strength, Kmod, Ksys):
    design_compressive_stress = calculate_design_compressive_stress(design_action, width, depth)
    effective_length = support_condition * length

    r_y, r_z = calculate_relative_slenderness_ratios_for_both_axes(effective_length, width, depth, xTic_compressive_strength, E005)
    design_compressive_strength = calculate_design_compressive_strength(xTic_compressive_strength, Kmod, Ksys)

    compression_check = False
    if r_y <= 0.3 and r_z <= 0.3:
        compression_check = design_compressive_stress <= design_compressive_strength
    else:
        max_r = max(r_y, r_z)
        K_factor = 0.5 * (1 + (beta_for_solid_timber * (max_r - 0.3)) + max_r ** 2)
        K_c_factor = 1 / (K_factor + math.sqrt((K_factor ** 2) - (max_r ** 2)))

        compression_check = design_compressive_stress <= (K_c_factor * design_compressive_strength)

    msg = ''
    if compression_check ==True:
        msg = f'PASSES Compression Check ({design_compressive_stress} </= {design_compressive_strength})'
    else:
        msg = f'FAILS Compression Check ({design_compressive_stress} > {design_compressive_strength})'

    return 'compression', compression_check, msg


if __name__ == '__main__':

    from utils import get_design_load

    permanent_load = eval(input("Enter the permanent load(kN): "))
    variable_load = eval(input("Enter the variable load(kN): "))
    width = eval(input("Enter the width(mm): "))
    depth = eval(input("Enter the depth(mm): "))
    length = eval(input("Enter the length(mm): "))
    support_condition = eval(input("Enter the support condition (e.g. 0.5): "))
    E005 = eval(input("Enter the E0.05(N/mm^2): "))
    xTic_compressive_strength = eval(input("Enter the Characteristic Compressive Strength(N/mm^2): "))
    Kmod = eval(input("Enter the Kmod: "))
    Ksys = eval(input("Enter the Ksys: "))

    design_action = get_design_load(permanent_load, variable_load)

    check_for_compression(design_action, width, depth, length, support_condition, E005, xTic_compressive_strength, Kmod, Ksys)
