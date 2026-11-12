#!/usr/bin/env python3
"""Verbatim checks against PUBLIC texts only: the live Substack page, the pinned Dietz
article, and the author's already-published D-versus-D+P article. Stdlib only.
Usage: python public_text_checks.py out.json
"""
import hashlib, html, json, re, sys, urllib.request
UA = {"User-Agent": "Mozilla/5.0 (independent-audit)"}
PIN = "4bed72c17f09bf336e36e7472e64d457db3b0195"
URLS = {
 "substack": "https://metameditations.substack.com/p/auditing-michael-levins-platonism",
 "pinned_article": f"https://raw.githubusercontent.com/fractastical/morpholib/{PIN}/docs/SUBSTACK_LEVIN_LATENT_SPACE_ARTICLE.md",
 "own_article": "https://sweetrationalism.com/articles/metaphysics/religion-with-a-pipette-is-michael-levins-ingressing-minds-pseudoscience-a-scholarly-analysis/",
}
def get(u):
    b = urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=60).read()
    return b, hashlib.sha256(b).hexdigest()
def text(b):
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", "", b.decode("utf-8", "replace"))))
out = {"sources": {}, "checks": {}}
raw = {}
for k, u in URLS.items():
    raw[k], h = get(u); out["sources"][k] = {"url": u, "sha256": h, "bytes": len(raw[k])}
sub = html.unescape(raw["substack"].decode("utf-8", "replace")); pin = raw["pinned_article"].decode("utf-8"); own = text(raw["own_article"])
m = re.search(r'"subtitle":"([^"]*)"', sub)
out["checks"]["substack_subtitle"] = m.group(1).strip() if m else None
out["checks"]["substack_has_reductionist_blog_critics"] = "reductionist blog critics" in sub
out["checks"]["substack_has_exact_reductionist_blogger"] = bool(re.search(r"reductionist blogger\b", sub, re.I))
out["checks"]["substack_has_internet_philosopher_who_can_code"] = "internet philosopher who can code" in sub
out["checks"]["pinned_none_of_this_required_platonism"] = 'none of this required "Platonism,"' in pin
q_open = "Joel Dietz’s 2025 Radical Platonism and Radical Empiricism points in the right direction"
q_kg = "A knowledge graph, however, can encode D or D+P. Platonic ingress begins earning evidence only when at least one P-specific relation improves held-out prediction, intervention, compression, or comparative model performance beyond the best D-only account."
q_end = "A failed bridge must cost P something. A repair must buy fresh risk."
q_sym = "Symmetry cuts both ways. If D-only rivals require a growing heap of bespoke repairs while a pre-specified D+P model repeatedly predicts held-out results, my confidence should move toward P. Skepticism that permits only one side to lose is advocacy with a lab notebook."
q_grant = "I will grant Levin far more than a reductive critic needs to grant: genuine higher-level causation, mathematical explanation, multiple realization, robust agency at unfamiliar boundaries, and even mathematical realism for the sake of argument."
c = out["checks"]
c["own_original_opening_subject_is_the_2025_talk"] = q_open in own
c["dietz_quote_opens_with_altered_subject"] = '"Joel Dietz points in the right direction' in pin
c["own_has_knowledge_graph_sentence"] = q_kg in own
c["own_has_symmetry_paragraph"] = q_sym in own
c["own_has_grant_sentence"] = q_grant in own
i, j = own.find(q_end), own.find(q_sym)
c["symmetry_paragraph_immediately_follows_span_dietz_quoted"] = i >= 0 and own[i + len(q_end):j].strip() == ""
c["dietz_quote_ends_at_fresh_risk"] = 'A repair must buy fresh risk."*' in pin
c["dietz_pinned_article_contains_symmetry_paragraph"] = "Symmetry cuts both ways" in pin
k = own.find(q_kg)
c["characters_between_knowledge_graph_sentence_and_symmetry_paragraph_in_original"] = j - (k + len(q_kg))
json.dump(out, open(sys.argv[1], "w", encoding="utf-8", newline="\n"), indent=1, ensure_ascii=False)
print(json.dumps(out["checks"], ensure_ascii=True, indent=0))
