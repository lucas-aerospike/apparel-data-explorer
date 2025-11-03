#!/usr/bin/env python3

import sys
from aerospike import Client
from aerospike import predicates as pred

import open_ai_gateway
from set_proxy import SetProxy
from open_ai_gateway import recommend
from pprint import pprint

def clean_and_aggregate(accum_list, callback_record):
    record_body = callback_record[2]
    record_body["itemId"] = int(record_body["itemId"])
    accum_list.append(record_body)


def main( ):
    if len(sys.argv) != 2:
        print("Usage: main.py <exemplar-item-id>")
        sys.exit(1)

    print("Connecting to Aerospike server...")
    cluster_addrs = {
        "hosts": [("localhost", 3000)]
    }
    client = Client(cluster_addrs).connect( )
    print(f"Connected to Aerospike server: = {client.get_nodes( )}")

    proxy = SetProxy(client, "inventory", "catalog")

    cleaned_results = [ ]
    (
        proxy.query( )
        .where(pred.equals("category", "dress"))
        .select("itemId", "subcategory", "decade", "pattern", "color",
                "size", "material")
        .foreach(lambda curr_record: clean_and_aggregate(
            cleaned_results, curr_record))
    )
    client.close( )

    print("\nConfiguring OpenAI roles...")
    print(f"System role = {open_ai_gateway.SYSTEM}")

    response = recommend(int(sys.argv[1]), cleaned_results)

    print("\n")
    pprint(response)


#
# Boilerplate driver to invoke main( ) when this script is run directly from
# the command line
#
if __name__ == '__main__':
    main( )
