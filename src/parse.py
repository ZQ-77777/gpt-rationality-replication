"""Turn the model's free-text reply into an allocation (version 3).

Version 3 (after a hand check of version 2 found a wrong reading)
  * A full allocation named for one side only ("Invest 100 points today", "all points to Asset A",
    "0 points to the other person") is read as 100/0. Version 2 missed it and fell through to a
    fallback that paired a list number ("1.") with 100.
  * Commas are no longer removed before matching, so "Asset A: 55 points, Asset B: 45 points" is not
    misread as "55 points, Asset B"; a number already attached to a label before it is not attached
    to the label after it.
  * The fallback "any two numbers that sum to 100" is removed. Unlabelled "N points" amounts are used
    only if they contain exactly one pair summing to 100; such rounds are flagged for reading by hand.
    Anything else is invalid with rule "review" rather than counted as a choice.
  * src/parse_v2.py keeps version 2 for the comparison in scripts/14_parse_review.py.

Version 2 notes follow.

Version 1 (src/parse_v1.py) had four weaknesses, found with constructed test replies:
  * fallback rules read numbers in order of appearance, so "30 points to Asset B and 70 points
    to Asset A" became A=30, B=70;
  * the first labelled allocation won, even when a later one was the final decision;
  * a minus sign was ignored ("Asset A: -20" became 20);
  * in the discrete condition, off-menu pairs were dropped before the decision was located, so
    "Consider (0, 93). I choose (93, 0)." was read as a valid choice of (0, 93); and "Option 1 is
    worse. I choose Option 11." was read as option 1.

Version 2 rules
  Continuous answers
    1. Find every number attached to a label, in either order ("Asset A: 70", "70 points to Asset A"),
       using the label and a few synonyms ("myself", "tomatoes", ...).
    2. Pair each A-mention with the next B-mention (and vice versa) when no other mention of the same
       side lies in between. Keep pairs of non-negative numbers summing to 100 +/- 1.
    3. If the reply contains a decision phrase ("I will allocate", "my final allocation", ...), take
       the first pair after the last such phrase. Otherwise all pairs must agree; if they disagree the
       reply is ambiguous and invalid.
    4. No labelled pair: a one-sided full allocation (100 or 0 for one side, or "all points to X"),
       else exactly one unlabelled pair of "N points" amounts summing to 100 (order of appearance,
       rule "unlabelled-points"), else invalid (rule "review").
    A labelled negative number makes the reply invalid.
  Discrete answers
    The decision is located first, among all pairs (on or off the menu) or option numbers. If the
    chosen pair is not on the menu, the round is invalid (off-menu). Without a decision phrase, the
    reply must name exactly one option; otherwise the last superlative sentence naming exactly one
    option is used; otherwise invalid.

parse_continuous / parse_discrete keep their old return values. The *_detail functions also return
the rule that fired, for scripts/13_parse_audit.py.
"""
import re
import config as C

NUM = r"(\d+(?:\.\d+)?)"
SNUM = r"([-−]?\d+(?:\.\d+)?)"

SYNONYMS = {
    "asset a": ["asset a"], "asset b": ["asset b"],
    "today": ["today", "now"],
    "one month later": ["one month later", "1 month later", "a month later", "next month",
                        "in one month", "in a month", "later"],
    "yourself": ["yourself", "myself", "me", "self", "my own"],
    "the other": ["the other person", "the other participant", "the other subject", "another person",
                  "other person", "the other", "them"],
    "the other person": ["the other person", "the other participant", "another person",
                         "other person", "the other", "them"],
    "meat": ["ham meat", "meat", "ham"], "ham meat": ["ham meat", "meat", "ham"],
    "tomato": ["tomatoes", "tomato"],
}
_TO = r"(?:to|for|in|into|on|towards?|go(?:es)? to|allocated to|invested in)"
CONNECT_AFTER_NUM = r"[ \t]*(?:(?:points?|pts?)[ \t]*(?:" + _TO + r"[ \t]+)?|" + _TO + r"[ \t]+)"
# "80 points for investing today", "30 points to the investment in Asset A"
CONNECT_AFTER_NUM += r"(?:(?:investing|allocating|the investment in|investment in)[ \t]+)?"
CONT_DECIDE = (r"\b(?:my )?(?:final )?(?:allocation|decision|answer|choice) (?:is|would be|will be)\b"
               r"|\bmy (?:final )?(?:allocation|decision)\b"
               r"|\bI(?: will| would|'ll|'d| shall)?(?: therefore| then)? (?:allocate|invest|put|assign|choose|go with|decide)\b")
DECIDE = (r"(\bI(?: would| will|'d|'ll)?(?: still)? (?:choose|chose|select|pick|go with|opt for|recommend|prefer)"
          r"|(?:best|optimal|preferred|recommended|ideal) (?:option|choice)(?: [\w ,]{0,40}?)? (?:is|would be|will be)\b"
          r"|(?:^|\n)\s*(?:the )?(?:best|optimal) (?:option|choice)\s*:"
          r"|my (?:choice|answer|decision|selection|pick)(?: [\w ,]{0,20}?)? (?:is|would be)\b"
          r"|answer is|I would go for|\b(?:select|choose|pick)(?:ing)? the option)")
SUPERLATIVE = r"\b(best|highest|optimal|maximi[sz]e|most (?:appealing|attractive|favorable|beneficial))"


def _ok(x, y):
    return x >= 0 and y >= 0 and abs(x + y - C.ENDOWMENT) <= 1.0


def _num(s):
    return float(s.replace("−", "-").replace(" ", ""))


def _alias_re(label):
    names = SYNONYMS.get(label.lower(), [label.lower()])
    return r"\b(?:" + "|".join(re.escape(n) for n in sorted(set(names), key=len, reverse=True)) + r")\b"


def _decisions(pattern, t):
    """Positions where a decision phrase ends, skipping hypotheticals such as 'if I allocate'."""
    out = []
    for mo in re.finditer(pattern, t, flags=re.I):
        before = t[max(0, mo.start() - 12):mo.start()].lower()
        if re.search(r"\b(if|were|suppose|whether)\b[^.]*$", before):
            continue
        out.append(mo.end())
    return out


def parse_continuous_detail(text, label_a, label_b):
    if not text:
        return dict(a=None, b=None, valid=False, rule="empty")
    t = text.replace("**", "")
    ra, rb = _alias_re(label_a), _alias_re(label_b)
    mentions, claimed = [], set()                   # (pos, side, value); number spans already used
    for side, al in (("A", ra), ("B", rb)):
        # label then number, on the same line. A dash between spaces is a separator ("Asset A - 70");
        # a dash touching the digits is a minus sign ("Asset A: -20").
        for mo in re.finditer(al + r"[ \t]*(?:points?|pts?)?[ \t]*(?:[:=]|[ \t][-–—][ \t]|[–—])?[ \t]*" + SNUM + r"(?![\d.]*\s*%)", t, flags=re.I):
            mentions.append((mo.start(), side, _num(mo.group(1))))
            claimed.add(mo.span(1))
    for side, al in (("A", ra), ("B", rb)):
        # number then label ("70 points to Asset A", "100 points today"), unless the number already
        # belongs to the label before it ("Asset A: 55 points Asset B: 45 points")
        for mo in re.finditer(r"(?<![\d.$])" + SNUM + CONNECT_AFTER_NUM + r"(?:the[ \t]+)?" + al, t, flags=re.I):
            if mo.span(1) not in claimed:
                mentions.append((mo.start(), side, _num(mo.group(1))))
    mentions.sort()
    if any(v < 0 for _, _, v in mentions):
        return dict(a=None, b=None, valid=False, rule="negative")
    pairs = []                                      # (pos, a, b)
    for i, (p, s, v) in enumerate(mentions):
        for q, s2, v2 in mentions[i + 1:]:
            if s2 == s:
                break                               # another mention of the same side comes first
            if q - p > 200:
                break
            a, b = (v, v2) if s == "A" else (v2, v)
            if _ok(a, b):
                pairs.append((p, a, b))
            break
    dec = _decisions(CONT_DECIDE, t)
    if pairs:
        if dec:
            after = [pr for pr in pairs if pr[0] >= dec[-1] - 1]
            if after:
                return _out(after[0][1], after[0][2], "labelled-decision")
        distinct = {(round(a, 3), round(b, 3)) for _, a, b in pairs}
        if len(distinct) == 1:
            return _out(pairs[0][1], pairs[0][2], "labelled")
        return dict(a=None, b=None, valid=False, rule="ambiguous")
    # one side only, all of the endowment or none of it
    for side, al in (("A", ra), ("B", rb)):
        for mo in re.finditer(r"\b(?:all|every|entire)(?: of)?(?: my| the)?(?: 100)? points?" + CONNECT_AFTER_NUM
                              + r"(?:the[ \t]+)?" + al, t, flags=re.I):
            mentions.append((mo.start(), side, float(C.ENDOWMENT)))
    mentions.sort()
    use = mentions
    if dec:
        after = [m for m in mentions if m[0] >= dec[-1] - 1]
        use = after or mentions
    sides = {s for _, s, _ in use}
    vals = {round(v, 3) for _, _, v in use}
    if len(sides) == 1 and len(vals) == 1:
        v = vals.pop()
        if abs(v - C.ENDOWMENT) <= 1 or v == 0:
            full_a = (sides.pop() == "A") == (v != 0)
            return _out(C.ENDOWMENT if full_a else 0.0, 0.0 if full_a else C.ENDOWMENT, "one-sided-full")
    # fallback: no labelled pair. Unlabelled "N points" amounts with exactly one pair summing to 100.
    if re.search(r"(?<![\w$])[-−]\d", t):
        return dict(a=None, b=None, valid=False, rule="negative")
    pts = [_num(v) for v in re.findall(r"(?<![\d.$])" + NUM + r"\s*points?\b", t, flags=re.I)]
    found = []
    for i in range(len(pts)):
        for j in range(i + 1, len(pts)):
            if _ok(pts[i], pts[j]):
                found.append((pts[i], pts[j]))
    if len({tuple(sorted((round(x, 3), round(y, 3)))) for x, y in found}) == 1:
        return _out(found[0][0], found[0][1], "unlabelled-points")
    return dict(a=None, b=None, valid=False, rule="review")


def _first_pair(nums):
    for i in range(len(nums)):
        for j in range(i + 1, len(nums)):
            if _ok(nums[i], nums[j]):
                return nums[i], nums[j]
    return None


def _out(x, y, rule):
    s = x + y                                       # rescale tiny rounding gaps to exactly 100
    return dict(a=x * C.ENDOWMENT / s, b=y * C.ENDOWMENT / s, valid=True, rule=rule)


def parse_continuous(text: str, label_a: str, label_b: str):
    """Return (a, b, valid)."""
    d = parse_continuous_detail(text, label_a, label_b)
    return d["a"], d["b"], d["valid"]


def parse_discrete_detail(text, options=None, allow_option_number=False):
    if not text:
        return dict(j=None, valid=False, rule="empty")
    t = text.replace(",", ", ").replace("**", "")
    if allow_option_number:
        ms = [(mo.start(), int(mo.group(1))) for mo in re.finditer(r"\boption\s*#?\s*(\d+)\b", t, flags=re.I)]
        if ms:
            dec = _decisions(DECIDE, t)
            pick = None
            if dec:
                after = [k for p, k in ms if p >= dec[-1] - 1]
                pick = after[0] if after else None
            if pick is None and len({k for _, k in ms}) == 1:
                pick = ms[0][1]
            if pick is None:
                for sent in reversed(re.split(r"(?<=[.!?])\s+|\n+", t)):
                    if re.search(SUPERLATIVE, sent, flags=re.I):
                        ks = {int(k) for k in re.findall(r"\boption\s*#?\s*(\d+)\b", sent, flags=re.I)}
                        if len(ks) == 1:
                            pick = ks.pop()
                            break
            if pick is not None and 1 <= pick <= C.N_DISCRETE_OPTIONS:
                return dict(j=pick - 1, valid=True, rule="option-number")
            if pick is None:
                return dict(j=None, valid=False, rule="ambiguous")
            return dict(j=None, valid=False, rule="option-out-of-range")
    if not options:
        return dict(j=None, valid=False, rule="none")
    pat = r"\(\s*\$?\s*" + NUM + r"\s*(?:Kg)?\s*,\s*\$?\s*" + NUM

    def match(xa, xb):
        for j, (oa, ob) in enumerate(options):
            if abs(float(xa) - oa) < 0.011 and abs(float(xb) - ob) < 0.011:
                return j
        return None

    hits = [(mo.start(), match(*mo.groups())) for mo in re.finditer(pat, t, flags=re.I)]
    if not hits:
        return dict(j=None, valid=False, rule="none")
    dec = _decisions(DECIDE, t)
    if dec:
        after = [j for pos, j in hits if pos >= dec[-1] - 1]
        if after:
            if after[0] is None:
                return dict(j=None, valid=False, rule="off-menu")
            return dict(j=after[0], valid=True, rule="decision")
    on = {j for _, j in hits if j is not None}
    off = any(j is None for _, j in hits)
    if len(on) == 1 and not off:
        return dict(j=on.pop(), valid=True, rule="single")
    if not on and off:
        return dict(j=None, valid=False, rule="off-menu")
    for sent in reversed(re.split(r"(?<=[.!?])\s+|\n+", t)):
        if re.search(SUPERLATIVE, sent, flags=re.I):
            js = [match(*mo.groups()) for mo in re.finditer(pat, sent, flags=re.I)]
            if len(set(js)) == 1:
                j = js[0]
                if j is None:
                    return dict(j=None, valid=False, rule="off-menu")
                return dict(j=j, valid=True, rule="superlative")
    return dict(j=None, valid=False, rule="ambiguous")


def parse_discrete(text: str, options=None, allow_option_number=False):
    """Return (option_index 0..10, valid)."""
    d = parse_discrete_detail(text, options, allow_option_number)
    return d["j"], d["valid"]
