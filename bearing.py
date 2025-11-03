from utils import partial_factor_of_safety_for_materials

def calculate_design_compressive_stress_90(design_action, width, bearing_length, tributory_width, length):

    design_load_per_element = design_action * tributory_width * length
    fd = design_load_per_element / 2

    design_compressive_stress_90 = fd / (width * bearing_length)
    return round(design_compressive_stress_90, 3)

def calculate_design_compressive_strength_90(Kmod, Ksys, characteristic_compressive_strength_90, partial_factor_of_safety_for_materials):
    design_compressive_strength_90 = (characteristic_compressive_strength_90 * Kmod * Ksys) / (partial_factor_of_safety_for_materials)
    return round(design_compressive_strength_90, 3)


def design_for_bearing(design_action, width, bearing_length, tributory_width, length, characteristic_compressive_strength_90, Kmod, Ksys):
    design_compressive_stress_90 = calculate_design_compressive_stress_90(design_action, width, bearing_length, tributory_width, length)
    design_compressive_strength_90 = calculate_design_compressive_strength_90(Kmod, Ksys, characteristic_compressive_strength_90, partial_factor_of_safety_for_materials)
    
    msg = ''
    bearing_check = design_compressive_stress_90 <= design_compressive_strength_90
    if bearing_check:
        msg = f'SUFFICIENT IN BEARING ({design_compressive_stress_90} </= {design_compressive_strength_90})'
    else:
        msg = f'NOT SUFFICIENT IN BEARING ({design_compressive_stress_90} > {design_compressive_strength_90})'
    
    return 'bearing', bearing_check, msg
  

if __name__ == "__main__":
    from utils import get_design_load

    permanent_load = eval(input("Enter the permanent load(KN): "))
    variable_load = eval(input("Enter the variable load(KN): "))
    width = eval(input("Enter the width(mm): "))
    Kmod = eval(input("Enter the Kmod: "))
    Ksys = eval(input("Enter the Ksys: "))
    bearing_length = eval(input("Enter the bearing length(mm): "))
    characteristic_compressive_strength_90 = eval(input("Enter the Characteristic Compressive Strength perpendicular to the grain(N/mm^2): "))

    design_action = get_design_load(permanent_load, variable_load)
    design_for_bearing(design_action, width, bearing_length, characteristic_compressive_strength_90, Kmod, Ksys)
