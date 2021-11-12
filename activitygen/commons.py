from enum import Enum
from functools import total_ordering

@total_ordering
class Difficulty(Enum):
  EASY = 0
  MEDIUM = 1
  HARD = 2

  def __lt__(self, other):
    return self.value < other.value

  @staticmethod
  def from_str(s, default):
    # Try initialising from name string (e.g. "hard", "HARD")
    try:
      return Difficulty[s.upper()]
    except (AttributeError, KeyError):
      pass
    # Otherwise try initialising from integer string (e.g. "2")
    try:
      return Difficulty(int(s))
    except:
      # Otherwise return default
      return default
