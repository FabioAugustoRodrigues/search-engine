from redisearch import Client, TextField, NumericField, TagField, IndexDefinition, Query
import redis


class RedisSearchProvider:
    """
    Infrastructure provider that manages Redisearch connections and common data operations.
    """

    def __init__(self, client: redis.Redis):
        """
        Initialize the provider with an existing Redis client.
        """
        self._client = client

    def create_index(self, index_name: str, fields: list):
        client = Client(index_name, conn=self._client)

        redis_fields = []
        for f in fields:
            ftype = f["type"].lower()
            if ftype == "text":
                redis_fields.append(TextField(
                    f["name"],
                    sortable=f.get("sortable", False),
                    weight=f.get("weight", 1.0)
                ))
            elif ftype == "numeric":
                redis_fields.append(NumericField(
                    f["name"],
                    sortable=f.get("sortable", False)
                ))
            elif ftype == "tag":
                redis_fields.append(TagField(
                    f["name"],
                    sortable=f.get("sortable", False)
                ))
            else:
                pass

        try:
            client.create_index(
                redis_fields,
                definition=IndexDefinition(
                    prefix=[f"{index_name.lower()}:"]
                )
            )
        except Exception as e:
            pass