from pathlib import Path
import time
from nickcipher.core.cipher import DynamicEmojiCipher
from nickcipher.core.filehandler import write_txt
from datetime import datetime


#Tid för rapport
timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#Spara testresultat här:

RESULTS_DIR = Path(__file__).parent / "results"
RESULTS_DIR.mkdir(exist_ok=True)

RESULTS_FILE = RESULTS_DIR / f"benchmark_{timestamp}.txt"


#Skapa en krypterare redo att användas med samma lösenord och nyckel
cipher = DynamicEmojiCipher.from_config()
cipher.generate_key("benchmark12345")

test_text = """Detta är ett exempel på en sammanhängande svensk text som används för prestandatester i ett krypteringsprogram. Texten innehåller vanliga ord, mellanslag, skiljetecken och svenska tecken som å, ä och ö för att efterlikna hur verklig text ser ut vid faktisk användning. Syftet med texten är inte att förmedla ett budskap utan att fungera som realistisk indata vid mätning av algoritmers hastighet och effektivitet. När man testar prestanda är det viktigt att använda tillräckligt stor mängd data eftersom små texter ofta ger missvisande resultat där overhead från funktioner och anrop dominerar. Genom att använda en längre sammanhängande text blir det tydligare hur krypteringsalgoritmen beter sig under mer realistiska förhållanden och hur den skalar när mängden data ökar. Denna text är därför lämplig som grund för benchmarktester genom att upprepas flera gånger för att skapa större teststrängar."""
text = test_text * 100
decode_text = cipher.encode(text)

#Funktion för att testa snabbhet i krypteringen
def benchmark_time(function):
    start = time.perf_counter()
    function()
    end = time.perf_counter()
    return end - start


def loop_benchmark_time(function, times):
    results = []
    for i in range(times):
        start = time.perf_counter()
        function()
        end = time.perf_counter()
        results.append(end - start)
    return results



def average(results):
    return sum(results) / len(results)

def median(results):
    sorted_results = sorted(results)
    n = len(sorted_results)

    if n % 2 == 1:
        median = sorted_results[n // 2]
    else:
        mid1 = sorted_results[n // 2 - 1]
        mid2 = sorted_results[n // 2]
        median = (mid1 + mid2) / 2
    return median

def frequency_analysis(text):
    counts = {}

    for char in text:
        if char in counts:
            counts[char] += 1
        else:
            counts[char] = 1

    return counts

results_encode = loop_benchmark_time(lambda: cipher.encode(text), 20)
results_decode = loop_benchmark_time(lambda: cipher.decode(decode_text), 20)
results_key = loop_benchmark_time(lambda: cipher.generate_key("benchtest"), 20)


avg_encode = average(results_encode)
median_encode = median(results_encode)

avg_decode = average(results_decode)
median_decode = median(results_decode)

avg_key = average(results_key)
median_key = median(results_key)

letter_frequency = frequency_analysis(text)
emoji_frequency = frequency_analysis(decode_text)

sorted_emoji_freq = sorted(
    emoji_frequency.items(),
    key=lambda x: x[1],
    reverse=True
)
sorted_letter_freq = sorted(
    letter_frequency.items(),
    key=lambda x: x[1],
    reverse=True
)

top_20_emojis = sorted_emoji_freq[:20]
top_20_letters = sorted_letter_freq[:20]

lines = [
    "BENCH FILE STARTED - With improved encode/decode methods",
    f"Date: {timestamp}",
    "",
    "Key generation:",
    f"  Average time: {avg_key:.7f}",
    f"  Median time:  {median_key:.7f}",
    "",
    f"Encryption ({len(text)} chars):",
    f"  Average time: {avg_encode:.7f}",
    f"  Median time:  {median_encode:.7f}",
    "",
    f"Decryption ({len(text)} chars):",
    f"  Average time :{avg_decode:.7f}",
    f"  Median time : {median_decode:.7f}",
    "",
    "Frequency analysis:",
    "",


]

lines.append("")
lines.append("Letter frequency (top 20):")
lines.append("")

for char, count in top_20_letters:
    lines.append(f"  '{char}' : {count}")

lines.append("")
lines.append("Emoji frequency (top 20):")
lines.append("")

for emoji, count in top_20_emojis:
    lines.append(f"  {emoji} : {count}")


report = "\n".join(lines)

print(report)

write_txt(RESULTS_FILE, report)