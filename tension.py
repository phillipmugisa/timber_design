from utils import partial_factor_of_safety_for_materials

def calculate_design_tensile_stress(design_action, width, depth, largest_area_reduction_as_percentage):
    original_area = width * depth
    # remove connection fitting areas
    # eg largest_area_reduction_as_percentage = 5

    net_area = (100 - largest_area_reduction_as_percentage) / 100 * original_area
    stress = design_action / net_area
    return round(stress, 3)
  

def calculate_design_tensile_strength(xTic_tensile_strength, Kmod, Ksys, depth):
    Kh = 1
    if depth < 150:
        value = (150/depth) ** 0.2
        Kh = min(value, 1.3)

    Kh = round(Kh, 3)

    design_strength = (xTic_tensile_strength * Kmod * Kh * Ksys) / partial_factor_of_safety_for_materials
    return round(design_strength, 3)


def design_for_tension(design_action, width, depth, largest_area_reduction, xTic_tensile_strength, Kmod, Ksys):

    design_tensile_stress = calculate_design_tensile_stress(design_action, width, depth, largest_area_reduction)
    design_tensile_strength = calculate_design_tensile_strength(xTic_tensile_strength, Kmod, Ksys, depth)
    
    tension_check = design_tensile_stress <= design_tensile_strength
    msg = ''
    if tension_check == True:
        msg = f'PASSES for Tension ({design_tensile_stress} </= {design_tensile_strength})'
    else:
        msg = f'FAILS for Tension ({design_tensile_stress} > {design_tensile_strength})'

    return 'tension', tension_check, msg


if __name__ == '__main__':
    from utils import get_design_load

    permanent_load = eval(input("Enter the permanent load(KN): "))
    variable_load = eval(input("Enter the variable load(KN): "))
    width = eval(input("Enter the width(mm): "))
    depth = eval(input("Enter the depth(mm): "))
    largest_area_reduction = eval(input("Enter the largest area reduction(e.g 20): "))
    xTic_tensile_strength = eval(input("Enter the Characteristic Tensile Strength(N/mm^2): "))
    Kmod = eval(input("Enter the Kmod: "))
    Ksys = eval(input("Enter the Ksys: "))

    design_action = get_design_load(permanent_load, variable_load)
    design_for_tension(design_action, width, depth, largest_area_reduction, xTic_tensile_strength, Kmod, Ksys)
