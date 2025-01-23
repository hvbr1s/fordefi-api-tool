def evm_tx_tokens(evm_chain, vault_id, destination, custom_note, on_chain_value, contract_address):

    request_json = {
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


def sol_tx_tokens(vault_id, destination, custom_note, on_chain_value, program_address):

    request_json = {
        "signer_type": "api_signer",
        "type": "solana_transaction",
        "details": {
            "type": "solana_transfer",
            "to": destination,
            "value": {
                "type": "value",
                "value": on_chain_value
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