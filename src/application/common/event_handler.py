from abc import abstractmethod, ABC


class EventHandler(ABC):
    @property
    @abstractmethod
    def get_event_names(self) -> list:
        raise NotImplementedError
