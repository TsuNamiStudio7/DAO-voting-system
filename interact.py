import json
from web3 import Web3
from config import INFURA_URL, PRIVATE_KEY, PUBLIC_ADDRESS

with open("abi.json") as f:
    abi = json.load(f)
with open("contract_address.txt") as f:
    contract_address = f.read().strip()

w3 = Web3(Web3.HTTPProvider(INFURA_URL))
contract = w3.eth.contract(address=contract_address, abi=abi)

def create_proposal(description):
    nonce = w3.eth.get_transaction_count(PUBLIC_ADDRESS)
    tx = contract.functions.createProposal(description).build_transaction({
        "from": PUBLIC_ADDRESS,
        "nonce": nonce,
        "gas": 200000,
        "gasPrice": w3.to_wei("10", "gwei")
    })
    signed = w3.eth.account.sign_transaction(tx, PRIVATE_KEY)
    tx_hash = w3.eth.send_raw_transaction(signed.rawTransaction)
    print("📢 Proposal submitted:", tx_hash.hex())

def vote(proposal_id):
    nonce = w3.eth.get_transaction_count(PUBLIC_ADDRESS)
    tx = contract.functions.vote(proposal_id).build_transaction({
        "from": PUBLIC_ADDRESS,
        "nonce": nonce,
        "gas": 200000,
        "gasPrice": w3.to_wei("10", "gwei")
    })
    signed = w3.eth.account.sign_transaction(tx, PRIVATE_KEY)
    tx_hash = w3.eth.send_raw_transaction(signed.rawTransaction)
    print("🗳️ Vote submitted:", tx_hash.hex())

def get_results():
    total = contract.functions.totalProposals().call()
    for i in range(total):
        desc, count = contract.functions.getProposal(i).call()
        print(f"#{i}: {desc} — {count} votes")

# Example usage:
# create_proposal("Build coffee machine")
# vote(0)
# get_results()
