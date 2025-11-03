'''
This file contains relevant codes to be used by other files
'''

# values for Kmod for solid timber
# keys -> load duration
# values -> service class values
service_classes = [1, 2, 3] 
Kmod_values = {
    'permanent': [0.60, 0.60, 0.50],
    'long': [0.70, 0.70, 0.55],
    'medium': [0.80, 0.80, 0.65],
    'short': [0.90, 0.90, 0.70],
    'instantaneous': [1.10, 1.10, 0.90]
}

# partial factor of safety for materials based on design situations
Ym_fundatamental_combinations_for_solid_timber = 1.3
Ym_accidential_combinations = 1.0
Ym_serviceability_limit_states = 1.0

# strength classes - characteristic values
# keys -> loading kind
# values -> array of strength properties
timber_classes = [
    'C14', 'C16', 'C18', 'C20', 'C22', 'C24', 'C27', 'C30', 'C35', 'C40', 'C45', 'C50', # hard wood
    'D30', 'D35', 'D40', 'D50', 'D60', 'D70' # soft word
]
# (N/mm^2)
strength_properties = {
    'fmk': [14, 16, 18, 20, 22, 24, 27, 30, 35, 40, 45, 50, 30, 35, 40, 50, 60, 70], # bending
    'ft0k': [8, 10, 11, 12, 13, 14, 16, 18, 21, 24, 27, 30, 18, 21, 24, 30, 36, 43], # tension parallel
    'ft90k': [0.4, 0.5, 0.5, 0.5, 0.5, 0.5, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6], # tension perpendicular
    'fc0k': [16, 17, 18, 19, 20, 21, 22, 23, 25, 26, 27, 29, 23, 25, 26, 29, 32, 34], # compression parallel
    'fc90k': [2.0, 2.2, 2.2, 2.3, 2.4, 2.5, 2.5, 2.7, 2.8, 2.9, 3.1, 3.2, 8.0, 8.4, 8.4, 9.7, 10.5, 13.5], # compression perpendicular
    'fvk': [1.7, 1.8, 2.0, 2.2, 2.4, 2.5, 2.8, 3.0, 3.4, 3.8, 3.8, 3.8, 3.0, 3.4, 3.8, 4.6, 5.3, 6.0] # shear
}

# stiffness properties (KN/mm^2)
stiffness_properties = {
    'E0mean': [7, 8, 9, 9.5, 10, 11, 11.5, 12, 13, 14, 15, 16, 10, 10, 11, 14, 17, 20], # mean modulus of elasticity parallel
    'E005': [4.7, 5.4, 6.0, 6.4, 6.7, 7.4, 7.7, 8.0, 8.7, 9.4, 10.0, 10.7, 8.0, 8.7, 9.4, 11.8, 14.3, 16.8], # 5% modulus of elasticity parallel
    'E90mean': [0.23, 0.27, 0.30, 0.32, 0.33, 0.37, 0.38, 0.40, 0.43, 0.47, 0.50, 0.53, 0.64, 0.69, 0.75, 0.93, 1.13, 1.33], # mean modulus of elasticity perpendicular
    'Gmean': [0.44, 0.5, 0.56, 0.59, 0.63, 0.69, 0.72, 0.75, 0.81, 0.88, 0.94, 1.00, 0.60, 0.65, 0.70, 0.88, 1.06, 1.25] # mean shear modulus
}

def get_kmod_value(loading_duration: str, service_class: int) -> int|float:
    duration = Kmod_values.get(loading_duration)
    if not duration:
        raise ValueError(f'Loading Duration {duration} not provided for.')

    if service_class not in service_classes:
        raise ValueError(f'Service class {service_class} not provided for.')

    return duration[service_class - 1]


def get_eurocode_value(property: str, property_name: str, timber_class: str) -> int|float:
    # check if the provided timber class is in the timber classes
    if timber_class not in timber_classes:
        raise ValueError(f'Timber class {timber_class} not provided for.')
    
    if property == 'stiffness':
        target_table = stiffness_properties
    else:
        target_table = strength_properties

    if not target_table.get(property_name, None):
        raise ValueError(f'{property} name {property_name} not provided for.')

    values = target_table.get(property_name, [])

    # get timner class index
    index = timber_classes.index(timber_class)
    return values[index]
