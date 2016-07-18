class CaesarShifr:
    def __init__(self, shifr_key):
        self.shifr_key = str(shifr_key)

    def encryption(self, phrase):
        phrase = str(phrase)
        encryption_phrase = []

        index_shifr_key = 0
        for symbol in phrase:
            if index_shifr_key >= len(self.shifr_key):
                index_shifr_key = 0

            encryption_phrase.append(ord(symbol) + int(self.shifr_key[index_shifr_key]))
            index_shifr_key += 1
        return encryption_phrase

    def decryption(self, phrase_of_codes_symbols): 
        # phrase_of_codes_symbols - list encryption symbols gotten from CaesarShifr.encryption 
        decryption_phrase = ''

        index_shifr_key = 0
        for shifr_code_symbol in phrase_of_codes_symbols:
            if index_shifr_key >= len(self.shifr_key):
                index_shifr_key = 0

            decryption_phrase += chr(shifr_code_symbol - int(self.shifr_key[index_shifr_key]))

            index_shifr_key += 1
        return decryption_phrase


if __name__ == '__main__':
    main_key = 32142
    caesar = CaesarShifr(main_key)

    phrase = "Hi, I'm Caesar 123"
    encrypt_phrase = caesar.encryption(phrase)
    print(encrypt_phrase)  # [75, 107, 45, 36, 75, 42, 111, 33, 71, 99, 104, 117, 98, 118, 34, 52, 52, 52]

    decrypt_phrase = caesar.decryption(encrypt_phrase)
    print(decrypt_phrase)  # Hi, I'm Caesar 123

    assert phrase == decrypt_phrase
