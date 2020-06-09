import json
# requires Python SDK version 1.3 or higher
from algosdk.v2client import indexer

data = {
    "indexer_token": "",
    "indexer_address": "http://localhost:8980"
}

# instantiate indexer client
myindexer = indexer.IndexerClient(**data)

data = {
    "address": "SWOUICD7Y5PQBWWEYC4XZAQZI7FJRZLD5O3CP4GU2Y7FP3QFKA7RHN2WJU",
    "txn_type": "acfg"
    }
response = myindexer.search_transactions_by_address(**data)
print("txn_type: acfg = " +
      json.dumps(response, indent=2, sort_keys=True))