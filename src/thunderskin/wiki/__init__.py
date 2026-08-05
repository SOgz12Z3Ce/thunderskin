from thunderskin.object import Object
from thunderskin.resource import Resource
from thunderskin.wiki.escape import escape


def key(entry: Object | Resource) -> str:
    return escape(entry.symbol())
