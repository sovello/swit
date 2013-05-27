import os

from sb.util import safe


def is_testing():
  return bool(safe(lambda: int(os.environ["TESTING"])))

