# Asset ID: 2653885
import json
from algosdk import account, mnemonic, transaction, future
from algosdk.v2client import algod

# Shown for demonstration purposes. NEVER reveal secret mnemonics in practice.
# Change these values with your mnemonics
# mnemonic1 = "PASTE your phrase for account 1"
# mnemonic2 = "PASTE your phrase for account 2"
# mnemonic3 = "PASTE your phrase for account 3"

mnemonic1 = "canal enact luggage spring similar zoo couple stomach shoe laptop middle wonder eager monitor weather number heavy skirt siren purity spell maze warfare ability ten"
mnemonic2 = "beauty nurse season autumn curve slice cry strategy frozen spy panic hobby strong goose employ review love fee pride enlist friend enroll clip ability runway"
mnemonic3 = "picnic bright know ticket purity pluck stumble destroy ugly tuna luggage quote frame loan wealth edge carpet drift cinnamon resemble shrimp grain dynamic absorb edge"


# For ease of reference, add account public and private keys to
# an accounts dict.
accounts = {}
counter = 1
for m in [mnemonic1, mnemonic2, mnemonic3]:
    accounts[counter] = {}
    accounts[counter]['pk'] = mnemonic.to_public_key(m)
    accounts[counter]['sk'] = mnemonic.to_private_key(m)
    counter += 1

# Specify your node address and token. This must be updated.
# algod_address = ""  # ADD ADDRESS
# algod_token = ""  # ADD TOKEN

algod_address = "http://localhost:4001"
algod_token = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"

# Initialize an algod client
algod_client = algod.AlgodClient(
    algod_token=algod_token, algod_address=algod_address)

#   Utility function to wait for a transaction to be confirmed by network


def wait_for_confirmation(algod_client, txid):
   last_round = algod_client.status().get('last-round')
   while True:
       txinfo = algod_client.pending_transaction_info(txid)
       if txinfo.get('confirmed-round') and txinfo.get('confirmed-round') > 0:
           print("Transaction {} confirmed in round {}.".format(
               txid, txinfo.get('confirmed-round')))
           break
       else:
           print("Waiting for confirmation...")
           last_round += 1
           algod_client.status_after_block(last_round)

#   Utility function used to print created asset for account and assetid


def printCreatedAsset(algodclient, account, assetid):
    # note: if you have an indexer instance available it is easier to just use this
    # response = myindexer.accounts(asset_id = assetid)
    # then use 'accountInfo['created-assets'][0] to get info on the created asset
    accountInfo = algodclient.account_info(account)
    idx = 0
    for myaccountInfo in accountInfo['created-assets']:
        scrutinizedAsset = accountInfo['created-assets'][idx]
        idx = idx + 1
        if (scrutinizedAsset['index'] == assetid):
            print("Asset ID: {}".format(scrutinizedAsset['index']))
            print(json.dumps(myaccountInfo['params'], indent=4))
            break

#   Utility function used to print asset holding for account and assetid


def printAssetHolding(algodclient, account, assetid):
    # note: if you have an indexer instance available it is easier to just use this
    # response = myindexer.accounts(asset_id = assetid)
    # then loop thru the accounts returned and match the account you are looking for
    accountInfo = algodclient.account_info(account)
    idx = 0
    for myaccountInfo in accountInfo['assets']:
        scrutinizedAsset = accountInfo['assets'][idx]
        idx = idx + 1
        if (scrutinizedAsset['asset-id'] == assetid):
            print("Asset ID: {}".format(scrutinizedAsset['asset-id']))
            print(json.dumps(scrutinizedAsset, indent=4))
            break


print("Account 1 address: {}".format(accounts[1]['pk']))
print("Account 2 address: {}".format(accounts[2]['pk']))
print("Account 3 address: {}".format(accounts[3]['pk']))

# your terminal output should look similar to the following
# Account 1 address: ATTR6RUEHHBHXKUHT4GUOYWNBVDV2GJ5FHUWCSFZLHD55EVKZWOWSM7ABQ
# Account 2 address: AK6Q33PDO4RJZQPHEMODC6PUE5AR2UD4FBU6TNEJOU4UR4KC6XL5PWW5K4
# Account 3 address: IWR4CLLCN2TIVX2QPVVKVR5ER5OZGMWAV5QB2UIPYMPKBPLJZX4C37C4AA
asset_id = 2653885

# CHANGE MANAGER

# The current manager(Account 2) issues an asset configuration transaction that assigns Account 1 as the new manager.
# Keep reserve, freeze, and clawback address same as before, i.e. account 2
params = algod_client.suggested_params()
# comment these two lines if you want to use suggested params
params.fee = 1000
params.flat_fee = True

# asset_id = 328952;

txn = future.transaction.AssetConfigTxn(
    sender=accounts[2]['pk'],
    sp=params,
    index=asset_id,
    manager=accounts[1]['pk'],
    reserve=accounts[2]['pk'],
    freeze=accounts[2]['pk'],
    clawback=accounts[2]['pk'])
# sign by the current manager - Account 2
stxn = txn.sign(accounts[2]['sk'])
txid = algod_client.send_transaction(stxn)
print(txid)

# Wait for the transaction to be confirmed
wait_for_confirmation(algod_client, txid)

# Check asset info to view change in management. manager should now be account 1
printCreatedAsset(algod_client, accounts[1]['pk'], asset_id)
# terminal output should be similar to...
# Transaction Y7EYBJNFP7YPGCV7ZD47PMJZHXB2PRT3SZ534M7BZE7G55IMPKUA confirmed in round 3982910.
# Asset ID: 2653870
# {
#     "clawback": "AK6Q33PDO4RJZQPHEMODC6PUE5AR2UD4FBU6TNEJOU4UR4KC6XL5PWW5K4",
#     "creator": "ATTR6RUEHHBHXKUHT4GUOYWNBVDV2GJ5FHUWCSFZLHD55EVKZWOWSM7ABQ",
#     "decimals": 0,
#     "default-frozen": false,
#     "freeze": "AK6Q33PDO4RJZQPHEMODC6PUE5AR2UD4FBU6TNEJOU4UR4KC6XL5PWW5K4",
#     "manager": "ATTR6RUEHHBHXKUHT4GUOYWNBVDV2GJ5FHUWCSFZLHD55EVKZWOWSM7ABQ",
#     "metadata-hash": "MTZlZmFhMzkyNGE2ZmQ5ZDNhNDgyNDc5OWE0YWM2NWQ=",
#     "name": "latinum",
#     "reserve": "AK6Q33PDO4RJZQPHEMODC6PUE5AR2UD4FBU6TNEJOU4UR4KC6XL5PWW5K4",
#     "total": 1000,
#     "unit-name": "LATINUM",
#     "url": "https://path/to/my/asset/details"
# }