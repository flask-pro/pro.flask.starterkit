from sqlalchemy.ext.hybrid import hybrid_property

from nucleus.common.extensions import db
from nucleus.models.base import Base


class Logs(Base):
    __filterable__ = ["email", "event"]
    __interval_filterable__ = ["datetime_created"]
    __sortable__ = ["datetime_created"]

    email = db.Column(db.String, comment="email")
    _event = db.Column(db.String, nullable=False, comment="Event")

    events_messages = {
        "user_signup": "Регистрация пользователя",
        "user_created": "Пользователь создан",
        "user_blocked": "Пользователь заблокирован",
        "user_unblocked": "Пользователь разблокирован",
        "user_deleted": "Пользователь удалён",
    }

    @hybrid_property
    def event(self) -> str:
        return self._event

    @event.setter
    def event(self, event: str) -> None:
        if event in self.events_messages:
            self._event = event
        else:
            raise ValueError(f"Non-existent event <{event}> is assigned to be logged!")

    def to_dict(self) -> dict:
        article = {
            "id": self.id,
            "email": self.email,
            "event": self.event,
            "message": self.events_messages[self._event],
            "description": self.description,
            "datetime_created": self.datetime_created,
        }
        return self.non_empty_parameters_to_dict(article)
