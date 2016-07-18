class DiffieHellman(object):

    def __init__(self, shared_prime, shared_base, secret_key):
        self.shared_prime = self.convert_key_to_numbers(shared_prime) # p
        self.shared_base = self.convert_key_to_numbers(shared_base) # q
        self.secret_key = self.convert_key_to_numbers(secret_key)# x
        print(self.shared_base, self.shared_prime, self.secret_key)

    def convert_key_to_numbers(self, key):
        converted_key = ''
        for symbol in key:
            number_for_symbol = ord(symbol) % 10
            converted_key += str(number_for_symbol)
        return int(converted_key)

    def compute_medium_key(self):
        print('medium key')
        powerov = self.shared_base ** self.secret_key
        print(powerov % self.shared_prime)
        return powerov % self.shared_prime

    def compute_general_secret_key(self, mixed_key):
        powerov = mixed_key ** self.secret_key
        print(powerov % self.shared_prime)
        return powerov % self.shared_prime


if __name__ == '__main__':
    shared_prime, shared_base = 'prime_123', 'base_456'

    a_secret_key = 'a_123'
    a_diffie = DiffieHellman(shared_prime=shared_prime, shared_base=shared_base, secret_key=a_secret_key)
    b_secret_key = 'b_key'
    b_diffie = DiffieHellman(shared_prime=shared_prime, shared_base=shared_base, secret_key=b_secret_key)

    a_medium_key = a_diffie.compute_medium_key()
    b_medium_key = b_diffie.compute_medium_key()

    assert a_diffie.compute_general_secret_key(b_medium_key) == b_diffie.compute_general_secret_key(a_medium_key)