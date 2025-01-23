__all__ = ['evm_tx_tokens', 'sol_tx_tokens']
from decimal import Decimal
from configs.token_configs.evm import EVM_TOKEN_CONFIG
from configs.token_configs.solana import SOL_TOKEN_CONFIG


def evm_tx_tokens(evm_chain, vault_id, destination, custom_note, value, token):

    # 1. Validate the chain
    if evm_chain not in EVM_TOKEN_CONFIG:
        raise ValueError(f"Chain '{evm_chain}' is not supported. Please add it to './api_requests/token_configs/evm.py'")

    # 2. Validate the token
    chain_data = EVM_TOKEN_CONFIG[evm_chain]
    if token not in chain_data:
        raise ValueError(f"Token '{token}' is not supported for chain '{evm_chain}'.")

    # 3. Retrieve contract and decimals
    token_info = chain_data[token]
    contract_address = token_info["contract_address"]
    decimals = token_info["decimals"]

    # 4. Convert human-readable value to the proper decimal representation
    multiplier = Decimal(10) ** decimals
    on_chain_value = str(int(Decimal(value) * multiplier))

    request_json =  {
    "signer_type": "api_signer",
    "type": "evm_transaction",
    "details": {
        "type": "evm_transfer",
        "gas": {
          "type": "priority",
          "priority_level": "medium"
        },
        "to": destination,
        "value": {
           "type": "value",
           "value": on_chain_value
        },
        "asset_identifier": {
             "type": "evm",
             "details": {
                 "type": "erc20",
                 "token": {
                     "chain": f"evm_{evm_chain}_mainnet",
                     "hex_repr": contract_address
                 }
             }
        }
    },
    "note": custom_note,
    "vault_id": vault_id
}

    return request_json

def sol_tx_tokens(vault_id, destination, custom_note, value, token):

    # 1. Validate that the token is supported
    if token not in SOL_TOKEN_CONFIG:
        raise ValueError(f"Token '{token}' is not supported on Solana. Please add it to './api_requests/token_configs/solana.py")

    # 2. Retrieve the program address from the dictionary
    program_address = SOL_TOKEN_CONFIG[token]
    
    # 3. (Optional) Log for debugging or user feedback
    print(f"Sending {value} {token} from {vault_id} to {destination}")
    

    request_json = {
        "signer_type": "api_signer",
        "type": "solana_transaction",
        "details": {
            "type": "solana_transfer",
            "to": destination,
            "value": {
                "type": "value",
                "value": value
            },
            "asset_identifier": {
                "type": "solana",
                "details": {
                    "type": "spl_token",
                    "token": {
                        "chain": "solana_mainnet",
                        "base58_repr": program_address
                    }
                }
            }
        },
        "note": custom_note,
        "vault_id": vault_id
    }


    return request_json