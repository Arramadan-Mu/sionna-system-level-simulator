# main.py

"""
Main entry point for the Sionna system-level simulation.
This script reproduces the exact same functionality as the original End-to-End_Example.py
"""

import os
import sys

# Import Sionna
try:
    import sionna.sys
except ImportError as e:
    import sys
    if 'google.colab' in sys.modules:
       # Install Sionna in Google Colab
       print("Installing Sionna and restarting the runtime. Please run the cell again.")
       os.system("pip install sionna")
       os.kill(os.getpid(), 5)
    else:
       raise e

# Additional external libraries
import matplotlib.pyplot as plt
import numpy as np

# Sionna components
import sionna.phy.config
#import sionna.phy.dtypes

# Set random seed for reproducibility
sionna.phy.config.seed = 42

# Internal computational precision
sionna.phy.config.precision = 'single'  # 'single' or 'double'

# Import our modular components
import config.simulation_config as config
from simulation.run_simulation import run_simulation


def main():
    """
    Main function that executes the complete simulation workflow
    """
    print("=" * 60)
    print("SIONNA SYSTEM-LEVEL SIMULATION")
    print("=" * 60)
    print(f"Configuration:")
    print(f"  - Direction: {config.DIRECTION}")
    print(f"  - Scenario: {config.SCENARIO}")
    print(f"  - Carrier frequency: {config.CARRIER_FREQUENCY/1e9:.1f} GHz")
    print(f"  - Number of rings: {config.NUM_RINGS}")
    print(f"  - Users per sector: {config.NUM_UT_PER_SECTOR}")
    print(f"  - Number of slots: {config.NUM_SLOTS}")
    print(f"  - Batch size: {config.BATCH_SIZE}")
    print("=" * 60)
    
    try:
        # Run the complete simulation
        results = run_simulation(config)
        
        print("Simulation completed successfully!")
        print("=" * 60)
        print("RESULTS SUMMARY:")
        print("=" * 60)
        
        # Print some key metrics
        results_avg = results['results_avg']
        print(f"Average TBLER: {np.mean(results_avg['TBLER']):.3f}")
        print(f"Average MCS: {np.mean(results_avg['MCS']):.1f}")
        print(f"Average throughput (decoded bits/slot): {np.mean(results_avg['# decoded bits / slot']):.0f}")
        print(f"Average effective SINR: {np.mean(results_avg['Effective SINR [dB]']):.1f} dB")
        print(f"Average TX power: {np.mean(results_avg['TX power [dBm]']):.1f} dBm")
        print("=" * 60)
        
        # Show all plots
        print("Displaying plots...")
        plt.show()
        
        return results
        
    except Exception as e:
        print(f"Error during simulation: {e}")
        import traceback
        traceback.print_exc()
        return None


if __name__ == "__main__":
    results = main()
    
    if results is not None:
        print("\nSimulation data is available in the 'results' variable.")
        print("Available components:")
        print("  - results['simulator']: SystemLevelSimulator instance")
        print("  - results['results']: Raw simulation history")
        print("  - results['results_avg']: Averaged results dictionary")
        print("  - results['figures']: Dictionary of matplotlib figures")
        print("\nPlots have been generated and displayed.")
    else:
        print("\nSimulation failed. Please check the error messages above.")
