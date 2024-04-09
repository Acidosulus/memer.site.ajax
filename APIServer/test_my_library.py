# test_my_library.py

from my_library import is_char_russian, code_char, Code_string, prepare_str, sx, delete_non_english_alphabet_characters

def test_is_char_russian():
    assert is_char_russian('а') == True
    assert is_char_russian('Я') == True
    assert is_char_russian('Ё') == True
    assert is_char_russian('щ') == True

    assert is_char_russian('a') == False
    assert is_char_russian('1') == False
    assert is_char_russian('!') == False

def test_code_char():
    assert code_char('а') == '%5B1%5D'
    assert code_char('б') == '%5B2%5D'
    assert code_char('в') == '%5B3%5D'
    assert code_char('г') == '%5B4%5D'

    assert code_char('x') == '%5B0%5D'
    assert code_char('1') == '%5B0%5D'
    assert code_char('!') == '%5B0%5D'

def test_Code_string():
    assert Code_string('Привет, мир!') == '%5B100%5D%5B18%5D%5B10%5D%5B3%5D%5B6%5D%5B20%5D, %5B14%5D%5B10%5D%5B18%5D!'
    print(Code_string('Hello, world!'))
    assert Code_string('Hello, world!') == 'Hello, world!'
    print(Code_string('Привет, world!'))
    assert Code_string('Привет, world!') == '%5B100%5D%5B18%5D%5B10%5D%5B3%5D%5B6%5D%5B20%5D, world!'

def test_prepare_str():
    assert prepare_str('Hello; "World"\n') == 'Hello  World '
    assert prepare_str('This is a test') == 'This is a test'
    assert prepare_str('"This is a; test\nwith" tab and\nnewline\tcharacters') == 'This is a  test with tab and newline characters'


def test_sx():
    assert sx("abc123def456ghi", "abc", "def") == "123"
    assert sx("abc123def456ghi", "abc", "def", 2) == ""
    assert sx("abc123def456ghi", "xyz", "def") == ""
    assert sx("abc123def456ghi", "abc", "xyz") == "123def456gh"
    assert sx("abc123def456ghi", "abc", "def", 3) == ""