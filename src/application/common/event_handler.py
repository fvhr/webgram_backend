from abc import abstractmethod, ABC


class EventHandler(ABC):
    @property
    @abstractmethod
    def get_event_name(self) -> str:
        raise NotImplementedError
