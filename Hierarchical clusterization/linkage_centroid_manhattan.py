from head import *
from preprocessing import *

class triple:
    def __init__(self, left_c, right_c, d):
        self.left_c = left_c
        self.right_c = right_c
        self.d = d
    def __eq__(self, other):
        if (self is None or other is None):
            return (self is None and other is None)
        return (self.left_c == other.left_c and self.right_c == other.right_c and self.d == other.d)
    def __ne__(self, other):
        if (self is None or other is None):
            return not (self is None and other is None)
        return not (self.left_c == other.left_c and self.right_c == other.right_c and self.d == other.d)
    def __lt__(self, other):
        return (self.d < other.d or (self.d == other.d and self.left_c < other.left_c) or (self.d == other.d and self.left_c == other.left_c and self.right_c < other.right_c))
    def __leq__(self, other):
        return self.__lt__(other) or self.__eq__(other)
    def __gt__(self, other):
        return (self.d > other.d or (self.d == other.d and self.left_c > other.left_c) or (self.d == other.d and self.left_c == other.left_c and self.right_c > other.right_c))
    def __ge__(self, other):
        return self.__gt__(other) or self.__eq__(other)


def linkage(df):
    T = RedBlackTree()
    link = []
    INF = 1e9
    centroids = {}
    number = {}
    n = df.shape[0]
    for i in range(n):
        centroids[i] = list(df.loc[i, :])
        number[i] = 1
    current_clusters = set([i for i in range(n)])
    for i in current_clusters:
        for j in current_clusters:
            if (i != j):
                T.add(triple(i, j, cityblock(centroids[i], centroids[j])))
    for z in range(n - 1):
        iter = T.__iter__()
        x = iter.__next__()
        while (not (x.left_c in current_clusters and x.right_c in current_clusters)):
            T.remove(x)
            iter = T.__iter__()
            x = iter.__next__()

        centroids[n + z] = [0 for i in range(df.shape[1])]
        for i in range(df.shape[1]):
            centroids[n + z][i] = (centroids[x.left_c][i] * number[x.left_c] + centroids[x.right_c][i] * number[x.right_c]) / (number[x.left_c] + number[x.right_c])
        number[n + z] = number[x.left_c] + number[x.right_c]
        link.append([x.left_c, x.right_c, x.d, number[n + z]])
        current_clusters.add(n + z)
        current_clusters.remove(x.left_c)
        current_clusters.remove(x.right_c)
        for i in current_clusters:
            if (i != n + z):
                T.add(triple(i, n + z, cityblock(centroids[i], centroids[n + z])))
    return np.array(link)

if __name__ == '__main__':
    link = linkage(df)
    savetxt('link.csv', link, delimiter=',')
    #print(link)
    #_is_link(df.shape[0], link)


