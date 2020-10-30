from head import *

os.chdir('/home/artem/Desktop/programming/data_analysis/digits')
df = pd.read_csv('data/digit.dat', sep=';')
df = df.drop(axis=1, columns=['A2', 'B2', 'C2', 'D2', 'E2', 'F2', 'G2', 'H2'])
Y = df['A']
df = df.drop(axis=1, columns=['A'])

for i in range(df.shape[0]):
    for j in range(df.shape[1]):
        if (df.iat[i, j] == "ONE "):
            df.iat[i, j] = 1
        else:
            df.iat[i, j] = 0

df.astype('int32')

m = {}
m['eight'] = 8
m['nine '] = 9
m['three'] = 3
m['five '] = 5
m['four '] = 4
m['six  '] = 6
m['seven'] = 7
m['one  '] = 1
m['two  '] = 2
m['zero '] = 0

for i in range(len(Y)):
    if (not Y[i] in range(0, 10)):
        Y[i] = m[Y[i]]






