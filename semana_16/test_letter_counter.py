from letter_counter import letter_counter  

def test_mixed_case_text():
    # Arrange
    text = "Leave The Gun and Take the Cannoli"
    expected = (5, 26)
    # Act
    result = letter_counter(text)
    # Assert
    assert result == expected

def test_all_lowercase():
    # Arrange
    text = "this is all lowercase"
    expected = (0, 19)
    # Act
    result = letter_counter(text)
    # Assert
    assert result == expected

def test_no_letters():
    # Arrange
    text = "1234!@#$"
    expected = (0, 0)
    # Act
    result = letter_counter(text)
    # Assert
    assert result == expected
