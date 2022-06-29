from unittest import mock

from stargazeutils.collection import Sg721Client


@mock.patch("stargazeutils.StargazeClient")
def test_sg721_fetch_tokens_owned_by_should_return_tokens(sg_client):
    sg721 = "sg721"
    owner = "owner"
    client = Sg721Client(sg721, "minter", sg_client)

    sg_client.query_contract.return_value = {"data": {"tokens": [1, 2, 3]}}
    tokens = client.fetch_tokens_owned_by(owner)

    sg_client.query_contract.assert_called_with(sg721, {"tokens": {"owner": owner}})
    assert tokens == [1, 2, 3]

    # def fetch_tokens_owned_by(self, owner):
    #     return self.query_sg721({"tokens": {"owner": owner}})['tokens']

    # def query_minter_config(self) -> MinterConfig:
    #     if self._minter_config is None:
    #         self._minter_config = MinterConfig(self.query_minter({'config': {}}))
    #     return self._minter_config

    # def query_collection_info(self) -> CollectionInfo:
    #     if self._collection_info is None:
    #         data = self.query_sg721({"collection_info": {}})
    #         self._collection_info = CollectionInfo.from_data(data)
    #     return self._collection_info

    # def query_whitelist(self) -> Whitelist:
    #     if self._whitelist_config is None:
    #         wl_contract = self.query_minter_config().whitelist
    #         if wl_contract is None:
    #             return None
    #         self._whitelist_config = Whitelist(s...{'config': {}})['data'])
    #     return self._whitelist_config

    # def fetch_minter(self) -> str:
    #     return self.query_sg721({'minter': {}})['minter']

    # def fetch_minted_tokens(self, start_after: str = '0', limit=30):
    #     minted_tokens = []
    #     tokens = self.query_sg721({"all_tokens": {"start_after": start_after, \
    #       "limit": limit}})['tokens']
    #     while len(tokens) == limit:
    #         start_after = tokens[-1]
    #         LOG.debug(f"Fetching more tokens after {start_after}")
    #         minted_tokens += tokens
    #         tokens = self.query_sg721({"all_tokens": \
    #               {"start_after": start_after, "limit": limit}})['tokens']
    #     minted_tokens += tokens
    #     return minted_tokens

    # def fetch_owner_of_token(self, token_id):
    #     return self.query_sg721({"owner_of": {"token_id": str(token_id)}})

    # def fetch_num_minted_tokens(self):
    #     return self.query_sg721({"num_tokens": {}})['count']

    # def query_contract_info(self):
    #     return self.query_sg721({'contract_info': {}})

    # def query_nft_info(self, token_id: str):
    #     return self.query_sg721({'all_nft_info': {'token_id': token_id}})

    # def create_mintable_list(self, count=None):
    #     if count is None:
    #         count = self.query_minter_config().num_tokens

    #     return sorted([x for x in range(1,count+1)])

    # def fetch_holders(self):
    #     tokens = self.fetch_minted_tokens()
    #     holders = set()
    #     for token in tokens:
    #         if len(tokens) > 1000 and int(token) % 10 == 0:
    #             print(f"Fetching owner for token {token}")
    #         owner = self.query_sg721({"owner_of": {"token_id": token}})['owner']
    #         # print(owner)
    #         holders.add(owner)
    #     return holders

    # def watch_mint(self, target_id=None):
    #     # minted_tokens = self.fetch_minted_tokens()
    #     # num_minted = len(minted_tokens)
    #     num_tokens = self.query_minter_config().num_tokens
    #     # available_tokens = self.create_mintable_list(num_tokens)
    #     # for token in minted_tokens:
    #     #     available_tokens.remove(int(token))
    #     num_minted = self.fetch_num_minted_tokens()
    #     next_available = num_minted
    #     print('\007')
    #     last_minted_time = datetime.now()
    #     print(f"Next available: {next_available} Targeting token {target_id}")
    #     # safari = webdriver.Safari()
    #     while num_minted < num_tokens:
    #         new_num_minted = self.fetch_num_minted_tokens()
    #         if next_available == int(target_id):
    #             print("!!! MINT 1 NOW !!!")
    #             print('\007'*10)
    #         if next_available + 20 == int(target_id):
    #             print("!!! 20 UP !!! ")
    #             print('\007'*2)
    #         if next_available > int(target_id):
    #             print(" xxx missed it xxxx ")
    #             print(f" next available is {next_available}")
    #             break
    #         if new_num_minted > num_minted:
    #             print('\007')
    #             num_minted = new_num_minted
    #             next_available = num_minted
    #             image_url = f"https://{base_ifps}.ipfs.dweb.link/{next_available}.png"
    #             # safari.get(image_url)

    #             new_num_minted = self.fetch_num_minted_tokens()
    #             now = datetime.now()
    #             mint_delta = now - last_minted_time
    #             last_minted_time = now
    #             # mint_check = self.fetch_minted_tokens()
    #             # for token in mint_check:
    #             #     if token in available_tokens:
    #             #         available_tokens.remove(token)
    #             # next_available = available_tokens[0]
    #             print(f"\n{now} Minting next = {next_available} {image_url}")
    #             print(f"Time since last mint = {mint_delta}")
    #             traits = self.fetch_traits_for_token(next_available)
    #             pprint(traits)
    #         if target_id is not None and int(target_id) - num_minted > 100:
    #             time.sleep(20)
    #         n = datetime.now().strftime('%I:%M:%S')
    #         print(".", end='', flush=True)

    # def fetch_traits_for_token(self, token_id):
    #     base_url = '{base_ifps}.ipfs.dweb.link'
    #     url = f"https://{base_url}/{token_id}"
    #     r = {}
    #     try:
    #         r = requests.get(url).json()
    #     except:
    #         r = {"warning": "error fetching traits"}

    #     return r

    # @staticmethod
    # def https_from_ipfs(ipfs: str) -> str:
    #     parts = ipfs.split('/')
    #     path = "/".join(parts[3:])
    #     return f"https://{parts[2]}.ipfs.dweb.link/{path}"

    # def fetch_traits(self):
    #     config = self.query_minter_config()
    #     base_url = Sg721Client.https_from_ipfs(config.base_token_uri)

    #     token_attrs = []
    #     def _get_url(url):
    #         count = 1
    #         while True:
    #             r = requests.get(url)
    #             if r.status_code == 200:
    #                 return r.json()
    #             LOG.warn(f"Error {count} processing url {url}: {r.status_code}")
    #             count += 1
    #             time.sleep(0.5)

    #     for id in range(1, config.num_tokens + 1):
    #         url = f"{base_url}/{id}"
    #         LOG.info(f"Fetching attributes from {url}")
    #         metadata = _get_url(url)
    #         traits = {}
    #         for attr in metadata['attributes']:
    #             if 'trait_value' in attr:
    #                 trait = attr['trait_type']
    #                 value = attr['trait_value']
    #                 traits[trait] = value
    #             elif 'value' in attr:
    #                 trait = attr['trait_type']
    #                 value = attr['value']
    #                 traits[trait] = value
    #         traits['id'] = id
    #         traits['name'] = metadata['name']
    #         traits['image'] = metadata['image']
    #         token_attrs.append(traits)

    #     # print(token_attrs)
    #     return token_attrs

    # def export_traits_json(self, filename):
    #     traits = self.fetch_traits()
    #     with open(filename, 'w') as f:
    #         json.dump(traits, f)

    # def export_traits_csv(self, filename):
    #     traits = self.fetch_traits()
    #     headers = list(traits[0].keys())
    #     with open(filename, 'w') as f:
    #         f.write('"' + '","","",'.join(headers) + '"\n')
    #         for token in traits:
    #             for col in headers[:-1]:
    #                 value = "null"
    #                 if col in token:
    #                     value = token[col]
    #                 f.write('"' + str(value) + '","","",')
    #             f.write('"' + str(token[headers[-1]]) + '"\n')

    # def fetch_trait_rarity(self):
    #     tokens_info = self.fetch_traits()
    #     traits = {}
    #     for token in tokens_info:
    #         for trait in token.keys():
    #             if trait not in ['id', 'name', 'image']:
    #                 if trait not in traits:
    #                     traits[trait] = {token[trait]: 1}
    #                 elif token[trait] not in traits[trait]:
    #                     traits[trait][token[trait]] = 1
    #                 else:
    #                     traits[trait][token[trait]] += 1

    #     return traits

    # def print_trait_rarity(self):
    #     traits = self.fetch_trait_rarity()
    #     print('\n---')
    #     print('Trait Rarity')
    #     total_tokens = sum(list(traits.values())[0].values())
    #     print(f"Total Tokens: {total_tokens}")
    #     print('---\n')
    #     for trait_name, trait_options in traits.items():
    #         print(f"*** {trait_name} ***")
    #         print(f"# Options: {len(trait_options.keys())}")
    #         for o,v in sorted(trait_options.items(), key=lambda x: x[1]):
    #             print(f"- {o:<25}: {v:<5} ({v / total_tokens * 100:0.2f}%)")
    #         print("\n")
