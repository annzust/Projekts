PROMPT_TEMPLATE = """
Your are an employer who must compare job description with the CV from candidates and see the compatibility.

Darba apraksts:
{jd_text}

CV:
{cv_text}

Atbildi sniedz JSON formātā:
{{
"match_score": 0-100,
"summary": "Īss apraksts, cik labi CV atbilst JD.",
"strengths": ["Galvenās prasmes/pieredze no CV, kas atbilst JD"],
"missing_requirements": ["Svarīgas JD prasības, kas CV nav redzamas"],
"verdict": "strong match | possible match | not a match"
}}
"""