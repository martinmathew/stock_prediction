import numpy as np
from hmmlearn import hmm
def check():
    X1 = [[36] , [44], [52] ,[56], [49], [44]]
    X2 = [[42], [46], [54], [62], [68], [65], [60], [56]]
    X3 = [[42], [40], [41],[43], [52], [55],[59], [60], [55], [47]]

    X = np.concatenate([X1, X2, X3])
    lengths = [len(X1), len(X2), len(X3)]
    res = hmm.GaussianHMM(algorithm='viterbi',n_components=3).fit(X, lengths)
    print res

if __name__ == "__main__":
    check()
