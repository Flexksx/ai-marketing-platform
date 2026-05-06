from ulid import ULID


NANOID_ALPHABET = "23456789ABCDEFGHJKLMNPQRSTUVWXYZ"
DEFAULT_ID_LENGTH = 12


def new_id() -> str:
    return str(ULID())
