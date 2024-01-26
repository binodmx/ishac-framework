from web3 import Web3
from solcx import compile_standard, install_solc
from dotenv import load_dotenv
import os

# Setup the web3 provider and other configurations.
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))
install_solc("0.8.0")
with open("../contracts/OracleContract.sol", "r") as file:
    client_contract_file = file.read()
compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"OracleContract.sol": {"content": client_contract_file}},
        "settings": {"outputSelection": {"*": {"*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]}}}
    },
    solc_version="0.8.0"
)
contract_address = os.getenv("CONTRACT_ADDRESS")
contract_abi = compiled_sol["contracts"]["OracleContract.sol"]["Oracle"]["abi"]
w3 = Web3(Web3.HTTPProvider(os.getenv("HTTP_PROVIDER")))
contract = w3.eth.contract(address=contract_address, abi=contract_abi)
event_filter1 = contract.events.RequestEvent.create_filter(fromBlock="latest")
event_filter2 = contract.events.ResponseEvent.create_filter(fromBlock="latest")
event_filter3 = contract.events.DebugEvent.create_filter(fromBlock="latest")
print("[INFO] Listening for events...")

# This while loop continuously listens for new events from the oracle contract.
while True:
    for event in event_filter1.get_new_entries():
        print(f"[INFO] Received request event: {event}", end="\n\n")
    for event in event_filter2.get_new_entries():
        print(f"[INFO] Received response event: {event}", end="\n\n")
    for event in event_filter3.get_new_entries():
        print(f"[INFO] Received debug event: {event}", end="\n\n")
