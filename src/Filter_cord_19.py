import pandas as pd

file = pd.read_csv('D:/NLP/EasyNER/data/metadata.csv')
print(file['license'],file['cord_uid'])
