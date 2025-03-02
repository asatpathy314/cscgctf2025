
password = list(map(ord, list("b9yPw:MwqcoHuFz^r-o*{>I\x10Y")))
for i in range(len(password)):
    password[i] = password[i] + 2
    password[i] ^= i + 0xa
print(''.join(map(chr, password)))