#!/usr/bin/env python3

import os
import json
import datetime
import argparse
from dotenv import load_dotenv
from signing.signer import sign
from api_requests.broadcast import post_tx
from api_requests.tx_processor import process_transaction

def main():
    # 1. Load environment variables
    load_dotenv()
    FORDEFI_API_USER_TOKEN = os.getenv("FORDEFI_API_USER_TOKEN")

    if not FORDEFI_API_USER_TOKEN:
        raise RuntimeError("FORDEFI_API_USER_TOKEN not set in environment or .env file.")

    # 2. Parse arguments
    parser = argparse.ArgumentParser(
        description="CLI to broadcast transactions using the Fordefi API."
    )

    parser.add_argument(
        "--vault-id",
        required=True,
        help="The vault ID from which to send the transaction (required)."
    )
    parser.add_argument(
        "--destination",
        required=True,
        help="The destination address (required)."
    )
    parser.add_argument(
        "--ecosystem",
        choices=["sol", "evm", "sui", "ton", "apt", "btc"],
        required=True,
        help="Network on which to broadcast the transaction. Must be one of [sol, evm, sui, ton, apt, btc]."
    )
    parser.add_argument(
        "--evm-chain",
        choices=["arbitrum", "optimism", "ethereum", "bsc"],
        help="Required only if ecosystem is 'evm'; specify which EVM chain."
    )
    parser.add_argument(
        "--token",
        help="Token ticker (e.g., 'usdc', 'weth'). If sending a native asset (ETH, SOL, BNB, BTC, APT, SUI, TON, etc.), leave this flag out or pass an empty string."
    )
    parser.add_argument(
        "--value",
        required=True,
        help="Amount to spend (required)."
    )
    parser.add_argument(
        "--note",
        help="A custom note for the transaction (required)."
    )

    args = parser.parse_args()

    # 3. Validate arguments
    ecosystem = args.ecosystem.lower()
    
    if ecosystem == "evm":
        if not args.evm_chain:
            parser.error("When ecosystem is 'evm', --evm-chain is required.")
        evm_chain = args.evm_chain.lower()
    else:
        # Non-EVM networks won't need evm_chain
        evm_chain = None

    token = args.token.lower() if args.token else None
    vault_id = args.vault_id.lower()
    destination = args.destination.lower()
    value = args.value.lower()
    custom_note = args.note

    # 4. Print summary (like your old script did)
    print(f"🚀 Excellent! Sending from vault {vault_id} to {destination} on {ecosystem.upper()}"
          f"{f' -> {evm_chain}' if evm_chain else ''}.")

    # 5. Build the transaction
    request_json = process_transaction(
        ecosystem=ecosystem,
        evm_chain=evm_chain,
        vault_id=vault_id,
        destination=destination,
        value=value,
        custom_note=custom_note,
        token=token
    )

    # 6. Prepare request
    request_body = json.dumps(request_json)
    path = "/api/v1/transactions"
    timestamp = datetime.datetime.now().strftime("%s")
    payload = f"{path}|{timestamp}|{request_body}"

    # 7. Sign payload
    signature = sign(payload=payload)

    # 8. Broadcast transaction
    try:
        resp_tx = post_tx(path, FORDEFI_API_USER_TOKEN, signature, timestamp, request_body)
        print("✅ Transaction submitted successfully!")
        print(f"Transaction ID: {resp_tx.json().get('id', 'N/A')}")
    except RuntimeError as e:
        print(f"❌ {str(e)}")
        exit(1)
    except json.JSONDecodeError as e:
        print(f"❌ Failed to parse response: {str(e)}")
        print(f"Raw response: {resp_tx.text}")
        exit(1)

if __name__ == "__main__":
    main()