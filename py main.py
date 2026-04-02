from conllu import parse_incr
import random
import matplotlib.pyplot as plt
import os

# ----------- Dependency Length (DL) -----------
def compute_dl(sentence):
    total = 0
    for token in sentence:
        if token["head"] == 0:
            continue
        total += abs(token["id"] - token["head"])
    return total


# ----------- Intervener Complexity (IC) -----------
def compute_ic(sentence):
    total = 0
    for token in sentence:
        i = token["id"]
        j = token["head"]
        
        if j == 0:
            continue
        
        total += abs(i - j) - 1
    
    return total


# ----------- Random Baseline -----------
def randomize_sentence(sentence):
    tokens = list(sentence)
    
    positions = [token["id"] for token in tokens]
    shuffled = positions[:]
    random.shuffle(shuffled)
    
    mapping = dict(zip(positions, shuffled))
    
    new_sentence = []
    
    for token in tokens:
        new_token = token.copy()
        
        new_token["id"] = mapping[token["id"]]
        
        if token["head"] != 0:
            new_token["head"] = mapping[token["head"]]
        
        new_sentence.append(new_token)
    
    return new_sentence


# ----------- PROCESS FUNCTION -----------
def process_file(filename, language_name):
    
    if not os.path.exists(filename):
        print(f"{language_name}: File not found")
        return None
    
    total_dl_real = 0
    total_ic_real = 0
    total_dl_rand = 0
    total_ic_rand = 0
    count = 0

    with open(filename, "r", encoding="utf-8") as f:
        for sentence in parse_incr(f):
            try:
                if not all(isinstance(token["id"], int) for token in sentence):
                    continue
                
                dl_real = compute_dl(sentence)
                ic_real = compute_ic(sentence)
                
                random_sentence = randomize_sentence(sentence)
                dl_rand = compute_dl(random_sentence)
                ic_rand = compute_ic(random_sentence)
                
                total_dl_real += dl_real
                total_ic_real += ic_real
                total_dl_rand += dl_rand
                total_ic_rand += ic_rand
                
                count += 1
                
                if count >= 1000:
                    break
            
            except:
                continue

    if count == 0:
        return None

    return {
        "language": language_name,
        "dl_real": total_dl_real / count,
        "dl_rand": total_dl_rand / count,
        "ic_real": total_ic_real / count,
        "ic_rand": total_ic_rand / count
    }


# ----------- MAIN PROGRAM -----------

files = [
    ("en_ewt-ud-train.conllu", "English"),
    ("hi_hdtb-ud-train.conllu", "Hindi"),
    ("de_gsd-ud-train.conllu", "German"),
    ("fr_gsd-ud-train.conllu", "French")
]

all_runs = []

# ----------- RUN EXPERIMENT MULTIPLE TIMES -----------
for i in range(3):
    print(f"\n--- Run {i+1} ---\n")
    
    results = []

    for file, lang in files:
        result = process_file(file, lang)
        if result:
            results.append(result)
    
    all_runs.append(results)


# ----------- AVERAGE RESULTS -----------

final_results = {}

for run in all_runs:
    for r in run:
        lang = r["language"]
        
        if lang not in final_results:
            final_results[lang] = {
                "dl_real": 0,
                "dl_rand": 0,
                "ic_real": 0,
                "ic_rand": 0,
                "count": 0
            }
        
        final_results[lang]["dl_real"] += r["dl_real"]
        final_results[lang]["dl_rand"] += r["dl_rand"]
        final_results[lang]["ic_real"] += r["ic_real"]
        final_results[lang]["ic_rand"] += r["ic_rand"]
        final_results[lang]["count"] += 1


# ----------- PRINT + SAVE RESULTS -----------

print("\n===== FINAL AVERAGED RESULTS =====\n")
print("Language   DL(real)   DL(random)   IC(real)   IC(random)\n")

with open("results.txt", "w") as f:
    f.write("Language   DL(real)   DL(random)   IC(real)   IC(random)\n\n")

    for lang, values in final_results.items():
        c = values["count"]
        
        dl_real = round(values["dl_real"] / c, 2)
        dl_rand = round(values["dl_rand"] / c, 2)
        ic_real = round(values["ic_real"] / c, 2)
        ic_rand = round(values["ic_rand"] / c, 2)

        line = f"{lang}      {dl_real}        {dl_rand}         {ic_real}        {ic_rand}"
        
        print(line)
        f.write(line + "\n")

print("\nResults saved to results.txt")


# ----------- GRAPH -----------

languages = []
dl_real_values = []
dl_random_values = []

for lang, values in final_results.items():
    c = values["count"]
    
    languages.append(lang)
    dl_real_values.append(values["dl_real"] / c)
    dl_random_values.append(values["dl_rand"] / c)

plt.figure()

plt.plot(languages, dl_real_values, marker='o', label='DL Real')
plt.plot(languages, dl_random_values, marker='o', label='DL Random')

plt.xlabel("Language")
plt.ylabel("Dependency Length")
plt.title("Dependency Length Comparison (Real vs Random)")

plt.legend()

plt.savefig("graph.png")
plt.show()

print("Graph saved as graph.png")