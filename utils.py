from transliterate import translit
from typing import Set
chars_to_remove = {
    '!',
    '"',
    '#',
    '%',
    '&',
    "'",
    '(',
    ')',
    '*',
    '+',
    ',',
    '-',
    '.',
    '/',
    ':',
    ';',
    '<',
    '=',
    '>',
    '?',
    '[',
    ']',
    '_',
    '`',
    '«',
    '°',
    '²',
    '³',
    'µ',
    '·',
    '»',
    '½',
    '‑',
    '–',
    '‘',
    '’',
    '“',
    '”',
    '„',
    '•',
    '…',
    '‰',
    '″',
    '₂',
    '₃',
    '€',
    '™',
    '→',
    '−',
    '∕',
    '😀',
    '😉',
    '🙁',
    '🙂'

}

def remove_chars(input_text: str, chars_to_remove: Set[str] = chars_to_remove) -> str:
    for c in chars_to_remove:
        input_text = input_text.replace(c, "")
    return input_text


def transliterate(input_text: str) -> str:
    from transliterate import translit
    return translit(input_text, "sr", reversed=True)

def is_alpha(token:str) -> bool:
    import re
    pattern = "^[a-zšđčćž]+$"
    compiled_pattern = re.compile(pattern)
    return bool(compiled_pattern.match(token))