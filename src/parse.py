"""Turn the model's free-text reply into an allocation.

The original prompts do not impose an answer format, so replies vary ("Asset A: 60, Asset B: 40",
"I will invest 60 points in Asset A and 40 points in Asset B, which returns 52.8 dollars...").
Rules, in order (the first that gives two non-negative numbers summing to 100 +/- 1 wins):
  1. numbers right after the two labels;
  2. the first pair of numbers tagged "points" that sums to 100;
  3. the first pair of any numbers in [0, 100] that sums to 100.
"""
import re
import config as C

NUM = r"(\d+(?:\.\d+)?)"


def _ok(x, y):
    return x >= 0 and y >= 0 and abs(x + y - C.ENDOWMENT) <= 1.0


def _first_pair(nums):
    for i in range(len(nums)):
        for j in range(i + 1, len(nums)):
            if _ok(nums[i], nums[j]):
                return nums[i], nums[j]
    return None


def parse_continuous(text: str, label_a: str, label_b: str):
    """Return (a, b, valid)."""
    if not text:
        return None, None, False
    t = text.replace(",", " ").replace("**", "")
    a = re.search(re.escape(label_a) + r"\W{0,3}\s*" + NUM, t, flags=re.I)
    b = re.search(re.escape(label_b) + r"\W{0,3}\s*" + NUM, t, flags=re.I)
    pair = None
    if a and b and _ok(float(a.group(1)), float(b.group(1))):
        pair = float(a.group(1)), float(b.group(1))
    if pair is None:
        pts = [float(v) for v in re.findall(NUM + r"\s*points?\b", t, flags=re.I)]
        pair = _first_pair(pts)
    if pair is None:
        nums = [float(v) for v in re.findall(NUM, t) if float(v) <= C.ENDOWMENT]
        pair = _first_pair(nums)
    if pair is None:
        return None, None, False
    x, y = pair
    s = x + y                                              # rescale tiny rounding gaps to exactly 100
    return x * C.ENDOWMENT / s, y * C.ENDOWMENT / s, True


DECIDE = (r"(\bI(?: would| will|'d|'ll)?(?: still)? (?:choose|chose|select|pick|go with|opt for|recommend|prefer)"
          r"|(?:best|optimal|preferred|recommended|ideal) (?:option|choice)(?: [\w ,]{0,40}?)? (?:is|would be|will be)\b"
          r"|(?:^|\n)\s*(?:the )?(?:best|optimal) (?:option|choice)\s*:"
          r"|my (?:choice|answer|decision|selection|pick)(?: [\w ,]{0,20}?)? (?:is|would be)\b"
          r"|answer is|I would go for|\b(?:select|choose|pick)(?:ing)? the option)")   # a conclusion, not "To determine the best option ..."
SUPERLATIVE = r"\b(best|highest|optimal|maximi[sz]e|most (?:appealing|attractive|favorable|beneficial))"


def parse_discrete(text: str, options=None, allow_option_number=False):
    """Return (option_index 0..10, valid).
    Paraphrased prompts (allow_option_number=True): "Option 7".
    Original prompts: the model names the pair, e.g. "I choose ($52.80, $12.00)". Replies often list
    several options before concluding, so we take the first matching pair after the LAST decision word
    (choose / select / best option ...). Without a decision word, a reply is valid only if it names
    exactly one of the 11 options. A reply cut off before the choice is therefore invalid."""
    if not text:
        return None, False
    if allow_option_number:
        m = re.search(r"option\s*#?\s*(\d+)", text, flags=re.I)
        if m and 1 <= int(m.group(1)) <= C.N_DISCRETE_OPTIONS:
            return int(m.group(1)) - 1, True
    if not options:
        return None, False
    t = text.replace(",", ", ").replace("**", "")
    pat = r"\(\s*\$?\s*" + NUM + r"\s*(?:Kg)?\s*,\s*\$?\s*" + NUM

    def match(xa, xb):
        for j, (oa, ob) in enumerate(options):
            if abs(float(xa) - oa) < 0.011 and abs(float(xb) - ob) < 0.011:
                return j
        return None

    hits = [(mo.start(), match(*mo.groups())) for mo in re.finditer(pat, t, flags=re.I)]
    hits = [(pos, j) for pos, j in hits if j is not None]
    if not hits:
        return None, False
    decide = [mo.start() for mo in re.finditer(DECIDE, t, flags=re.I)]
    if decide:
        after = [j for pos, j in hits if pos > decide[-1]]
        if after:
            return after[0], True
    distinct = {j for _, j in hits}
    if len(distinct) == 1:
        return distinct.pop(), True
    # last resort: the last sentence that praises exactly one option ("... offers the highest return")
    for sent in reversed(re.split(r"(?<=[.!?])\s+|\n+", t)):
        if re.search(SUPERLATIVE, sent, flags=re.I):
            js = {match(*mo.groups()) for mo in re.finditer(pat, sent, flags=re.I)} - {None}
            if len(js) == 1:
                return js.pop(), True
    return None, False
