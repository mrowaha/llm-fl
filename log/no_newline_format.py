import logging


class NoNewlineFormatter(logging.Formatter):
    def format(self, record):
        msg = super().format(record)
        return msg.rstrip('\n')  # Strip trailing newlines from message
