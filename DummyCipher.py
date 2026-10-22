from StringCipher import StringCipher


class DummyCipher(StringCipher):
    def encrypt(self, text: str) -> str:
        return text[::-1]
    def decrypt(self, text: str) -> str:
        return text[::-1]