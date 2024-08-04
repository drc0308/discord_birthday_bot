import datetime
import logging
import re
from typing import Optional
from .bday_types import BirthdayEntry

DEFAULT_VAL_NON_USER = "-1"


def parse_message_bday_add(msg: str, command_key: str, user_id: str, username: str) -> Optional[BirthdayEntry]:
    """
    Parses a message to extract a birthday entry.

    Args:
        msg (str): The message to parse.
        command_key (str): The command key to search for in the message.
        user_id (str): The user ID associated with the birthday entry.
        username (str): The username associated with the birthday entry.

    Returns:
        Optional[BirthdayEntry]: The parsed birthday entry if the message is valid, otherwise None.
    """
    logging.error(msg)
    # Note $ is a special character in python regex so it needs to be escaped
    m = re.search(f'\\{command_key}' + r'\s([0-9][0-9][/,\-][0-9][0-9])', msg)
    if m is None or user_id is None or username is None:
        logging.warning(f'Invalid formatted message {msg}')
        return None
    else:
        result = BirthdayEntry()
        date_string = m.group(1)
        try:
            date = datetime.datetime.strptime(date_string, '%m-%d')
        except ValueError:
            try:
                date = datetime.datetime.strptime(date_string, '%m/%d')
            except ValueError:
                return None
        result.user_id = user_id
        result.username = username
        result.date = date.strftime("%m/%d")
        return result


def parse_message_bday_add_other(msg: str, command_key: str) -> Optional[BirthdayEntry]:
    """
    Parses a message to extract a birthday entry for a non user on the server itself.

    Args:
        msg (str): The message to parse.
        command_key (str): The command key used to trigger the parsing.

    Returns:
        Optional[BirthdayEntry]: The extracted birthday entry if the message is valid, otherwise None.
    """
    logging.error(msg)
    # Note $ is a special character in python regex so it needs to be escaped
    m = re.search(f'\\{command_key}' + r'\s([A-z]+)\s([0-9][0-9][/,\-][0-9][0-9])', msg)
    if m is None:
        logging.warning(f'Invalid formatted message {msg}')
        return None
    else:
        result = BirthdayEntry()
        date_string = m.group(2)
        try:
            date = datetime.datetime.strptime(date_string, '%m-%d')
        except ValueError:
            try:
                date = datetime.datetime.strptime(date_string, '%m/%d')
            except ValueError:
                return None
        result.user_id = DEFAULT_VAL_NON_USER
        result.username = str(m.group(1))
        result.date = date.strftime("%m/%d")
        return result
