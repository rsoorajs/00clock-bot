from clock.storage.data_source.data_sources.sqlite.sql.item.base import NamedItem


class Type(NamedItem):
    pass


TYPE_INTEGER = Type("integer")
TYPE_TEXT = Type("text")
TYPE_REAL = Type("real")
