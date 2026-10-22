class PowmodHash:
    """
        This class works on integers
        suppose a is a private key
        to obtain b, the pulic key, we do the following
        compute b := p^a (mod q)
        p and q are large prime numbers
    """

    def __init__(self,
                 base=737169686765646362615958575553525150494746454443413938373534333231292726252322211917,
                 mod=1983116034341975454789449189498620955194254460449807567074683265838922666583379392681647):
        self.base=base
        self.mod=mod

    def __powmod(self, a: int, n: int, m: int) -> int:
        c=1
        while n>0:
            if n%2==1:
                c=c*a%m
            n=n//2
            a=a*a%m
        return c

    def __hexstring_to_number(self,hexstring) -> int:
        try:
            number=int(hexstring,16)
        except ValueError as error:
            raise ValueError('Key must be a valid hex string') from error
        if number<0:
            raise ValueError('Key must be positive')
        return number

    def __number_to_hexstring(self,number) -> int:
        return hex(number)[2:]

    def private_key_to_public_key(self, private_key: str) -> str:
        private_key_number=self.__hexstring_to_number(private_key)
        public_key_number=self.__powmod(self.base,private_key_number,self.mod)
        public_key=self.__number_to_hexstring(public_key_number)
        return public_key

    def get_common_key(self,private_key: str, public_key: str) -> str:
        private_key_number=self.__hexstring_to_number(private_key)
        public_key_number=self.__hexstring_to_number(public_key)
        common_key_number=self.__powmod(public_key_number,private_key_number,self.mod)
        common_key=self.__number_to_hexstring(common_key_number)
        return common_key


