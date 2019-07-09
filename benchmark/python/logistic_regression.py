import sys
import time
import numpy as np
import scipy


def run_sklearn(params, X_train, y_train, X_test, y_test):
    from sklearn.linear_model import LogisticRegression

    start = time.time()
    clf = LogisticRegression(**params).fit(X_train, y_train)
    end = time.time()

    y_pred = clf.predict(X_test)
    score = 1.0 * sum(y_test == y_pred) / len(y_test)

    return score, end - start


def run_frovedis(params, X_train, y_train, X_test, y_test, nproc):
    from frovedis.exrpc.server import FrovedisServer
    from frovedis.mllib.linear_model import LogisticRegression

    FrovedisServer.initialize(
        "{mpirun} -np {nproc} -x {server}".format(
            mpirun="/opt/nec/ve/bin/mpirun",
            nproc=nproc,
            server="/opt/nec/nosupport/frovedis/ve/bin/frovedis_server"
        )
    )

    start = time.time()
    clf = LogisticRegression(**params).fit(X_train, y_train)
    end = time.time()
    
    y_pred = clf.predict(X_test)
    score = 1.0 * sum(y_test == y_pred) / len(y_test)
    
    clf.release()
    FrovedisServer.shut_down()
    return score, end - start


def show_results(X_train, y_train, X_test, y_test, params, with_sklearn=True, with_frovedis=True, frovedis_nproc=8):
    if with_sklearn:
        results_sklearn = run_sklearn(params, X_train, y_train, X_test, y_test)
    if with_frovedis:
        results_frovedis = run_frovedis(params, X_train, y_train, X_test, y_test, frovedis_nproc)

    if with_sklearn:
        print("* Run scikit-learn")
        print("elapsed = {}".format(results_sklearn[1]))

    if with_frovedis:
        print("* Run frovedis")
        print("elapsed = {}".format(results_frovedis[1]))


if __name__ == "__main__":
    import argparse
    from sklearn.model_selection import train_test_split 

    # inside project
    import utility

    parser = argparse.ArgumentParser(
        description="Command line for LogisticRegression.fit",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument("X_path", 
                        help="binary file of scipy sparse matrix")  
    parser.add_argument("y_path", 
                        help="binary file of ndarray label")
    parser.add_argument("--test_size", default=0.2, type=float,
                        help="proportion of the data in the test split")
    parser.add_argument("--C", default=10.0, type=float,
                        help="'C' parameter")
    parser.add_argument("--max_iter", default=100, type=int,
                        help="'max_iter' parameter")
    parser.add_argument("--solver", default="sag", type=str,
                        help="'solver' parameter")
    parser.add_argument("--n_jobs", type=int,
                        help="'n_jobs' parameter")
    
    args = parser.parse_args()
    X, y = utility.dataset.load_np_binary(args.X_path, args.y_path)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=args.test_size, random_state=42)
    
    params = dict(
        C=args.C, max_iter=args.max_iter, solver=args.solver, n_jobs=args.n_jobs
    )

    show_results(X_train, y_train, X_test, y_test, params, with_sklearn=1)
