from .royalty_info import RoyaltyInfo


class CollectionInfo:
    """An object representing the collection_info response data."""

    def __init__(
        self,
        creator: str,
        description: str,
        royalty_info: RoyaltyInfo,
        image_url: str = None,
        external_link: str = None,
    ):
        """Initializes a new CollectionInfo object.

        Arguments:
        - creator: The collection creator address
        - description: The description of the collection
        - royalty_info: The collection royalty info
        - image_url: A marketing image URL
        - external_url: An external collecction web URL"""
        self.creator = creator
        self.description = description
        self.royalty_info = royalty_info
        self.image_url = image_url
        self.external_link = external_link

    def __eq__(self, o: object) -> bool:
        if type(o) is not type(self):
            return False
        if len(self.__dict__) != len(o.__dict__):
            return False
        for k, v in self.__dict__.items():
            if k not in o.__dict__:
                return False
            if v != o.__dict__[k]:
                return False
        return True

    def print(self):
        """Prints the collection information."""
        print("--- Collection Info ---")
        print(f"Creator: {self.creator}")
        print(f"Description: {self.description}")
        print(f"Royalties: {self.royalty_info}")
        print(f"Image: {self.image_url}")
        print(f"External URL: {self.external_link}")

    @classmethod
    def from_data(cls, data: dict):
        """Creates a CollectionInfo object from a collection_info
        starsd contract query.

        Arguments:
        - data: The data dictionary returned from the starsd query."""
        royalty_info = RoyaltyInfo.from_data(data["royalty_info"])
        return cls(
            creator=data["creator"],
            description=data["description"],
            royalty_info=royalty_info,
            image_url=data["image"],
            external_link=data["external_link"],
        )
