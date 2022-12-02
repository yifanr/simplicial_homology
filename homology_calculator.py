import numpy as np
from scipy.linalg import null_space
from numpy.linalg import matrix_rank

def simplex_calculator(simplexes):
    #Start by reordering each given simplex alphabetically so "acb" would become "abc"
    for i in range(len(simplexes)):
        sorted_characters = sorted(simplexes[i])
        simplexes[i] = "".join(sorted_characters)
    #Find the highest dimension simplex in this simplicial complex
    maxLen = 0
    for simplex in simplexes:
        if (len(simplex) > maxLen):
            maxLen = len(simplex)
    allSimplexes = []
    #Create an empty bin for each dimension from 0 to the maximum dimension
    for i in range(maxLen):
        allSimplexes.append(set())
    #Add each given simplex to the respective bin
    for simplex in simplexes:
        allSimplexes[len(simplex)-1].add(simplex)
    #Starting from the highest bin, add faces of each simplex to the bin below
    allSimplexes[maxLen-1] = sorted(allSimplexes[maxLen-1])
    for k in range(maxLen-1, 0, -1):
        kSimplexes = allSimplexes[k]
        for kSimplex in kSimplexes:
            for j in range(k+1):
                allSimplexes[k-1].add(kSimplex[:j] + kSimplex[j+1:])
        allSimplexes[k-1] = sorted(allSimplexes[k-1])
    #return the list of bins
    return allSimplexes


def boundaries_calculator(simplexes):
    #initialize the list of boundary matrices
    boundaries = []
    #The 0th boundary matrix is just all 0's since the boundary of a point is 0.
    boundaries.append(np.zeros((1,len(simplexes[0]))))
    #loop through the bins
    for k in range(1,len(simplexes)):
        #initialize a matrix filled with 0s of the correct dimension
        matrix = np.zeros((len(simplexes[k-1]),len(simplexes[k])))
        for i in range(len(simplexes[k])):
            #for each k-simplex
            kSimplex = simplexes[k][i]
            #loop through its k-1 dimensional faces
            for j in range(k+1):
                #add either -1 or 1 to the relevant spot in our matrix
                matrix[simplexes[k-1].index(kSimplex[:j] + kSimplex[j+1:]), i] = -2*(j%2)+1
        #add this new matrix to the list of boundary matrices
        boundaries.append(matrix)
    return boundaries

def homology_calculator(boundaries):
    homologies = []
    for k in range(len(boundaries)):
        if(k == len(boundaries)-1):
            b = 0
        else:
            bk1 = boundaries[k+1]
            b = matrix_rank(bk1)
        bk = boundaries[k]
        z = len(null_space(bk)[0])
        print("Dimension of Z_"+str(k)+" is "+str(z))
        print("Dimension of B_"+str(k)+" is "+str(b))
        homologies.append(z-b)
    return homologies


twosphere = ["abc", "abd", "acd", "dcb"]
threesphere = ["bcde", "acde", "abde", "abce", "abcd", "f"]
torus = ["abd", "dbe", "ebc", "efc", "cfa", "fad", "gde", "egh", "hfe", "hfi", "ifd", "idg", "agh", "ahb", "bhi", "bic", "cig", "cag"]
mobius = ["abd", "dbe", "bce", "ecf", "cdf", "fda"]
klein = ["abd", "ebd", "ebc", "efc", "cfa", "afg", "gde", "ghe", "hef", "hif", "fig", "dig", "hag", "bah", "hib", "bic", "cid", "cad"]
cylinder = ["abd", "ebd", "ebc", "ecf", "caf", "fad"]
triangle = ["ab","bc","ac", "d", "ef", "egh"]
allSimplexes = simplex_calculator(twosphere)
for simplex in allSimplexes:
    print(simplex)
boundaries = boundaries_calculator(allSimplexes)
for boundary in boundaries:
    print(boundary)
homologies = homology_calculator(boundaries)
print(homologies)
