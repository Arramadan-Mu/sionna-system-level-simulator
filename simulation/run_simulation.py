# simulation/run_simulation.py

import tensorflow as tf
import numpy as np
from sionna.phy.channel.tr38901 import PanelArray
from sionna.phy.ofdm import ResourceGrid

from models.system_simulator import SystemLevelSimulator
from utils.results_utils import clean_hist
from visualization.plots import (plot_performance_metrics, show_network_topology,
                                plot_sinr_mcs_throughput, plot_bler_mcs_olla, 
                                plot_pf_resources_mcs)


def create_antenna_arrays(carrier_frequency):
    """
    Create the antenna arrays for base stations and user terminals
    """
    # Create the antenna arrays at the base stations
    bs_array = PanelArray(num_rows_per_panel=2,
                          num_cols_per_panel=3,
                          polarization='dual',
                          polarization_type='VH',
                          antenna_pattern='38.901',
                          carrier_frequency=carrier_frequency)

    # Create the antenna array at the user terminals
    ut_array = PanelArray(num_rows_per_panel=1,
                          num_cols_per_panel=1,
                          polarization='single',
                          polarization_type='V',
                          antenna_pattern='omni',
                          carrier_frequency=carrier_frequency)
    
    return bs_array, ut_array


def create_resource_grid(num_ofdm_sym, num_subcarriers, subcarrier_spacing, 
                        num_ut_per_sector, ut_array):
    """
    Create the OFDM resource grid
    """
    resource_grid = ResourceGrid(num_ofdm_symbols=num_ofdm_sym,
                                 fft_size=num_subcarriers,
                                 subcarrier_spacing=subcarrier_spacing,
                                 num_tx=num_ut_per_sector,
                                 num_streams_per_tx=ut_array.num_ant)
    return resource_grid


def initialize_system_simulator(config):
    """
    Initialize the system level simulator with given configuration
    """
    # Create antenna arrays
    bs_array, ut_array = create_antenna_arrays(config.CARRIER_FREQUENCY)
    
    # Create resource grid
    resource_grid = create_resource_grid(
        config.NUM_OFDM_SYM, 
        config.NUM_SUBCARRIERS, 
        config.SUBCARRIER_SPACING,
        config.NUM_UT_PER_SECTOR, 
        ut_array
    )
    
    # Initialize SystemLevelSimulator
    sls = SystemLevelSimulator(
        config.BATCH_SIZE,
        config.NUM_RINGS,
        config.NUM_UT_PER_SECTOR,
        config.CARRIER_FREQUENCY,
        resource_grid,
        config.SCENARIO,
        config.DIRECTION,
        ut_array,
        bs_array,
        config.BS_MAX_POWER_DBM,
        config.UT_MAX_POWER_DBM,
        config.COHERENCE_TIME,
        max_bs_ut_dist=config.MAX_BS_UT_DIST,
        min_bs_ut_dist=config.MIN_BS_UT_DIST,
        temperature=config.TEMPERATURE,
        o2i_model=config.O2I_MODEL,
        average_street_width=config.AVERAGE_STREET_WIDTH,
        average_building_height=config.AVERAGE_BUILDING_HEIGHT
    )
    
    return sls


def run_simulation(config):
    """
    Run the complete system-level simulation
    """
    print("Initializing system...")
    sls = initialize_system_simulator(config)
    
    print("Showing network topology...")
    topology_fig = show_network_topology(sls)
    
    print("Running simulation...")
    # Convert configuration values to TensorFlow constants
    num_slots = tf.constant(config.NUM_SLOTS, tf.int32)
    bler_target = tf.constant(config.BLER_TARGET, tf.float32)
    olla_delta_up = tf.constant(config.OLLA_DELTA_UP, tf.float32)
    alpha_ul = tf.constant(config.ALPHA_UL, tf.float32)
    p0_dbm_ul = tf.constant(config.P0_DBM_UL, tf.float32)
    
    # System-level simulations
    hist = sls(num_slots,
               alpha_ul,
               p0_dbm_ul,
               bler_target,
               olla_delta_up)
    
    print("Processing results...")
    hist = clean_hist(hist)
    
    # Average across slots and store in dictionary
    results_avg = {
        'TBLER': (1 - np.nanmean(hist['harq'], axis=0)).flatten(),
        'MCS': np.nanmean(hist['mcs_index'], axis=0).flatten(),
        '# decoded bits / slot': np.nanmean(hist['num_decoded_bits'], axis=0).flatten(),
        'Effective SINR [dB]': 10*np.log10(np.nanmean(hist['sinr_eff'], axis=0).flatten()),
        'OLLA offset': np.nanmean(hist['olla_offset'], axis=0).flatten(),
        'TX power [dBm]': 10*np.log10(np.nanmean(hist['tx_power'], axis=0).flatten()) + 30,
        'Pathloss [dB]': 10*np.log10(np.nanmean(hist['pathloss_serving_cell'], axis=0).flatten()),
        '# allocated REs / slot': np.nanmean(hist['num_allocated_re'], axis=0).flatten(),
        'PF metric': np.nanmean(hist['pf_metric'], axis=0).flatten()
    }
    
    print("Creating plots...")
    # Generate all plots
    metrics_fig = plot_performance_metrics(results_avg, config.BLER_TARGET)
    sinr_fig, sinr_axs = plot_sinr_mcs_throughput(results_avg)
    bler_fig, bler_axs = plot_bler_mcs_olla(results_avg, config.BLER_TARGET)
    pf_fig, pf_axs = plot_pf_resources_mcs(results_avg)
    
    return {
        'simulator': sls,
        'results': hist,
        'results_avg': results_avg,
        'figures': {
            'topology': topology_fig,
            'metrics': metrics_fig,
            'sinr_mcs_throughput': sinr_fig,
            'bler_mcs_olla': bler_fig,
            'pf_resources_mcs': pf_fig
        }
    }
