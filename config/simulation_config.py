# config/simulation_config.py

import os
import tensorflow as tf

# GPU Configuration
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
if os.getenv("CUDA_VISIBLE_DEVICES") is None:
    gpu_num = 0  # Use "" to use the CPU
    if gpu_num != "":
        print(f'\nUsing GPU {gpu_num}\n')
    else:
        print('\nUsing CPU\n')
    os.environ["CUDA_VISIBLE_DEVICES"] = f"{gpu_num}"

# Configure the notebook to use only a single GPU and allocate only as much memory as needed
tf.get_logger().setLevel('ERROR')
gpus = tf.config.list_physical_devices('GPU')
if gpus:
    try:
        tf.config.experimental.set_memory_growth(gpus[0], True)
    except RuntimeError as e:
        print(e)

# Communication direction
DIRECTION = 'downlink'  # 'uplink' or 'downlink'

# 3GPP scenario parameters
SCENARIO = 'umi'  # 'umi', 'uma' or 'rma'

# Number of rings of the hexagonal grid
# With num_rings=1, 7*3=21 base stations are placed
NUM_RINGS = 1

# N. users per sector
NUM_UT_PER_SECTOR = 10

# Max/min distance between base station and served users
MAX_BS_UT_DIST = 80  # [m]
MIN_BS_UT_DIST = 0   # [m]

# Carrier frequency
CARRIER_FREQUENCY = 3.5e9  # [Hz]

# Transmit power for base station and user terminals
BS_MAX_POWER_DBM = 56  # [dBm]
UT_MAX_POWER_DBM = 26  # [dBm]

# Channel is regenerated every coherence_time slots
COHERENCE_TIME = 100  # [slots]

# MCS table index
# Ranges within [1;4] for downlink and [1;2] for uplink, as in TS 38.214
MCS_TABLE_INDEX = 1

# Number of examples
BATCH_SIZE = 1

# OFDM parameters
NUM_OFDM_SYM = 1        # n. OFDM symbols, i.e., time samples, in a slot
NUM_SUBCARRIERS = 128   # N. available subcarriers
SUBCARRIER_SPACING = 15e3  # [Hz] Subcarrier spacing

# Simulation parameters
NUM_SLOTS = 1000  # N. slots to simulate

# Link Adaptation
BLER_TARGET = 0.1    # Must be in [0, 1]
OLLA_DELTA_UP = 0.2

# Uplink power control parameters
ALPHA_UL = 1.0       # Pathloss compensation factor, must be in [0, 1]
P0_DBM_UL = -80.0    # [dBm] Target received power at the base station

# System environment parameters
TEMPERATURE = 294    # Environment temperature for noise power computation
O2I_MODEL = 'low'    # 'low' or 'high'
AVERAGE_STREET_WIDTH = 20.0
AVERAGE_BUILDING_HEIGHT = 10.0
