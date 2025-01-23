from decimal import Decimal

def evm_tx_native(evm_chain, vault_id, destination, custom_note, value):
    """
    Build a transaction JSON for sending native EVM currency (ETH, BNB, etc.)
    - 'value' is assumed to be in decimal ETH-like units (e.g. "0.001" for 0.001 ETH).
    """

    # 1) Convert to smallest units (wei). For EVM: 1 ETH = 10^18 wei
    decimal_value = Decimal(value)
    smallest_unit = int(decimal_value * Decimal("1000000000000000000"))  # 1e18

    # 2) Check for at least 1 wei
    if smallest_unit < 1:
        raise ValueError(
            f"Value {value} is too small. Must be >= {Decimal(1) / Decimal('1e18')} ETH."
        )

    final_value = str(smallest_unit)

    print(f"⚙️ Preparing transaction to {destination} for {final_value} wei!")

    request_json = {
        "signer_type": "api_signer",
        "vault_id": vault_id,
        "note": custom_note,
        "type": "evm_transaction",
        "details": {
            "type": "evm_transfer",
            "gas": {
                "type": "priority",
                "priority_level": "medium"
            },
            "to": destination,
            "asset_identifier": {
                "type": "evm",
                "details": {
                    "type": "native",
                    "chain": f"evm_{evm_chain}_mainnet"
                }
            },
            "value": {
                "type": "value",
                "value": final_value  # <-- Must be integer-only string
            }
        }
    }

    return request_json


def sol_tx_native(vault_id, destination, custom_note, value):
    """
    Build a transaction JSON for sending SOL.
    - 'value' is assumed to be in decimal SOL units (e.g. "0.000000001" for 1 lamport).
    """

    # 1) Convert to lamports. 1 SOL = 1_000_000_000 lamports
    decimal_value = Decimal(value)
    smallest_unit = int(decimal_value * Decimal("1000000000"))

    # 2) Check for at least 1 lamport
    if smallest_unit < 1:
        raise ValueError(
            f"SOL amount {value} is too small. Must be >= {Decimal(1) / Decimal('1e9')} SOL."
        )

    final_value = str(smallest_unit)

    print(f"⚙️ Preparing transaction to {destination} for {final_value} lamports!")

    request_json = {
        "signer_type": "api_signer",
        "type": "solana_transaction",
        "details": {
            "type": "solana_transfer",
            "to": destination,
            "value": {
                "type": "value",
                "value": final_value  # integer-only
            },
            "asset_identifier": {
                "type": "solana",
                "details": {
                    "type": "native",
                    "chain": "solana_mainnet"
                }
            }
        },
        "note": custom_note,
        "vault_id": vault_id
    }

    return request_json


def sui_tx_native(vault_id, destination, custom_note, value):
    """
    Build a transaction JSON for sending SUI.
    - 'value' is assumed to be in decimal SUI units.
    - 1 SUI = 1_000_000_000 mist.
    """

    decimal_value = Decimal(value)
    smallest_unit = int(decimal_value * Decimal("1000000000"))  # 1 SUI = 1e9 mist

    if smallest_unit < 1:
        raise ValueError(
            f"SUI amount {value} is too small. Must be >= {Decimal(1) / Decimal('1e9')} SUI."
        )

    final_value = str(smallest_unit)

    print(f"⚙️ Preparing transaction to {destination} for {final_value} mist!")

    request_json = {
        "signer_type": "api_signer",
        "type": "sui_transaction",
        "details": {
            "type": "sui_transfer",
            "to": {
                "type": "hex",
                "address": destination
            },
            "value": {
                "type": "value",
                "value": final_value
            },
            "gas_config": {
                "payment": []
            },
            "asset_identifier": {
                "type": "sui",
                "details": {
                    "type": "native",
                    "chain": "sui_mainnet"
                }
            }
        },
        "note": custom_note,
        "vault_id": vault_id
    }

    return request_json


def ton_tx_native(vault_id, destination, custom_note, value):
    """
    Build a transaction JSON for sending TON.
    - 'value' is assumed to be in decimal TON.
    - 1 TON = 1_000_000_000 nanotons.
    """

    decimal_value = Decimal(value)
    smallest_unit = int(decimal_value * Decimal("1000000000"))

    if smallest_unit < 1:
        raise ValueError(
            f"TON amount {value} is too small. Must be >= {Decimal(1) / Decimal('1e9')} TON."
        )

    final_value = str(smallest_unit)

    print(f"⚙️ Preparing transaction to {destination} for {final_value} nanotons!")

    request_json = {
        "vault_id": vault_id,
        "note": custom_note,
        "signer_type": "api_signer",
        "sign_mode": "auto",
        "type": "ton_transaction",
        "details": {
            "type": "ton_transfer",
            "fail_on_prediction_failure": True,
            "push_mode": "auto",
            "to": {
                "type": "hex",
                "address": destination
            },
            "value": {
                "type": "value",
                "value": final_value
            },
            "asset_identifier": {
                "type": "ton",
                "details": {
                    "type": "native",
                    "chain": "ton_mainnet"
                }
            },
            "skip_prediction": False
        }
    }

    return request_json


def aptos_tx_native(vault_id, destination, custom_note, value):
    """
    Build a transaction JSON for sending APT.
    - 'value' is assumed to be in decimal APT.
    - 1 APT = 100_000_000 octas.
    """

    decimal_value = Decimal(value)
    smallest_unit = int(decimal_value * Decimal("100000000"))  # 1 APT = 1e8 octas

    if smallest_unit < 1:
        raise ValueError(
            f"APT amount {value} is too small. Must be >= {Decimal(1) / Decimal('1e8')} APT."
        )

    final_value = str(smallest_unit)

    print(f"⚙️ Preparing transaction to {destination} for {final_value} octas!")

    request_json = {
        "vault_id": vault_id,
        "note": custom_note,
        "signer_type": "api_signer",
        "sign_mode": "auto",
        "type": "aptos_transaction",
        "details": {
            "type": "aptos_transfer",
            "fail_on_prediction_failure": True,
            "gas_config": {
                "max_gas": "20000",
                "price": {
                    "type": "custom",
                    "price": "100"
                }
            },
            "to": {
                "type": "hex",
                "address": destination,
            },
            "value": {
                "type": "value",
                "value": final_value
            },
            "asset_identifier": {
                "type": "aptos",
                "details": {
                    "type": "native",
                    "chain": "aptos_mainnet"
                }
            },
            "skip_prediction": False,
            "push_mode": "auto"
        }
    }

    return request_json


def btc_tx_native(vault_id, destination, custom_note, value):
    """
    Build a transaction JSON for sending BTC.
    - 'value' is assumed to be in decimal BTC.
    - 1 BTC = 100_000_000 sats.
    """

    decimal_value = Decimal(value)
    smallest_unit = int(decimal_value * Decimal("100000000"))

    if smallest_unit < 1:
        raise ValueError(
            f"BTC amount {value} is too small. Must be >= {Decimal(1) / Decimal('1e8')} BTC."
        )

    final_value = str(smallest_unit)

    print(f"⚙️ Preparing transaction to {destination} for {final_value} sats!")

    request_json = {
        "vault_id": vault_id,
        "note": custom_note,
        "signer_type": "api_signer",
        "sign_mode": "auto",
        "type": "utxo_transaction",
        "details": {
            "type": "utxo_transfer",
            "outputs": [
                {
                    "to": {
                        "type": "address",
                        "address": destination
                    },
                    "value": final_value  # must be integer-only
                }
            ],
            "fee_per_byte": {
                "type": "priority",
                "priority_level": "low"
            },
            "push_mode": "auto"
        }
    }
    return request_json