# Bertini Precision Demonstration Program
# This program shows how different precision settings affect polynomial calculations

import bertini
import numpy as np
import time


def setup_simple_system():
    """Create a simple polynomial system for testing precision"""
    # Create variables
    x = bertini.function_tree.symbol.Variable("x")
    y = bertini.function_tree.symbol.Variable("y")

    # Define polynomial system: circle intersecting with line
    # f1: x^2 + y^2 - 1 = 0  (unit circle)
    # f2: x + y - 0.1234567890123456789 = 0  (line with high precision constant)
    f1 = x ** 2 + y ** 2 - 1
    f2 = x + y - bertini.multiprec.complex("0.1234567890123456789012345678901234567890")

    # Create system
    sys = bertini.System()

    # Create variable group
    var_group = bertini.VariableGroup()
    var_group.append(x)
    var_group.append(y)
    sys.add_variable_group(var_group)

    # Add functions to system
    sys.add_function(f1)
    sys.add_function(f2)

    return sys, x, y


def test_double_precision():
    """Test calculations using double precision"""
    print("=" * 60)
    print("DOUBLE PRECISION TEST")
    print("=" * 60)

    sys, x, y = setup_simple_system()

    # Create total degree start system
    td = bertini.TotalDegree(sys)

    # Create homotopy
    t = bertini.function_tree.symbol.Variable("t")
    homotopy = (1 - t) * sys + t * td
    homotopy.add_path_variable(t)

    # Use double precision tracker
    tracker = bertini.tracking.DoublePrecisionTracker(homotopy)
    tracker.set_tolerance(1e-12)

    print(f"Default precision: {bertini.default_precision()} bits")
    print(f"Tracker tolerance: {tracker.tolerance()}")

    # Track a path
    start_time = time.time()
    result = bertini.VectorXd()  # Double precision vector

    try:
        tracker.track_path(result,
                           1.0,  # start time
                           0.0,  # end time
                           td.start_point_d(0))  # start point in double precision

        end_time = time.time()

        print(f"Solution found in {end_time - start_time:.6f} seconds")
        print(f"Solution: x = {result[0]}, y = {result[1]}")
        print(f"Verification: x + y = {result[0] + result[1]}")
        print(f"Verification: xÂ² + yÂ² = {result[0] ** 2 + result[1] ** 2}")

    except Exception as e:
        print(f"Error in double precision tracking: {e}")


def test_multiple_precision(precision_bits=128):
    """Test calculations using fixed multiple precision"""
    print("=" * 60)
    print(f"MULTIPLE PRECISION TEST ({precision_bits} bits)")
    print("=" * 60)

    # Set precision globally
    old_precision = bertini.default_precision()
    bertini.set_precision(precision_bits)

    sys, x, y = setup_simple_system()

    # Create total degree start system
    td = bertini.TotalDegree(sys)

    # Create homotopy
    t = bertini.function_tree.symbol.Variable("t")
    homotopy = (1 - t) * sys + t * td
    homotopy.add_path_variable(t)

    # Use multiple precision tracker
    tracker = bertini.tracking.MultiplePrecisionTracker(homotopy)
    tracker.set_tolerance(bertini.multiprec.complex("1e-30"))

    print(f"Current precision: {bertini.default_precision()} bits")
    print(f"Tracker tolerance: {tracker.tolerance()}")

    # Track a path
    start_time = time.time()
    result = bertini.VectorXmp()  # Multiple precision vector

    try:
        tracker.track_path(result,
                           bertini.multiprec.complex(1),  # start time
                           bertini.multiprec.complex(0),  # end time
                           td.start_point_mp(0))  # start point in multiple precision

        end_time = time.time()

        print(f"Solution found in {end_time - start_time:.6f} seconds")
        print(f"Solution: x = {result[0]}")
        print(f"Solution: y = {result[1]}")
        print(f"Verification: x + y = {result[0] + result[1]}")
        print(f"Verification: xÂ² + yÂ² = {result[0] ** 2 + result[1] ** 2}")

        # Show more digits
        print(f"High precision x: {result[0].str(50)}")  # Show 50 digits
        print(f"High precision y: {result[1].str(50)}")  # Show 50 digits

    except Exception as e:
        print(f"Error in multiple precision tracking: {e}")
    finally:
        # Restore original precision
        bertini.set_precision(old_precision)


def test_adaptive_precision():
    """Test calculations using adaptive precision"""
    print("=" * 60)
    print("ADAPTIVE PRECISION TEST")
    print("=" * 60)

    sys, x, y = setup_simple_system()

    # Create total degree start system
    td = bertini.TotalDegree(sys)

    # Create homotopy
    t = bertini.function_tree.symbol.Variable("t")
    homotopy = (1 - t) * sys + t * td
    homotopy.add_path_variable(t)

    # Use adaptive precision tracker
    tracker = bertini.tracking.AMPTracker(homotopy)
    tracker.set_tolerance(bertini.multiprec.complex("1e-50"))

    print(f"Default precision: {bertini.default_precision()} bits")
    print(f"Tracker tolerance: {tracker.tolerance()}")

    # Track a path
    start_time = time.time()
    result = bertini.VectorXmp()  # Multiple precision vector for AMP

    try:
        tracker.track_path(result,
                           bertini.multiprec.complex(1),  # start time
                           bertini.multiprec.complex(0),  # end time
                           td.start_point_mp(0))  # start point

        end_time = time.time()

        print(f"Solution found in {end_time - start_time:.6f} seconds")
        print(f"Final precision used: {result[0].precision()} bits")
        print(f"Solution: x = {result[0]}")
        print(f"Solution: y = {result[1]}")
        print(f"Verification: x + y = {result[0] + result[1]}")
        print(f"Verification: xÂ² + yÂ² = {result[0] ** 2 + result[1] ** 2}")

        # Show maximum available digits
        max_digits = int(result[0].precision() * 0.301)  # Convert bits to decimal digits
        print(f"Ultra-high precision x: {result[0].str(max_digits)}")
        print(f"Ultra-high precision y: {result[1].str(max_digits)}")

    except Exception as e:
        print(f"Error in adaptive precision tracking: {e}")


def precision_comparison():
    """Compare precision capabilities"""
    print("=" * 60)
    print("PRECISION COMPARISON")
    print("=" * 60)

    # Test different precision values
    test_value = "0.1234567890123456789012345678901234567890"

    print("Creating high-precision constant:")
    print(f"Input string: {test_value}")

    # Double precision representation
    double_val = float(test_value)
    print(f"Double precision:     {double_val:.16f}")

    # Multiple precision representations
    for bits in [64, 128, 256, 512]:
        bertini.set_precision(bits)
        mp_val = bertini.multiprec.complex(test_value)
        digits = int(bits * 0.301)  # Approximate decimal digits
        print(f"{bits:3d} bit precision:   {mp_val.str(min(digits, 50))}")

    # Reset to default
    bertini.set_precision(53)


def main():
    """Main demonstration function"""
    print("PyBertini Precision Demonstration")
    print("This program demonstrates different precision levels in polynomial solving")
    print()

    try:
        # Show precision comparison first
        precision_comparison()
        print()

        # Test different tracker precisions
        test_double_precision()
        print()

        test_multiple_precision(128)
        print()

        test_multiple_precision(256)
        print()

        test_adaptive_precision()
        print()

        print("=" * 60)
        print("DEMONSTRATION COMPLETE")
        print("=" * 60)
        print("Key observations:")
        print("1. Double precision: Fast but limited to ~15-16 digits")
        print("2. Multiple precision: Slower but user-controlled precision")
        print("3. Adaptive precision: Automatically adjusts precision as needed")
        print("4. Higher precision requires more computation time")
        print("5. Bertini can handle up to 3328 bits of precision")

    except Exception as e:
        print(f"Error running demonstration: {e}")
        print("Make sure PyBertini is properly installed and configured")


if __name__ == "__main__":
    main()