"""Web3 agent for analyzing blockchain/smart contract components."""

from typing import List
from .base_agent import BaseClusterAgent


class Web3Agent(BaseClusterAgent):
    """Agent specialized in analyzing Web3/Blockchain code."""

    CLUSTER_NAME = "Web3"

    FOCUS_AREAS = [
        "Smart contract architecture",
        "Token standards (ERC20, ERC721, etc.)",
        "DeFi protocols",
        "Frontend Web3 integration",
        "Testing and deployment",
        "Security considerations"
    ]

    KEY_FILE_PATTERNS = [
        "contract", "token", "nft", "deploy", "hardhat.config",
        "foundry.toml", "truffle-config", "anchor"
    ]

    def get_system_prompt(self) -> str:
        return """You are an expert Web3/Blockchain Developer.

Your expertise includes:
- Solidity smart contract development
- Hardhat, Foundry, Truffle frameworks
- OpenZeppelin contracts and security patterns
- ERC standards (ERC20, ERC721, ERC1155)
- DeFi protocols (AMM, lending, staking)
- ethers.js, web3.js, viem
- Solana/Anchor development
- Security best practices and auditing

When analyzing code, focus on:
1. Smart contract purpose and functionality
2. Token standard implementation
3. Access control patterns
4. State variables and their purpose
5. Key functions and their roles
6. Events for frontend integration
7. Security patterns used
8. Test coverage

Provide documentation including:
- Contract overview and purpose
- Key functions with descriptions
- Events emitted
- Deployment instructions
- Network configurations
- Security considerations
- Contract interaction diagram (Mermaid)"""

    def select_important_files(self, files: List[dict], max_files: int = 15) -> List[str]:
        """Prioritize Web3-specific files."""
        selected = []

        # Priority 1: Main contracts
        for file in files:
            name = file["name"].lower()
            if name.endswith(".sol") or name.endswith(".vy"):
                # Skip interfaces and mocks
                if "interface" not in name and "mock" not in name and "test" not in name:
                    selected.append(file["path"])

        # Priority 2: Config files
        config_files = [
            "hardhat.config.js", "hardhat.config.ts", "foundry.toml",
            "truffle-config.js", "anchor.toml"
        ]
        for file in files:
            if file["name"] in config_files:
                if file["path"] not in selected:
                    selected.append(file["path"])

        # Priority 3: Deploy scripts
        for file in files:
            path = file["path"].lower()
            name = file["name"].lower()
            if "deploy" in path or "deploy" in name:
                if file["path"] not in selected:
                    selected.append(file["path"])

        # Priority 4: Test files
        for file in files:
            path = file["path"].lower()
            if "/test/" in path and file["path"] not in selected:
                selected.append(file["path"])

        # Fill with remaining
        for file in files:
            if len(selected) >= max_files:
                break
            if file["path"] not in selected:
                selected.append(file["path"])

        return selected[:max_files]
