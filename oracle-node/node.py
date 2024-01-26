from web3 import Web3
from solcx import compile_standard, install_solc
from dotenv import load_dotenv
import os
import sys

node_index = sys.argv[1]
node_status = sys.argv[2]

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
event_filter = contract.events.RequestEvent.create_filter(fromBlock="latest")
# Without this fix we get `The transaction declared chain ID 74565, but the connected node is on 12345`
chain_id = int(os.getenv("CHAIN_ID"))
account_address = os.getenv("ACCOUNT_ADDRESS_" + node_index)
private_key = os.getenv("ACCOUNT_PRIVATE_KEY_" + node_index)
print(f"[INFO] Node {node_index} started.")
print(f"[INFO] Listening for events...")

# This while loop continuously listens for new request events from the oracle contract.
# When a new request event is received, it sends a response to the oracle contract.
while True:
    for event in event_filter.get_new_entries():
        print(f"[INFO] Received event: {event}")
        id = event['args']['id']
        name = event['args']['name']
        id = int(id)
        # This value should be the requested data from the oracle contract.
        if node_status == "1":
            value = Web3.to_bytes(text="__TRUE__")
        else:
            value = Web3.to_bytes(text="__FALSE__")
        # Without this fix we get `Function invocation failed due to no matching argument types`
        value = Web3.to_bytes(hexstr=value.hex().zfill(64))
        # Without this type of nonce, the transaction will fail to submit
        nonce = w3.eth.get_transaction_count(account_address)
        tx = contract.functions.updateRequest(_id=id, _valueRetrieved=value).build_transaction(
            {
                "chainId": chain_id,
                "gasPrice": w3.eth.gas_price,
                "from": account_address,
                "nonce": nonce,
            }
        )
        signed_tx = w3.eth.account.sign_transaction(tx, private_key=private_key)
        tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
        tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        print(f"[INFO] Response sent to oracle contract.")
