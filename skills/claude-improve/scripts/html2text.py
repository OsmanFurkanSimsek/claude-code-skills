"""Strip an /insights HTML report to plain text (scripts and styles dropped). Usage: html2text.py <in.html> <out.txt>"""
import html, re, sys


def convert(src):
    src = re.sub(r"(?is)<(script|style)[^>]*>.*?</\1>", " ", src)
    src = re.sub(r"(?i)<br\s*/?>|</(p|div|li|h[1-6]|tr|section)>", "\n", src)
    src = re.sub(r"(?i)<h([1-6])[^>]*>", lambda m: "\n" + "#" * int(m.group(1)) + " ", src)
    src = re.sub(r"(?i)<li[^>]*>", "- ", src)
    src = re.sub(r"<[^>]+>", " ", src)
    src = html.unescape(src)
    lines = [re.sub(r"[ \t]+", " ", l).strip() for l in src.splitlines()]
    return "\n".join(l for l in lines if l)


if __name__ == "__main__":
    text = convert(open(sys.argv[1], encoding="utf-8", errors="replace").read())
    open(sys.argv[2], "w", encoding="utf-8").write(text)
    print(len(text), "chars")
