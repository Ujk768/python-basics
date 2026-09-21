from abc import ABC, abstractmethod

class BaseProcessor(ABC):
    @abstractmethod
    def process_data(self, data: dict) -> dict:
        """Subclasses must implement this method."""
        pass

class JSONProcessor(BaseProcessor):
    def process_data(self, data: dict) -> dict:
        # Implementation details hidden behind the abstract interface
        return {k.upper(): v for k, v in data.items()}