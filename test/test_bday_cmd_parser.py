import datetime
import pytest
from birthday_bot.bday_cmd_parser import parse_message_bday_add, parse_message_bday_add_other
from birthday_bot.bday_types import BirthdayEntry

@pytest.mark.parametrize("msg, command_key, user_id, username, expected_result", [
    ("$bday-add 12/31", "$bday-add", "123", "John", BirthdayEntry(user_id="123", date="12/31", username="John")),
    ("$bday-add 02/28", "$bday-add", "1234", "John", BirthdayEntry(user_id="1234", date="02/28", username="John")),
    ("$bday-add 06-23", "$bday-add", "4", "Jane", BirthdayEntry(user_id="4", date="06/23", username="Jane")),
    ("$bday-add 03-15", "$bday-add", "23423", "Jane", BirthdayEntry(user_id="23423", date="03/15", username="Jane")),
    ("$bday-add 33-15", "$bday-add", "123", "John", None),
    ("$bday-add 03-15", "$bday-bad-add", "123", "John", None),
    ("$bday-add 03-15", "$bday-add", None, "John", None),
    ("$bday-add 03-15", "$bday-add", "123", None, None),
])
def test_parse_message_bday_add(msg, command_key, user_id, username, expected_result):
    result = parse_message_bday_add(msg, command_key, user_id, username)
    assert result == expected_result

@pytest.mark.parametrize("msg, command_key, expected_result", [
    ("$bday-add-other John 12/31", "$bday-add-other", BirthdayEntry(user_id="-1", date="12/31", username="John")),
    ("$bday-add-other John 02/28", "$bday-add-other", BirthdayEntry(user_id="-1", date="02/28", username="John")),
    ("$bday-add-other Jane 06-23", "$bday-add-other", BirthdayEntry(user_id="-1", date="06/23", username="Jane")),
    ("$bday-add-other Jane 03-15", "$bday-add-other", BirthdayEntry(user_id="-1", date="03/15", username="Jane")),
    ("$bday-add-other John 33-15", "$bday-add-other", None),
    ("$bday-add-other John 03-15", "$bday-bad-adddd", None),
    ("$bday-add-other 03-15", "$bday-add-other", None),
    ("$bday-add-other 03-15 John", "$bday-add-other", None),
])
def test_parse_message_bday_add(msg, command_key, expected_result):
    result = parse_message_bday_add_other(msg, command_key)
    assert result == expected_result