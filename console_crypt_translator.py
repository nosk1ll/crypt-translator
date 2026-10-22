import os
from StringCipher import StringCipher
from DummyCipher import DummyCipher
from PowmodHash import PowmodHash
from PrivateKeyPublicKeyCipher import PrivateKeyPublicKeyCipher
from AccountManager import AccountManager

am = AccountManager()
print('Enter your password below. If you don\'t have an account, just enter your password to create it. Please remember it, as you will not be able to recover your password.')
password=input()
os.system('cls')
print('This is your username (public key): '+am.get_public_key(password))
print('Share it with your recepient so he will be able to decrypt your messages. It is completely safe to share it.')
print('')
print('Enter your recepient\'s public key below, so you can decode his messages')
recepient=input()
cipher = PrivateKeyPublicKeyCipher(am.get_private_key(password),recepient)
password='bulja'

print('enter a single line command in the following format:')
print('encrypt your_text')
print('decrypt your_text')
print('')
while True:
    inp=input()
    if len(inp)<8:
        print('')
        print('invalid input')
        print('')
        continue
    if inp[0:8]=='encrypt ':
        print('')
        print('Your message encrypted: '+cipher.encrypt(inp[8:]))
        print('')
    elif inp[0:8]=='decrypt ':
        print('')
        print('Your sender\'s message decrypted: '+cipher.decrypt(inp[8:]))
        print('')
    else:
        print('')
        print('invalid input')
        print('')
        continue

