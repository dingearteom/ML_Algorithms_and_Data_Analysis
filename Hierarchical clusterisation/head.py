import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from sklearn.metrics import accuracy_score
import os
from rb_tree import RedBlackTree
import time
#matplotlib.style.use('ggplot')
import scipy.cluster.hierarchy
from scipy.spatial.distance import cityblock
from scipy.cluster.hierarchy import dendrogram, fcluster, linkage
from scipy.spatial.distance import pdist
import sys
from numpy import savetxt, loadtxt