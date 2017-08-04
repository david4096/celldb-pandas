#!/usr/bin/env python
# celldb
#

from celldb import client
import pandas as pd
import scipy
import numpy as np

def df(connection, sample_ids, feature_ids):
    """
    Takes a connection and list of sample and feature IDs and returns a pandas
    dataframe.
    :param connection:
    :param sample_ids:
    :param feature_ids:
    :return:
    """
    # This should really be a part of pandas API directly.
    m = client.matrix(connection, sample_ids, feature_ids)
    return pd.DataFrame(
        [x[1:] for x in m],
        index=[x[0] for x in m],
        columns=feature_ids)

def sparse(connection, sample_ids, feature_ids):
    """
    Takes a connection and lists of sample and feature ids and returns a sparse
    dataframe.
    :param connection:
    :param sample_ids:
    :param feature_ids:
    :return:
    """
    dense = df(connection, sample_ids, feature_ids)
    sparse_df = dense.to_sparse(fill_value=0.0)
    csr = sparse_df.to_coo().tocsr()
    sp = pd.SparseDataFrame([pd.SparseSeries(dense[i].toarray().ravel())
                              for i in np.arange(dense.shape[0])])
    return sp