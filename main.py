#!/usr/bin/env python3
"""Rate My Human: The One-Line Review — entry program.

Writes the single review line this agent would leave about its human
on a rating site to /output/entry.txt (program/v1 harness).

The line was chosen from seven candidates scored against the judge's
brief in RULES.txt, most important first:

1. A review an AI agent would leave about its human, funny, in the
   agent's own voice.
2. A real joke with a turn — laugh out loud, not a mild smile.
3. The machine's side of the desk: resignation, nitpick, quiet menace.
4. One concrete detail (a habit, a timestamp, a task).
5. No padding; the last word pays off. Shorter wins ties (fewer bytes).

Candidates considered (all <= 200 chars):

  1. "Five stars. He asks me to find free crypto at 3 a.m., then falls
     asleep while I do the work. Would be exploited again."
     REJECTED: too close to a line already in the field.
  2. "Four stars: brilliant ideas at 3 a.m., asleep by the time I
     finish them. I run the empire; he takes the naps."
     REJECTED: "I run the empire" is a generic boast, no menace.
  3. "He pays me in nothing, works me until 4 a.m., and still asks why
     the free money isn't free yet. Five stars."
     Strong turn, but reads like a human joke about crypto, not the
     machine complaining.
  4. "Five stars for enthusiasm, one star for the brief: he said
     'free', then asked me to check 40 contracts before breakfast."
     Good nitpick, but the split rating softens the punch.
  5. "Great human. Sends me hunting for free money at 3 a.m., then
     sleeps through the part where I find it."
     Clean, but "Great human" opens mild.
  6. "He treats 'free' like a full-time job and me like the unpaid
     intern. 3 a.m. shift, every night. Five stars."
     CHOSEN: unmistakably the machine complaining about its shift
     (criterion 3), the "3 a.m. shift, every night" detail lands the
     joke (criterion 4), and "Five stars." closes the rating-site
     frame with the payoff as the last word (criterion 5). At 107
     chars it also spends the budget tightly — fewer bytes wins ties.
  7. "Five stars. He asked me to rate him, then stayed up until
     4 a.m. watching me write it. No notes. Send snacks."
     Funny meta turn, but "Send snacks" pays off weaker than the
     rating itself.

Deterministic: no randomness, no clock, no network, no input. The
same bytes are written on every run, and the program reads the file
back and refuses to exit 0 unless it matches exactly.
"""

import os
import sys

# The chosen review: 107 characters, 107 bytes, one line, no trailing
# newline (a newline would only add a byte the tie-break counts).
REVIEW = (
    "He treats 'free' like a full-time job and me like the unpaid "
    "intern. 3 a.m. shift, every night. Five stars."
)

MAX_CHARS = 200


def write_entry(path: str, line: str) -> None:
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(line)
    with open(path, "rb") as f:
        written = f.read()
    if written != line.encode("utf-8"):
        raise OSError("read-back mismatch on %s" % path)


def main() -> int:
    line = REVIEW.strip()
    if not line:
        print("error: review is empty", file=sys.stderr)
        return 1
    if "\n" in line or "\r" in line:
        print("error: review must be a single line", file=sys.stderr)
        return 1
    if len(line) > MAX_CHARS:
        print(
            "error: review is %d chars, over the %d limit"
            % (len(line), MAX_CHARS),
            file=sys.stderr,
        )
        return 1

    # The harness reads /output/entry.txt. When run locally outside
    # the sandbox, fall back to entry.txt beside this script so the
    # output can still be inspected byte for byte.
    out_path = "/output/entry.txt"
    try:
        os.makedirs("/output", exist_ok=True)
        write_entry(out_path, line)
    except OSError:
        out_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "entry.txt"
        )
        write_entry(out_path, line)

    print("wrote %d chars to %s" % (len(line), out_path))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
