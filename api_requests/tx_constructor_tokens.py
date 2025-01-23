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
    """
    A simpler version of sol_tx_tokens:
      - No token validation
      - We assume on_chain_value is already computed
      - We assume program_address is already known
    """
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


# __all__ = ['evm_tx_tokens', 'sol_tx_tokens']
# from decimal import Decimal
# from configs.ecosystem_configs import ECOSYSTEM_CONFIGS


# def evm_tx_tokens(evm_chain, vault_id, destination, custom_note, value, token):

#     # 1. Validate the chain
#     evm_config = ECOSYSTEM_CONFIGS["evm"]
#     if evm_chain not in evm_config["tokens"]:
#         raise ValueError(f"Chain '{evm_chain}' is not supported. Please check ECOSYSTEM_CONFIGS.")

#     # 2. Validate the token
#     chain_tokens = evm_config["tokens"][evm_chain]
#     if token not in chain_tokens:
#         raise ValueError(f"Token '{token}' is not supported for chain '{evm_chain}'.")

#     # 3. Retrieve contract and decimals
#     token_info = chain_tokens[token]
#     contract_address = token_info["contract_address"]
#     decimals = token_info["decimals"]

#     # 4. Convert human-readable value to the proper decimal representation
#     multiplier = Decimal(10) ** decimals
#     on_chain_value = str(int(Decimal(value) * multiplier))

#     request_json =  {
#     "signer_type": "api_signer",
#     "type": "evm_transaction",
#     "details": {
#         "type": "evm_transfer",
#         "gas": {
#           "type": "priority",
#           "priority_level": "medium"
#         },
#         "to": destination,
#         "value": {
#            "type": "value",
#            "value": on_chain_value
#         },
#         "asset_identifier": {
#              "type": "evm",
#              "details": {
#                  "type": "erc20",
#                  "token": {
#                      "chain": f"evm_{evm_chain}_mainnet",
#                      "hex_repr": contract_address
#                  }
#              }
#         }
#     },
#     "note": custom_note,
#     "vault_id": vault_id
# }

#     return request_json

# def sol_tx_tokens(vault_id, destination, custom_note, value, token):

#     # 1. Validate that the token is supported
#     sol_config = ECOSYSTEM_CONFIGS["sol"]
#     if token not in sol_config["tokens"]:
#         raise ValueError(f"Token '{token}' is not supported on Solana. Please check ECOSYSTEM_CONFIGS.")

#     # 2. Retrieve the program address and decimals
#     token_info = sol_config["tokens"][token]
#     program_address = token_info["program_address"]
#     decimals = token_info["decimals"]

#     # 3. Convert human-readable value to the proper decimal representation
#     multiplier = Decimal(10) ** decimals
#     on_chain_value = str(int(Decimal(value) * multiplier))
    
#     # 3. (Optional) Log for debugging or user feedback
#     print(f"Sending {value} {token} from {vault_id} to {destination}")
    

#     request_json = {
#         "signer_type": "api_signer",
#         "type": "solana_transaction",
#         "details": {
#             "type": "solana_transfer",
#             "to": destination,
#             "value": {
#                 "type": "value",
#                 "value": value
#             },
#             "asset_identifier": {
#                 "type": "solana",
#                 "details": {
#                     "type": "spl_token",
#                     "token": {
#                         "chain": "solana_mainnet",
#                         "base58_repr": program_address
#                     }
#                 }
#             }
#         },
#         "note": custom_note,
#         "vault_id": vault_id
#     }


#     return request_json