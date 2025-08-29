import pytest
from bubble_sort import bubble_sort  

def test_small_list():
    # Arrange
    data = [4, 2, 1]
    expected = [1, 2, 4]
    # Act
    result = bubble_sort(data)
    # Assert
    assert result == expected

def test_large_list():
    # Arrange
    import random
    data = random.sample(range(1000), 150)  # 150 elementos únicos
    expected = sorted(data)
    # Act
    result = bubble_sort(data)
    # Assert
    assert result == expected

def test_empty_list():
    # Arrange
    data = []
    expected = []
    # Act
    result = bubble_sort(data)
    # Assert
    assert result == expected

@pytest.mark.parametrize("invalid_input", [
    None,
    123,
    "not a list",
    {1, 2, 3},
    (1, 2, 3),
])
def test_invalid_input_raises_type_error(invalid_input):
    # Act + Assert
    with pytest.raises(TypeError):
        bubble_sort(invalid_input)
