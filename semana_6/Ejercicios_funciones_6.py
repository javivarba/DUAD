
def words_sequence (text):
    list_words = text.split("-")
    list_sequence = sorted(list_words)
    return "-".join(list_sequence)

results = words_sequence (" tiger - car - web - ball - cup - trail - apple - biscuit")

print(results)