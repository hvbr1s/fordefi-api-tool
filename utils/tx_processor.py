import os
from decimal import Decimal
from configs.ecosystem_configs import ECOSYSTEM_CONFIGS
from api_requests.tx_constructor import evm_tx_native, sol_tx_native, sui_tx_native, ton_tx_native, aptos_tx_native, btc_tx_native
from api_requests.tx_constructor_tokens import evm_tx_tokens, sol_tx_tokens

def process_transaction(ecosystem, evm_chain, vault_id, destination, value, custom_note, token):
    """
    This is your main entry point, combining both "native_configs" logic
    and "transaction processing" logic in one place.
    """

    # 1) Grab the ecosystem's config
    eco_config = ECOSYSTEM_CONFIGS.get(ecosystem)
    if not eco_config:
        raise ValueError(f"Ecosystem '{ecosystem}' is not supported.")

    # 2) If user didn't specify vault_id or destination, pull from config
    if vault_id == "default":
        vault_id = os.getenv(eco_config["vault_env"])
        print(f"Sending from vault {vault_id}")

    if destination == "default":
        destination = eco_config["default_dest"]
    
    # 3) Convert value to float, handle potential decimal or comma
    try:
        value = value.replace(",", ".")  # e.g. "1,5" => "1.5"
        float_value = float(value)
    except ValueError:
        raise ValueError("Invalid amount provided")

    # 4) Decide which dictionary to use for decimals
    if token:
        # For tokens, we do a basic decimal guess/validation 
        # but final conversion is in the token constructor
        assert float_value > 0, f"{token} amount must be positive!"
        print(f"Sending {value} {token.upper()} on {ecosystem.upper()}!")
    else:
        # For native coins
        decimals_native = eco_config["native"]["decimals"]
        smallest_unit = int(float_value * decimals_native)
        assert smallest_unit > 0, f"{eco_config['native']['unit_name']} amount must be positive!"
        print(f"Sending {float_value} {eco_config['native']['unit_name'].upper()} on {ecosystem.upper()}!")

    # 5) Decide which function to call based on ecosystem + token
    if not token:
        # If no token => do a "native" transfer
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
            raise ValueError(f"No native TX builder found for {ecosystem}")
        if ecosystem == "evm":
            # evm_tx_native expects chain + vault + dest + note + smallest_unit_value
            return builder(evm_chain, vault_id, destination, custom_note, str(smallest_unit))
        else:
            # sol_tx_native, etc. expect vault_id + destination + note + smallest_unit_value
            return builder(vault_id, destination, custom_note, str(smallest_unit))
    else:
        # If token => do a "token" transfer
        tx_functions = {
            "sol": sol_tx_tokens,
            "evm": evm_tx_tokens,
        }
        builder = tx_functions.get(ecosystem)
        if not builder:
            raise ValueError(f"No token TX builder found for {ecosystem}")

        if ecosystem == "evm":
            # evm_tx_tokens expects chain, vault, dest, note, value, token
            return builder(evm_chain, vault_id, destination, custom_note, value, token)
        else:
            # sol_tx_tokens expects vault_id, destination, note, smallest_unit_str, token
            # We still want to convert to the smallest-unit form
            # in case we want to ensure "1 USDC" => "1000000"
            decimals_token = ECOSYSTEM_CONFIGS["sol"]["tokens"][token]["decimals"]
            smallest_unit_value = int(Decimal(value) * Decimal(10 ** decimals_token))

            return builder(vault_id, destination, custom_note, str(smallest_unit_value), token)