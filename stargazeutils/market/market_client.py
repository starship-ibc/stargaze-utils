import logging
from typing import List

from stargazeutils.market.ask_collection import AskCollection

from ..errors import QueryError
from ..collection import NFTCollection
from ..common import DEFAULT_MARKET_CONTRACT
from ..stargaze import StargazeClient
from .market_ask import MarketAsk, SaleType
from .market_sale import MarketSale
from .unstable_helper import fetch_unstable_paged_data

LOG = logging.getLogger(__name__)


class MarketClient:
    """Client for the Stargaze Marketplace contract"""

    def __init__(
        self, contract: str = DEFAULT_MARKET_CONTRACT, sg_client: StargazeClient = None
    ):
        """Initializes the MarketClient.

        Arguments:
        - contract: The marketplace contract address
        - sg_client: The StargazeClient used for queries
        """
        self.contract = contract
        self.sg_client = sg_client or StargazeClient()

    def query_market(self, query: dict) -> dict:
        """Queries the market contract

        Arguments:
        - query: The market contract query"""
        return self.sg_client.query_contract(self.contract, query)

    def query_floor_price(self, sg721: str, count: int = 30) -> List[MarketAsk]:
        query = {
            "asks_sorted_by_price": {
                "collection": sg721,
                "limit": count,
            }
        }
        asks = self.query_market(query)["asks"]

        # Always strict verify because we shouldn't need to make many calls.
        for ask_dict in asks:
            ask = MarketAsk.from_dict(ask_dict)

            # Ignore auction floors
            if ask.sale_type != SaleType.FIXED_PRICE:
                LOG.warning(f"Ignoring {ask.sale_type} ask for token {ask.token_id}")
                continue

            # This should usually be a cached call.
            contract_info = self.sg_client.fetch_sg721_contract_info(ask.collection)
            ask.collection_name = contract_info.name

            owner_query = {"owner_of": {"token_id": str(ask.token_id)}}

            try:
                owner = self.sg_client.query_contract(ask.collection, owner_query)
            except QueryError as e:
                LOG.warning("Possilble burnt token on the floor")
                LOG.warning(f"{ask.collection} ({ask.collection_name}) #{ask.token_id}")
                continue

            ask.owner = owner["owner"]
            ask.approvals = owner["approvals"]
            if ask.is_valid(self.contract):
                return ask

        LOG.warning(f"Valid ask not found within the first {count} results")
        return None

    def fetch_bids_by_bidder(self, bidder: str) -> dict:
        """Fetches all bids for a given bidder.

        Arguments:
        - bidder: The bidder's stars address
        """
        query = {"bids_by_bidder": {"bidder": bidder}}
        return self.query_market(query)

    def fetch_ask_for_token(self, sg721: str, token_id: int) -> MarketAsk:
        """Fetches the current ask for a given token

        Arguments:
        - collection_sg721: The sg721 address for the collection
        - token_id: The token to query"""
        LOG.info(f"Looking up ask for token: {token_id}")
        query = {"ask": {"collection": sg721, "token_id": token_id}}
        ask = self.query_market(query)["ask"]
        if ask is None:
            return None

        return MarketAsk.from_dict(ask)

    # def fetch_collection_ask_count(self, sg721):
    #     """Fetches the number of asks for a given collection.

    #     Arguments:
    #     - sg721: The sg721 address to check"""
    #     query = {"ask_count": {"collection": sg721}}
    #     return self.query_market(query)["count"]

    # def remove_bid(self, sg721: str, token_id: int, wallet: str):
    #     cmd = {"remove_bid": {"collection": sg721, "token_id": token_id}}
    #     self.sg_client.execute_contract(self.contract, cmd, wallet)

    def fetch_asks_for_collection(
        self, nft_collection: NFTCollection, exclude_invalid=True, strict_verify=False
    ) -> AskCollection:
        """
        Fetches the current asks for a collection. Can include ownership and ]
        approval information for stricter validation but takes longer since each
        token must be queried.

        :param collection: str the NFT collection address
        :param exclude_invalid: If True, only returns valid asks (default True)
        :param strict_verify: Check token ownership and approvals.
                              Slows query. (default False)
        """
        collection_asks = []
        start_after = 0
        limit = 100

        query = {
            "asks": {
                "collection": nft_collection.sg721,
                "start_after": start_after,
                "limit": limit,
            }
        }
        asks = self.query_market(query)["asks"]

        while len(asks) > 0:
            LOG.info(f"Querying asks after {start_after}")
            for ask_data in asks:
                ask = MarketAsk.from_dict(ask_data)

                if ask.is_valid(self.contract) and strict_verify:
                    owner = self.sg_client.query_contract(
                        ask.collection, {"owner_of": {"token_id": str(ask.token_id)}}
                    )
                    ask.owner = owner["owner"]
                    ask.approvals = owner["approvals"]

                if not exclude_invalid or ask.is_valid(self.contract):
                    collection_asks.append(ask)

            start_after = asks[-1]["token_id"]
            query = {
                "asks": {
                    "collection": nft_collection.sg721,
                    "start_after": start_after,
                    "limit": limit,
                }
            }
            asks = self.query_market(query)["asks"]

        return AskCollection(collection_asks, nft_collection)

    def fetch_asks_for_tokens(
        self, nft_collection: NFTCollection, tokens: List[str]
    ) -> AskCollection:
        """Fetches the asks for a given list of tokens. This method
        can be used with NFTCollection.filter_tokens to speed up
        queries for listings.

        Arguments:
        - sg721: The collection sg721 address
        - tokens: A list of token ids to query"""
        asks = []
        for token_id in tokens:
            ask = self.fetch_ask_for_token(nft_collection.sg721, token_id)
            if ask is not None:
                asks.append(ask)

        return AskCollection(asks, nft_collection)

    def fetch_filtered_asks(
        self, nft_collection: NFTCollection, filters
    ) -> AskCollection:
        """Fetches asks for a given set of tokens by providing
        the collection tokens and a filter. This is a convenience
        method for the following:

        Arguments:
        - nft_collection: The collection of tokens with metadata
        - filters: {trait_name:[trait_value,...]}"""
        tokens = nft_collection.filter_tokens(filters)
        LOG.info(f"Selecting {len(tokens)} tokens")

        return self.fetch_asks_for_tokens(nft_collection, tokens)

    def fetch_collection_sales(self, sg721: str) -> List[MarketSale]:
        """Fetches the sales for a given collection by querying
        the blockchain for "wasm-finalize-sale" events. Please note
        that the chain sometimes returns unstable results.

        :param sg721: The collection SG721 address
        :return A list of MarketSales
        """
        url = self.sg_client.rest_url + "/txs"
        finalize_sale_params = {
            "wasm-finalize-sale.collection": sg721,
            "limit": 100,
            "page": 1,
        }
        pages = fetch_unstable_paged_data(url, finalize_sale_params)
        txs = []
        for page in pages:
            if "txs" in page:
                txs.extend([MarketSale.from_tx(tx) for tx in page["txs"]])
        return txs
