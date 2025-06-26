from words_sequence import words_sequence  

def test_random_order():
    # Arrange
    text = "tiger-car-web-ball-cup-trail-apple-biscuit"
    expected = "apple-ball-biscuit-car-cup-tiger-trail-web"
    # Act
    result = words_sequence(text)
    # Assert
    assert result == expected

def test_already_sorted():
    # Arrange
    text = "apple-ball-biscuit-car"
    expected = "apple-ball-biscuit-car"
    # Act
    result = words_sequence(text)
    # Assert
    assert result == expected

def test_reverse_order():
    # Arrange
    text = "zebra-yellow-xray-apple"
    expected = "apple-xray-yellow-zebra"
    # Act
    result = words_sequence(text)
    # Assert
    assert result == expected
