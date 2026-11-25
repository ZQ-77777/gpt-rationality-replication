"""Turn the model's free-text reply into an allocation (version 2).

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
    4. Only if no labelled pair exists: unlabelled numbers in order of appearance (as in version 1),
       flagged as rule "unlabelled" so the audit can count them.
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
    t = text.replace(",", " ").replace("**", "")
    ra, rb = _alias_re(label_a), _alias_re(label_b)
    mentions = []                                   # (pos, side, value)
    for side, al in (("A", ra), ("B", rb)):
        # label then number, on the same line. A dash between spaces is a separator ("Asset A - 70");
        # a dash touching the digits is a minus sign ("Asset A: -20").
        for mo in re.finditer(al + r"[ \t]*(?:points?|pts?)?[ \t]*(?:[:=]|[ \t][-–—][ \t]|[–—])?[ \t]*" + SNUM + r"(?!\s*%)", t, flags=re.I):
            mentions.append((mo.start(), side, _num(mo.group(1))))
        # number then label ("70 points to Asset A")
        for mo in re.finditer(r"(?<![\d.$])" + SNUM + CONNECT_AFTER_NUM + r"(?:the[ \t]+)?" + al, t, flags=re.I):
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
    if pairs:
        dec = _decisions(CONT_DECIDE, t)
        if dec:
            after = [pr for pr in pairs if pr[0] >= dec[-1] - 1]
            if after:
                return _out(after[0][1], after[0][2], "labelled-decision")
        distinct = {(round(a, 3), round(b, 3)) for _, a, b in pairs}
        if len(distinct) == 1:
            return _out(pairs[0][1], pairs[0][2], "labelled")
        return dict(a=None, b=None, valid=False, rule="ambiguous")
    # fallback: no labelled pair. Numbers in order of appearance (version 1 behaviour), flagged.
    if re.search(r"(?<![\w$])[-−]\d", t):
        return dict(a=None, b=None, valid=False, rule="negative")
    pts = [_num(v) for v in re.findall(NUM + r"\s*points?\b", t, flags=re.I)]
    pair = _first_pair(pts)
    rule = "unlabelled-points"
    if pair is None:
        nums = [_num(v) for v in re.findall(NUM, t) if _num(v) <= C.ENDOWMENT]
        pair, rule = _first_pair(nums), "unlabelled-any"
    if pair is None:
        return dict(a=None, b=None, valid=False, rule="none")
    return _out(pair[0], pair[1], rule)


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
