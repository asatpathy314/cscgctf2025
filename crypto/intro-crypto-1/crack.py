from binascii import unhexlify

with open("flags.txt", "r") as f:
    flags = f.readlines()

flags = [flag.split(": ")[1].strip() for flag in flags]
flags = [unhexlify(flag) for flag in flags]
flag = flags[-1]
ciphertexts = flags[:-1]

for ciphertext in ciphertexts: 
    plaintext = ''.join(list(chr(f ^ c ^ ord("a")) for f, c in zip(flag, ciphertext)))
    print(plaintext)