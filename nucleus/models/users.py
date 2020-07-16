from nucleus.models import db
from nucleus.models.base import Base


class Users(Base):
    username = db.Column(db.String, nullable=False, comment='Username')

    @classmethod
    def create(cls, user: dict) -> dict:
        create_user = Users(**user)
        db.session.add(create_user)
        db.session.commit()
        return create_user.to_dict()

    @classmethod
    def get(cls, id_: int):
        user = Users.query.filter_by(id=id_).one()
        return user.to_dict()

    @classmethod
    def update(cls, user: dict):
        new_user = Users.query.filter_by(id=user['id']).one()
        new_user.username = user['username']
        db.session.commit()
        return user

    @classmethod
    def delete(cls, id_: int):
        Users.query.filter_by(id=id_).delete()
        return None

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'username': self.username,
        }
