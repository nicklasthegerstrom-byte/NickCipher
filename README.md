# 🔐 NickCipher

**NickCipher** är ett CLI-baserat krypteringsverktyg skrivet i Python som implementerar ett **homofoniskt substitutionschiffer** med dynamisk emoji-mappning.

Projektet är utvecklat som ett **lärande- och designprojekt** med fokus på:
- kryptografiska principer
- hotmodellering
- session- och nyckelhantering
- säker filhantering

NickCipher är **inte avsett som industrikrypto**, utan som ett transparent och pedagogiskt system där designval och begränsningar är tydliga.

---

## ✨ Grundidé

Till skillnad från ett enkelt substitutionschiffer (där t.ex. `A → 🍎` varje gång), använder NickCipher **homofonisk substitution**:

- varje tecken mappas till **flera möjliga emojis**
- vid kryptering väljs en emoji slumpmässigt från tecknets pool
- samma klartext ger olika kryptotext varje gång

Detta reducerar mönster som annars kan utnyttjas i frekvensanalys.

---

## 📊 Frekvensbaserad Emoji-allokering

Emoji-fördelningen baseras på **svensk teckenfrekvens**.

Vanliga tecken får fler “alias” (emojis), ovanliga färre.  
Syftet är att jämna ut det statistiska fingeravtrycket i kryptotexten.

Exempel:

| Tecken | Antal emojis |
|------|--------------|
| Mellanslag (` `) | 18 |
| A, E | 12 |
| T, N | 11 |
| R | 10 |
| S, I | 8 |
| ., ,, !, ? | 7 |
| X, W, Z, Q | 2 |

Mellanslag har högst vikt för att dölja:
- ordlängder
- rytm
- textstruktur  

(en klassisk svaghet i enkla chiffer).

---

## 🧠 Nyckelgenerering

### Deterministisk nyckel
Nyckeln genereras deterministiskt från användarens lösenord:

- lösenord → SHA-256
- hash → 256-bitars seed
- seed → deterministisk emoji-mappning

Det innebär:
- samma lösenord → samma nyckel
- ingen nyckel behöver lagras för att dekryptera

⚠️ **Viktigt:**  
SHA-256 gör processen deterministisk – inte säker mot lösenordsgissning.  
Systemets praktiska säkerhet beror helt på lösenordets entropi.

---

## 🔐 Session Management

NickCipher har ett medvetet designat **minnes- och sessionsflöde**:

### Volatile Mode (High Security)
- nyckeln raderas ur RAM efter varje operation
- lösenord krävs för varje kryptering/dekryptering
- minimerar exponering av nyckelmaterial

### Persistent Session
- nyckeln hålls i minnet under programkörningen
- smidigare arbetsflöde
- kan manuellt rensas via menyval

Detta demonstrerar skillnaden mellan **säkerhet** och **användbarhet** i praktiken.

---

## 🗝️ Key Management

NickCipher erbjuder även explicit nyckelhantering:

- **Export:** spara emoji-mappningen som `.json`
- **Import:** ladda nyckel för dekryptering utan lösenord

⚠️ En exporterad nyckelfil är **en hemlighet**.  
Alla som har filen kan dekryptera tillhörande data.

---

## 🧮 Nyckelutrymme & Brute Force

Antalet möjliga emoji-nycklar beräknas som permutationer:

```
P(n, k) = n! / (n - k)!
```

Med aktuell emoji-pool resulterar detta i en nyckelrymd med **~80–90 decimal­siffror**.

Detta gör:
- brute-force mot **själva emoji-mappningen** beräkningsmässigt orealistisk
- verkliga attacker riktas istället mot **lösenordet**

---

## 🛡️ Säker Filhantering

Alla filoperationer skyddas mot path traversal:

```python
base_path.resolve() in target_path.resolve().parents
```

Detta förhindrar attacker som `../../etc/passwd`.

---

## 📁 Mappstruktur

```
data/
├── input/    # Klartextfiler (.txt)
├── output/   # Krypterad / dekrypterad text
├── keys/     # Nyckelfiler (bör gitignoreras)
```

---

## 🚀 Installation & Körning

```bash
git clone https://github.com/nicklasthegerstrom-byte/NickCipher.git
cd NickCipher
python -m nickcipher.main
```

**Krav:** Python 3.9+

---

## ⚠️ Begränsningar & Designval

- Detta är **inte modern industrikryptografi**
- Ingen KDF, salt eller hårdvarubackning används
- Skyddar inte mot komprometterad maskin eller keylogging
- Avsiktligt pedagogisk implementation

Projektets mål är **förståelse**, inte militär certifiering.

---

## 🧠 Sammanfattning

NickCipher demonstrerar:
- homofonisk substitution
- frekvensutjämning
- deterministisk nyckelgenerering
- session- och minnessäkerhet
- realistisk hotmodellering

Ett genomtänkt kryptografiskt experiment – byggt från grunden.
