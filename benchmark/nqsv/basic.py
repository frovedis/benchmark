from frovedis.exrpc.server import FrovedisServer
import os

if __name__ == "__main__":
    FrovedisServer.initialize(
        "mpirun -np {nproc} {server}".format(
            nproc=8,
            server=os.environ['FROVEDIS_SERVER']
        )
    )
    print("initialize server")

    # Do your work here with Frovedis 

    FrovedisServer.shut_down()
    print("shutdown server")


