import hashlib
from PowmodHash import PowmodHash


class AccountManager:
    def __init__(self):
        self.powmodhash=PowmodHash()

    def get_private_key(self, password: str) -> str:
        private_key=hashlib.sha256(password.encode('utf-8')).hexdigest()
        return private_key

    def get_public_key(self,password: str) -> str:
        private_key=self.get_private_key(password)
        public_key=self.powmodhash.private_key_to_public_key(private_key)
        return public_key
