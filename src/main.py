import aerospike
from aerospike import predicates as pred

from src.SetProxy import SetProxy


def clean_and_aggregate(accum_list, callback_record):
    record_body = callback_record[2]
    record_body["itemId"] = int(record_body["itemId"])
    accum_list.append(record_body)


def main( ):
    print("Connecting to Aerospike server...")
    cluster_addrs = {
        "hosts": [("localhost", 3000)]
    }
    client = aerospike.Client(cluster_addrs).connect( )
    print("Connected to Aerospike server")

    proxy = SetProxy(client, "inventory", "catalog")

    cleaned_results = [ ]
    (
        proxy.query()
        .where(pred.equals("category", "dress"))
        .select("itemId", "subcategory", "decade", "pattern", "color",
                "size", "material")
        .foreach(lambda curr_record: clean_and_aggregate(
            cleaned_results, curr_record))
    )

    print(cleaned_results)

    client.close( )


#
# Boilerplate driver to invoke main( ) when this script is run directly from
# the command line
#
if __name__ == '__main__':
    main( )
