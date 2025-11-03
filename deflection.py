def U_inst(action, length, youngs_modulus, area, second_moment_of_area):
    """
        catering for UDL only
    """
    bending = (5 / 384) * ((action * (length ** 3)) / (youngs_modulus * second_moment_of_area))
    shear = (12 / 5) * ( (action * length) / ( youngs_modulus * area))

    return bending +  shear

def check_for_deflection(permanent_load, variable_load, width, depth, length, tributory_width, K_def, qausi_permanent_value_for_variable_load, youngs_modulus):
    # convert loads from kN/m to KN/mm
    permanent_load = permanent_load / 1000
    variable_load = variable_load / 1000

    area = width * depth
    second_moment_of_area = (width * (depth ** 3)) / 12

    deflection_value_for_permanent_loads = U_inst(permanent_load * tributory_width * length, length, youngs_modulus, area, second_moment_of_area) * (1 + K_def)
    deflection_value_for_variable_loads = U_inst(variable_load * tributory_width * length, length, youngs_modulus, area, second_moment_of_area) * (1 + (qausi_permanent_value_for_variable_load) * K_def)

    msg = ''
    final_deflection = round(deflection_value_for_permanent_loads + deflection_value_for_variable_loads, 3)
    deflection_check = final_deflection < (length / 250)
    if deflection_check:
        msg = f'PASSES for deflection {final_deflection} > {length / 250}'
    else:
        msg = f'FAILS for deflection {final_deflection} < {length / 250}'

    return 'deflection', deflection_check, msg
        

if __name__ == "__main__":
    permanent_load = eval(input("Enter the permanent load(KN/m): "))
    variable_load = eval(input("Enter the variable load(KN/m): "))
    width = eval(input("Enter the width(mm): "))
    depth = eval(input("Enter the depth(mm): "))
    length = eval(input("Enter the length(mm): "))
    tributory_width = eval(input("Enter the tributory width(mm): "))
    K_def = eval(input("Enter the K_def: "))
    qausi_permanent_value_for_variable_load = eval(input("Enter the qausi permanent value for variable load: "))
    youngs_modulus = eval(input("Enter the young's modulus: "))

    check_for_deflection(permanent_load, variable_load, width, depth, length, tributory_width, K_def, qausi_permanent_value_for_variable_load, youngs_modulus)
