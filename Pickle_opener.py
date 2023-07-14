import pickle
from pprint import pprint
path = 'data/2/Player_2_data.pickle'
with open(path, 'rb') as file:
    data = pickle.load(file)

for attribute in dir(data):
    if not attribute.startswith('__'):
        value = getattr(data, attribute)
        print("")
        pprint(f'{attribute}: {value}')
