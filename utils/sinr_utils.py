# utils/sinr_utils.py

import tensorflow as tf
from sionna.phy.utils import db_to_lin, log2, insert_dims
from sionna.phy.ofdm import RZFPrecodedChannel, EyePrecodedChannel, \
    LMMSEPostEqualizationSINR


def get_sinr(tx_power,
             stream_management,
             no,
             direction,
             h_freq_fading,
             num_bs,
             num_ut_per_sector,
             num_streams_per_ut,
             resource_grid):
    """ Compute post-equalization SINR. It is assumed:
     - DL: Regularized zero-forcing precoding
     - UL: No precoding, only power allocation
    LMMSE equalizer is used in both DL and UL.
    """
    # tx_power: [batch_size, num_bs, num_tx_per_sector,
    #            num_streams_per_tx, num_ofdm_sym, num_subcarriers]
    # Flatten across sectors
    # [batch_size, num_tx, num_streams_per_tx, num_ofdm_symbols, num_subcarriers]
    s = tx_power.shape
    tx_power = tf.reshape(tx_power, [s[0], s[1]*s[2]] + s[3:])

    # Compute SINR
    # [batch_size, num_ofdm_sym, num_subcarriers, num_ut,
    #  num_streams_per_ut]
    if direction == 'downlink':
        # Regularized zero-forcing precoding in the DL
        precoded_channel = RZFPrecodedChannel(resource_grid=resource_grid,
                                              stream_management=stream_management)
        h_eff = precoded_channel(h_freq_fading,
                                 tx_power=tx_power,
                                 alpha=no)  # Regularizer
    else:
        # No precoding in the UL: just power allocation
        precoded_channel = EyePrecodedChannel(resource_grid=resource_grid,
                                              stream_management=stream_management)
        h_eff = precoded_channel(h_freq_fading,
                                 tx_power=tx_power)

    # LMMSE equalizer
    lmmse_posteq_sinr = LMMSEPostEqualizationSINR(resource_grid=resource_grid,
                                                  stream_management=stream_management)
    # Post-equalization SINR
    # [batch_size, num_ofdm_symbols, num_subcarriers, num_rx, num_streams_per_rx]
    sinr = lmmse_posteq_sinr(h_eff, no=no, interference_whitening=True)

    # [batch_size, num_ofdm_symbols, num_subcarriers, num_ut, num_streams_per_ut]
    sinr = tf.reshape(
        sinr, sinr.shape[:-2] + [num_bs*num_ut_per_sector, num_streams_per_ut])

    # Regroup by sector
    # [batch_size, num_ofdm_symbols, num_subcarriers, num_bs, num_ut_per_sector, num_streams_per_ut]
    sinr = tf.reshape(
        sinr, sinr.shape[:-2] + [num_bs, num_ut_per_sector, num_streams_per_ut])

    # [batch_size, num_bs, num_ofdm_sym, num_subcarriers, num_ut_per_sector, num_streams_per_ut]
    sinr = tf.transpose(sinr, [0, 3, 1, 2, 4, 5])
    return sinr


def estimate_achievable_rate(sinr_eff_db_last,
                             num_ofdm_sym,
                             num_subcarriers):
    """ Estimate achievable rate """
    # [batch_size, num_bs, num_ut_per_sector]
    rate_achievable_est = log2(tf.cast(1, sinr_eff_db_last.dtype) +
                               db_to_lin(sinr_eff_db_last))

    # Broadcast to time/frequency grid
    # [batch_size, num_bs, num_ofdm_sym, num_subcarriers, num_ut_per_sector]
    rate_achievable_est = insert_dims(
        rate_achievable_est, 2, axis=-2)
    rate_achievable_est = tf.tile(rate_achievable_est,
                                  [1, 1, num_ofdm_sym, num_subcarriers, 1])
    return rate_achievable_est
