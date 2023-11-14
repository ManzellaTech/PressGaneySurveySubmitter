import re
import datetime
from email_validator import EmailUndeliverableError, validate_email
from typing import Callable

def numbers_only(v: str) -> str:
    """Only keep digits in a string."""
    return re.sub("[^0-9]", "", v)

def has_characters(v: str) -> str:
    """Validate string has one or more characters."""
    if len(v) >= 1:
        return v
    raise ValueError

def get_last_name(v: str) -> str:
    """Get last name from an input column formatted as: LASTNAME, FIRSTNAME."""
    parts_with_whitespace = v.split(sep=',', maxsplit=1)
    parts = [p.strip() for p in parts_with_whitespace]
    return parts[0]

def get_first_name(v: str) -> str:
    """Get first name from an input column formatted as: LASTNAME, FIRSTNAME."""
    parts_with_whitespace = v.split(sep=',', maxsplit=1)
    parts = [p.strip() for p in parts_with_whitespace]
    return parts[1]

def flip_name(v: str) -> str:
    """
    Take a name in the format 'Lastname, Firstname', 
    remove any commas, and move the last name to the end.
    Such as: 'Firstname Lastname'
    """
    parts_with_whitespace = v.split(sep=',', maxsplit=1)
    parts = [p.strip() for p in parts_with_whitespace]
    parts.append(parts.pop(0))
    for idx, part in enumerate(parts[:]):
        if len(part) == 0:
            del parts[idx]
    return ' '.join(parts)

def to_yn_from_yesno(v: str) -> str:
    """Parse variations on 'yes' and 'no' to single character representations."""
    bool_map = {
        'yes': 'y',
        'y': 'y',
        'no': 'n',
        'n': 'n',
        '': 'n'
    }
    return bool_map[v.strip().lower()] 

def state_initials(v: str) -> str:
    """Parse two character state initials."""
    v = v.strip()
    if len(v) == 2:
        return v.upper()
    raise ValueError

def zip_code(v: str) -> str:
    """Validate and sanitize zip code."""
    v = numbers_only(v)
    if len(v) == 0:
        raise ValueError
    if len(v) <= 5:
        return v.zfill(5)
    elif len(v) == 9:
        return f'{v[:5]}-{v[5:]}'
    raise ValueError

def gender(v: str) -> str:
    lookup = {
        'Male': '1',
        'M': '1',
        'Female': '2',
        'F': '2',
        'Unknown': 'M',
        'U': 'M',
    }
    return lookup[v]

def transform_date(v: str) -> str:
    date_formats = ('%Y-%m-%d', '%m/%d/%Y')
    for date_format in date_formats:
        try:
            dt = datetime.datetime.strptime(v, date_format)
            return dt.strftime('%m%d%Y')
        except ValueError:
            pass
    raise ValueError(f'time data does not match formats: {', '.join(date_formats)}')

def email(v: str) -> str:
    """Validate email address."""
    try:
        v = validate_email(v).email
    except EmailUndeliverableError:
        if not v.endswith('@example.com'):
            raise EmailUndeliverableError
    return v

def format_phone(v: str) -> str:
    """Parse a ten digit phone number to the expected phone number format."""
    return f'{v[:3]}-{v[3:6]}-{v[6:]}'

def phone(v: str) -> str:
    """Validate a phone number."""
    n = numbers_only(v)
    if len(n) == 0:
        return n
    if n.startswith('1'):
        n = n[1:]
    if n.startswith('1'):
        raise ValueError('US area codes cannot start with the number "1".')
    if len(n) == 10:
        return format_phone(n)
    raise ValueError('Phone number must contain 10 digits. '
                     f'The following is invalid: {v}')

def sanitize_phone_with_truncation(v: str) -> str:
    """
    Sanitize a phone number.  Truncate the phone number if longer than the
    maximum length of 10 characters.
    """
    n = numbers_only(v)
    if len(n) == 0:
        return n
    if n.startswith('1'):
        n = n[1:]
    if n.startswith('1'):
        raise ValueError('US area codes cannot start with the number "1".')
    if len(n) >= 10:
        return format_phone(n[0:10])
    raise ValueError('Phone number must contain 10 digits. '
                         f'The following is invalid: {v}')

def address(v: str) -> str:
    """Parse address text."""
    if v == '-':
        return ''
    elif v is None:
        return ''
    elif v == 'nan':
        return ''
    else:
        return v.lower().title()

def language(v: str) -> str:
    """Parse languages and return the appropriate Press Ganey language code."""
    v = v.strip().lower()
    try:
        index_of_first_comma = v.index(',')
    except ValueError:
        index_of_first_comma = None
    if index_of_first_comma:
        v = v.split(',')[0]
    language_lookup = {
        'albanian': '57',
        'arabic': '22',
        'armenian': '31',
        'bengali': '60',
        'bosnian': '50',
        'bosnian-croatian': '49',
        'bosnian-muslim': '48',
        'bosnian-serbian': '32',
        'cambodian': '34',
        'chao-chou': '41',
        'chinese-simplified': '12',
        'chinese-traditional': '10',
        'chuukese': '23',
        'creole': '21',
        'croatian': '52',
        'english': '0',
        'english/spanish': '33',
        'farsi': '59',
        'french-canadian': '35',
        'french-france': '20',
        'german': '4',
        'greek': '7',
        'haitian-creole': '36',
        'hakha chin': '66',
        'hebrew': '37',
        'hindi': '38',
        'hmong': '26',
        'ilocano': '56',
        'indonesian': '42',
        'italian': '5',
        'japanese': '28',
        'korean': '29',
        'laotian': '43',
        'malayan': '44',
        'malayalam': '58',
        'marshallese': '24',
        'polish': '6',
        'portuguese-brazilian': '8',
        'portuguese-continental': '47',
        'punjabi': '54',
        'romanian': '55',
        'russian': '3',
        'samoan': '25',
        'serbian': '51',
        'somali': '27',
        'spanish': '1',
        'swahili': '45',
        'tagalog': '30',
        'tamil': '64',
        'telugu': '65',
        'thai': '46',
        'turkish': '53',
        'urdu': '39',
        'vietnamese': '13',
        'yiddish': '40',
    }
    code = language_lookup.get(v)
    if code is None:
        code = '0' # English
    return code

def city(v: str) -> str:
    """Parse city text."""
    return v.lower().title()

def get_validator_func_from_name(name: str) -> Callable:
    """
    Mapping of functions for validation and sanitization.
    Used to take in values from the config .JSON file and return the appropriate
    function.
    """
    mapping = {
        'has_characters': has_characters,
        'get_first_name': get_first_name,
        'get_last_name': get_last_name,
        'address': address,
        'city': city,
        'state_initials': state_initials,
        'zip_code': zip_code,
        'phone': phone,
        'sanitize_phone_with_truncation': sanitize_phone_with_truncation,
        'gender': gender,
        'transform_date': transform_date,
        'numbers_only': numbers_only,
        'flip_name': flip_name,
        'to_yn_from_yesno': to_yn_from_yesno,
        'email': email,
    }
    return mapping[name]