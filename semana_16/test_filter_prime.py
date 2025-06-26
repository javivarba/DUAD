from filter_prime import filter_prime  

def test_mixed_list():
    # Arrange
    data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    expected = [2, 3, 5, 7]
    # Act
    result = filter_prime(data)
    # Assert
    assert result == expected

def test_empty_list():
    # Arrange
    data = []
    expected = []
    # Act
    result = filter_prime(data)
    # Assert
    assert result == expected

def test_all_primes():
    # Arrange
    data = [2, 3, 5, 7, 11, 13, 17]
    expected = [2, 3, 5, 7, 11, 13, 17]
    # Act
    result = filter_prime(data)
    # Assert
    assert result == expected
