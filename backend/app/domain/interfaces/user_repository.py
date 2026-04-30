from abc import ABC, abstractmethod

class IUserRepository(ABC):

    @abstractmethod
    def find_by_email(self, email):
        pass

    @abstractmethod
    def save(self, user):
        pass