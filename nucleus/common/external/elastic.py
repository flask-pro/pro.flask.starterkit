from typing import Tuple

from elasticsearch import Elasticsearch

from nucleus.common.extensions import db
from nucleus.config import Config

elasticsearch = Elasticsearch([Config.ELASTICSEARCH_URL])


class FulltextSearch:
    @classmethod
    def add_to_index(cls, obj: db.Model):
        if hasattr(obj, "dict_to_search"):
            index = obj.__tablename__
            payload = obj.dict_to_search()
            elasticsearch.index(index=index, doc_type=index, id=obj.id, body=payload)

    @classmethod
    def remove_from_index(cls, obj: db.Model):
        if hasattr(obj, "dict_to_search"):
            index = obj.__tablename__
            elasticsearch.delete(index=index, doc_type=index, id=obj.id)

    @classmethod
    def query_index(
        cls, model: db.Model, query: str, page: int, per_page: int, fields_to_filter: dict
    ) -> Tuple[list, dict]:
        index = model.__tablename__

        search_query = {
            "query": {
                "bool": {"must": [{"query_string": {"query": f"*{query}*", "fields": ["*"]}}]}
            },
            "from": (page - 1) * per_page,
            "size": per_page,
        }

        if fields_to_filter:
            search_query["query"]["bool"]["filter"] = [{"match": fields_to_filter}]

        result = elasticsearch.search(index=index, doc_type=index, body=search_query)

        ids = [hit["_id"] for hit in result["hits"]["hits"]]
        return ids, result["hits"]["total"]
