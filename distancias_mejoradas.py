import numpy as np
import math
from trie import Trie

class Distances:
    def levenshtein(x, y, threshold=2**31):
        M = np.ones((len(x) + 1, len(y) + 1))*np.inf
        for i in range(0, len(x) + 1):
            M[i, 0] = i
        for j in range(0, len(y) + 1):
            M[0, j] = j
        m = len(y)/len(x)
        for i in range(1, len(x) + 1):
            colMin = np.inf;
            for j in range(max(math.floor(m*i-threshold), 1), min(math.ceil(m*i+threshold)+1, len(y) + 1)):
                if x[i - 1] == y[j - 1]:
                    M[i, j] = min(M[i - 1, j] + 1, M[i, j - 1] + 1, M[i-1][j-1])
                else:
                    M[i, j] = min(M[i - 1, j] + 1, M[i, j - 1] + 1, M[i-1][j-1] + 1)
                if colMin > M[i,j]:
                    colMin = M[i,j]
            if colMin > threshold:
                return None
        return M[len(x), len(y)]
        
    def damerau_levenshtein_restringida(x, y, threshold=2**31):
        M = np.ones((len(x) + 1, len(y) + 1))*np.inf
        for i in range(0, len(x) + 1):
            M[i, 0] = i
        for j in range(0, len(y) + 1):
            M[0, j] = j
        m = len(y)/len(x)
        for i in range(1, len(x) + 1):
            colMin = np.inf;
            for j in range(max(math.floor(m*i-threshold), 1), min(math.ceil(m*i+threshold)+1, len(y) + 1)):
                if i > 1 and j > 1 and x[i - 2] == y[j - 1] and x[i - 1] == y[j - 2]:
                    if x[i - 1] == y[j - 1]:
                        M[i, j] = min(M[i - 1, j] + 1, M[i, j - 1] + 1, M[i-1][j-1], M[i-2][j-2] + 1)
                    else:
                        M[i, j] = min(M[i - 1, j] + 1, M[i, j - 1] + 1, M[i-1][j-1] + 1, M[i-2][j-2] + 1)
                else:
                    if x[i - 1] == y[j - 1]:
                        M[i, j] = min(M[i - 1, j] + 1, M[i, j - 1] + 1, M[i-1][j-1])
                    else:
                        M[i, j] = min(M[i - 1, j] + 1, M[i, j - 1] + 1, M[i-1][j-1] + 1)
                if colMin > M[i,j]:
                    colMin = M[i,j]
            if colMin > threshold:
                return None
        return M[len(x), len(y)]
        
    def damerau_levenshtein_intermedia(x, y,threshold=2**31):
        M = np.ones((len(x) + 1, len(y) + 1))*np.inf
        for i in range(0, len(x) + 1):
            M[i, 0] = i
        for j in range(0, len(y) + 1):
            M[0, j] = j
        m = len(y)/len(x)
        for i in range(1, len(x) + 1):
            colMin = np.inf;
            for j in range(max(math.floor(m*i-threshold), 1), min(math.ceil(m*i+threshold)+1, len(y) + 1)):
                minInit = 2**31
                if x[i - 1] == y[j - 1]:
                    minInit = min(M[i-1, j] + 1, M[i, j-1] + 1, M[i-1][j-1])
                else:
                    minInit = min(M[i-1, j] + 1, M[i, j-1] + 1, M[i-1][j-1] + 1)

                if j > 1 and i > 1 and x[i - 2] == y[j - 1] and x[i - 1] == y[j - 2]:
                    minInit = min(minInit, M[i-2][j-2] + 1)
                
                if j > 2 and i > 1 and x[i-2] == y[j-1] and x[i-1] == y[j-3]:
                    minInit = min(minInit, M[i-2][j-3] + 2)
                
                if i > 2 and j > 1 and x[i - 3] == y[j-1] and x[i-1] == y[j-2]:
                    minInit = min(minInit, M[i-3][j-2] + 2)
                
                M[i,j] = minInit
                if colMin > M[i,j]:
                    colMin = M[i,j]
            
            if colMin > threshold:
                return None
        return M[len(x), len(y)]
        
    """ Implementaciones trie """
        
    def levenshtein_trie(t, y, threshold=2**31):
        M = np.ones((t.get_num_states() + 1, len(y) + 1))*np.inf
        M[0,0] = 0
        for i in range(1, t.get_num_states() + 1):
            M[i, 0] = M[t.get_parent(i), 0] + 1
        for j in range(1, len(y) + 1):
            M[0, j] = M[0, j - 1] + 1
            
        for i in range(1, t.get_num_states() + 1):
            for j in range(1, len(y) + 1):
                if t.get_label(i) == y[j - 1]:
                    M[i, j] = min(M[t.get_parent(i), j] + 1, M[i, j - 1] + 1, M[t.get_parent(i), j - 1])
                else:
                    M[i, j] = min(M[t.get_parent(i), j] + 1, M[i, j - 1] + 1, M[t.get_parent(i), j - 1] + 1)
        
        result = [(i, M[i, len(y)]) for i in range(0, t.get_num_states() + 1) if M[i, len(y)] <= threshold]
        return result
        
    def damerau_levenshtein_restringida_trie(t, y, threshold=2**31):
        M = np.ones((t.get_num_states() + 1, len(y) + 1))*np.inf
        M[0, 0] = 0
        for i in range(1, t.get_num_states() + 1):
            M[i, 0] = M[t.get_parent(i), 0] + 1
        for j in range(1, len(y) + 1):
            M[0, j] = M[0, j - 1] + 1
        for i in range(1, t.get_num_states() + 1):
            for j in range(1, len(y) + 1):
                if i > 0 and j > 1 and t.get_label(t.get_parent(i)) == y[j - 1] and t.get_label(i) == y[j - 2]:
                    if t.get_label(i) == y[j - 1]:
                        M[i, j] = min(M[t.get_parent(i), j] + 1, M[i, j - 1] + 1, M[t.get_parent(i), j-1], M[t.get_parent(t.get_parent(i)), j-2] + 1)
                    else:
                        M[i, j] = min(M[t.get_parent(i), j] + 1, M[i, j - 1] + 1, M[t.get_parent(i), j-1] + 1, M[t.get_parent(t.get_parent(i)), j-2] + 1)
                else:
                    if t.get_label(i) == y[j - 1]:
                        M[i, j] = min(M[t.get_parent(i), j] + 1, M[i, j - 1] + 1, M[t.get_parent(i), j-1])
                    else:
                        M[i, j] = min(M[t.get_parent(i), j] + 1, M[i, j - 1] + 1, M[t.get_parent(i), j-1] + 1)
        
        result = [(i, M[i, len(y)]) for i in range(0, t.get_num_states() + 1) if M[i, len(y)] <= threshold]
        return result
                    
    def damerau_levenshtein_intermedia_trie(t, y,threshold=2**31):
        M = np.ones((t.get_num_states() + 1, len(y) + 1))*np.inf
        M[0, 0] = 0
        for i in range(1, t.get_num_states() + 1):
            M[i, 0] = M[t.get_parent(i), 0] + 1
        for j in range(1, len(y) + 1):
            M[0, j] = M[0, j - 1] + 1
        for i in range(1, t.get_num_states() + 1):
            for j in range(1, len(y) + 1):
                minInit = 2**31
                if t.get_label(i) == y[j - 1]:
                    minInit = min(M[t.get_parent(i), j] + 1, M[i, j-1] + 1, M[t.get_parent(i), j-1])
                else:
                    minInit = min(M[t.get_parent(i), j] + 1, M[i, j-1] + 1, M[t.get_parent(i), j-1] + 1)

                if j > 1 and i > 1 and t.get_label(t.get_parent(i)) == y[j - 1] and t.get_label(i) == y[j - 2]:
                    minInit = min(minInit, M[t.get_parent(t.get_parent(i)), j-2] + 1)
                
                if j > 2 and i > 1 and t.get_label(t.get_parent(i)) == y[j-1] and t.get_label(i) == y[j-3]:
                    minInit = min(minInit, M[t.get_parent(t.get_parent(i)), j-3] + 2)
                
                if i > 2 and j > 1 and t.get_label(t.get_parent(t.get_parent(i))) == y[j-1] and t.get_label(i) == y[j-2]:
                    minInit = min(minInit, M[t.get_parent(t.get_parent(t.get_parent(i))), j-2] + 2)
                
                M[i,j] = minInit
        result = [(i, M[i, len(y)]) for i in range(0, t.get_num_states() + 1) if M[i, len(y)] <= threshold]
        return result

def test():
    x = "google"
    y = {"google","kooble","bubble", "gogole","ggole"}
    
    for w in y:
        d1 = levenshtein(x, w, 7)
        d2 = damerau_levenshtein_restringida(x, w, 7)
        d3 = damerau_levenshtein_intermedia(x, w, 7)
        print("Distances between " + x + " and " + w + ":")
        print("Levenshtein = " + str(d1))
        print("Damerau restringida = " + str(d2))
        print("Damerau intermedia = " + str(d3))
        print()
    
    
if __name__ == "__main__":
    test()
