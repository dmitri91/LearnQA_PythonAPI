def test_phrase_length_check():
    phrase = input("Set a phrase shorter than 15 characters:")
    phrase_length = len(phrase)
    assert phrase_length <= 15, "phrase more than 15 characters"