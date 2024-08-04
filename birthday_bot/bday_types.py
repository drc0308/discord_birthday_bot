
from dataclasses import dataclass

# Helper functions and data types
@dataclass
class BirthdayEntry:
    """ Data submitted by a user to store in leaderboard
    """
    user_id: str = ""
    date: str = ""
    username: str = ""