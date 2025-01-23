import os
from dotenv import load_dotenv

load_dotenv()

ECOSYSTEM_CONFIGS = {
    "sol": {
        "default_vault": "9597e08a-32a8-4f96-a043-a3e7f1675f8d",
        "default_dest": os.getenv("DEFAULT_DESTINATION_ADDRESS_SOL"),
        "native": {
            "decimals": 1_000_000_000,  # lamports
            "unit_name": "SOL"
        },
        "tokens": {
            "usdc": {
                "decimals": 6,
                "program_address": "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v"
            }
            # Add more Solana tokens here as needed
        },
    },
    "evm": {
        "default_vault": os.getenv("EVM_VAULT_ID"),
        "default_dest": os.getenv("DEFAULT_DESTINATION_ADDRESS_EVM"),
        "native": {
            "decimals": 1_000_000_000_000_000_000,  # wei
            "unit_name": "ETH"
        },
        "tokens": {
            "arbitrum": {
                "usdc": {
                    "contract_address": "0xaf88d065e77c8cC2239327C5EDb3A432268e5831",
                    "decimals": 6
                },
                "usdt": {
                    "contract_address": "0xFd086bC7CD5C481DCC9C85ebE478A1C0b69FCbb9",
                    "decimals": 6
                }
            },
            "bsc": {
                "usdt": {
                    "contract_address": "0x55d398326f99059fF775485246999027B3197955",
                    "decimals": 18
                }
            },
            "ethereum": {
                "usdt": {
                    "contract_address": "0xdAC17F958D2ee523a2206206994597C13D831ec7",
                    "decimals": 6
                }
            }
            # Add more Solana tokens here as needed
        },
    },
    "sui": {
        "default_vault": "0bbd4f4b-dcb0-47f0-a1a9-4a09614cd8c2",
        "default_dest": "0x20f2b0d2fe3ca33deba567a660d156b500ef7711d50be36aef71e5216d460b82",
        "native": {
            "decimals": 1_000_000_000,  # mist
            "unit_name": "SUI"
        },
    },
    "aptos": {
        "default_vault": "c1a0a9db-8520-45f9-ac0e-d004df2316c0",
        "default_dest": "0x08bfeca2e5589e112324dfdcb2f4f3c733d91955b6c8c6ca8ea329587f61d46c",
        "native": {
            "decimals": 100_000_000, # octa
            "unit_name": "APT"
        },
    },
    "ton": {
        "default_vault": "ab5fe345-4182-4ddc-b52d-f83821d4870f",
        "default_dest": "UQAarzA2uNSBq-FHxvP9RMgpggR7mGNnQRFRKoIWYJpdjSsq",
        "native": {
            "decimals": 1_000_000_000,  # nanotons
            "unit_name": "TON"
        },
    }
    # Add additional ecosystems here: 'btc', etc.
}
