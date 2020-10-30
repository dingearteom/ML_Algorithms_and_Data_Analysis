from head import *
from preprocessing import df, Y
import linkage_centroid_manhattan

link = linkage(df, 'ward', 'euclidean')
#link = loadtxt('link.csv', delimiter=',')

plt.figure(figsize=(15,15))
dendrogram(link, color_threshold=-1)
plt.savefig('dendrogram.png')

dist = link[:, 2]

plt.figure(figsize=(15,12))
plt.plot(range(len(dist)), dist[::-1], marker='o')
#plt.axhline(y=2.4, c='blue', linestyle='dashed')
#plt.text(400, 2.4, c='black', s='10 clasters')
plt.savefig('elbow.png')

df['cluster'] = fcluster(link, 10, 'maxclust')


c = [[0 for j in range(10)] for i in range(11)]
mv = [0 for i in range(11)]
for i in range(df.shape[0]):
    c[df.at[i, 'cluster']][Y[i]] += 1
for i in range(1, 11):
    mv[i] = -1
    num = -1
    for j in range(10):
        if (c[i][j] > num):
            num = c[i][j]
            mv[i] = j
df['answer'] = [0 for i in range(df.shape[0])]

for i in range(df.shape[0]):
    df.at[i, 'answer'] = mv[df.at[i, 'cluster']]

p = accuracy_score(list(Y), list(df['answer']))
print(p)





