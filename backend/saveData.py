import argparse
import time
import numpy as np
import pandas as pd
import os

import brainflow
from brainflow.board_shim import BoardShim, BrainFlowInputParams, LogLevels, BoardIds
from brainflow.data_filter import DataFilter, FilterTypes, AggOperations

def createDataFolder(currentDir):
    folderName = "data"
    folderPath = os.path.join(currentDir, folderName)
    if(not os.path.exists(folderPath)):
        os.mkdir(folderPath)
    return folderPath

def initializeBoard(boardName, comNum):
    if(boardName == "S"):
        # Synthetic board
        params = BrainFlowInputParams ()
        board_id = BoardIds.SYNTHETIC_BOARD.value # Synthetic board
    elif(boardName == "C"):
        # Cyton board
        params.serial_port = comNum
        board_id = BoardIds.CYTON_BOARD
    else:
        print("Please have boardName as \"S\" or \"C\"")

    board = BoardShim (board_id, params)
    return board

def getData (dataPath, board):
    BoardShim.enable_dev_board_logger ()    
    board.prepare_session ()
    board.start_stream ()
    BoardShim.log_message (LogLevels.LEVEL_INFO.value, 'start sleeping in the main thread')
    time.sleep (10)
    data = board.get_current_board_data (20) # get 20 latest data points dont remove them from internal buffer
    board.stop_stream ()
    board.release_session ()

    # demo how to convert it to pandas DF and plot data
    eeg_channels = BoardShim.get_eeg_channels (BoardIds.SYNTHETIC_BOARD.value)
    df = pd.DataFrame (np.transpose (data))
    print ('Data From the Board')
    print (df.head (10))

    # demo for data serialization using brainflow API, we recommend to use it instead pandas.to_csv()
    dataFilePath = os.path.join(dataPath, 'test.csv')
    DataFilter.write_file (data, dataFilePath, 'w') # use 'a' for append mode
    restored_data = DataFilter.read_file (dataFilePath)
    restored_df = pd.DataFrame (np.transpose (restored_data))
    print ('Data From the File')
    print (restored_df.head (10))


if __name__ == "__main__":
    currentDir = os.getcwd()
    dataPath = createDataFolder(currentDir)
    board = initializeBoard("S", "COM3") # "S" = Synthetic, "C" = Cyton
    getData (dataPath, board)