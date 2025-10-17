import os
import json
import google.generativeai as genai

# API atslēga un prompta šablons
from config import API_KEY
from prompts import PROMPT_TEMPLATE

# Gemini konfigurācija
genai.configure(api_key=API_KEY)
MODEL = "gemini-2.5-flash"

# =============================
# Palīgfunkcijas
# =============================

def read_txt(path):
    """Atver un nolasa tekstu"""
    with open(path, encoding="utf-8") as f:
        return f.read()

def save_txt(path, text):
    """Saglabā tekstu failā"""
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)

def save_json(path, data):
    """Saglabā datus JSON formātā"""
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def make_report(result):
    """Uztaisa Markdown pārskatu no JSON"""
    rep = f"# CV novērtējums\n\n"
    rep += f"**Atbilstība:** {result['match_score']}%\n\n"
    rep += f"**Kopsavilkums:** {result['summary']}\n\n"
    rep += "## Stiprās puses:\n"
    rep += "".join([f"- {s}\n" for s in result['strengths']])
    rep += "\n## Trūkstošās prasmes:\n"
    rep += "".join([f"- {m}\n" for m in result['missing_requirements']])
    rep += f"\n**Verdikts:** **{result['verdict'].upper()}**\n"
    return rep

# =============================
# AI analīze
# =============================

def run_gemini(jd, cv, prompt_out):
    """Izsauc Gemini modeli un atgriež rezultātu JSON formātā"""
    prompt = PROMPT_TEMPLATE.format(jd_text=jd, cv_text=cv)
    save_txt(prompt_out, prompt)

    model = genai.GenerativeModel(MODEL)
    response = model.generate_content(
        prompt,
        generation_config=genai.types.GenerationConfig(
            temperature=0.3,
            response_mime_type="application/json"
        )
    )

    try:
        return json.loads(response.text)
    except Exception as e:
        print("Neizdevās nolasīt JSON no modeļa atbildes:", e)
        return {"error": True, "raw": response.text}

# =============================
# Galvenā daļa
# =============================

def main():
    os.makedirs("outputs", exist_ok=True)

    jd_path = "sample_inputs/jd.txt"
    if not os.path.exists(jd_path):
        print("Nav jd.txt faila mapē sample_inputs/.")
        return

    jd = read_txt(jd_path)

    for i in range(1, 4):
        cv_file = f"sample_inputs/cv{i}.txt"
        if not os.path.exists(cv_file):
            print(f"Trūkst {cv_file}")
            continue

        print(f"\n>>> Analizēju {cv_file}...")
        cv = read_txt(cv_file)

        prompt_file = f"outputs/cv{i}_prompt.md"
        json_out = f"outputs/cv{i}.json"
        report_out = f"outputs/cv{i}_report.md"

        res = run_gemini(jd, cv, prompt_file)
        save_json(json_out, res)

        if "error" not in res:
            save_txt(report_out, make_report(res))
            print(f"OK: {report_out} saglabāts.")
        else:
            print(f"Kļūda {cv_file}")

    print("\nDarbs pabeigts! Rezultāti mapē 'outputs/'.")

# =============================
# Izpilde
# =============================
if __name__ == "__main__":
    main()

