import pandas as pd 
import os
from datetime import datetime


# file = os.path.join(os.path.dirname(__file__),'../data/file.csv')

# df = pd.read_csv(file)

# print(df.columns)

today = datetime.now().date()
print("We are here:",today)