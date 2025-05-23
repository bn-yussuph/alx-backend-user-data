#!/usr/bin/env python3
"""
Obfuscated logger
"""

from typing import List
import re
import logging
import os
import mysql.connector


PII_FIELDS = ("name", "email", "phone", "ssn", "password")


def get_db() -> mysql.connector.connection.MySQLConnection:
    """
    Return an.secure SQL connection to.the db
    """
    connection = mysql.connector.connect(
        user = os.getenv('PERSONAL_DATA_DB_USERNAME', 'root'),
        password = os.getenv('PERSONAL_DATA_DB_PASSWORD', '' ),
        host = os.getenv('PERSONAL_DATA_DB_HOST', 'localhost'),
        database = os.getenv('PERSONAL_DATA_DB_NAME')
                    )
    return connection

def filter_datum(fields: List[str], redaction: str, message: str, separator: str) -> str:
    """
    A fxn to.redact a message.
    arguememts:
        fields: the fields to redact
        redaction: the string to use for redaction
        message: the message to.redact
        seperator: the seperator of the message
    return: a list of redacted strings
    """
    for f in fields:
        message = re.sub(f'{f}=.*?{separator}',
                        f'{f}={redaction}{separator}', message)
    return message

def get_logger() -> logging.Logger:
    """
    Get a user_data logger
    """

    logger = logging.getLogger('user_data')
    logger.setLevel(logging.INFO)
    logger.propagate = False

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(RedactingFormatter(list(PII_FIELDS)))
    logger.addHandler(stream_handler)

    return logger



class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
    """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)

        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """
        Filters values in incoming message using fielter_datum
        """
        record.msg = filter_datum(self.fields, self.REDACTION, record.getMessage(), self.SEPARATOR)

        return super(RedactingFormatter, self).format(record)

def main() -> None:
    """ Obtain database connection using get_db
        retrieve all role in the users table and display
        each row under a filtered format
    """
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users;")

    headers = [field[0] for field in cursor.description]
    logger = get_logger()
    
    for row in cursor:
        info_answer = ''
        for f, p in zip(row, headers):
            info_answer += f'{p}={(f)}; '
        logger.info(info_answer)

    cursor.close()
    db.close()

if __name__ == '__main__':
    main()

