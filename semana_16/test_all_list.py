
from all_list import all_list  

def test_sum_positive_numbers():
    # Arrange
    data = [1, 2, 3, 4, 5]
    expected = 15
    # Act
    result = all_list(data)
    # Assert
    assert result == expected

def test_sum_with_negatives():
    # Arrange
    data = [10, -5, 3, -2]
    expected = 6
    # Act
    result = all_list(data)
    # Assert
    assert result == expected

def test_sum_with_zeros():
    # Arrange
    data = [0, 0, 0, 0]
    expected = 0
    # Act
    result = all_list(data)
    # Assert
    assert result == expected
