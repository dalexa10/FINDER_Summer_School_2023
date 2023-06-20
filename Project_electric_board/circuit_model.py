import math

# Check 1: Make sure the components are on the board
def is_component_inside(board_width, board_height, component_x, component_y, margin=0.1):
    """ Determines if components are on the board """
    if (margin <= component_x < board_width - margin) and (margin <= component_y < board_height - margin):
        return True
    else:
        return False
    
def are_components_on_board(design_parameters):
    board_width = design_parameters['board_width']
    board_height = design_parameters['board_height']
    components = ['L', 'D', 'C', 'S']

    for component in components:
        component_x = design_parameters[component + '_x']
        component_y = design_parameters[component + '_y']
        if not is_component_inside(board_width, board_height, component_x, component_y):
            return False

    return True

# Check 2: Check for capacitor strain
def compute_deflection(F, E, I, l, a, x):
    b = l - a
    numerator = F * b**2 * x**2 * (x * (3 * a + b) - 3 * a * l)
    denominator = 6 * E * I * l**3
    deflection = numerator / denominator
    return deflection

def compute_slope(F, E, I, l, a, x):
    b = l - a
    numerator = F * b**2 * (3 * a + 3 * b - 6 * x) * x
    denominator = 6 * E * I * l**3
    slope = numerator / denominator
    return slope

def compute_strain(F, E, I, l, a, x):
    b = l - a
    numerator = F * b**2 * (x*(3*a+b) - a * l)
    denominator = E*I*l**3
    strain = numerator / denominator
    return strain

def compute_capacitor_strain(design_parameters):
    board_width = design_parameters['board_width']
    board_height = design_parameters['board_height']
    thickness = 0.1  # Board Thickness
    L_x = design_parameters['L_x']
    C_x = design_parameters['C_x']
    # Compute the moment of inertia (I) for a rectangular cross-section
    I = (board_height * thickness**3) / 12
    l = board_width
    E = 2.4e10  # Young's modulus of Board
    # Location of the Inductor
    a = L_x 
    F = 1  # Assume a constant max value dynamic force from inductor vibration
    # Location of Capacitor
    x = C_x 
    
    # Compute slope
    strain = compute_strain(F, E, I, l, a, x)
    return strain
    
def is_capacitor_safe(design_parameters):
    critical_strain = 2.0e-7
    strain = compute_capacitor_strain(design_parameters)
    if abs(strain) > critical_strain:
        return False
    return True


# Check 3: Thermal contraction of switch

def compute_kernel_distances(design_parameters, bandwidth, threshold):
    L_x = design_parameters['L_x']
    L_y = design_parameters['L_y']
    C_x = design_parameters['C_x']
    C_y = design_parameters['C_y']
    D_x = design_parameters['D_x']
    D_y = design_parameters['D_y']
    S_x = design_parameters['S_x']
    S_y = design_parameters['S_y']

    # Computing proximity using Euclidean distance
    LS_distance = math.sqrt((S_x - L_x)**2 + (S_y - L_y)**2)
    CS_distance = math.sqrt((S_x - C_x)**2 + (S_y - C_y)**2)
    DS_distance = math.sqrt((S_x - D_x)**2 + (S_y - D_y)**2)

    # Computing RBF kernel distances
    LS_kernel_distance = math.exp(-(LS_distance**2) / (2 * bandwidth**2))
    CS_kernel_distance = math.exp(-(CS_distance**2) / (2 * bandwidth**2))
    DS_kernel_distance = math.exp(-(DS_distance**2) / (2 * bandwidth**2))

    # Creating a list of kernel distances
    kernel_distances = [LS_kernel_distance, CS_kernel_distance, DS_kernel_distance]
    #print(kernel_distances)
    return kernel_distances

def is_thermal_cycling_safe(design_parameters, bandwidth = 0.5, threshold=0.8):
    kernel_distances = compute_kernel_distances(design_parameters, bandwidth, threshold)
    # Finding the maximum kernel distance
    max_kernel_distance = max(kernel_distances)

    # Comparing the maximum kernel distance to the threshold value
    is_below_threshold = max_kernel_distance <= threshold

    return is_below_threshold

def is_device_safe(design_parameters):
    on_board = are_components_on_board(design_parameters)
    cap_safe = is_capacitor_safe(design_parameters)
    thermal_safe = is_thermal_cycling_safe(design_parameters)
    is_board_safe = (on_board and cap_safe and thermal_safe)
    return is_board_safe