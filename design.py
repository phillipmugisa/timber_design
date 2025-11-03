from typing import List, Tuple
from tension import design_for_tension
from utils import get_design_load
from compression import check_for_compression
from shear import design_for_shear
from flexure import design_for_flexure
from bearing import design_for_bearing
from deflection import check_for_deflection
from eurocode import Kmod_values, service_classes, get_kmod_value, timber_classes, get_eurocode_value

def get_numeric_input(name: str, prompt: str, mode: str, source) -> float:
    if mode == 'gui' and source is not None:
        value = source.get_field_value(name)
        return float(value) if value else 0.0
    else:
        return float(input(prompt))

def perform_checks(checks : List[str], source, mode : str='cmd') -> List[Tuple[str, bool, str]]:
    width = get_numeric_input('width', "Enter the width (mm): ", mode, source)
    depth = get_numeric_input('depth', "Enter the depth (mm): ", mode, source)
    Ksys = get_numeric_input('Ksys', "Enter the Ksys: ", mode, source)

    permanent_load = 0
    variable_load = 0
    if 'tension' in checks or 'compression' in checks or 'deflection' in checks:
        permanent_load = get_numeric_input('permanent_load', "Enter the permanent load (kN): ", mode, source)
        variable_load = get_numeric_input('variable_load', "Enter the variable load (kN): ", mode, source)


    if mode == 'gui' and source is not None:
        service_class = int(source.get_field_value('service_class'))
        loading_duration = source.get_field_value('loading_duration')
        timber_class = source.get_field_value('timber_class')
    else:
        service_class = eval(input(f'Select service class {service_classes}: '))
        loading_duration = input(f'Select loading duration {Kmod_values.keys()}: ')
        timber_class = input(f'Select timber class {timber_classes}: ')

    Kmod = get_kmod_value(loading_duration, service_class)
    # since these are not required for all the checks we are declaring them and setting them to 0
    # if the check being performed requires any of these variables, then we prompt the user for their value
    length = 0
    largest_area_reduction = 0
    xTic_tensile_strength = 0
    support_condition = 0
    E005 = 0
    xTic_compressive_strength = 0
    tributory_width = 0
    xTic_shear_strength = 0
    Kv = 0
    tributory_width = 0
    xTic_bending_strength = 0
    bearing_length = 0
    characteristic_compressive_strength_90 = 0
    tributory_width = 0
    K_def = 0
    qausi_permanent_value_for_variable_load = 0
    youngs_modulus = 0
    permanent_load_per_square_m = 0
    variable_load__per_square_m = 0

    if 'shear' in checks or 'flexure' in checks or 'bearing' in checks:
        # convert from KN/m^2 to KN/mm^2
        permanent_load_per_square_m = get_numeric_input('permanent_load_per_square_m', "Enter the permanent load(shear/flexure)(kN/m^2):", mode, source)
        variable_load__per_square_m = get_numeric_input('variable_load__per_square_m', "Enter the variable load(shear/flexure)(kN/m^2):", mode, source)
        permanent_load_per_square_m = permanent_load_per_square_m / 1000 ** 2
        variable_load__per_square_m = variable_load__per_square_m / 1000 ** 2

        tributory_width = get_numeric_input('tributory_width', "Enter the tributory_width(mm): ", mode, source)

    if ('tension' in checks and not (len(checks) == 1)) or ('tension' not in checks and len(checks) > 0):
        length = get_numeric_input('length', "Enter the length (mm): ", mode, source)

    design_action = get_design_load(permanent_load, variable_load)

    if 'tension' in checks:
        print('\nProvide values for Tension')
        largest_area_reduction = get_numeric_input('largest_area_reduction', "Enter the largest area reduction(e.g 20): ", mode, source)
        xTic_tensile_strength = get_eurocode_value('strength', 'ft0k', timber_class)

    if 'compression' in checks:
        print('\nProvide values for Compression')
        support_condition = get_numeric_input('support_condition', "Enter the support condition (e.g. 0.5): ", mode, source)
        E005 = get_eurocode_value('stiffness', 'E005', timber_class)
        xTic_compressive_strength = get_eurocode_value('strength', 'fc0k', timber_class)

    if 'shear' in checks:
        print('\nProvide values for Shear')
        Kv = get_numeric_input('Kv', "Enter the Kv: ", mode, source)
        xTic_shear_strength = get_eurocode_value('strength', 'fvk', timber_class)

    if 'flexure' in checks:
        print('\nProvide values for Flexure')
        xTic_bending_strength = get_eurocode_value('strength', 'fmk', timber_class)
        
    if 'bearing' in checks:
        print('\nProvide values for Bearing')
        bearing_length = get_numeric_input('bearing_length', "Enter the bearing length(mm): ", mode, source)
        characteristic_compressive_strength_90 = get_eurocode_value('strength', 'fc90k', timber_class)

    if 'deflection' in checks:
        print('\nProvide values for Deflection')
        tributory_width = get_numeric_input('tributory_width', "Enter the tributory width(mm): ", mode, source)
        K_def = get_numeric_input('K_def', "Enter the K_def: ", mode, source)
        qausi_permanent_value_for_variable_load = get_numeric_input(
            'qausi_permanent_value_for_variable_load',
            "Enter the qausi permanent value for variable load: ",
            mode, source
        )
        youngs_modulus = get_numeric_input('youngs_modulus', "Enter the young's modulus: ", mode, source)

    results = []
    if 'tension' in checks:
        results.append(design_for_tension(design_action, width, depth, largest_area_reduction, xTic_tensile_strength, Kmod, Ksys))

    if 'compression' in checks:
        results.append(check_for_compression(design_action, width, depth, length, support_condition, E005, xTic_compressive_strength, Kmod, Ksys))

    if 'shear' in checks:
        design_action_2 = get_design_load(permanent_load_per_square_m, variable_load__per_square_m)
        results.append(design_for_shear(design_action_2, width, depth, length, tributory_width, xTic_shear_strength, Kmod, Ksys, Kv))

    if 'flexure' in checks:
        design_action_2 = get_design_load(permanent_load_per_square_m, variable_load__per_square_m)
        results.append(design_for_flexure(design_action_2, width, depth, length, tributory_width, xTic_bending_strength, Kmod, Ksys))

    if 'bearing' in checks:
        results.append(design_for_bearing(design_action, width, bearing_length, tributory_width, length, characteristic_compressive_strength_90, Kmod, Ksys))

    if 'deflection' in checks:
        results.append(check_for_deflection(permanent_load, variable_load, width, depth, length, tributory_width, K_def, qausi_permanent_value_for_variable_load, youngs_modulus))

    return results

def perform_specific_check(option: int = 0):
    if not option:
        option = int(input("Select desired check 1(Tension), 2(Compression), 3(Shear), 4(Flexure), 5(Bearing), 6(Deflection): "))

    checks = []
    if option == 1:
        checks = ['tension']
    elif option == 2:
        checks = ['compression']
    elif option == 3:
        checks = ['shear']
    elif option == 4:
        checks = ['flexure']
    elif option == 5:
        checks = ['bearing']
    elif option == 6:
        checks = ['deflection']

    if checks:
        return perform_checks(checks, source=None)
    return [('', False, '')]

def design_a_member(option:int = 0):
    if not option:
        option = int(input("Select desired member 1(Beam), 2(Column), 3(Ties), 4(Struts), 5(Tie Beam), 6(Studs), 7(Joists), 8(Header Plate), 9(Rafter), 10(Base Plate): "))

    checks = []
    if option == 1:
        checks = ['flexure', 'shear', 'bearing', 'deflection']
    elif option == 2:
        checks = ['compression']
    elif option == 3:
        checks = ['tension']
    elif option == 4:
        checks = ['compression']
    elif option == 5:
        checks = ['flexure']
    elif option == 6:
        checks = ['compression']
    elif option == 7:
        checks = ['flexure', 'shear']
    elif option == 8:
        checks = ['flexure', 'shear', 'bearing']
    elif option == 9:
        checks = ['tension', 'compression', 'shear', 'bearing']
    elif option == 10:
        checks = ['bearing']

    if checks:
        return perform_checks(checks, source=None)
    return [('', False, '')]


def display_results(results: list[tuple[str, bool, str]]):
    # Determine column widths
    headers = ["Check", "Status", "Comment"]
    col_widths = [max(len(str(r[i])) for r in results + [headers]) for i in range(3)]

    # Print headers
    header_row = " | ".join(f"{headers[i]:<{col_widths[i]}}" for i in range(3))
    print(header_row)
    print("-" * len(header_row))

    # Print rows
    for r in results:
        status_str = "Pass" if r[1] else "Fail"
        print(" | ".join(f"{str(r[i]):<{col_widths[i]}}" if i != 1 else f"{status_str:<{col_widths[i]}}" for i in range(3)))

