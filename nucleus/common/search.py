from typing import Tuple

from elasticsearch import Elasticsearch

from nucleus.common.errors import NoResultSearch
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
        cls, model: db.Model, query: str, page: int, per_page: int
    ) -> Tuple[list, dict]:
        index = model.__tablename__
        result = elasticsearch.search(
            index=index,
            doc_type=index,
            body={
                "query": {"multi_match": {"query": query, "fields": ["*"]}},
                "from": (page - 1) * per_page,
                "size": per_page,
            },
        )

        if result["hits"]["total"]["value"] == 0:
            raise NoResultSearch(f"Result query <{query}> for index <{index}> empty.")

        ids = [hit["_id"] for hit in result["hits"]["hits"]]
        return ids, result["hits"]["total"]
