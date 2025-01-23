# Fordefi CLI

A command-line interface for broadcasting transactions using the Fordefi API.

⚠️ This tool is still in development, please test extensively with _small amounts_.

## Prerequisites

- Python 3.x
- Fordefi API User Token
- Fordefi API Signer

## Setup

1. Install `uv` package manager:
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

2. Set up the project an install dependencies:
   ```bash
   git clone <repository-url>
   cd <repository-name>
   uv sync
   ```

3. Configure environment variables:
   Create a `.env` file in the root directory with your Fordefi API user token:
   ```plaintext
   FORDEFI_API_USER_TOKEN="your_token"
   ```
4. Place your API Signer's `.pem` private key file in a `/secret` directory in the root folder.

5. Start the Fordefi API Signer:
   ```bash
   docker run --rm --log-driver local --mount source=vol,destination=/storage -it fordefi.jfrog.io/fordefi/api-signer:latest
   ```
   Then select "Run signer" in the Docker container.

6. Make the script executable:
   ```bash
   chmod +x fordefi_cli.py
   ```

## Usage

```bash
./fordefi_cli.py --vault-id <VAULT_ID> --destination <ADDRESS> --ecosystem <NETWORK> --value <AMOUNT> [OPTIONS]
```

### Required Arguments

- `--vault-id`: The vault ID from which to send the transaction
- `--destination`: The destination address
- `--ecosystem`: Network on which to broadcast the transaction (`sol`, `evm`, `sui`, `ton`, `apt`, `btc`)
- `--value`: Amount to send

### Optional Arguments

- `--evm-chain`: Required only if ecosystem is 'evm'. Options: `arbitrum`, `optimism`, `ethereum`, `bsc`
- `--token`: Token ticker (e.g., 'usdc', 'weth'). Omit for native assets
- `--note`: Custom note for the transaction

### Example

```bash
./fordefi_cli.py --vault-id v123 --destination 0x123... --ecosystem evm --evm-chain ethereum --value 1.5 --token usdc --note "Test transfer"
```

The transaction will be broadcast after confirming all details.

## This tool currently supports the following networks and assets:

- Ethereum (ETH)
- BSC (BNB and USDT)
- Arbitrum (ETH and USDC)
- Solana (SOL coins only)
- Sui (SUI coins only)
- Ton (TON coins only)
- Aptos (APT coins only)
- Bitcoin


## Adding more assets and networks

[Learn more](https://docs.fordefi.com/reference/transaction-types) about integrating other networks and assets.
