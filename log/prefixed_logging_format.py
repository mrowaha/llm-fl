import logging


class PrefixedFormatter(logging.Formatter):
    def __init__(self, prefix, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.prefix = prefix

    def format(self, record):
        record.msg = f"{self.prefix} {record.msg}"
        return super().format(record)
