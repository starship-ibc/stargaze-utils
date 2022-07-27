# Stargaze Utilities

This python package provides a set of utilities for interacting with the [Stargaze](https://www.stargaze.zone/) NFT blockchain.

- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Examples](#examples)
- [Caching](#caching)
- [Donations](#donations)

## Prerequisites

- Python 3.10+ [install](https://www.python.org/downloads/)
- Poetry [install](https://python-poetry.org/docs/master/#installation)
- `starsd` in your `$PATH` [github](https://github.com/public-awesome/stargaze)

> If you don't have the starsd binary and want to try out, there is limited functionality by using the `QueryMethod.REST` query method passed in when creating your `StargazeClient`.

## Installation

You can install the package for use on your system with the following command:

```sh
poetry install
```

## Examples

There are some [examples](./examples) to get your started and some ideas on what you can do with the package. You can run them through poetry, for example:

```sh
poetry run python examples/get_new_collections.py
```

## Caching

Since much of the information on Stargaze doesn't change, specifically related to collection information and metadata, some data is automatically cached in the `cache` folder in either CSV or JSON format depending on the data. You can change where this by passing in custom parameter values.

IPFS, can be especially slow so you will likely want to use "requests_cache" as seen in the `get_collection_info` example. This package will automatically cache web requests, but be aware how that may affect other commands if you are not using the Stargaze binary.

```py
import requests_cache
requests_cache.install_cache("stargaze-ipfs")
```

The requests_cache package uses a sqlite database under the hood to store responses for any requests being made. See the [docs](https://requests-cache.readthedocs.io/en/stable/) for more information.

## Donations

A special thanks to [Andromeda Labs](https://twitter.com/AndromaverseLab) for sponsoring this library.

If you'd like to make a donation, you may send $STARS to the following address. If you're like to sponsor a specific issue, feel free to include it in the memo line so I know what's most important to the community.

```txt
stars1z6mj02l2s8v0vsxfsark5v7t076ds8pu9nj2fv
```
