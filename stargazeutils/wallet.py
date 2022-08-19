import json
import logging
from datetime import datetime, timedelta
from typing import List

from .coin import Coin
from .collection import Sg721Client
from .common import str_from_timestamp
from .market import MarketAsk, MarketClient

LOG = logging.getLogger(__name__)


class Wallet:
    """Allows querying and signing transactions using the underlying
    starsd binary. This class will not function without being able to
    access the binary and will not be able to request signed transactions
    without the wallet being set up _in starsd_ prior to use.

    ⚠️ DANGER! THESE METHODS CALL STARSD TX AND HAS THE ABILITY TO AUTO-SIGN
    TRANSACTIONS. IT'S RECOMMENDED YOU REVIEW THIS CODE AND UNDERSTAND IT
    BEFORE USE. IT'S ALSO RECOMMENDED TO USE A SEPARATE WALLET WITH A LIMITED
    BALANCE WHEN USING THIS CLASS.

    NEVER SHARE YOUR MNEMONIC SEED PHRASE WITHOUT UNDERSTANDING WHAT YOU'RE
    DOING. THIS PYTHON PACKAGE DOES NOT ASK YOUR MNEMONIC."""

    def __init__(
        self,
        address: str,
        keyring_backend: str = "os",
        market_client: MarketClient = None,
    ):
        self.address = address
        self.keyring_backend = keyring_backend
        self.market_client = market_client or MarketClient()
        self.sg_client = self.market_client.sg_client

        self.query_flags = [
            "--node",
            self.sg_client.node,
            "--chain-id",
            self.sg_client.chain_id,
        ]

        self.tx_flags = self.query_flags + [
            "--keyring-backend",
            self.keyring_backend,
            "--gas-prices",
            "0.01ustars",
            "--gas",
            "auto",
            "--gas-adjustment",
            "1.15",
        ]

        print("┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓")
        print("┃                    🚨 DANGER!  DANGER! 🚨                    ┃")
        print("┃                                                              ┃")
        print(f"┃  Loaded wallet {self.address:44}  ┃")
        keyring_msg = f"with expected backend keyring {self.keyring_backend:7}"
        print(f"┃  {keyring_msg}                       ┃")
        print("┃                                                              ┃")
        print("┃  THIS APPLICATION MAY USE STARSD TO AUTO-SIGN TRANSACTIONS!  ┃")
        print("┃  PLEASE USE CAUTION!                                         ┃")
        print("┃                                                              ┃")
        print("┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛")

    def get_coins(self) -> List[Coin]:
        """Gets a list of coins that show the current balances of the
        address. For now, it's likely to either be 0 or 1 coin ($STARS).
        """
        cmd = ["starsd", "query", "bank", "balances", self.address] + self.query_flags
        tokens = self.sg_client._get_json(cmd)["balances"]
        coins = []
        for token in tokens:
            coins.append(Coin(token["amount"], token["denom"]))
        return coins

    def query_owned_tokens(self, collection):
        """Queries for the tokens in a collection owned by the wallet."""
        client = Sg721Client(collection, sg_client=self.sg_client)
        return client.query_tokens_owned_by(self.address)

    def _execute_wasm(
        self, contract: str, query: dict, amount: Coin = None, auto_sign: bool = False
    ):
        cmd = ["starsd", "tx", "wasm", "execute", contract, json.dumps(query)]
        if amount is not None:
            cmd.append("--amount")
            cmd.append(f"{amount.amount}{amount.denom}")

        cmd.append("--from")
        cmd.append(self.address)

        cmd.extend(self.tx_flags)
        if auto_sign:
            cmd.append("--yes")

        return self.sg_client._get_json(cmd)["txhash"]

    def send_funds(self, funds: Coin, to_address: str, auto_sign: bool = False) -> str:
        """Sends funds to another address."""
        LOG.info(f"Sending {funds} to {to_address} (auto_sign = {auto_sign})")

        funds_str = f"{funds.amount}{funds.denom}"
        cmd = [
            "starsd",
            "tx",
            "bank",
            "send",
            self.address,
            to_address,
            funds_str,
        ] + self.query_flags
        if auto_sign:
            cmd.append("--yes")

        return self.sg_client._get_json(cmd)["txhash"]

    def set_bid_from_ask(self, ask: MarketAsk, auto_sign: bool = False):
        """Sets a bid to purchase an ask."""
        return self.set_bid(ask.collection, ask.token_id, ask.price, auto_sign)

    def set_bid(
        self, collection: str, token_id: int, price: Coin, auto_sign: bool = False
    ):
        """Sets a bid for a token in a specific collection at a given price."""
        LOG.info(
            f"Setting bid on {collection} "
            f"#{token_id} @ {price} (auto_sign = {auto_sign})"
        )
        query = {
            "set_bid": {
                "collection": collection,
                "token_id": int(token_id),
                "expires": str_from_timestamp(datetime.utcnow() + timedelta(days=5)),
            }
        }

        return self._execute_wasm(self.market_client.contract, query, price, auto_sign)

    def transfer_nft(
        self, collection: str, token_id: int, recipient: str, auto_sign: bool = False
    ):
        """Transfers an NFT to another address."""
        LOG.info(
            f"Transferring token {token_id} in {collection}"
            f" to {recipient} (auto_sign={auto_sign})"
        )
        query = {"transfer_nft": {"token_id": str(token_id), "recipient": recipient}}

        return self._execute_wasm(collection, query, auto_sign=auto_sign)
