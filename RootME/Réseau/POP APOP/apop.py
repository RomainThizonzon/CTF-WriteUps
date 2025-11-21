import sys
import hashlib

wordlist = sys.argv[1]

challenge = "<1755.1.5f403625.BcWGgpKzUPRC8vscWn0wuA==@vps-7e2f5a72>"
target_hash = "4ddd4137b84ff2db7291b568289717f0"

def md5hex(s):
    return hashlib.md5(s.encode('utf-8')).hexdigest()

count = 0
with open(wordlist, "r", errors="ignore") as f:
    for line in f:
        pwd = line.strip()
        if not pwd:
            continue
        count += 1
        candidate = challenge + pwd
        h = md5hex(candidate)
        if h == target_hash:
            print("[+] FOUND:", pwd)
            print("[+] md5(challenge+pwd) =", h)
            break
    else:
        print("[-] Not found in wordlist.")
