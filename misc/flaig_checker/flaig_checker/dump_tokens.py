# dump_tokens.py
from gguf_parser import GGUFParser
import re, itertools

p = GGUFParser("flaig_checker.gguf")
tokens = p.tokens                              # plain list[str]

# collect contiguous runs that look like “CTF{…}” even if split
flagish = []
for i in range(len(tokens)):
    run = ""
    for j in itertools.count(i):
        if j >= len(tokens): break
        piece = tokens[j]
        run += piece.replace("▁", "")          # leading U+2581 is “start-of-word” for sentencepiece
        if "}" in piece:
            flagish.append(run)
            break

for cand in flagish:
    if re.fullmatch(r".{0,5}\{[A-Za-z0-9_]{4,40}\}", cand):
        print("🔑  candidate:", cand)

