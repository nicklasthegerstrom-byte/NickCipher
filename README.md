# 🤫 NickCipher 🔐

**NickCipher** is a Python-based CLI encryption tool implementing a **homophonic substitution cipher** with dynamic emoji mapping.

The project is designed as a **learning and design-focused cryptography experiment**, emphasizing:
- cryptographic fundamentals
- threat modeling
- session and key management
- secure file handling

NickCipher is **not intended as industrial-grade cryptography**, but as a transparent and pedagogical system where design decisions and limitations are explicit.

---

## ✨ Core Idea

Unlike simple substitution ciphers (where a character always maps to the same symbol), NickCipher uses **homophonic substitution**:

- each character maps to **multiple possible emojis**
- encryption randomly selects from the character’s emoji pool
- identical plaintext produces different ciphertext each time

This significantly reduces patterns exploitable by classical frequency analysis.

---

## 📊 Frequency-Based Emoji Allocation

Emoji distribution is based on **Swedish character frequency**.

Common characters are assigned more emoji “aliases”, rare characters fewer.  
The goal is to flatten the statistical fingerprint of the ciphertext.

Example:

| Character | Emoji count |
|---------|-------------|
| Space (` `) | 18 |
| A, E | 12 |
| T, N | 11 |
| R | 10 |
| S, I | 8 |
| ., ,, !, ? | 7 |
| X, W, Z, Q | 2 |

The space character is intentionally given the highest weight to obscure:
- word boundaries
- word length
- sentence rhythm  

(a classic weakness in simple ciphers).

---

## 🧠 Key Generation

### Deterministic Key Derivation

Keys are generated deterministically from a user-provided password:

- password → SHA-256
- hash → 256-bit seed
- seed → deterministic emoji mapping

This means:
- the same password always produces the same key
- no key must be stored to decrypt ciphertext

⚠️ **Important:**  
SHA-256 makes the process deterministic — **not resistant to password guessing**.  
The system’s practical security is entirely bounded by password entropy (length and randomness).

---

## 🔐 Session Management

NickCipher includes explicit **session and memory management**:

### Volatile Mode (High Security)
- key material is erased from RAM after each operation
- password required for every encrypt/decrypt
- minimizes key exposure

### Persistent Session
- key remains in memory for the duration of the program
- smoother workflow
- can be manually wiped via the menu

This intentionally demonstrates the trade-off between **security** and **usability**.

---

## 🗝️ Key Management

NickCipher also supports explicit key handling:

- **Export:** save the emoji mapping as a `.json` key file
- **Import:** load a key to decrypt data without entering the original password

⚠️ An exported key file is **a secret**.  
Anyone with access to the file can decrypt associated ciphertext.

---

## 🧮 Key Space & Brute Force

The number of possible emoji keys is calculated as permutations:

```
P(n, k) = n! / (n - k)!
```

With the current emoji pool, this results in a key space represented by a number with **~80–90 decimal digits**.

This makes:
- brute-force attacks against the emoji mapping computationally infeasible
- real-world attacks focus instead on **password guessing**

---

## 🛡️ Secure File Handling

All file operations are protected against path traversal attacks:

```python
base_path.resolve() in target_path.resolve().parents
```

This prevents attacks such as `../../etc/passwd`.

---

## 📁 Directory Structure

```
nickcipher/
├── core/
│   ├── cipher.py         # Encryption engine (encode/decode) + key lifecycle
│   ├── keygen.py         # Loads emoji pool & weights, builds key mappings
│   ├── filehandler.py    # Secure file I/O & path validation
│   └── __init__.py
│
├── utils/
│   ├── logger.py         # Centralized logging
│   └── __init__.py
│
├── config.py             # Paths, constants, configuration
├── __main__.py           # CLI entry point (console script)
├── __init__.py
│
data/
├── base/
│   ├── emoji_pool.json   # Emoji symbol source
│   └── char_weight.json  # Swedish character frequency weights
├── input/                # Plaintext files (.txt)
├── output/               # Encrypted / decrypted output
├── keys/                 # Exported key files (gitignored)
│
README.md
pyproject.toml
```

---

## 🚀 Installation & Usage

### Install (development)

```bash
git clone https://github.com/nicklasthegerstrom-byte/NickCipher.git
cd NickCipher
python -m venv venv
source venv/bin/activate
pip install -e .
run nickcipher

```

**Requirements:** Python 3.9+

---

## ⚠️ Limitations & Design Choices

- This is **not modern industrial cryptography**
- No KDF, salt, or hardware-backed key storage is used
- Does not protect against a compromised system or keylogging
- Designed intentionally for clarity and learning

The goal of this project is **understanding**, not certification.

### Unsupported Characters & Fallback Handling

NickCipher operates on a predefined character set defined by its frequency weights.
If a character is encountered that does not exist in the current key mapping
(e.g. uncommon Unicode symbols or emojis), the system applies a deterministic
fallback character.

This design choice ensures that:
- encryption never fails due to unexpected input
- the output remains decryptable
- unsupported characters do not leak information through errors

A warning is emitted during encryption to make this behavior explicit.

--

📊 Benchmark & Frequency Analysis

NickCipher has been empirically tested for both performance and resistance to basic frequency analysis.

⏱ Performance (90,000 characters)

Measured on a local machine using repeated runs (n = 20):

Key generation:
  Average time: ~0.0007 s

Encryption:
  Average time: ~0.043 s

Decryption:
  Average time: ~0.014 s

Result: Encryption and decryption scale linearly with input size and are fast enough for interactive CLI usage.

🔍 Frequency Analysis (Plaintext vs Ciphertext)

Plaintext letter frequency (top examples):

' ' : 13400
'e' : 8600
't' : 8500
'a' : 6900
'n' : 6400

Emoji ciphertext frequency (top examples):

🦝 : 768
🐩 : 753
🐐 : 753
🌝 : 745
💚 : 737

🧠 Interpretation
	•	Plaintext shows strong statistical bias (space and common letters dominate).
	•	Emoji ciphertext shows a much flatter frequency distribution.
	•	High-frequency symbols such as spaces are effectively obscured.

This demonstrates that NickCipher’s homophonic substitution significantly reduces the effectiveness of classical frequency analysis compared to simple substitution ciphers.


## 🧠 Summary

NickCipher demonstrates:
- homophonic substitution
- frequency flattening
- deterministic key generation
- session-based key lifecycle control
- realistic threat modeling

A deliberately transparent cryptographic experiment — built from the ground up.
