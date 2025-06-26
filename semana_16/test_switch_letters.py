from switch_letters import switch_letters 

def test_reverse_single_word():
    # Arrange
    phrase = "hello"
    expected = "olleh"
    # Act
    result = switch_letters(phrase)
    # Assert
    assert result == expected

def test_reverse_phrase_with_spaces():
    # Arrange
    phrase = "Python rocks"
    expected = "skcor nohtyP"
    # Act
    result = switch_letters(phrase)
    # Assert
    assert result == expected

def test_reverse_with_special_characters():
    # Arrange
    phrase = "¡Hola, mundo!"
    expected = "!odnum ,aloH¡"
    # Act
    result = switch_letters(phrase)
    # Assert
    assert result == expected
