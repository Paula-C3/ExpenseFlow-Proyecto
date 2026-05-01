from abc import ABC, abstractmethod

class RequestState(ABC):

    @abstractmethod
    def submit(self, request):
        pass

    @abstractmethod
    def approve(self, request):
        pass

    @abstractmethod
    def reject(self, request):
        pass

    @abstractmethod
    def complete(self, request):
        pass