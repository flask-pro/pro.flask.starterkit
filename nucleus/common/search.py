from typing import Tuple

from nucleus.common.extensions import db
from elasticsearch import Elasticsearch
from sqlalchemy.orm.query import Query
from sqlalchemy.orm.session import Session

from nucleus.common.errors import NoResultSearch
from nucleus.config import Config

elasticsearch = Elasticsearch([Config.ELASTICSEARCH_URL])


class SearchEngineMixin:
    @classmethod
    def add_to_index(cls, index: str, model: db.Model):
        payload = {}
        for field in model.__searchable__:
            payload[field] = getattr(model, field)
        elasticsearch.index(index=index, doc_type=index, id=model.id, body=payload)

    @classmethod
    def remove_from_index(cls, index: str, model: db.Model):
        elasticsearch.delete(index=index, doc_type=index, id=model.id)

    @classmethod
    def query_index(cls, index: str, query: str, page: int, per_page: int) -> Tuple[list, dict]:
        search = elasticsearch.search(
            index=index,
            doc_type=index,
            body={
                "query": {"multi_match": {"query": query, "fields": ["*"]}},
                "from": (page - 1) * per_page,
                "size": per_page,
            },
        )

        if search["hits"]["total"]["value"] == 0:
            raise NoResultSearch(f"Result query <{query}> for index <{index}> empty.")

        ids = [int(hit["_id"]) for hit in search["hits"]["hits"]]
        return ids, search["hits"]["total"]


class FullTextSearchMixin(SearchEngineMixin):
    @classmethod
    def search(cls, expression: str, page: int, per_page: int) -> Tuple[Query, dict]:
        ids, total = cls.query_index(cls.__tablename__, expression, page, per_page)

        when = [(ids[i], i) for i in range(len(ids))]
        query_result = cls.query.filter(cls.id.in_(ids)).order_by(db.case(when, value=cls.id))

        return query_result, total

    @classmethod
    def before_commit(cls, session: Session):
        session._changes = {
            "add": list(session.new),
            "update": list(session.dirty),
            "delete": list(session.deleted),
        }

    @classmethod
    def after_commit(cls, session: Session):
        for obj in session._changes["add"]:
            if isinstance(obj, SearchEngineMixin):
                cls.add_to_index(obj.__tablename__, obj)
        for obj in session._changes["update"]:
            if isinstance(obj, SearchEngineMixin):
                cls.add_to_index(obj.__tablename__, obj)
        for obj in session._changes["delete"]:
            if isinstance(obj, SearchEngineMixin):
                cls.remove_from_index(obj.__tablename__, obj)
        session._changes = None

    @classmethod
    def reindex(cls):
        for obj in cls.query:
            cls.add_to_index(cls.__tablename__, obj)


db.event.listen(db.session, "before_commit", FullTextSearchMixin.before_commit)
db.event.listen(db.session, "after_commit", FullTextSearchMixin.after_commit)
