from utils import partial_factor_of_safety_for_materials

def calculate_design_shear_stress(design_action, width, depth, tributory_width, length):
    area = width * depth
    design_load_per_element = design_action * tributory_width * length
    shear_force = design_load_per_element / 2
    stress = (1.5 * shear_force) / area
    return round(stress, 5)

def calculate_design_shear_strength(xTic_shear_strength, Kmod, Ksys, Kv):
    design_strength = (xTic_shear_strength * Kmod * Ksys * Kv) / partial_factor_of_safety_for_materials
    return round(design_strength, 5)

def design_for_shear(design_action, width, depth, length, tributory_width, xTic_shear_strength, Kmod, Ksys, Kv):
    print(design_action, width, depth, tributory_width, length)
    design_shear_stress = calculate_design_shear_stress(design_action, width, depth, tributory_width, length)
    design_shear_strength = calculate_design_shear_strength(xTic_shear_strength, Kmod, Ksys, Kv)

    shear_check = design_shear_stress <= design_shear_strength
    msg = ''
    if shear_check ==True:
        msg = f'PASSES for Shear ({design_shear_stress} </= {design_shear_strength})'
    else:
        msg = f'FAILS for Shear ({design_shear_stress} > {design_shear_strength})'

    return 'shear', shear_check, msg



if __name__ == '__main__':
    from utils import get_design_load
    permanent_load = eval(input("Enter the permanent load(KN/m^2): "))
    variable_load = eval(input("Enter the variable load(KNm^2): "))
    width = eval(input("Enter the width(mm): "))
    depth = eval(input("Enter the depth(mm): "))
    length = eval(input("Enter the length(mm): "))
    tributory_width = eval(input("Enter the tributory_width(mm): "))

    xTic_shear_strength = eval(input("Enter the Characteristic Shear Strength(N/mm^2): "))
    Kmod = eval(input("Enter the Kmod: "))
    Ksys = eval(input("Enter the Ksys: "))
    Kv = eval(input("Enter the Kv: "))

    design_action = get_design_load(permanent_load, variable_load)

    design_for_shear(design_action, width, depth, length, tributory_width, xTic_shear_strength, Kmod, Ksys, Kv)
