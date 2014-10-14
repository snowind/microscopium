from itertools import combinations
import numpy as np
from scipy.spatial.distance import pdist

def sq_to_dist(i, j, n):
    """Converts [i, j] co-ordinate of pairwise, square distance
    matrix to co-ordinate of condensed distance matrix.
    See scipy.spatial.distance.pdist

    Parameters
    ----------
    i : int
        i-th coordinate.
    j : int
        j-th coordinate.
    n : int
        Dimension n of n*n distance matrix.

    Returns
    -------
    index : int
        Position of pairwise distance [i, j] in
        condensed distance matrix.

    Examples
    --------
    ## TODO it's not clear what this function is doing in the example ..
    >>> sq_to_dist(0, 1, 4)
    0
    """
    index = i*n + j - i*(i+1)/2 - i - 1
    return index


def gene_distance_score(X, gene_list, metric='euclidean'):
    """Finds distance scores between samples belonging to the
    same gene, samples not belonging to the same gene.

    Parameters
    ----------
    X : array, shape (n_samples, n_features)
        The data matrix.
    gene_list : array, shape (n_samples, )
        Array indicating which gene was knocked-down
        corresponding to each sample.
    metric : string, optional
        Which distance measure to use when calculating distances.
        Must be one of the options allowable in
        scipy.spatial.distance.pdist. Default euclidean.

    Returns
    -------
    all_intragene_data : array
        An 1D array with intra-gene distances (i.e. distances
        between samples with the same gene knocked down).
    all_intergene_data : array
        An 1D array with inter-gene distances (i.e. distances
        between samples with the same gene knocked down).

    Examples
    --------
    ## TODO make this doctest much prettier or make it a full test
    >>> data = np.zeros((6, 3))
    >>> data[0:2, :] = 1
    >>> data[2:4, :] = 4
    >>> data[4:6, :] = 7
    >>> genes = ['A', 'A', 'B', 'B', 'C', 'C']
    >>> intra, inter = gene_distance_score(data, genes, 'euclidean')
    >>> intra
    array([ 0.,  0.,  0.])
    >>> inter
    array([  5.19615242,   5.19615242,  10.39230485,  10.39230485,
             5.19615242,   5.19615242,  10.39230485,  10.39230485,
             5.19615242,   5.19615242,   5.19615242,   5.19615242])
    """
    all_intragene_index = []
    gene_list = np.array(gene_list)

    for gene in np.unique(gene_list):
        intragene_index = np.where(gene_list == gene)[0]

        for i, j in combinations(intragene_index, 2):
            all_intragene_index.append(sq_to_dist(i, j, X.shape[0]))

    n = sq_to_dist(X.shape[0], X.shape[0], X.shape[0])
    all_intergene_index = np.setdiff1d(np.arange(n), all_intragene_index)

    all_intragene_data = pdist(X, 'euclidean')[all_intragene_index]
    all_intergene_data = pdist(X, 'euclidean')[all_intergene_index]

    return all_intragene_data, all_intergene_data

