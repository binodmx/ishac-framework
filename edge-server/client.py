from web3 import Web3
from solcx import compile_standard, install_solc
from dotenv import load_dotenv
import os
import uuid

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
chain_id = int(os.getenv("CHAIN_ID"))
account_address = os.getenv("ACCOUNT_ADDRESS_1")
private_key = os.getenv("ACCOUNT_PRIVATE_KEY_1")
event_filter = contract.events.ResponseEvent.create_filter(fromBlock="latest")

def create_request(attr_name):
    """
    Calls createRequest function of the oracle contract.

    Args:
        attr_name (str): The name of the attribute.

    Returns:
        id (int): The uuid of the request.
    """
    id = Web3.to_int(hexstr=hex(uuid.uuid4().int))
    name = Web3.to_bytes(text=attr_name)
    # Without this fix we get `Function invocation failed due to no matching argument types`
    name = Web3.to_bytes(hexstr=name.hex().zfill(64))
    # Without this type of nonce, the transaction will fail to submit
    nonce = w3.eth.get_transaction_count(account_address)
    print(f"[INFO] Sending request to oracle contract...")
    tx = contract.functions.createRequest(id, name).build_transaction(
        {
            "chainId": chain_id,
            "gasPrice": w3.eth.gas_price,
            "from": account_address,
            "nonce": nonce,
        }
    )
    signed_tx = w3.eth.account.sign_transaction(tx, private_key)
    tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    print(f"[INFO] Request sent to oracle contract with id: {id}")
    return id

def get_attribute(id):
    """
    Waits for a response event from the oracle contract.

    Args:
        id (int): The uuid of the request.

    Returns:
        value (str): The value of the attribute.
    """
    print(f"[INFO] Waiting for response event...")
    # This while loop continuously listens for response events from the oracle contract.
    # When the required response event is received, it terminates the loop and returns the value.
    while True:
        for event in event_filter.get_new_entries():
            print(f"[INFO] Received response event: {event}")
            return Web3.to_text(event['args']['value'])