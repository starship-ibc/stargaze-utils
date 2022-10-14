#!/usr/bin/env python3

import argparse
import json

from stargazeutils.common import slugified

parser = argparse.ArgumentParser(
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description="""
Calculates the rarity usng the same method as hubble, as saves the
information back to the json file.
""",
)

parser.add_argument("collection_name")
args = parser.parse_args()


trait_json = f"cache/collections/{slugified(args.collection_name)}.json"
with open(trait_json) as f:
    tokens = json.load(f)

ignored_traits = [
    "id",
    "image",
    "dna",
    "edition",
    "name",
    "hubble_rank",
    "rank",
    "score",
    "description",
    "egg_color",
    "egg_type",
    "egg_rarity",
]


def create_trait_rarity(tokens):
    traits = {}
    for token in tokens:
        for k, v in token.items():
            if k in ignored_traits:
                continue
            if k not in traits:
                traits[k] = {}
            if v not in traits[k]:
                traits[k][v] = 0
            traits[k][v] += 1
    return traits


def add_rarity_score(tokens):
    trait_counts = create_trait_rarity(tokens)
    for token in tokens:
        rarity_score = 0
        for k, v in token.items():
            if k in ignored_traits:
                continue
            count = trait_counts[k][v]
            pct = count / len(tokens)
            rarity_score += 100 / (pct * 100)
        token["score"] = rarity_score

    rank = 1
    next_rank = 2
    tokens.sort(key=lambda x: -x["score"])
    for i in range(len(tokens) - 1):
        print(f"token {tokens[i]['id']} rank {rank}")
        tokens[i]["rank"] = rank
        if tokens[i]["score"] != tokens[i + 1]["score"]:
            rank = next_rank
        next_rank += 1

        if "hubble_rank" in token:
            token.pop("hubble_rank")
    tokens[-1]["rank"] = rank


add_rarity_score(tokens)

print(f"saving to {trait_json}")
with open(trait_json, "w") as f:
    json.dump(tokens, f)
