#!/usr/bin/env python3
import hashlib
import random
import string
import sys

# ── CONFIG ─────────────────────────────────────────────────────────────────────

TEMPLATE_FILE = "attack.js"  # must contain "{randomdata}" somewhere
OUTPUT_FILE = "attack_found.js"  # will be written when a match is found
PLACEHOLDER = "{randomdata}"
TARGET_PREFIX = "1b6"
RANDOM_LEN = 32  # length of the random string you inject

# ── HELPERS ────────────────────────────────────────────────────────────────────


def gen_random_data(n=RANDOM_LEN):
    alphabet = string.ascii_letters + string.digits
    return "".join(random.choice(alphabet) for _ in range(n))


def file_sha1(text):
    return hashlib.sha1(text.encode("utf-8")).hexdigest()


# ── MAIN LOOP ──────────────────────────────────────────────────────────────────


def main():
    try:
        with open(TEMPLATE_FILE, "r", encoding="utf-8") as f:
            template = f.read()
    except FileNotFoundError:
        print(f"Error: couldn’t open template '{TEMPLATE_FILE}'", file=sys.stderr)
        sys.exit(1)

    if PLACEHOLDER not in template:
        print(
            f"Error: placeholder '{PLACEHOLDER}' not found in {TEMPLATE_FILE}",
            file=sys.stderr,
        )
        sys.exit(1)

    attempt = 0
    while True:
        attempt += 1
        rnd = gen_random_data()
        filled = template.replace(PLACEHOLDER, rnd)
        digest = file_sha1(filled)

        if digest.startswith(TARGET_PREFIX):
            with open(OUTPUT_FILE, "w", encoding="utf-8") as out:
                out.write(filled)
            print(f"[+] Success after {attempt} attempts!  SHA1={digest}")
            print(f"    → output written to {OUTPUT_FILE}")
            break

        # progress indicator every 1000 tries
        if attempt % 1000 == 0:
            print(f"  Tried {attempt:,} → latest SHA1={digest}")


if __name__ == "__main__":
    main()
