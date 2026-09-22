"""Verify a rendered CV PDF is actually parseable by an ATS.

Usage:  python verify-pdf.py Matheus_Malagris_CV.pdf
Exit:   0 = clean, 1 = a problem worth fixing before sending.

Checks three failure modes that are invisible when you look at the PDF:

  ligatures      Chromium shapes fi/fl/ff into single glyphs (U+FB00-FB04).
                 pypdf and Apache PDFBox return the raw glyph, so an ATS
                 searching for "Cloudflare" scores zero on a CV that has it.
  leaked markers PT-BR review notes or [ESTIMADO] / [DADO AUSENTE] annotations
                 that should have been stripped before rendering.
  glued words    Font embedding dropped the spaces between words.

Deliberately uses pypdf rather than pdftotext: pdftotext silently normalises
ligatures back to "fi"/"fl" and reports a broken file as clean.
"""

import re
import sys

LIGATURES = {
    "\ufb00": "ff", "\ufb01": "fi", "\ufb02": "fl",
    "\ufb03": "ffi", "\ufb04": "ffl",
}
MARKERS = ("DADO AUSENTE", "ESTIMADO", "Perfil inferido", "Gaps reais",
           "Cobertura da JD", "Lista de revis")


def main(path):
    try:
        import pypdf
    except ImportError:
        print("pypdf not installed. Run: pip install pypdf")
        return 1

    reader = pypdf.PdfReader(path)
    text = "\n".join(page.extract_text() or "" for page in reader.pages)

    found = {lig: text.count(lig) for lig in LIGATURES if lig in text}
    leaks = [m for m in MARKERS if m.lower() in text.lower()]
    glued = re.findall(r"[A-Za-z]{25,}", text)

    print("%-16s %d" % ("pages", len(reader.pages)))
    print("%-16s %d" % ("words", len(text.split())))

    if found:
        total = sum(found.values())
        print("%-16s FAIL (%d)" % ("ligatures", total))
        words = {m.group(0) for m in
                 re.finditer(r"[A-Za-z\ufb00-\ufb04]*[\ufb00-\ufb04][A-Za-z\ufb00-\ufb04]*", text)}
        for w in sorted(words)[:8]:
            plain = w
            for lig, sub in LIGATURES.items():
                plain = plain.replace(lig, sub)
            print("%-16s   stored as %r, an ATS searching %r finds nothing"
                  % ("", w, plain))
        print("%-16s   fix: add font-variant-ligatures:none to cv-style.css"
              % "")
    else:
        print("%-16s ok" % "ligatures")

    if leaks:
        print("%-16s FAIL %s" % ("leaked markers", leaks))
        print("%-16s   the strip step did not run. Do not send this file."
              % "")
    else:
        print("%-16s ok" % "leaked markers")

    if glued:
        print("%-16s FAIL %s" % ("glued words", glued[:3]))
        print("%-16s   spaces were lost. Try font-family: Arial, sans-serif."
              % "")
    else:
        print("%-16s ok" % "glued words")

    bad = bool(found or leaks or glued)
    print()
    print("SEND IT" if not bad else "FIX BEFORE SENDING")
    return 1 if bad else 0


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(__doc__)
        sys.exit(2)
    sys.exit(main(sys.argv[1]))
