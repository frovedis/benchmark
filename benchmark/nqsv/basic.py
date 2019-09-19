from frovedis.exrpc.server import FrovedisServer


if __name__ == "__main__":
    FrovedisServer.initialize(
        "{mpirun} -np {nproc} {server}".format(
            mpirun="/opt/nec/ve/bin/mpirun",
            nproc=8,
            server="/opt/nec/nosupport/frovedis/ve/bin/frovedis_server"
        )
    )
    print("initialize server")

    # Do your work here with Frovedis 

    FrovedisServer.shut_down()
    print("shutdown server")
