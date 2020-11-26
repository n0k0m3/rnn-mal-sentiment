import importlib
import pickle
import pandas as pd


class PickleProtocol:
    def __init__(self, level):
        self.previous = pickle.HIGHEST_PROTOCOL
        self.level = level

    def __enter__(self):
        importlib.reload(pickle)
        pickle.HIGHEST_PROTOCOL = self.level

    def __exit__(self, *exc):
        importlib.reload(pickle)
        pickle.HIGHEST_PROTOCOL = self.previous


def pickle_protocol(level):
    return PickleProtocol(level)


df = pd.read_hdf("data.h5")
with pickle_protocol(4):
    df.to_hdf("data.h5", "df", mode='w')
