from app.domain.interfaces.user_repository import IUserRepository
from app.infrastructure.orm.user_model import UserModel

class SQLUserRepository(IUserRepository):

    def __init__(self, db):
        self.db = db

    def find_by_email(self, email):
        return self.db.query(UserModel).filter_by(email=email).first()

    def save(self, user):
        db_user = UserModel(
            email=user.email,
            password=user.password,
            role=user.role
        )
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user