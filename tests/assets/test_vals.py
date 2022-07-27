from datetime import datetime, timedelta

from stargazeutils.common import EPOCH

collection_name = "Test Collection"
sg721_cach_csv_path = "tests/assets/sg721_cache.csv"
sg721_addr = "stars17s7emulfygjuk0xn906athk5e5efsdtumsat5n2nad7mtrg4xres3ysf3p"
minter_addr = "minter"
whitelist_addr = "stars137gvy58wsjykawq0lqqys2een87v6e045qwu0nhr5rpqvpp9dsmqjnzaru"
owner = "owner"
ipfs_cid = "QmRvYPEHjsyXSg5UfqwnPoKMqcPuMHpo8ip5ReTCLh7621"
ipfs_hash = "bafybeibvigt7h6ysdkr62zb2uq5tcwbmiapnby2t3otgbvogli5otzfg7y"
collection_file = "tests/assets/eg_collection.json"
traitless_collection_file = "tests/assets/traitless_collection.json"


def str_from_timestamp(ts):
    return str(int((ts - EPOCH).total_seconds() * 1000)) + "000000"


future_timestamp_str = str_from_timestamp(datetime.utcnow() + timedelta(3))


minter_config_data = {
    "admin": "stars1zja6krwtcaa2ushn3z2m658k38qlg9qwg8casg",
    "base_token_uri": "ipfs://hash/metadata",
    "num_tokens": 8888,
    "per_address_limit": 2,
    "sg721_address": sg721_addr,
    "sg721_code_id": 1,
    "start_time": "1647129600000000000",
    "unit_price": {"denom": "ustars", "amount": "148000000"},
    "whitelist": whitelist_addr,
}

collection_info_data = {
    "creator": "stars1zja6krwtcaa2ushn3z2m658k38qlg9qwg8casg",
    "description": "test description",
    "image": "ipfs://QmVBi8jxc1mvucbiP712FQygbNFtNs8vdm3uCxxKtXiA4h",
    "external_link": None,
    "royalty_info": {
        "payment_address": "stars1fq6sg5knlc3a8j4y54wtg5mcsszzumvshxjpua",
        "share": "0.07",
    },
}

whitelist_data = {
    "num_members": 3593,
    "per_address_limit": 1,
    "member_limit": 4000,
    "start_time": "1647043200000000000",
    "end_time": "1647129600000000000",
    "unit_price": {"denom": "ustars", "amount": "148000000"},
    "is_active": False,
}

sg721_contract_info_data = {"name": "Stargaze Punks", "symbol": "SGP"}

token_traits = {
    1: {
        "id": 1,
        "name": "Stargaze Punks #1",
        "description": "test description",
        "image": "ipfs://hash/images/1.png",
        "dna": "d4134522511c42f71aba2a092119c188e71dfafd",
        "edition": 1,
        "Background": "control_room_stargaze_clouds",
        "Glow": "empty",
        "Back": "empty",
        "Species": "aphroditian",
        "FaceDetail": "mole",
        "Mouth": "basic_mouth",
        "Eyes": "magenta_eyes",
        "Tops": "orange__vapor_sun",
        "Hair": "pinkmidsideslick_hair",
        "Front": "yellowblack_headphones",
        "Bubble": "empty",
    },
    2: {
        "id": 2,
        "name": "Stargaze Punks #2",
        "description": "test description",
        "image": "ipfs://hash/images/2.png",
        "dna": "12800607f30210ffe58592c0c247ce0fccc958d2",
        "edition": 2,
        "Background": "teal_magic",
        "Glow": "pink_headglow",
        "Back": "empty",
        "Species": "humanoid7",
        "FaceDetail": "eyescar",
        "Mouth": "smaller_mouth",
        "Eyes": "blackwhite_eyes",
        "Tops": "white_turtleneck_top",
        "Hair": "pinkmediumwavy_hair",
        "Front": "redbugeye_glasses",
        "Bubble": "empty",
    },
}

traitless_token_metadata = [
    {
        "name": "Token #1",
        "description": "test description",
        "image": "ipfs://hash/images/1.png",
    },
    {
        "name": "Token #2",
        "description": "test description",
        "image": "ipfs://hash/images/1.png",
    },
]

traitless_token_traits = {
    1: {
        "id": 1,
        "name": "Token #1",
        "description": "test description",
        "image": "ipfs://hash/images/1.png",
    },
    2: {
        "id": 2,
        "name": "Token #2",
        "description": "test description",
        "image": "ipfs://hash/images/1.png",
    },
}

token_metadata = [
    {
        "name": "Stargaze Punks #1",
        "description": "test description",
        "image": "ipfs://hash/images/1.png",
        "dna": "d4134522511c42f71aba2a092119c188e71dfafd",
        "edition": 1,
        "attributes": [
            {"trait_type": "Background", "value": "control_room_stargaze_clouds"},
            {"trait_type": "Glow", "value": "empty"},
            {"trait_type": "Back", "value": "empty"},
            {"trait_type": "Species", "value": "aphroditian"},
            {"trait_type": "FaceDetail", "value": "mole"},
            {"trait_type": "Mouth", "value": "basic_mouth"},
            {"trait_type": "Eyes", "value": "magenta_eyes"},
            {"trait_type": "Tops", "value": "orange__vapor_sun"},
            {"trait_type": "Hair", "value": "pinkmidsideslick_hair"},
            {"trait_type": "Front", "value": "yellowblack_headphones"},
            {"trait_type": "Bubble", "value": "empty"},
        ],
    },
    {
        "name": "Stargaze Punks #2",
        "description": "test description",
        "image": "ipfs://hash/images/2.png",
        "dna": "12800607f30210ffe58592c0c247ce0fccc958d2",
        "edition": 2,
        "attributes": [
            {"trait_type": "Background", "value": "teal_magic"},
            {"trait_type": "Glow", "value": "pink_headglow"},
            {"trait_type": "Back", "value": "empty"},
            {"trait_type": "Species", "value": "humanoid7"},
            {"trait_type": "FaceDetail", "value": "eyescar"},
            {"trait_type": "Mouth", "value": "smaller_mouth"},
            {"trait_type": "Eyes", "value": "blackwhite_eyes"},
            {"trait_type": "Tops", "value": "white_turtleneck_top"},
            {"trait_type": "Hair", "value": "pinkmediumwavy_hair"},
            {"trait_type": "Front", "value": "redbugeye_glasses"},
            {"trait_type": "Bubble", "trait_value": "empty"},
        ],
    },
]
rarity = {
    "Background": {"control_room_stargaze_clouds": 1, "teal_magic": 1},
    "Glow": {"empty": 1, "pink_headglow": 1},
    "Back": {"empty": 2},
    "Species": {"aphroditian": 1, "humanoid7": 1},
    "FaceDetail": {"mole": 1, "eyescar": 1},
    "Mouth": {"basic_mouth": 1, "smaller_mouth": 1},
    "Eyes": {"magenta_eyes": 1, "blackwhite_eyes": 1},
    "Tops": {"orange__vapor_sun": 1, "white_turtleneck_top": 1},
    "Hair": {"pinkmidsideslick_hair": 1, "pinkmediumwavy_hair": 1},
    "Front": {"yellowblack_headphones": 1, "redbugeye_glasses": 1},
    "Bubble": {"empty": 2},
}

market_ask = {
    "sale_type": "fixed_price",
    "collection": sg721_addr,
    "token_id": 1,
    "seller": "seller-1",
    "price": "15000000000",
    "expires_at": future_timestamp_str,
    "funds_recipient": "seller-1",
    "reserve_for": None,
    "is_active": True,
    "finders_fee_bps": None,
}

sale_token_id = 42
sale_seller = "seller-1"
sale_buyer = "buyer-2"
sale_timestamp = datetime(2022, 5, 16, 22, 3, 48)
sale_height = 2901543
sale_price = "14000000000"
sale_tx_hash = "12345"
sale_tx = {
    "timestamp": sale_timestamp.strftime("%Y-%m-%dT%H:%M:%SZ"),
    "height": sale_height,
    "txhash": sale_tx_hash,
    "logs": [
        {
            "events": [
                {
                    "type": "wasm-finalize-sale",
                    "attributes": [
                        {"key": "token_id", "value": sale_token_id},
                        {"key": "price", "value": sale_price},
                        {"key": "seller", "value": sale_seller},
                        {"key": "buyer", "value": sale_buyer},
                    ],
                }
            ]
        }
    ],
}
