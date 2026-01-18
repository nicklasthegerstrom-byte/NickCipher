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
text = test_text * 10
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


results_encode = loop_benchmark_time(lambda: cipher.encode(text), 20)
results_decode = loop_benchmark_time(lambda: cipher.decode(decode_text), 20)
results_key = loop_benchmark_time(lambda: cipher.generate_key("benchtest"), 20)


avg_encode = average(results_encode)
median_encode = median(results_encode)

avg_decode = average(results_decode)
median_decode = median(results_decode)

avg_key = average(results_key)
median_key = median(results_key)



lines = [
    "BENCH FILE STARTED",
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
    f"  Average time : {median_decode:.7f}",

]

report = "\n".join(lines)

print(report)

write_txt(RESULTS_FILE, report)