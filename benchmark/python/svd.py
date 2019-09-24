import sys
import time
import numpy as np
import scipy
import os


def run_sklearn(params, X):
    from sklearn.decomposition import TruncatedSVD

    start = time.time()
    clf = TruncatedSVD(**params).fit(X)
    end = time.time()

    return end - start


def run_frovedis(params, X, nproc):
    from frovedis.exrpc.server import FrovedisServer
    from frovedis.matrix.wrapper import ARPACK

    FrovedisServer.initialize(
        "mpirun -np {nproc} {server}".format(
            nproc=nproc,
            server=os.environ['FROVEDIS_SERVER']
        )
    )

    start = time.time()
    clf = ARPACK.computeSVD(X, params["n_components"])
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
        description="Command line for TruncatedSVD.fit",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument("X_path", 
                        help="binary file of scipy sparse matrix")  
    parser.add_argument("--n_components", default=30, type=int,
                        help="'n_components' parameter")
    parser.add_argument("--algorithm", default="arpack", type=str,
                        help="'algorithm' parameter")
    
    args = parser.parse_args()
    X = scipy.sparse.load_npz(args.X_path)

    params = dict(
        n_components=args.n_components, algorithm=args.algorithm
    )

    show_results(X, params)
