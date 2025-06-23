import numpy as np
from mean_var_std import calculate

# Example usage
if __name__ == "__main__":
    # Test the function
    my_list = np.arange(9)
    result = calculate(my_list)
    
    print("\nResult:\n", result)
