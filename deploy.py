from web3 import Web3
import json
from solcx import compile_standard, install_solc
from config import INFURA_URL, PRIVATE_KEY, PUBLIC_ADDRESS

install_solc("0.8.0")
w3 = Web3(Web3.HTTPProvider(INFURA_URL))
chain_id = 11155111  # Sepolia

with open("VotingDAO.sol", "r") as file:
    source_code = file.read()

compiled = compile_standard({
    "language": "Solidity",
    "sources": {"VotingDAO.sol": {"content": source_code}},
    "settings": {"outputSelection": {"*": {"*": ["abi", "metadata", "evm.bytecode"]}}}
}, solc_version="0.8.0")

abi = compiled["contracts"]["VotingDAO.sol"]["VotingDAO"]["abi"]
bytecode = compiled["contracts"]["VotingDAO.sol"]["VotingDAO"]["evm"]["bytecode"]["object"]

contract = w3.eth.contract(abi=abi, bytecode=bytecode)
nonce = w3.eth.get_transaction_count(PUBLIC_ADDRESS)

tx = contract.constructor().build_transaction({
    "from": PUBLIC_ADDRESS,
    "nonce": nonce,
    "gas": 3000000,
    "gasPrice": w3.to_wei("10", "gwei"),
    "chainId": chain_id
})

signed = w3.eth.account.sign_transaction(tx, PRIVATE_KEY)
tx_hash = w3.eth.send_raw_transaction(signed.rawTransaction)
print("Deploying... TX hash:", tx_hash.hex())

tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
print("✅ Contract deployed at:", tx_receipt.contractAddress)

# Save ABI and address
with open("abi.json", "w") as f:
    json.dump(abi, f)
with open("contract_address.txt", "w") as f:
    f.write(tx_receipt.contractAddress)
