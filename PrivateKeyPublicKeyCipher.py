import hashlib
from PowmodHash import PowmodHash
from StringCipher import StringCipher


class PrivateKeyPublicKeyCipher(StringCipher):
    """
        Private key is user one user's password
        Public key is the hash of the other user's password
        This class works both ways:
        Having A's private and B's public keys allows to encrypt and decrypt
        Likewise, having A's public and B's private key allows to communicate
        Note: keys must be hex strings, without the 0x prefix!!
    """

    def __init__(self,private_key: str, public_key: str):
        self.powmodhash=PowmodHash()
        temp_seed=self.powmodhash.get_common_key(private_key,public_key)
        self.seed=hashlib.sha256(temp_seed.encode('utf-8')).hexdigest()

    def __hash_char(self, c: chr, key: str) -> str:
        char_hashed=hex(ord(c)^ord(key[0]))[2:]
        if len(char_hashed)==1:
            char_hashed='0'+char_hashed
        return char_hashed
    def encrypt(self, text: str) -> str:
        ret=''
        current_seed=self.seed
        for c in text:
            ret=ret+self.__hash_char(c,current_seed)
            current_seed=hashlib.sha256((current_seed+c).encode('utf-8')).hexdigest()
        return ret
    def decrypt(self, text: str) -> str:
        chunk_size=2
        if (len(text)%chunk_size!=0):
            return 'invalid text'
        ret=''
        current_seed=self.seed
        for i in range(len(text)//chunk_size):
            chunk=text[i*chunk_size:(i+1)*chunk_size]
            succeeded=False
            for c in range(256):
                if self.__hash_char(chr(c),current_seed)==chunk:
                    ret+=chr(c)
                    succeeded=True
                    break
            if not succeeded:
                return 'decryption failed'
            current_seed=hashlib.sha256((current_seed+chr(c)).encode('utf-8')).hexdigest()
        return ret
