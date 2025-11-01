import aerospike

def main( ):
    print("Connecting to Aerospike server...")

    cluster_addrs = {
        "hosts": [("localhost", 3000)]
    }

    client = aerospike.Client(cluster_addrs).connect( )

    print("Connected to Aerospike server.")

    key = ("inventory", "catalog", 4768)
    (outkey, meta, bins) = client.get(key)
    print("Found outkey:", outkey)
    print("Found meta:", meta)
    print("Found bins:", bins)

    client.close( )

#
# Boilerplate driver if this is the script invoked by the user
#
if __name__ == '__main__':
    main( )

