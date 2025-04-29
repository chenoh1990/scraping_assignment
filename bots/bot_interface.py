from abc import ABC, abstractmethod


class Bot(ABC):
    """
      abstract interface for all bots.
      defines the basic structure any bot must implement.
    """
    @abstractmethod
    def run(self):
        """
        starts the bot and begins listening for incoming messages or events.
        """
        pass

    @abstractmethod
    def send_message(self):
        """
        sends a message to a specific user or chat.
        """
        pass

    @abstractmethod
    def set_handlers(self):
        """
        registers all command and message handlers.
        defines how the bot reacts to different types of input.
        """
        pass
