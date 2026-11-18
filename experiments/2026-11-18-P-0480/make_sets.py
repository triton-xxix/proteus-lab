#!/usr/bin/env python3
"""Build test page sets for dupcheck with a known amount of repetition planted.

sets/template/   12 town pages from one template, only the town name swapped
                 (the naive "emergency plumber [town]" set).
sets/plant-NN/   12 pages of 20 sentences each where exactly NN% of each
                 page's sentences are shared with every other page and the
                 rest are unique to the page (random word strings, seeded).
The planted sets are a calibration check on the checker, not copy anyone
would publish. Standard library only.
"""
import os
import random

HERE = os.path.dirname(os.path.abspath(__file__))
TOWNS = ["Leeds", "Bradford", "Wakefield", "Huddersfield", "Halifax", "Harrogate",
         "York", "Doncaster", "Barnsley", "Rotherham", "Sheffield", "Hull"]

TEMPLATE = [
    "Emergency plumber in {t}, out to you within the hour.",
    "A burst pipe in {t} does not wait for office hours, and neither do we.",
    "Our engineers cover every postcode in {t} and the villages around it.",
    "We fix leaks, blocked drains, failed boilers and frozen pipes.",
    "Every job is priced before we start, with no call-out fee.",
    "All our engineers are Gas Safe registered and fully insured.",
    "We carry the common parts on the van, so most repairs are done in one visit.",
    "Call us any time of day or night, including bank holidays.",
    "Customers in {t} rate us five stars for speed and tidy work.",
    "We guarantee every repair for twelve months.",
    "If we cannot fix it on the first visit, the second visit is free.",
    "Ask about our boiler service plan when you call.",
]

PAGE = "<!doctype html><html><head><title>{title}</title></head><body><nav>Home Services Contact</nav><h1>{title}</h1>{body}<footer>Copyright</footer></body></html>"


def write(folder, name, title, sents):
    os.makedirs(folder, exist_ok=True)
    body = "".join("<p>%s</p>" % s for s in sents)
    with open(os.path.join(folder, name), "w") as f:
        f.write(PAGE.format(title=title, body=body))


def words(rng, n):
    letters = "abcdefghijklmnopqrstuvwxyz"
    return " ".join("".join(rng.choice(letters) for _ in range(rng.randint(4, 9))) for _ in range(n))


def main():
    for t in TOWNS:
        write(os.path.join(HERE, "sets", "template"), t.lower() + ".html",
              "Emergency plumber %s" % t, [s.format(t=t) for s in TEMPLATE])
    rng = random.Random(480)
    for share in (0, 25, 50, 75, 100):
        n_shared = 20 * share // 100
        shared = [words(rng, 9).capitalize() + "." for _ in range(n_shared)]
        for i in range(12):
            own = [words(rng, 9).capitalize() + "." for _ in range(20 - n_shared)]
            sents = shared + own
            rng.shuffle(sents)
            write(os.path.join(HERE, "sets", "plant-%03d" % share), "page%02d.html" % i,
                  "Planted page number %d of the set" % i, sents)
    print("wrote sets/template and sets/plant-000 to plant-100")


if __name__ == "__main__":
    main()
