import sys
import time
import numpy as np
import scipy
import os


def run_sklearn(params, X):
    from sklearn.cluster import KMeans

    start = time.time()
    clf = KMeans(**params).fit(X)
    end = time.time()

    return end - start


def run_frovedis(params, X, nproc):
    from frovedis.exrpc.server import FrovedisServer
    from frovedis.mllib.cluster import KMeans

    FrovedisServer.initialize(
        "mpirun -np {nproc} {server}".format(
            nproc=nproc,
            server=os.environ['FROVEDIS_SERVER']
        )
    )

    start = time.time()
    clf = KMeans(**params).fit(X)
    end = time.time()
    
    clf.release()
    FrovedisServer.shut_down()
    return end - start


def show_results(X, params, with_sklearn=True, with_frovedis=True, frovedis_nproc=8):
    if with_sklearn:
        results_sklearn = run_sklearn(params, X)
    if with_frovedis:
        results_frovedis = run_frovedis(params, X, frovedis_nproc)

    if with_sklearn:
        print("* Run scikit-learn")
        print("elapsed = {}".format(results_sklearn))

    if with_frovedis:
        print("* Run frovedis")
        print("elapsed = {}".format(results_frovedis))


if __name__ == "__main__":
    import argparse

    # inside project
    import utility

    parser = argparse.ArgumentParser(
        description="Command line for KMeans.fit",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument("X_path", 
                        help="binary file of scipy sparse matrix")  
    parser.add_argument("--n_clusters", default=10, type=int,
                        help="'n_clusters' parameter")
    parser.add_argument("--init", default="random", type=str,
                        help="'init' parameter")
    parser.add_argument("--max_iter", default=100, type=int,
                        help="'max_iter' parameter")
    parser.add_argument("--n_jobs", default=None, type=int,
                        help="'n_jobs' parameter (works only for sklearn")
    
    args = parser.parse_args()
    X = scipy.sparse.load_npz(args.X_path)
    X = X.todense()

    params = dict(
        n_clusters=args.n_clusters, init=args.init, max_iter=args.max_iter, n_jobs=args.n_jobs
    )

    show_results(X, params)
