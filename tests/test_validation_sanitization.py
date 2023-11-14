import pytest
from email_validator import EmailSyntaxError, EmailUndeliverableError

from pgsurvey import (
    address,
    city,
    email,
    flip_name,
    gender,
    get_first_name,
    get_last_name,
    get_validator_func_from_name,
    has_characters,
    language,
    numbers_only,
    phone,
    sanitize_phone_with_truncation,
    state_initials,
    to_yn_from_yesno,
    transform_date,
    zip_code,
)


@pytest.mark.parametrize('test_input, expected', [
    ('1', '1'),
    ('123', '123'),
    ('a1', '1'),
    ('ABC', ''),
    ('  a1  ', '1'),
])
def test_numbers_only_valid(test_input, expected):
    assert numbers_only(test_input) == expected

@pytest.mark.parametrize('test_input', [1, [], 1.2, True, None])
def test_numbers_only_type_error(test_input):
    with pytest.raises(TypeError):
        assert numbers_only(test_input)

@pytest.mark.parametrize('test_input, expected', [
    ('1', '1'),
    ('123', '123'),
    ('a1', 'a1'),
    ('ABC', 'ABC'),
    ('  a1  ', '  a1  '),
])
def test_has_characters_valid(test_input, expected):
    assert has_characters(test_input) == expected

@pytest.mark.parametrize('test_input', [1, 1.2, True, None])
def test_has_characters_type_error(test_input):
    with pytest.raises(TypeError):
        assert has_characters(test_input)

@pytest.mark.parametrize('test_input', [[]])
def test_has_characters_value_error(test_input):
    with pytest.raises(ValueError):
        assert has_characters(test_input)

@pytest.mark.parametrize('test_input, expected', [
    ('SMITH, ALICE', 'SMITH'),
    ('Hopper, Grace', 'Hopper'),
    ('a,1', 'a'),
    ('ABC', 'ABC'),
    ('  a1  ', 'a1'),
])
def test_get_last_name_valid(test_input, expected):
    assert get_last_name(test_input) == expected

@pytest.mark.parametrize('test_input', [1, [], 1.2, True, None])
def test_get_last_name_attribute_error(test_input):
    with pytest.raises(AttributeError):
        assert get_last_name(test_input)

@pytest.mark.parametrize('test_input, expected', [
    ('SMITH, ALICE', 'ALICE'),
    ('Hopper, Grace G', 'Grace G'),
    ('a,1', '1'),
    ('  a,   1   ', '1'),
    ('SMITH,', '')
])
def test_get_first_name_valid(test_input, expected):
    assert get_first_name(test_input) == expected # type: ignore

@pytest.mark.parametrize('test_input', ['Hopper', 'ABC', '  a1  '])
def test_get_first_name_index_error(test_input):
    with pytest.raises(IndexError):
        assert get_first_name(test_input)

@pytest.mark.parametrize('test_input', [1, [], 1.2, True, None])
def test_get_first_name_attribute_error(test_input):
    with pytest.raises(AttributeError):
        assert get_first_name(test_input)

@pytest.mark.parametrize('test_input, expected', [
    ('SMITH, ALICE', 'ALICE SMITH'),
    ('Hopper, Grace G', 'Grace G Hopper'),
    ('a,1', '1 a'),
    ('  a,   1   ', '1 a'),
    ('SMITH,', 'SMITH')
])
def test_flip_name_valid(test_input, expected):
    assert flip_name(test_input) == expected

@pytest.mark.parametrize('test_input', [1, [], 1.2, True, None])
def test_flip_name_attribute_error(test_input):
    with pytest.raises(AttributeError):
        assert flip_name(test_input)

@pytest.mark.parametrize('test_input, expected', [
    ('yes', 'y'),
    ('Yes', 'y'),
    ('yES', 'y'),
    ('y', 'y'),
    ('no', 'n'),
    ('  no  ', 'n'),
    ('n', 'n'),
    ('', 'n'),
])
def test_to_yn_from_yesno_valid(test_input, expected):
    assert to_yn_from_yesno(test_input) == expected

@pytest.mark.parametrize('test_input', ['a', 'no thank you', 'nien', 'si'])
def test_to_yn_from_yesno_key_error(test_input):
    with pytest.raises(KeyError):
        assert to_yn_from_yesno(test_input)

@pytest.mark.parametrize('test_input', [1, [], 1.2, True, None])
def test_to_yn_from_yesno_attribute_error(test_input):
    with pytest.raises(AttributeError):
        assert to_yn_from_yesno(test_input)

@pytest.mark.parametrize('test_input, expected', [
    ('ma', 'MA'),
    ('MA', 'MA'),
    ('  Ma ', 'MA'),
    ('NH', 'NH'),
])
def test_state_initials_valid(test_input, expected):
    assert state_initials(test_input) == expected

@pytest.mark.parametrize('test_input', ['a', 'no thank you', 'nien', 'MASS'])
def test_state_initials_value_error(test_input):
    with pytest.raises(ValueError):
        assert state_initials(test_input)

@pytest.mark.parametrize('test_input',  [1, [], 1.2, True, None])
def test_state_initials_attribute_error(test_input):
    with pytest.raises(AttributeError):
        assert state_initials(test_input)

@pytest.mark.parametrize('test_input, expected', [
    ('1234', '01234'),
    ('12345', '12345'),
    (' 12345  ', '12345'),
    (' aa12345  ', '12345'),
    ('987654321', '98765-4321'),
    ('98765 - 4321', '98765-4321'),
])
def test_zip_code_valid(test_input, expected):
    assert zip_code(test_input) == expected

@pytest.mark.parametrize('test_input', ['1234567890', 'nien', 'MASS'])
def test_zip_code_value_error(test_input):
    with pytest.raises(ValueError):
        assert zip_code(test_input)

@pytest.mark.parametrize('test_input, expected', [
    ('Male', '1'),
    ('M', '1'),
    ('Female', '2'),
    ('F', '2'),
    ('Unknown', 'M'),
    ('U', 'M'),
])
def test_gender_valid(test_input, expected):
    assert gender(test_input) == expected

@pytest.mark.parametrize('test_input', ['1234567890', 'nien', 'MASS', 'man'])
def test_gender_key_error(test_input):
    with pytest.raises(KeyError):
        assert gender(test_input)

@pytest.mark.parametrize('test_input, expected', [
    ('2023-01-13', '01132023'),
    ('2023-1-2', '01022023'),
    ('09/14/2023', '09142023'),
    ('8/9/2023', '08092023'),
    ('8/9/1900', '08091900'),
    ('8/9/2051', '08092051'),
])
def test_transform_date_valid(test_input, expected):
    assert transform_date(test_input) == expected

@pytest.mark.parametrize('test_input', ['1234567890', '01012023', '13/13/2023', '19000101'])
def test_transform_date_value_error(test_input):
    with pytest.raises(ValueError):
        assert transform_date(test_input)

@pytest.mark.parametrize('test_input, expected', [
    ('bill@microsoft.com', 'bill@microsoft.com'),
    ('ghopper@gmail.com', 'ghopper@gmail.com'),
    ('linus@eff.org', 'linus@eff.org'),
    ('elovelace@example.com', 'elovelace@example.com'),
])
def test_email_valid(test_input, expected):
    assert email(test_input) == expected

@pytest.mark.parametrize('test_input', ['test@local.local', '1234567890',
                                        '01012023', '13/13/2023', '19000101'])
def test_email_email_syntax_error(test_input):
    with pytest.raises(EmailSyntaxError):
        assert email(test_input)

@pytest.mark.parametrize('test_input', ['a@b.c', 'test@asdfasdfasdf.iwueyiouyisdfiyiosf'])
def test_email_email_undeliverable_error(test_input):
    with pytest.raises(EmailUndeliverableError):
        assert email(test_input)

@pytest.mark.parametrize('test_input, expected', [
    ('9234567890', '923-456-7890'),
    ('19234567890', '923-456-7890'),
    ('+1 (923) 456-7890', '923-456-7890'),
    ('98765 - 43210', '987-654-3210'),
    ('(923) 456-7890', '923-456-7890'),
    ('', ''),
    ('None', ''),
    ('-', ''),
])
def test_phone_valid(test_input, expected):
    assert phone(test_input) == expected

@pytest.mark.parametrize('test_input, exception', [
                        (1, pytest.raises(TypeError)),
                        ([], pytest.raises(TypeError)),
                        (1.2, pytest.raises(TypeError)),
                        (True, pytest.raises(TypeError)),
                        (None, pytest.raises(TypeError)),
                        ('987-654-3210 x312', pytest.raises(ValueError)),
                        ('11234567890', pytest.raises(ValueError)),
                        ('1234567890', pytest.raises(ValueError)),
                        ('11234567890 x321', pytest.raises(ValueError)),
                        ('123', pytest.raises(ValueError)),
                        ('123-4567', pytest.raises(ValueError)),
                        ])
def test_phone_error(test_input, exception):
    with exception:
        assert phone(test_input)

@pytest.mark.parametrize('test_input, expected', [
    ('1234567890', '1234567890'),
    ('123 MAIN ST.', '123 Main St.'),
    ('456 elm lane', '456 Elm Lane'),
    ('', ''),
    ('nan', ''),
    ('-', ''),
    (None, ''),
])
def test_address_valid(test_input, expected):
    assert address(test_input) == expected

@pytest.mark.parametrize('test_input', [1, [], 1.2, True])
def test_address_attribute_error(test_input):
    with pytest.raises(AttributeError):
        assert address(test_input)

@pytest.mark.parametrize('test_input, expected', [
    ('Albanian', '57'),
    ('arabic', '22'),
    ('ARMENIAN', '31'),
    ('  Bengali   ', '60'),
    ('greek, modern (1453-)', '7'),
    ('english', '0'),
])
def test_language_valid(test_input, expected):
    assert language(test_input) == expected

@pytest.mark.parametrize('test_input, expected', [('Klingon', '0'), ('British English', '0')])
def test_language_unknown_to_english(test_input, expected):
    assert language(test_input) == expected

@pytest.mark.parametrize('test_input', [1, [], 1.2, True, None])
def test_language_attribute_error(test_input):
    with pytest.raises(AttributeError):
        assert language(test_input)

@pytest.mark.parametrize('test_input, expected', [
    ('1234567890', '1234567890'),
    ('Springfield', 'Springfield'),
    ('lONg mEADow', 'Long Meadow'),
    ('BOSTON', 'Boston'),
    ('nan', 'Nan'),
    ('-', '-'),
])
def test_city_valid(test_input, expected):
    assert city(test_input) == expected

@pytest.mark.parametrize('test_input', [1, [], 1.2, True, None])
def test_city_attribute_error(test_input):
    with pytest.raises(AttributeError):
        assert city(test_input)

@pytest.mark.parametrize('test_input, expected', [
    ('has_characters', has_characters),
    ('city', city),
    ('phone', phone),
])
def test_get_validator_func_from_name_valid(test_input, expected):
    assert get_validator_func_from_name(test_input) == expected

@pytest.mark.parametrize('test_input', ['a', 'no thank you', 'nien', 'si', 1, 1.2, True, None])
def test_get_validator_func_from_name_key_error(test_input):
    with pytest.raises(KeyError):
        assert get_validator_func_from_name(test_input)

@pytest.mark.parametrize('test_input', [[]])
def test_get_validator_func_from_name_type_error(test_input):
    with pytest.raises(TypeError):
        assert get_validator_func_from_name(test_input)

@pytest.mark.parametrize('test_input, expected', [
    ('2234567890', '223-456-7890'),
    ('12234567890', '223-456-7890'),
    ('98765 - 43210', '987-654-3210'),
    ('(223) 456-7890', '223-456-7890'),
    ('(223) 456-7890 x3', '223-456-7890'),
    ('12234567890 ext 10', '223-456-7890'),
    ('98765 - 43210 ext. 91', '987-654-3210'),
    ('', ''),
    ('None', ''),
    ('-', ''),
])
def test_sanitize_phone_with_truncation_valid(test_input, expected):
    assert sanitize_phone_with_truncation(test_input) == expected

@pytest.mark.parametrize('test_input, exception', [
                        (1, pytest.raises(TypeError)),
                        ([], pytest.raises(TypeError)),
                        (1.2, pytest.raises(TypeError)),
                        (True, pytest.raises(TypeError)),
                        (None, pytest.raises(TypeError)),
                        ('11234567890', pytest.raises(ValueError)),
                        ('11234567890 x321', pytest.raises(ValueError)),
                        ('123', pytest.raises(ValueError)),
                        ('123-4567', pytest.raises(ValueError)),
                        ])
def test_sanitize_phone_with_truncation_type_error(test_input, exception):
    with exception:
        assert sanitize_phone_with_truncation(test_input)