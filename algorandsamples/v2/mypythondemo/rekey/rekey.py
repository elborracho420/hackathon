import json
import time
import base64
from algosdk import mnemonic
from algosdk.v2client import algod
from algosdk.future.transaction import PaymentTxn

def wait_for_confirmation(client, txid):
	"""
	Utility function to wait until the transaction is
	confirmed before proceeding.
	"""
	last_round = client.status().get('last-round')
	txinfo = client.pending_transaction_info(txid)
	while not (txinfo.get('confirmed-round') and txinfo.get('confirmed-round') > 0):
		print("Waiting for confirmation")
		last_round += 1
		client.status_after_block(last_round)
		txinfo = client.pending_transaction_info(txid)
	print("Transaction {} confirmed in round {}.".format(
		txid, txinfo.get('confirmed-round')))
	return txinfo

def getting_started_example():
    algod_address = "http://localhost:4001"
    algod_token = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
    algod_client = algod.AlgodClient(algod_token, algod_address)

# Part 1
# rekey from Account 3 to allow to sign from Account 1

# Part 2
# send from account 3 to account 2 and sign from Account 1

    account1_passphrase = "fringe model trophy claw stove perfect address market license abstract master slender choice around field embark sudden carbon exclude abuse square bulb front ability violin"
    account2_passphrase = "impulse nation creek toy carpet amused dream can small long disorder source mail game category damp spread length cupboard theory either baby squeeze about orbit"
    account3_passphrase = "fade exit sword someone lock minimum scout keen label dance jaguar select conduct luxury rose idea solid major solid lens globe agent assume abstract alien"
    
    account1 = mnemonic.to_public_key(account1_passphrase)
    account2 = mnemonic.to_public_key(account2_passphrase)    
    private_key = mnemonic.to_private_key(account3_passphrase)
    account3 = mnemonic.to_public_key(account3_passphrase)

    print("Account 1 : {}".format(account1))
    print("Account 2 : {}".format(account2))
    print("Account 3 : {}".format(account3))
    
    # Part 1
    # build transaction
    params = algod_client.suggested_params()
    # comment out the next two (2) lines to use suggested fees
    params.flat_fee = True
    params.fee = 1000


    # opt-in send tx to same address as sender and use 0 for amount w rekey account
    # to account 1
    amount = int(0)   
    rekeyaccount = account1
    sender = account3
    receiver = account3    
    unsigned_txn = PaymentTxn(
    	sender, params, receiver, amount, None, None, None, rekeyaccount)

    # sign transaction with account 3
    signed_txn = unsigned_txn.sign(
    	mnemonic.to_private_key(account3_passphrase))
    txid = algod_client.send_transaction(signed_txn)
    print("Signed transaction with txID: {}".format(txid))

    # wait for confirmation
    wait_for_confirmation(algod_client, txid)

    # read transction
    try:
        confirmed_txn = algod_client.pending_transaction_info(txid)
        account_info = algod_client.account_info(account3)
        
    except Exception as err:
        print(err)
    print("Transaction information: {}".format(
        json.dumps(confirmed_txn, indent=4)))
    print("Account 3 information : {}".format(
        json.dumps(account_info, indent=4)))

    #  Part 2
    #  send payment from account 3
    #  to acct 2 and signed by account 1


    account1 = mnemonic.to_public_key(account1_passphrase)
    private_key_account1 = mnemonic.to_private_key(account1_passphrase)  
    account2 = mnemonic.to_public_key(account2_passphrase)
    account3 = mnemonic.to_public_key(account3_passphrase)

    amount = int(1000000)
    receiver = account2
    unsigned_txn = PaymentTxn(
    	account3, params, receiver, amount, None, None, None, account1)
    # sign transaction
    signed_txn = unsigned_txn.sign(
    	mnemonic.to_private_key(account1_passphrase))
    txid = algod_client.send_transaction(signed_txn)
    print("Signed transaction with txID: {}".format(txid))

    # wait for confirmation
    wait_for_confirmation(algod_client, txid)

    account_info_rekey = algod_client.account_info(account3)
    print("Account 3 information (from) : {}".format(
        json.dumps(account_info_rekey, indent=4)))
    account_info_rekey = algod_client.account_info(account2)
    print("Account 2 information (to) : {}".format(
        json.dumps(account_info_rekey, indent=4)))


getting_started_example()
