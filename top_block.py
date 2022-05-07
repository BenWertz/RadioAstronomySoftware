#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Top Block
# GNU Radio version: 3.7.13.5
##################################################
import threading

from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import gr
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from optparse import OptionParser
import osmosdr
import time


class top_block(gr.top_block):

    def __init__(self):
        gr.top_block.__init__(self, "Top Block")

        self._lock = threading.RLock()

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 2e6
        self.integrationFreq = integrationFreq = 4
        self.freq = freq = 1420405752

        ##################################################
        # Blocks
        ##################################################
        self.rtlsdr_source_0_0 = osmosdr.source( args="numchan=" + str(1) + " " + 'rtl=1' )
        self.rtlsdr_source_0_0.set_sample_rate(samp_rate)
        self.rtlsdr_source_0_0.set_center_freq(freq, 0)
        self.rtlsdr_source_0_0.set_freq_corr(0, 0)
        self.rtlsdr_source_0_0.set_dc_offset_mode(2, 0)
        self.rtlsdr_source_0_0.set_iq_balance_mode(2, 0)
        self.rtlsdr_source_0_0.set_gain_mode(False, 0)
        self.rtlsdr_source_0_0.set_gain(34, 0)
        self.rtlsdr_source_0_0.set_if_gain(20, 0)
        self.rtlsdr_source_0_0.set_bb_gain(20, 0)
        self.rtlsdr_source_0_0.set_antenna('', 0)
        self.rtlsdr_source_0_0.set_bandwidth(0, 0)

        self.rtlsdr_source_0 = osmosdr.source( args="numchan=" + str(1) + " " + 'rtl=0' )
        self.rtlsdr_source_0.set_sample_rate(samp_rate)
        self.rtlsdr_source_0.set_center_freq(freq, 0)
        self.rtlsdr_source_0.set_freq_corr(0, 0)
        self.rtlsdr_source_0.set_dc_offset_mode(2, 0)
        self.rtlsdr_source_0.set_iq_balance_mode(2, 0)
        self.rtlsdr_source_0.set_gain_mode(False, 0)
        self.rtlsdr_source_0.set_gain(34, 0)
        self.rtlsdr_source_0.set_if_gain(20, 0)
        self.rtlsdr_source_0.set_bb_gain(20, 0)
        self.rtlsdr_source_0.set_antenna('', 0)
        self.rtlsdr_source_0.set_bandwidth(0, 0)

        self.blocks_sub_xx_1 = blocks.sub_ff(1)
        self.blocks_moving_average_xx_0 = blocks.moving_average_ff(int(0.25*samp_rate), 1, 4000, 1)
        self.blocks_keep_one_in_n_0_0_0 = blocks.keep_one_in_n(gr.sizeof_float*1, int(samp_rate/integrationFreq))
        self.blocks_keep_one_in_n_0_0 = blocks.keep_one_in_n(gr.sizeof_float*1, int(samp_rate/integrationFreq))
        self.blocks_file_sink_0 = blocks.file_sink(gr.sizeof_float*1, 'C:\\Users\\benwe\\EOS_OUTPUT1.dat', False)
        self.blocks_file_sink_0.set_unbuffered(True)
        self.blocks_complex_to_mag_squared_0_0 = blocks.complex_to_mag_squared(1)
        self.blocks_complex_to_mag_squared_0 = blocks.complex_to_mag_squared(1)



        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_complex_to_mag_squared_0, 0), (self.blocks_keep_one_in_n_0_0, 0))
        self.connect((self.blocks_complex_to_mag_squared_0_0, 0), (self.blocks_keep_one_in_n_0_0_0, 0))
        self.connect((self.blocks_keep_one_in_n_0_0, 0), (self.blocks_sub_xx_1, 0))
        self.connect((self.blocks_keep_one_in_n_0_0_0, 0), (self.blocks_sub_xx_1, 1))
        self.connect((self.blocks_moving_average_xx_0, 0), (self.blocks_file_sink_0, 0))
        self.connect((self.blocks_sub_xx_1, 0), (self.blocks_moving_average_xx_0, 0))
        self.connect((self.rtlsdr_source_0, 0), (self.blocks_complex_to_mag_squared_0, 0))
        self.connect((self.rtlsdr_source_0_0, 0), (self.blocks_complex_to_mag_squared_0_0, 0))

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        with self._lock:
            self.samp_rate = samp_rate
            self.rtlsdr_source_0_0.set_sample_rate(self.samp_rate)
            self.rtlsdr_source_0.set_sample_rate(self.samp_rate)
            self.blocks_moving_average_xx_0.set_length_and_scale(int(0.25*self.samp_rate), 1)
            self.blocks_keep_one_in_n_0_0_0.set_n(int(self.samp_rate/self.integrationFreq))
            self.blocks_keep_one_in_n_0_0.set_n(int(self.samp_rate/self.integrationFreq))

    def get_integrationFreq(self):
        return self.integrationFreq

    def set_integrationFreq(self, integrationFreq):
        with self._lock:
            self.integrationFreq = integrationFreq
            self.blocks_keep_one_in_n_0_0_0.set_n(int(self.samp_rate/self.integrationFreq))
            self.blocks_keep_one_in_n_0_0.set_n(int(self.samp_rate/self.integrationFreq))

    def get_freq(self):
        return self.freq

    def set_freq(self, freq):
        with self._lock:
            self.freq = freq
            self.rtlsdr_source_0_0.set_center_freq(self.freq, 0)
            self.rtlsdr_source_0.set_center_freq(self.freq, 0)


def main(top_block_cls=top_block, options=None):

    tb = top_block_cls()
    tb.start()
    tb.wait()


if __name__ == '__main__':
    main()
