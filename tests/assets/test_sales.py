# flake8: noqa E501
# JSON example

from stargazeutils.common import MARKET_CONTRACT

sales = {
    "total_count": "1",
    "count": "1",
    "page_number": "1",
    "page_total": "1",
    "limit": "100",
    "txs": [
        {
            "height": "2901543",
            "txhash": "823256EB2CAD90EE0E07ACC01980E8CF6A18E4C843F1015393598AC204B8C5A8",
            "data": "0A260A242F636F736D7761736D2E7761736D2E76312E4D736745786563757465436F6E7472616374",
            "logs": [
                {
                    "events": [
                        {
                            "type": "message",
                            "attributes": [
                                {
                                    "key": "action",
                                    "value": "/cosmwasm.wasm.v1.MsgExecuteContract",
                                },
                                {"key": "module", "value": "wasm"},
                                {"key": "sender", "value": "buyer-1"},
                            ],
                        },
                        {
                            "type": "transfer",
                            "attributes": [
                                {
                                    "key": "recipient",
                                    "value": MARKET_CONTRACT,
                                },
                                {"key": "sender", "value": "buyer-1"},
                                {"key": "amount", "value": "1300000000ustars"},
                                {
                                    "key": "recipient",
                                    "value": "stars1xds4f0m87ajl3a6az6s2enhxrd0wta48y6thcw",
                                },
                                {
                                    "key": "sender",
                                    "value": MARKET_CONTRACT,
                                },
                                {"key": "amount", "value": "13000000ustars"},
                                {
                                    "key": "recipient",
                                    "value": "stars1jv65s3grqf6v6jl3dp4t6c9t9rk99cd8nrnpzw",
                                },
                                {
                                    "key": "sender",
                                    "value": MARKET_CONTRACT,
                                },
                                {"key": "amount", "value": "13000000ustars"},
                                {
                                    "key": "recipient",
                                    "value": "stars1fq6sg5knlc3a8j4y54wtg5mcsszzumvshxjpua",
                                },
                                {
                                    "key": "sender",
                                    "value": MARKET_CONTRACT,
                                },
                                {"key": "amount", "value": "91000000ustars"},
                                {"key": "recipient", "value": "seller-1"},
                                {
                                    "key": "sender",
                                    "value": MARKET_CONTRACT,
                                },
                                {"key": "amount", "value": "1183000000ustars"},
                            ],
                        },
                        {
                            "type": "wasm",
                            "attributes": [
                                {
                                    "key": "_contract_address",
                                    "value": "stars17s7emulfygjuk0xn906athk5e5efsdtumsat5n2nad7mtrg4xres3ysf3p",
                                },
                                {"key": "action", "value": "transfer_nft"},
                                {
                                    "key": "sender",
                                    "value": MARKET_CONTRACT,
                                },
                                {"key": "recipient", "value": "buyer-1"},
                                {"key": "token_id", "value": "6681"},
                                {
                                    "key": "_contract_address",
                                    "value": "stars1vlwnjfxhtqvq8tf67wkt82utpkeuehha4rw9qjg6tecgnntq990qh8wcp9",
                                },
                                {"key": "action", "value": "claim_buy_nft"},
                                {
                                    "key": "collection",
                                    "value": "stars17s7emulfygjuk0xn906athk5e5efsdtumsat5n2nad7mtrg4xres3ysf3p",
                                },
                                {"key": "token_id", "value": "6681"},
                                {"key": "price", "value": "1300000000ustars"},
                                {"key": "seller", "value": "seller-1"},
                                {"key": "buyer", "value": "buyer-1"},
                            ],
                        },
                        {
                            "type": "wasm-fair_burn",
                            "attributes": [
                                {
                                    "key": "_contract_address",
                                    "value": MARKET_CONTRACT,
                                },
                                {"key": "burn_amount", "value": "13000000"},
                                {"key": "dist_amount", "value": "13000000"},
                            ],
                        },
                        {
                            "type": "wasm-finalize-sale",
                            "attributes": [
                                {
                                    "key": "_contract_address",
                                    "value": MARKET_CONTRACT,
                                },
                                {
                                    "key": "collection",
                                    "value": "stars17s7emulfygjuk0xn906athk5e5efsdtumsat5n2nad7mtrg4xres3ysf3p",
                                },
                                {"key": "token_id", "value": "6681"},
                                {"key": "seller", "value": "seller-1"},
                                {"key": "buyer", "value": "buyer-1"},
                                {"key": "price", "value": "1300000000"},
                            ],
                        },
                        {
                            "type": "wasm-royalty-payout",
                            "attributes": [
                                {
                                    "key": "_contract_address",
                                    "value": MARKET_CONTRACT,
                                },
                                {
                                    "key": "collection",
                                    "value": "stars17s7emulfygjuk0xn906athk5e5efsdtumsat5n2nad7mtrg4xres3ysf3p",
                                },
                                {"key": "amount", "value": "91000000ustars"},
                                {
                                    "key": "recipient",
                                    "value": "stars1fq6sg5knlc3a8j4y54wtg5mcsszzumvshxjpua",
                                },
                            ],
                        },
                        {
                            "type": "wasm-set-bid",
                            "attributes": [
                                {
                                    "key": "_contract_address",
                                    "value": MARKET_CONTRACT,
                                },
                                {
                                    "key": "collection",
                                    "value": "stars17s7emulfygjuk0xn906athk5e5efsdtumsat5n2nad7mtrg4xres3ysf3p",
                                },
                                {"key": "token_id", "value": "6681"},
                                {"key": "bidder", "value": "buyer-1"},
                                {"key": "bid_price", "value": "1300000000"},
                                {"key": "expires", "value": "1653948229.573000000"},
                            ],
                        },
                    ]
                }
            ],
            "gas_wanted": "666666",
            "gas_used": "216194",
            "tx": {
                "type": "cosmos-sdk/StdTx",
                "value": {
                    "msg": [
                        {
                            "type": "wasm/MsgExecuteContract",
                            "value": {
                                "sender": "buyer-1",
                                "contract": MARKET_CONTRACT,
                                "msg": {
                                    "set_bid": {
                                        "collection": "stars17s7emulfygjuk0xn906athk5e5efsdtumsat5n2nad7mtrg4xres3ysf3p",
                                        "token_id": 6681,
                                        "expires": "1653948229573000000",
                                    }
                                },
                                "funds": [{"denom": "ustars", "amount": "1300000000"}],
                            },
                        }
                    ],
                    "fee": {
                        "amount": [{"denom": "ustars", "amount": "16667"}],
                        "gas": "666666",
                    },
                    "signatures": [],
                    "memo": "",
                    "timeout_height": "0",
                },
            },
            "timestamp": "2022-05-16T22:03:48Z",
        }
    ],
}
