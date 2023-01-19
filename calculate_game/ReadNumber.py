import pandas as pd
import numpy as np
import random 

class ReadNumber():
    def __init__(self, path):
        #10にできる数を読み込む
        self.filepath = path
        self.df = pd.read_csv(self.filepath)
        self.n = self.df["n"].to_list()  

    def get_number(self):
        return np.reshape(random.sample(self.n, 64), (8, 8))



