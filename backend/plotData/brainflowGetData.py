### Example from https://brainflow.org/2021-07-05-real-time-example/

import argparse
import logging

import pyqtgraph as pg
from brainflow.board_shim import BoardShim, BrainFlowInputParams, BoardIds
from brainflow.data_filter import DataFilter, FilterTypes, DetrendOperations
from pyqtgraph.Qt import QtGui, QtCore
import numpy as np
from datetime import datetime
from datetime import date
import time
# from predict import predict
# from parse_offline_data import parse
data_collection = True

class Graph:
    def __init__(self, board_shim, start_time):
        self.name = start_time
        self.board_id = board_shim.get_board_id()
        self.board_shim = board_shim
        self.eeg_channels = BoardShim.get_eeg_channels(self.board_id)
        self.sampling_rate = BoardShim.get_sampling_rate(self.board_id)
        self.update_speed_ms = 100
        self.window_size = 0.1 # need to make this 100 ms
        self.num_points = int(self.window_size * self.sampling_rate)

        self.app = QtGui.QApplication([])
        self.win = pg.GraphicsWindow(title='BrainFlow Plot', size=(800, 600))

        self._init_timeseries()

        timer = QtCore.QTimer()
        timer.timeout.connect(self.update)
        timer.start(self.update_speed_ms)
        QtGui.QApplication.instance().exec_()

    def _init_timeseries(self):
        self.plots = list()
        self.curves = list()
        for i in range(len(self.eeg_channels)):
            p = self.win.addPlot(row=i, col=0)
            p.showAxis('left', False)
            p.setMenuEnabled('left', False)
            p.showAxis('bottom', False)
            p.setMenuEnabled('bottom', False)
            if i == 0:
                p.setTitle('TimeSeries Plot')
            self.plots.append(p)
            curve = p.plot()
            self.curves.append(curve)

    def update(self):
        data = self.board_shim.get_current_board_data(self.num_points)

        # Save raw data
        DataFilter.write_file(data, "RawEEG_"+self.name+".txt", 'a')  # use 'a' for append mode

        for count, channel in enumerate(self.eeg_channels):
            # plot timeseries
            DataFilter.detrend(data[channel], DetrendOperations.CONSTANT.value)
            DataFilter.perform_bandpass(data[channel], self.sampling_rate, 3.0, 45.0, 2,
                                        FilterTypes.BUTTERWORTH.value, 0)
            DataFilter.perform_bandstop(data[channel], self.sampling_rate, 48.0, 52.0, 2,
                                        FilterTypes.BUTTERWORTH.value, 0)
            DataFilter.perform_bandstop(data[channel], self.sampling_rate, 58.0, 62.0, 2,
                                        FilterTypes.BUTTERWORTH.value, 0)
            self.curves[count].setData(data[channel].tolist())

        self.app.processEvents()
        

def start(boardType):
    BoardShim.enable_dev_board_logger()
    logging.basicConfig(level=logging.DEBUG)

    parser = argparse.ArgumentParser()
    # use docs to check which parameters are required for specific board, e.g. for Cyton - set serial port

    parser.add_argument('--timeout', type=int, help='timeout for device discovery or connection', required=False,
                            default=0)
    parser.add_argument('--ip-port', type=int, help='ip port', required=False, default=0)
    parser.add_argument('--ip-protocol', type=int, help='ip protocol, check IpProtocolType enum', required=False,
                        default=0)
    parser.add_argument('--ip-address', type=str, help='ip address', required=False, default='')
    parser.add_argument('--mac-address', type=str, help='mac address', required=False, default='')
    parser.add_argument('--other-info', type=str, help='other info', required=False, default='')
    parser.add_argument('--streamer-params', type=str, help='streamer params', required=False, default='')
    parser.add_argument('--serial-number', type=str, help='serial number', required=False, default='')
    parser.add_argument('--file', type=str, help='file', required=False, default='')

    if(boardType == "Synthetic"):
        print("Synthetic board starts")
        
        parser.add_argument('--serial-port', type=str, help='serial port', required=False, default='')
        parser.add_argument('--board-id', type=int, help='board id, check docs to get a list of supported boards',
                            required=False, default=BoardIds.SYNTHETIC_BOARD)
    elif(boardType == "Cyton"):
        print("Cyton board starts")
        
        parser.add_argument('--serial-port', type=str, help='serial port', required=False, default="ttyUSB0")
        parser.add_argument('--board-id', type=int, help='board id, check docs to get a list of supported boards',
                            required=False, default=BoardIds.CYTON_DAISY_BOARD)
    else:
        print("Please choose between Synthetic and Cyton boards")

    args = parser.parse_args()

    params = BrainFlowInputParams()
    params.ip_port = args.ip_port
    params.serial_port = args.serial_port
    params.mac_address = args.mac_address
    params.other_info = args.other_info
    params.serial_number = args.serial_number
    params.ip_address = args.ip_address
    params.ip_protocol = args.ip_protocol
    params.timeout = args.timeout
    params.file = args.file

    # Create file name based on current time
    today = date.today()
    now = datetime.now()
    current_time = today.strftime("%Y%m%d_") + now.strftime("%H%M%S")
    # print(current_time)
    n400_list = []
    
    try:
        board_shim = BoardShim(args.board_id, params)
        
        board_shim.prepare_session()
        board_shim.start_stream(450000, args.streamer_params)
        # print(board_shim.get_current_board_data(256))

        if data_collection:
            time.sleep(10) # set how long we're recording for
        else:
            # wait for post
            pass



        data = board_shim.get_board_data()
        DataFilter.write_file(data, "RawEEG_"+current_time+".txt", 'a')  # use 'a' for append mode

        if not data_collection:
            X, _, words = parse("RawEEG_"+current_time+".txt") ####
            preds = predict(X)

            for i in range(len(preds)):
                if preds[i] == 1:
                    n400_list.append(words[i])


            summary = api_call(n400_list)

            # send summary to frontend to display


    except BaseException:
        logging.warning('Exception', exc_info=True)
    finally:
        logging.info('End')
        if board_shim.is_prepared():
            logging.info('Releasing session')
            board_shim.release_session()
 

# def main(boardType):
#     start(boardType)

if __name__ == '__main__':
    main("Cyton") # Or "Synthetic"

