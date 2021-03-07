import asyncio
import contextlib
import termios
import logging
import sys


class KeyReader:
    """Reads input from stdin and sets a new orientation for the relevant
    Snake object"""

    def __init__(self, snake_keys):
        """
        Parameters
        ----------
        snake_keys: dict(str, tuple(Snake, tuple))
            Mapping between snakes and their individual key bindings. Key
            bindings are a dictionary of strings and direction tuples.
        """
        self.snake_keys = snake_keys

    async def get_keys(self, loop):
        """Get each keypress from stdin and set new orientations

        Parameters
        ----------
        loop: asyncio.AbstractEventLoop
            An instance of the relevant (OS-dependent) event loop
        """
        try:
            # Connect up stdin and our event loop
            with raw_mode(sys.stdin):
                read = asyncio.StreamReader()
                await loop.connect_read_pipe(
                    lambda: asyncio.StreamReaderProtocol(read), sys.stdin
                )
            # Wait for input
            while not read.at_eof():
                ch = await read.read(1)
                logging.error(ch)
                if not ch or ord(ch) <= 4:
                    break
                ch = ch.decode('utf8')
                snake, dir = self.snake_keys.get(ch, (None, None))
                logging.error(f"snake {snake} dir {dir} ch{ch}")
                if snake is not None:
                    snake.set_direction(dir)
                    logging.error(snake.facing)
            logging.error('end of loop')
        finally:
            loop.create_task(self.get_keys(loop))


@contextlib.contextmanager
def raw_mode(file):
    """Set terminal up to accept character by character input"""
    old_attrs = termios.tcgetattr(file.fileno())
    new_attrs = old_attrs[:]
    # Switch off terminal echo and 'canonical mode' so we get input character
    # by character (rather than line by line).
    new_attrs[3] = new_attrs[3] & ~(termios.ECHO | termios.ICANON)

    try:
        termios.tcsetattr(file.fileno(), termios.TCSADRAIN, new_attrs)
        yield
    finally:
        termios.tcsetattr(file.fileno(), termios.TCSADRAIN, old_attrs)

