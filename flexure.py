from utils import partial_factor_of_safety_for_materials, beta_for_solid_timber

def get_elastic_section_modulus(width, depth):
    return (width * (depth ** 2)) / 6

def calculate_design_bending_stress(design_action, length, width, depth, tributory_width):

    design_load_per_element = design_action * tributory_width * length
    bending_moment = (design_load_per_element * length) / 8
    elastic_section_modulus = get_elastic_section_modulus(width, depth)
    stress = bending_moment / elastic_section_modulus
    return round(stress, 3)

def calculate_design_bending_strength(xTic_bending_strength, Kmod, Ksys, depth):
    Kh = 1
    if depth < 150:
        value = (150/depth) ** 0.2
        Kh = min(value, 1.3)

    Kh = round(Kh, 3)

    design_strength = (xTic_bending_strength * Kmod * Ksys * Kh) / partial_factor_of_safety_for_materials
    return round(design_strength, 3)

def design_for_flexure(design_action, width, depth, length, tributory_width, xTic_bending_strength, Kmod, Ksys):
    """
        caters for uniaxial bending only
    """

    design_bending_stress = calculate_design_bending_stress(design_action, length, width, depth, tributory_width)
    design_bending_strength = calculate_design_bending_strength(xTic_bending_strength, Kmod, Ksys, depth)

    flexure_check = design_bending_stress <= design_bending_strength
    msg = ''
    if flexure_check ==True:
        msg = f'PASSES for Bending ({design_bending_stress} </= {design_bending_strength})'
    else:
        msg = f'FAILS for Bending ({design_bending_stress} > {design_bending_strength})'

    return 'flexure', flexure_check, msg



if __name__ == '__main__':

    from utils import get_design_load

    permanent_load = eval(input("Enter the permanent load(KN/m^2): "))
    variable_load = eval(input("Enter the variable load(KNm^2): "))
    width = eval(input("Enter the width(mm): "))
    depth = eval(input("Enter the depth(mm): "))
    length = eval(input("Enter the length(mm): "))
    tributory_width = eval(input("Enter the tributory_width(mm): "))

    xTic_bending_strength = eval(input("Enter the Characteristic Bending Strength(N/mm^2): "))
    Kmod = eval(input("Enter the Kmod: "))
    Ksys = eval(input("Enter the Ksys: "))

    design_action = get_design_load(permanent_load, variable_load)

    design_for_flexure(design_action, width, depth, length, tributory_width, xTic_bending_strength, Kmod, Ksys)

