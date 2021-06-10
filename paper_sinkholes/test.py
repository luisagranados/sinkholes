import numpy as np 

datos = [847.599976,296.500000,1097.800049,13.000000,112.000000,336.500000
]

print(np.std(datos, ddof=1) / np.sqrt(len(datos)))