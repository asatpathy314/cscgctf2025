from pwn import *
import base64

URL = "52a2a17f47d57a5606ea9f6b-1338-shadows-of-neon-city.challenge.cscg.live"
PORT = 1337


def connect():
    if args.REMOTE:
        return remote(URL, PORT, ssl=True)
    else:
        return remote("0.0.0.0", 1338)


if __name__ == "__main__":
    conn = connect()
    n_bytes = conn.recvline_contains(b"n = ")
    e_bytes = conn.recvline_contains(b"e = ")
    cipher_bytes = conn.recvline_contains(b"cipher = ")

    n = int(n_bytes.split(b" = ")[1])
    e = int(e_bytes.split(b" = ")[1])
    c_b64 = cipher_bytes.split(b" = ")[1]

    print(f"The value of n is: {n}")

    # https://www.numberempire.com/numberfactorizer.php
    p = int(input("Enter the value of p: "))
    q = int(input("Enter the value of q: "))

    phi = (p - 1) * (q - 1)
    d = pow(e, -1, phi)

    c_bytes = base64.b64decode(c_b64)
    c_int = int.from_bytes(c_bytes, "big")

    m_int = pow(c_int, d, n)
    m_bytes = m_int.to_bytes((m_int.bit_length() + 7) // 8, "big")
    message = m_bytes.decode()
    print(f"Message: {message}")
    
    conn.interactive()
    conn.close()