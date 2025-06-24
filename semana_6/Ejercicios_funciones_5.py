
def letter_counter (text):
    uppercase = 0
    lowercase = 0

    for letter in text:
        if letter.isupper():
            uppercase += 1
        elif letter.islower():
            lowercase += 1
    print (f" There's {uppercase} upper cases and {lowercase} lower cases")


letter_counter ("Leave The Gun and Take the Cannoli")