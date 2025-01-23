from decimal import Decimal
from dotenv import load_dotenv
from configs.ecosystem_configs import ECOSYSTEM_CONFIGS
from api_requests.tx_constructor_native import (
    evm_tx_native, sol_tx_native, sui_tx_native, ton_tx_native, aptos_tx_native, btc_tx_native
)
from api_requests.tx_constructor_tokens import evm_tx_tokens, sol_tx_tokens

load_dotenv()

def process_transaction(ecosystem, evm_chain, vault_id, destination, value, custom_note, token):

    # 1) Grab the ecosystem config
    eco_config = ECOSYSTEM_CONFIGS.get(ecosystem)
    if not eco_config:
        raise ValueError(f"Ecosystem '{ecosystem}' is not supported.")

    # 2) Resolve "default" vault/destination from configs
    if vault_id == "default":
        vault_id = eco_config["default_vault"]
    if destination == "default":
        destination = eco_config["default_dest"]

    # 3) Convert value to float
    try:
        value = value.replace(",", ".")
        float_value = float(value)
    except ValueError:
        raise ValueError("Invalid amount provided.")

    if not token:
        # 4a) We summon the native coin logic
        decimals_native = eco_config["native"]["decimals"]
        smallest_unit = int(float_value * decimals_native)
        if smallest_unit <= 0:
            raise ValueError(f"{eco_config['native']['unit_name']} amount must be positive!")

        # Then we wecide which native tx builder to call
        tx_functions = {
            "sol": sol_tx_native,
            "evm": evm_tx_native,
            "sui": sui_tx_native,
            "ton": ton_tx_native,
            "apt": aptos_tx_native,
            "btc": btc_tx_native
        }
        builder = tx_functions.get(ecosystem)
        if not builder:
            raise ValueError(f"No native TX builder found for {ecosystem}.")

        # EVM native has a different signature that requires an extra evm param
        if ecosystem == "evm":
            return builder(evm_chain, vault_id, destination, custom_note, str(smallest_unit))
        else:
            return builder(vault_id, destination, custom_note, str(smallest_unit))

    else:
        # 4b) Token logic
        # Instead of letting the second script do *all* the checks, we do them here

        if ecosystem == "evm":
            evm_config = ECOSYSTEM_CONFIGS["evm"]
            if evm_chain not in evm_config["tokens"]:
                raise ValueError(f"Chain '{evm_chain}' is not supported in EVMC config.")

            chain_tokens = evm_config["tokens"][evm_chain]
            if token not in chain_tokens:
                raise ValueError(f"Token '{token}' is not supported on chain '{evm_chain}'.")

            token_info = chain_tokens[token]
            contract_address = token_info["contract_address"]
            decimals = token_info["decimals"]
            
            # Convert to on-chain value
            multiplier = Decimal(10) ** decimals
            on_chain_value = str(int(Decimal(value) * multiplier))

            # Call function to build json
            return evm_tx_tokens(
                evm_chain, vault_id, destination, custom_note, on_chain_value, contract_address
            )

        elif ecosystem == "sol":
            sol_config = ECOSYSTEM_CONFIGS["sol"]
            if token not in sol_config["tokens"]:
                raise ValueError(f"Token '{token}' is not supported on Solana.")

            token_info = sol_config["tokens"][token]
            program_address = token_info["program_address"]
            decimals = token_info["decimals"]

            multiplier = Decimal(10) ** decimals
            on_chain_value = str(int(Decimal(value) * multiplier))

            return sol_tx_tokens(
                vault_id, destination, custom_note, on_chain_value, program_address
            )
        else:
            raise ValueError(f"No token TX builder found for ecosystem '{ecosystem}'.")