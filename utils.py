
partial_factor_of_safety_for_permanent_load = 1.35
partial_factor_of_safety_for_variable_load = 1.5
partial_factor_of_safety_for_materials = 1.3
beta_for_solid_timber = 0.2
KC_90 = 1.0

def get_design_load(permanent_load, variable_load):
    """
        expect loads as KN
    """
    design_action = (permanent_load * partial_factor_of_safety_for_permanent_load) + (variable_load * partial_factor_of_safety_for_variable_load)
    design_action = design_action * 1000
    return design_action
