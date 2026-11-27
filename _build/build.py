#!/usr/bin/env python3
"""Build the Max's Picks static site into /workspace/plain-picks."""
from __future__ import annotations

import html as htmlmod
import re
from pathlib import Path
from urllib.parse import quote_plus

ROOT = Path("/workspace/plain-picks")
SITE = "Max’s Picks"
SITE_ASCII = "Max's Picks"

BOOKS = {
    "AMERICAN-HAGWON": ("American Hagwon", "Min Jin Lee"),
    "EXIT-PARTY": ("Exit Party", "Emily St. John Mandel"),
    "KIN": ("Kin", "Tayari Jones"),
    "LAND": ("Land", "Maggie O’Farrell"),
    "BIG-LITTLE-TRUTHS": ("Big Little Truths", "Liane Moriarty"),
    "COOL-MACHINE": ("Cool Machine", "Colson Whitehead"),
    "WHALE-HARBOR": ("Whale Harbor", "Mary Beth Keane"),
    "YESTERYEAR": ("Yesteryear", "Caro Claire Burke"),
    "FRUIT-FLY": ("Fruit Fly", "Josh Silver"),
    "VANISHING-FAMILY": ("The Vanishing Family: Love, Fate, and the Quest to End Dementia", "Robert Kolker"),
    "LONDON-FALLING": ("London Falling: A Mysterious Death in a Gilded City and a Family’s Search for Truth", "Patrick Radden Keefe"),
    "MOCKINGBIRD": ("To Kill a Mockingbird", "Harper Lee"),
    "GILEAD": ("Gilead", "Marilynne Robinson"),
    "THURSDAY-MURDER-CLUB": ("The Thursday Murder Club", "Richard Osman"),
    "1776": ("1776", "David McCullough"),
    "SPLENDID-AND-VILE": ("The Splendid and the Vile", "Erik Larson"),
    "BATTLE-CRY": ("Battle Cry of Freedom", "James M. McPherson"),
    "SAY-NOTHING": ("Say Nothing", "Patrick Radden Keefe"),
    "CHECKLIST-MANIFESTO": ("The Checklist Manifesto", "Atul Gawande"),
    "GUIDE-TO-THE-GOOD-LIFE": ("A Guide to the Good Life", "William B. Irvine"),
    "ON-WRITING": ("On Writing", "Stephen King"),
    "PROJECT-HAIL-MARY": ("Project Hail Mary", "Andy Weir"),
    "STATION-ELEVEN": ("Station Eleven", "Emily St. John Mandel"),
    "TEAM-OF-RIVALS": ("Team of Rivals", "Doris Kearns Goodwin"),
    "GUNS-OF-AUGUST": ("The Guns of August", "Barbara Tuchman"),
    "DEVIL-IN-THE-WHITE-CITY": ("The Devil in the White City", "Erik Larson"),
    "KILLERS-OF-THE-FLOWER-MOON": ("Killers of the Flower Moon", "David Grann"),
    "WARMTH-OF-OTHER-SUNS": ("The Warmth of Other Suns", "Isabel Wilkerson"),
    "INNOVATORS-DILEMMA": ("The Innovator’s Dilemma", "Clayton M. Christensen"),
    "GOOD-TO-GREAT": ("Good to Great", "Jim Collins"),
    "HARD-THING": ("The Hard Thing About Hard Things", "Ben Horowitz"),
    "LEAN-STARTUP": ("The Lean Startup", "Eric Ries"),
    "INTELLIGENT-INVESTOR": ("The Intelligent Investor", "Benjamin Graham"),
    "BUFFETT-ESSAYS": ("The Essays of Warren Buffett", "Lawrence Cunningham"),
    "ESSAYS-OF-WARREN-BUFFETT": ("The Essays of Warren Buffett", "Lawrence Cunningham"),
    "NEVER-SPLIT-THE-DIFFERENCE": ("Never Split the Difference", "Chris Voss"),
    "SHOE-DOG": ("Shoe Dog", "Phil Knight"),
    "7-HABITS": ("The 7 Habits of Highly Effective People", "Stephen R. Covey"),
    "CARNEGIE": ("How to Win Friends and Influence People", "Dale Carnegie"),
    "MANS-SEARCH": ("Man’s Search for Meaning", "Viktor E. Frankl"),
    "ATOMIC-HABITS": ("Atomic Habits", "James Clear"),
    "DEEP-WORK": ("Deep Work", "Cal Newport"),
    "FEELING-GOOD": ("Feeling Good", "David D. Burns"),
    "KILLER-ANGELS": ("The Killer Angels", "Michael Shaara"),
    "ALL-THE-LIGHT": ("All the Light We Cannot See", "Anthony Doerr"),
    "NIGHTINGALE": ("The Nightingale", "Kristin Hannah"),
    "BOOK-THIEF": ("The Book Thief", "Markus Zusak"),
    "WOLF-HALL": ("Wolf Hall", "Hilary Mantel"),
    "HAMNET": ("Hamnet", "Maggie O’Farrell"),
    "PILLARS-OF-THE-EARTH": ("The Pillars of the Earth", "Ken Follett"),
    "PACHINKO": ("Pachinko", "Min Jin Lee"),
    "AND-THEN-THERE-WERE-NONE": ("And Then There Were None", "Agatha Christie"),
    "SHERLOCK": ("The Adventures of Sherlock Holmes", "Arthur Conan Doyle"),
    "IN-THE-WOODS": ("In the Woods", "Tana French"),
    "MAGPIE-MURDERS": ("Magpie Murders", "Anthony Horowitz"),
    "CUCKOOS-CALLING": ("The Cuckoo’s Calling", "Robert Galbraith"),
    "GUEST-LIST": ("The Guest List", "Lucy Foley"),
    "IN-COLD-BLOOD": ("In Cold Blood", "Truman Capote"),
    "HELTER-SKELTER": ("Helter Skelter", "Vincent Bugliosi"),
    "ILL-BE-GONE": ("I’ll Be Gone in the Dark", "Michelle McNamara"),
    "EMPIRE-OF-PAIN": ("Empire of Pain", "Patrick Radden Keefe"),
    "MERE-CHRISTIANITY": ("Mere Christianity", "C.S. Lewis"),
    "SCREWTAPE": ("The Screwtape Letters", "C.S. Lewis"),
    "GREAT-DIVORCE": ("The Great Divorce", "C.S. Lewis"),
    "PILGRIMS-PROGRESS": ("The Pilgrim’s Progress", "John Bunyan"),
    "KNOWING-GOD": ("Knowing God", "J.I. Packer"),
    "CONFESSIONS": ("Confessions", "Augustine"),
    "COST-OF-DISCIPLESHIP": ("The Cost of Discipleship", "Dietrich Bonhoeffer"),
    "PRAYING-LIFE": ("A Praying Life", "Paul E. Miller"),
    "HIDING-PLACE": ("The Hiding Place", "Corrie ten Boom"),
}

# Official or retailer search/category pages verified Nov 27, 2026 (America/New_York).
# These are ordinary product/store pages, not affiliate tracking links.
PRODUCTS = {
    "WEATHERTECH": ("WeatherTech Tesla FloorLiners", "https://www.weathertech.com/floorliner-digitalfit/tesla/"),
    "TESMAG-MATS": ("TESMAG floor mats", "https://www.teslaacessories.com/collections/floor-mats"),
    "TESERY-MATS": ("Tesery floor mats", "https://www.tesery.com/collections/tesla-floor-mats"),
    "TESLA-BRAND-MATS": ("Tesla shop floor mats", "https://shop.tesla.com/category/vehicle-accessories"),
    "BRAND-MATS": ("Tesla-specialty floor mats", "https://www.teslaacessories.com/collections/floor-mats"),
    "AMAZON-MATS": ("all-weather Tesla floor mats on Amazon", "https://www.amazon.com/s?k=Tesla+Model+3+all+weather+floor+mats"),
    "AMAZON-MATS-WEATHERTECH-OR-EQUIVALENT": ("WeatherTech or equivalent Tesla mats on Amazon", "https://www.amazon.com/s?k=WeatherTech+Tesla+Model+3+FloorLiner"),
    "LECTRON": ("Lectron Tesla / NACS chargers", "https://ev-lectron.com/collections/tesla-chargers"),
    "LECTRON-ADAPTER": ("Lectron Tesla adapters", "https://ev-lectron.com/collections/tesla"),
    "AMAZON-CHARGER": ("Level 2 EV charger on Amazon", "https://www.amazon.com/s?k=Tesla+Level+2+home+charger+NACS"),
    "AMAZON-ADAPTER": ("Tesla / NACS charging adapter on Amazon", "https://www.amazon.com/s?k=Tesla+NACS+charging+adapter"),
    "AMAZON-FIRST-AID": ("car first-aid kit on Amazon", "https://www.amazon.com/s?k=car+first+aid+kit"),
    "AMAZON-FLASHLIGHT": ("flashlight on Amazon", "https://www.amazon.com/s?k=LED+flashlight"),
    "AMAZON-SCRAPER": ("ice scraper on Amazon", "https://www.amazon.com/s?k=car+ice+scraper"),
    "AMAZON-SHOVEL": ("compact snow shovel on Amazon", "https://www.amazon.com/s?k=compact+car+snow+shovel"),
    "AMAZON-TOWELS": ("absorbent towels on Amazon", "https://www.amazon.com/s?k=absorbent+car+towels"),
    "AMAZON-WASHER-FLUID": ("winter washer fluid on Amazon", "https://www.amazon.com/s?k=winter+windshield+washer+fluid"),
    "TIRES-OR-TIRE-CARE": ("Tesla wheel and tire care at T Sportline", "https://tsportline.com/collections/tesla-wheel-care-protection"),
    "AMAZON-CONSOLE-TRAY": ("Tesla center console tray on Amazon", "https://www.amazon.com/s?k=Tesla+Model+3+center+console+tray"),
    "BRAND-TRAY": ("Jowua center console organizers", "https://www.jowua-life.com/collections/center-console-organizer"),
    "JOWUA-TRAY": ("Jowua center console tray", "https://www.jowua-life.com/products/center-console-tray-organizer"),
    "CARGO-ORGANIZER": ("cargo organizer on Amazon", "https://www.amazon.com/s?k=Tesla+Model+Y+cargo+organizer"),
    "CUPHOLDER": ("Tesla cup holder insert on Amazon", "https://www.amazon.com/s?k=Tesla+Model+3+cup+holder+insert"),
    "HOOKS": ("Tesla cabin hooks on Amazon", "https://www.amazon.com/s?k=Tesla+Model+3+purse+hook"),
    "POUCH": ("seatback or console pouch on Amazon", "https://www.amazon.com/s?k=Tesla+Model+3+seat+back+organizer"),
    "AMAZON-INFLATOR": ("portable tire inflator on Amazon", "https://www.amazon.com/s?k=portable+tire+inflator"),
    "AMAZON-TREAD-GAUGE": ("tire tread gauge on Amazon", "https://www.amazon.com/s?k=tire+tread+depth+gauge"),
    "AMAZON-WHEEL-BRUSH": ("wheel brush on Amazon", "https://www.amazon.com/s?k=car+wheel+brush"),
    "AMAZON-WHEEL-CLEANER": ("wheel cleaner on Amazon", "https://www.amazon.com/s?k=car+wheel+cleaner"),
    "BRAND-WHEEL-CLEANER": ("Tesla wheel care at T Sportline", "https://tsportline.com/collections/tesla-wheel-care-protection"),
    "TSPORTLINE": ("T Sportline wheel care", "https://tsportline.com/collections/tesla-wheel-care-protection"),
    "WHEEL-COVERS": ("Tesla wheel covers on Amazon", "https://www.amazon.com/s?k=Tesla+Model+3+wheel+covers"),
    "WHEEL-SPRAY": ("wheel cleaner spray on Amazon", "https://www.amazon.com/s?k=car+wheel+cleaner+spray"),
    "AMAZON-COMB": ("undercoat rake / shedding comb on Amazon", "https://www.amazon.com/s?k=dog+undercoat+rake+large+dog"),
    "AMAZON-DESHED": ("deshedding tool on Amazon", "https://www.amazon.com/s?k=deshedding+tool+large+dog"),
    "AMAZON-HAMMOCK": ("dog car hammock on Amazon", "https://www.amazon.com/s?k=dog+car+hammock+large+dog"),
    "AMAZON-LINT": ("lint roller on Amazon", "https://www.amazon.com/s?k=lint+roller+pet+hair"),
    "AMAZON-SLICKER": ("slicker brush on Amazon", "https://www.amazon.com/s?k=slicker+brush+large+dog"),
    "AMAZON-SOFA-COVER": ("sofa cover for dogs on Amazon", "https://www.amazon.com/s?k=couch+cover+for+dogs+large"),
    "BRAND-DESHED": ("deshedding tools on Chewy", "https://www.chewy.com/s?query=deshedding%20tool%20large%20dog"),
    "CHEWY-COMB": ("shedding comb on Chewy", "https://www.chewy.com/s?query=undercoat%20rake%20large%20dog"),
    "CHEWY-DESHED": ("deshedding tool on Chewy", "https://www.chewy.com/s?query=deshedding%20tool%20large%20dog"),
    "CHEWY-HAMMOCK": ("dog car hammock on Chewy", "https://www.chewy.com/s?query=dog%20car%20hammock"),
    "CHEWY-LINT": ("lint roller on Chewy", "https://www.chewy.com/s?query=lint%20roller%20pet%20hair"),
    "CHEWY-SLICKER": ("slicker brush on Chewy", "https://www.chewy.com/s?query=slicker%20brush%20large%20dog"),
    "CHEWY-SOFA-COVER": ("sofa cover on Chewy", "https://www.chewy.com/s?query=couch%20cover%20for%20dogs"),
    "KURGO-HAMMOCK": ("Kurgo Rover Hammock", "https://www.kurgo.com/p/rover-hammock/POG30-17766"),
    "AMAZON-BED": ("large dog bed on Amazon", "https://www.amazon.com/s?k=large+dog+bed+55+65+lb"),
    "AMAZON-CRATE": ("large dog crate on Amazon", "https://www.amazon.com/s?k=large+dog+crate"),
    "CHEWY-BED": ("large dog bed on Chewy", "https://www.chewy.com/s?query=large%20dog%20bed"),
    "CHEWY-CRATE": ("large dog crate on Chewy", "https://www.chewy.com/s?query=large%20dog%20crate"),
    "AMAZON-CAR": ("dog car safety harness on Amazon", "https://www.amazon.com/s?k=dog+car+harness+large"),
    "AMAZON-LEASH": ("dog leash on Amazon", "https://www.amazon.com/s?k=large+dog+leash"),
    "AMAZON-WALK-HARNESS": ("walking harness for large dogs on Amazon", "https://www.amazon.com/s?k=large+dog+walking+harness"),
    "CHEWY-CAR": ("dog car harness on Chewy", "https://www.chewy.com/s?query=dog%20car%20harness%20large"),
    "CHEWY-LEASH": ("dog leash on Chewy", "https://www.chewy.com/s?query=large%20dog%20leash"),
    "CHEWY-WALK-HARNESS": ("walking harness on Chewy", "https://www.chewy.com/s?query=large%20dog%20walking%20harness"),
    "KURGO-CAR": ("Kurgo car harnesses", "https://www.kurgo.com/"),
    "KURGO-HARNESS": ("Kurgo harnesses", "https://www.kurgo.com/"),
    "PETSAFE-HARNESS": ("PetSafe Easy Walk 3 in 1 Harness", "https://www.petsafe.com/p/3in1-harness/3IN1-L-BLACK/"),
    "FANATICS-UK": ("Kentucky Wildcats shop at Fanatics", "https://www.fanatics.com/college/kentucky-wildcats"),
    "FANATICS-BENGALS": ("Cincinnati Bengals shop at Fanatics", "https://www.fanatics.com/nfl/cincinnati-bengals"),
    "FANATICS-REDS": ("Cincinnati Reds shop at Fanatics", "https://www.fanatics.com/mlb/cincinnati-reds"),
    "FANATICS-UK-JERSEY": ("Kentucky Wildcats jerseys at Fanatics", "https://www.fanatics.com/college/kentucky-wildcats/jerseys"),
    "FANATICS-BENGALS-JERSEY": ("Bengals jerseys at Fanatics", "https://www.fanatics.com/nfl/cincinnati-bengals/jerseys"),
    "FANATICS-REDS-JERSEY": ("Reds jerseys at Fanatics", "https://www.fanatics.com/mlb/cincinnati-reds/jerseys"),
    "FANATICS-HATS": ("team hats at Fanatics", "https://www.fanatics.com/college/kentucky-wildcats"),
    "FANATICS-APPAREL": ("licensed team apparel at Fanatics", "https://www.fanatics.com/college/kentucky-wildcats"),
    "FANATICS-GIFTS": ("team gifts at Fanatics", "https://www.fanatics.com/college/kentucky-wildcats"),
    "FANATICS-WINTER": ("team winter gear at Fanatics", "https://www.fanatics.com/college/kentucky-wildcats"),
    "LIDS-UK": ("Kentucky Wildcats hats at Lids", "https://www.lids.com/search?q=Kentucky%20Wildcats"),
    "LIDS-BENGALS": ("Bengals hats at Lids", "https://www.lids.com/search?q=Cincinnati%20Bengals"),
    "LIDS-REDS": ("Reds hats at Lids", "https://www.lids.com/search?q=Cincinnati%20Reds"),
    "LIDS-HATS": ("team hats at Lids", "https://www.lids.com/"),
    "RALLYHOUSE": ("Rally House", "https://www.rallyhouse.com/"),
    "RALLYHOUSE-APPAREL": ("team apparel at Rally House", "https://www.rallyhouse.com/"),
    "RALLYHOUSE-GIFTS": ("team gifts at Rally House", "https://www.rallyhouse.com/"),
    "RALLYHOUSE-HATS": ("hats at Rally House", "https://www.rallyhouse.com/"),
    "RALLYHOUSE-WINTER": ("winter fan gear at Rally House", "https://www.rallyhouse.com/"),
    "HOMAGE": ("Homage", "https://www.homage.com/"),
    "HOMAGE-TEES": ("Homage team tees", "https://www.homage.com/"),
    "AUDIBLE": ("Audible", "https://www.audible.com/"),
    "AUDIBLE-2026-SEARCH": ("2026 titles on Audible", "https://www.audible.com/search?keywords=best+books+2026"),
    "CHRISTIANBOOK-BIBLE": ("Bibles at Christianbook", "https://www.christianbook.com/page/bibles"),
    "AMAZON-BIBLE": ("Bibles on Amazon", "https://www.amazon.com/s?k=Bible"),
    "BOOKSHOP-BIBLE": ("Bibles at Bookshop.org", "https://bookshop.org/search?keywords=Bible"),
    "CHRISTIANBOOK-NIV": ("NIV Bible at Christianbook", "https://www.christianbook.com/apps/search?Ntt=NIV+Bible"),
    "AMAZON-NIV": ("NIV Bible on Amazon", "https://www.amazon.com/s?k=NIV+Bible"),
    "BOOKSHOP-NIV": ("NIV Bible at Bookshop.org", "https://bookshop.org/search?keywords=NIV+Bible"),
    "CHRISTIANBOOK-ESV": ("ESV Bible at Christianbook", "https://www.christianbook.com/apps/search?Ntt=ESV+Bible"),
    "AMAZON-ESV": ("ESV Bible on Amazon", "https://www.amazon.com/s?k=ESV+Bible"),
    "BOOKSHOP-ESV": ("ESV Bible at Bookshop.org", "https://bookshop.org/search?keywords=ESV+Bible"),
    "CHRISTIANBOOK-KJV": ("KJV Bible at Christianbook", "https://www.christianbook.com/apps/search?Ntt=KJV+Bible"),
    "AMAZON-KJV": ("KJV Bible on Amazon", "https://www.amazon.com/s?k=KJV+Bible"),
    "BOOKSHOP-KJV": ("KJV Bible at Bookshop.org", "https://bookshop.org/search?keywords=KJV+Bible"),
    "CHRISTIANBOOK-CATHOLIC": ("Catholic Bible at Christianbook", "https://www.christianbook.com/apps/search?Ntt=Catholic+Bible+NABRE"),
    "AMAZON-CATHOLIC": ("Catholic Bible on Amazon", "https://www.amazon.com/s?k=NABRE+Catholic+Bible"),
    "CHRISTIANBOOK-JOURNAL": ("journals at Christianbook", "https://www.christianbook.com/apps/search?Ntt=journal"),
    "AMAZON-JOURNAL": ("journal on Amazon", "https://www.amazon.com/s?k=hardcover+journal"),
    "CHRISTIANBOOK-CHILDRENS": ("children’s Bibles at Christianbook", "https://www.christianbook.com/apps/search?Ntt=children%27s+Bible"),
    "AMAZON-CHILDRENS": ("children’s Bible on Amazon", "https://www.amazon.com/s?k=children%27s+Bible"),
    "BOOKSHOP-CHILDRENS": ("children’s Bible at Bookshop.org", "https://bookshop.org/search?keywords=children%27s+Bible"),
    "CHRISTIANBOOK-MUSIC": ("Christian music at Christianbook", "https://www.christianbook.com/apps/search?Ntt=Christian+music"),
    "AMAZON-MUSIC": ("Christian music on Amazon", "https://www.amazon.com/s?k=Christian+music+CD"),
    "CHRISTIANBOOK-GIFTS": ("gifts at Christianbook", "https://www.christianbook.com/page/gifts"),
    "AMAZON-GIFTS": ("Christian gifts on Amazon", "https://www.amazon.com/s?k=Christian+gifts"),
    "CHRISTIANBOOK-BOOK": ("Christian books at Christianbook", "https://www.christianbook.com/"),
    "AMAZON-BOOK": ("books on Amazon", "https://www.amazon.com/s?k=Christian+books"),
    "BOOKSHOP-BOOK": ("Bookshop.org", "https://bookshop.org/"),
}

RETAILERS = {
    "BOOKSHOP": ("Bookshop.org", lambda q: f"https://bookshop.org/search?keywords={quote_plus(q)}"),
    "AMAZON": ("Amazon", lambda q: f"https://www.amazon.com/s?k={quote_plus(q)}"),
    "AUDIBLE": ("Audible", lambda q: f"https://www.audible.com/search?keywords={quote_plus(q)}"),
    "LIBRO": ("Libro.fm", lambda q: f"https://libro.fm/search?q={quote_plus(q)}"),
    "CHRISTIANBOOK": ("Christianbook", lambda q: f"https://www.christianbook.com/apps/search?Ntt={quote_plus(q)}"),
}

USED_SOURCES: list[tuple[str, str]] = []

def remember(label: str, url: str) -> None:
    pair = (label, url)
    if pair not in USED_SOURCES:
        USED_SOURCES.append(pair)

def resolve(token: str) -> tuple[str, str] | None:
    token = token.strip()
    if token in {",", "…", "..."} or token.endswith("…") or token.endswith("..."):
        if token in {"…", "...", "BOOKSHOP-…", "AMAZON-…", "AUDIBLE-…", "LIBRO-…", "CHRISTIANBOOK-…"}:
            return None
        if token.endswith("…") or token.endswith("..."):
            return None
    if token in PRODUCTS:
        label, url = PRODUCTS[token]
        remember(label, url)
        return label, url
    # retailer-book, e.g. BOOKSHOP-1776, AMAZON-SHOE-DOG
    for prefix, (rlabel, rfn) in RETAILERS.items():
        pfx = prefix + "-"
        if token.startswith(pfx):
            slug = token[len(pfx):]
            if slug in {"…", "...", ""} or "…" in slug:
                return None
            if slug in BOOKS:
                title, author = BOOKS[slug]
                q = f"{title} {author}"
                url = rfn(q)
                label = rlabel
                remember(f"{title} — {author} ({rlabel})", url)
                return label, url
            if token in PRODUCTS:
                return PRODUCTS[token]
            # generic search from slug
            q = slug.replace("-", " ")
            url = rfn(q)
            remember(f"{q} ({rlabel})", url)
            return rlabel, url
    # bare book slug? unlikely
    if token in BOOKS:
        title, author = BOOKS[token]
        url = RETAILERS["BOOKSHOP"][1](f"{title} {author}")
        remember(f"{title} — {author} (Bookshop.org)", url)
        return title, url
    # last resort: humanize and Amazon search
    label = token.replace("-", " ").title()
    url = f"https://www.amazon.com/s?k={quote_plus(label)}"
    remember(label, url)
    return label, url


def clean_markdown(text: str) -> str:
    text = text.replace("Plain Picks", SITE_ASCII)
    text = re.split(r"\n## VERIFY before you hit publish\b", text)[0].rstrip() + "\n"
    text = re.sub(r"\s*Use `\[[Aa]FFILIATE_LINK-[^\]]+\]`\.?", "", text)
    text = re.sub(r"`\[[Aa]FFILIATE_LINK-[^\]]+\]`", "", text)
    text = re.sub(
        r"For each title, after approval:\n\n(?:- \*\*[^*]+\*\*[^\n]*\n)+",
        "For each title, links go to the bookseller so you can check the current edition and price.\n\n",
        text,
    )
    text = re.sub(
        r"Independent-bookstore-friendly, and the official affiliate program pays the publisher of this site a higher commission than Amazon does on a physical book\.",
        "Independent-bookstore-friendly.",
        text,
    )
    text = text.replace(
        "If you use the Audible link on this page after it is live, it is an affiliate link:",
        "Audible:",
    )
    text = re.sub(
        r"After a brand program is approved, use that brand’s link\. Until then, do not invent a “best of” winner\.",
        "I am not inventing a single “best of” winner.",
        text,
    )
    # Accurate disclosure while programs are not yet approved
    text = text.replace("This article contains affiliate links to", "This page includes links to")
    text = text.replace("This article contains affiliate links (", "This page includes links to products and retailers (")
    text = text.replace("This article contains affiliate links.", "This page includes links to products and retailers.")
    for old, new in [
        (
            "If you buy through one of them, I may earn a commission at no extra cost to you.",
            "I may earn a commission if you buy through an affiliate link, at no extra cost to you. Until affiliate programs are approved, these links go to ordinary product or store pages and are not tracking links.",
        ),
        (
            "If you buy through one of them, I may earn a commission.",
            "I may earn a commission if you buy through an affiliate link, at no extra cost to you. Until affiliate programs are approved, these links go to ordinary product or store pages and are not tracking links.",
        ),
    ]:
        text = text.replace(old, new)
    return text


def replace_placeholders(text: str) -> str:
    def sub(m: re.Match) -> str:
        token = m.group(1)
        resolved = resolve(token)
        if not resolved:
            return ""
        label, url = resolved
        href = htmlmod.escape(url, quote=True)
        return f'<a class="product-link" href="{href}">{htmlmod.escape(label)}</a>'

    text = re.sub(r"\[AFFILIATE_LINK-([^\]]+)\]", sub, text)
    # tidy leftover blanks from removed ellipsis examples
    text = re.sub(r"- \*\*[^*]+\*\* — this is the default\.[^\n]*\n", "", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text


def inline(s: str) -> str:
    parts = re.split(r"(<a\s[^>]*>.*?</a>)", s)
    out = []
    for part in parts:
        if part.startswith("<a "):
            out.append(part)
            continue
        part = part.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        part = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", part)
        part = re.sub(r"(?<!\w)\*(?!\s)(.+?)(?<!\s)\*(?!\w)", r"<em>\1</em>", part)
        part = re.sub(
            r"\[([^\]]+)\]\((https?://[^)\s]+)\)",
            lambda m: f'<a href="{htmlmod.escape(m.group(2), quote=True)}">{m.group(1)}</a>',
            part,
        )
        out.append(part)
    return "".join(out)


def md_to_html(md: str) -> str:
    lines = md.splitlines()
    out: list[str] = []
    i = 0
    n = len(lines)

    def is_list_item(line: str) -> bool:
        return bool(re.match(r"^(\s*)([-*]|\d+\.)\s+", line))

    while i < n:
        line = lines[i]
        if not line.strip():
            i += 1
            continue
        if line.startswith("### "):
            out.append(f"<h3>{inline(line[4:].strip())}</h3>")
            i += 1
            continue
        if line.startswith("## "):
            out.append(f"<h2>{inline(line[3:].strip())}</h2>")
            i += 1
            continue
        if line.startswith("# "):
            out.append(f"<h1>{inline(line[2:].strip())}</h1>")
            i += 1
            continue
        if line.strip() in {"---", "***", "___"}:
            out.append("<hr>")
            i += 1
            continue
        if is_list_item(line):
            ordered = bool(re.match(r"^\d+\.\s+", line))
            tag = "ol" if ordered else "ul"
            items: list[str] = []
            while i < n and (is_list_item(lines[i]) or (items and lines[i].startswith("  ") and lines[i].strip())):
                if is_list_item(lines[i]):
                    items.append(re.sub(r"^(\s*)([-*]|\d+\.)\s+", "", lines[i]))
                else:
                    items[-1] += " " + lines[i].strip()
                i += 1
                # blank line inside a list: peek if next is continuation or new item
                while i < n and not lines[i].strip():
                    if i + 1 < n and (is_list_item(lines[i + 1]) or (lines[i + 1].startswith("  ") and lines[i + 1].strip())):
                        i += 1
                    else:
                        break
            out.append(f"<{tag}>")
            for item in items:
                out.append(f"<li>{inline(item)}</li>")
            out.append(f"</{tag}>")
            continue
        # paragraph
        buf = [line]
        i += 1
        while i < n and lines[i].strip() and not lines[i].startswith("#") and not is_list_item(lines[i]) and lines[i].strip() not in {"---", "***", "___"}:
            buf.append(lines[i])
            i += 1
        para = " ".join(x.strip() for x in buf)
        cls = ' class="disclosure"' if para.startswith("**Disclosure:**") or para.startswith("Disclosure:") else ""
        out.append(f"<p{cls}>{inline(para)}</p>")
    return "\n".join(out)


NAV = [
    ("index.html", "Home", "home"),
    ("sports/index.html", "Sports", "sports"),
    ("tesla/index.html", "Tesla", "tesla"),
    ("books/index.html", "Books", "books"),
    ("dogs/index.html", "Dogs", "dogs"),
    ("christian/index.html", "Christian", "christian"),
    ("tools/index.html", "Tools", "tools"),
    ("about.html", "About", "about"),
]


def prefix_for(rel: str) -> str:
    depth = rel.count("/")
    return "" if depth == 0 else "../" * depth


def nav_html(current: str, prefix: str) -> str:
    bits = []
    for href, label, key in NAV:
        here = ' aria-current="page"' if key == current else ""
        bits.append(f'<a href="{prefix}{href}"{here}>{label}</a>')
    return "\n        ".join(bits)


def page(rel: str, title: str, body: str, section: str, measure: bool = True) -> str:
    prefix = prefix_for(rel)
    main_class = "article-wrap" if measure else "wrap"
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{htmlmod.escape(title)} — {SITE}</title>
  <meta name="description" content="Honest shortlists from {SITE}. Affiliate links disclosed.">
  <link rel="stylesheet" href="{prefix}css/styles.css">
  <link rel="icon" href="{prefix}favicon.svg" type="image/svg+xml">
</head>
<body>
  <a class="skip" href="#content">Skip to content</a>
  <header class="site-header">
    <div class="header-inner">
      <a class="brand" href="{prefix}index.html">{SITE}</a>
      <p class="tagline">Honest shortlists. Affiliate links disclosed.</p>
      <nav class="main" aria-label="Main">
        {nav_html(section, prefix)}
      </nav>
    </div>
  </header>
  <main id="content" class="{main_class}">
{body}
  </main>
  <footer class="site-footer">
    <div class="footer-inner">
      <div class="footer-nav">
        <a href="{prefix}about.html">About</a>
        <a href="{prefix}disclosure.html">Disclosure</a>
        <a href="{prefix}privacy.html">Privacy</a>
      </div>
      <p>I may earn a commission if you buy through an affiliate link, at no extra cost to you. Until programs are approved, product links go to ordinary store pages. See the <a href="{prefix}disclosure.html">disclosure</a>.</p>
      <p>© 2026 {SITE}. Written from Villa Hills, Kentucky.</p>
    </div>
  </footer>
</body>
</html>
"""


ARTICLES = [
    ("/workspace/affiliate-tesla/03-articles/01-floor-mats-model-3-y.md", "tesla", "floor-mats-model-3-y", "All-weather floor mats for a Model 3 or Model Y — what to check before you order", "A buying checklist for winter slush, salt, and dog hair — not a one-SKU winner."),
    ("/workspace/affiliate-tesla/03-articles/02-home-level-2-charger.md", "tesla", "home-level-2-charger", "A home Level 2 charger for a Tesla — a calm buying guide", "When a wall unit is worth it, and how to shop without invented prices."),
    ("/workspace/affiliate-tesla/03-articles/03-kentucky-winter-tesla-kit.md", "tesla", "kentucky-winter-tesla-kit", "A practical winter kit for a Tesla in Kentucky or Ohio", "Mats, scraping, charging, and the unglamorous gear that actually gets used."),
    ("/workspace/affiliate-tesla/03-articles/04-cabin-organizers.md", "tesla", "cabin-organizers", "Cabin organizers for a Model 3 or Model Y — only if they earn the space they take", "Trays and hooks worth considering, and the clutter that is not."),
    ("/workspace/affiliate-tesla/03-articles/05-wheel-tire-care.md", "tesla", "wheel-tire-care", "Wheel and tire care for a Tesla you actually drive in winter", "Pressure, salt, and cleaning — not a wheel-upgrade catalog."),
    ("/workspace/affiliate/big-dogs/02-articles/01-shedding-large-dogs.md", "dogs", "shedding-large-dogs", "Shedding gear for a large dog — what is worth buying, and what is just more plastic", "Brushes, covers, and car gear for a household that already owns a vacuum."),
    ("/workspace/affiliate/big-dogs/02-articles/02-beds-and-crates-large-dogs.md", "dogs", "beds-and-crates-large-dogs", "Beds and crates for a large dog — measure the dog, then shop", "Sizing first, then a short list of places to look."),
    ("/workspace/affiliate/big-dogs/02-articles/03-harnesses-large-dogs.md", "dogs", "harnesses-large-dogs", "Harnesses for a large dog — fit, pulling, and car-time without the marketing", "Walking and car harnesses, with a reminder to measure."),
    ("/workspace/affiliate/sports-fans/02-articles/01-official-vs-bootleg.md", "sports", "official-vs-bootleg", "Official vs. bootleg fan gear — what to check before you buy UK, Bengals, or Reds stuff", "Licensed shops versus mystery listings, starting with Kentucky Wildcats."),
    ("/workspace/affiliate/sports-fans/02-articles/02-hats-and-casual-gear.md", "sports", "hats-and-casual-gear", "Hats and casual gear for UK, Bengals, and Reds fans", "The pieces people actually wear besides game day."),
    ("/workspace/affiliate/sports-fans/02-articles/03-gift-guide-uk-bengals-reds.md", "sports", "gift-guide-uk-bengals-reds", "A gift guide for UK, Bengals, and Reds fans", "Start with a hat or shirt if you do not know a jersey size."),
    ("/workspace/affiliate/books/02-articles/01-best-books-2026-gift-list.md", "books", "2026-gift-shortlist", "A 2026 gift shortlist: twelve books worth considering", "A short holiday list drawn from titles that actually exist this year."),
    ("/workspace/affiliate/books/02-articles/02-genre-starter-shortlists.md", "books", "genre-starter-shortlists", "Starter shortlists by genre: fiction, history, and useful nonfiction", "A map to one book, not a stack no one will finish."),
    ("/workspace/affiliate/books/02-articles/03-audiobook-starter-list.md", "books", "audiobook-starter-list", "An audiobook starter list — plus a free alternative to a paid app", "Try the library first, then a short pile that works as audio."),
    ("/workspace/affiliate/books/02-articles/04-history-shortlist.md", "books", "history-shortlist", "A history shortlist — books that read like a story, and a few that go deeper", "Narrative history you can finish in the evening, plus a longer stack."),
    ("/workspace/affiliate/books/02-articles/05-business-shortlist.md", "books", "business-shortlist", "A business shortlist — useful books, not a formula", "Starter titles. This is a book list, not investment advice."),
    ("/workspace/affiliate/books/02-articles/06-self-help-shortlist.md", "books", "self-help-shortlist", "A self-help shortlist that cuts the usual promises down to size", "Books people actually finish, without the guru tone."),
    ("/workspace/affiliate/books/02-articles/07-historical-fiction-shortlist.md", "books", "historical-fiction-shortlist", "A historical fiction shortlist — novels first, history lesson second", "Stories that still have to work if you already know how the war ends."),
    ("/workspace/affiliate/books/02-articles/08-mysteries-whodunits-shortlist.md", "books", "mysteries-whodunits-shortlist", "A mysteries and whodunits shortlist", "From Christie to a modern Thursday-night mystery."),
    ("/workspace/affiliate/books/02-articles/09-true-crime-shortlist.md", "books", "true-crime-shortlist", "A true crime shortlist — sober books, and the library as a fair first stop", "Heavy reading, recommended calmly, with no jokey tone."),
    ("/workspace/affiliate/christian-conservative/02-articles/01-choosing-a-bible.md", "christian", "choosing-a-bible", "Choosing a Bible — translation, format, and where to buy it", "Translation first, then a readable edition, then the seller."),
    ("/workspace/affiliate/christian-conservative/02-articles/02-christian-books-worth-giving.md", "christian", "christian-books-worth-giving", "Christian books worth giving — a short, plain list", "Lewis, Packer, and a few pastoral titles, without the junk aisle."),
    ("/workspace/affiliate/christian-conservative/02-articles/03-christian-gifts-not-junk.md", "christian", "christian-gifts-not-junk", "Christian gifts that are not junk — a short filter", "A book or Bible usually holds up better than a trinket."),
    ("/workspace/plain-picks/_build/tools-vpn-and-hosting.md", "tools", "vpn-and-hosting", "A VPN and a simple web host, without the scare tactics", "NordVPN and Hostinger, when you actually need them — and when GitHub Pages is enough."),
]

CATEGORY_INTRO = {
    "sports": ("UK, Bengals, and Reds fan gear", "Licensed Kentucky Wildcats, Cincinnati Bengals, and Cincinnati Reds gear, with UK listed first. Check the live shop page for sizes, shipping, and whether an item is actually licensed."),
    "tesla": ("Tesla owner accessories", "Practical gear for a Model 3 or Model S you actually drive around Cincinnati and Northern Kentucky. Confirm fitment for your exact year before you order."),
    "books": ("Books", "Shortlists across general fiction, history, business, self-help, historical fiction, mysteries, true crime, and audiobooks. The true crime list is first below because that is the shelf I come back to most. These are book lists, not investment advice."),
    "dogs": ("Gear for large dogs", "Shedding, beds, crates, and harnesses for large dogs — written with a ~55 lb and a ~65 lb dog in mind. Measure the dog. I am not a veterinarian."),
    "christian": ("Christian books and gifts", "A Bible-buying guide, a short list of books worth giving, and a filter for gifts that are not junk."),
    "tools": ("Tools", "A VPN for travel and public Wi-Fi, and a simple paid host if a free static site is not enough. Shopify waits until you are actually selling something."),
}

def excerpt_sources(start_count):
    used = USED_SOURCES[start_count:]
    if not used:
        return ""
    items = "\n".join(
        '<li><a href="%s">%s</a></li>' % (htmlmod.escape(url, quote=True), htmlmod.escape(label))
        for label, url in used
    )
    return (
        '<section class="sources" aria-labelledby="sources-heading">\n'
        '  <h2 id="sources-heading">Product and retailer pages referenced</h2>\n'
        '  <p>These are ordinary official or retailer pages, not affiliate tracking links, until programs are approved. Confirm fitment, edition, price, and stock on the live page.</p>\n'
        '  <ul>\n    %s\n  </ul>\n</section>'
    ) % items


def build_articles():
    by_cat = {}
    for src, section, slug, title, blurb in ARTICLES:
        start = len(USED_SOURCES)
        raw = Path(src).read_text(encoding="utf-8")
        raw = clean_markdown(raw)
        raw = replace_placeholders(raw)
        body_html = md_to_html(raw)
        if section == "books" and slug == "business-shortlist":
            body_html += (
                '<p class="note"><strong>Note:</strong> This is a book list, not investment advice. '
                "I am not recommending that you buy or sell any security.</p>"
            )
        body_html += excerpt_sources(start)
        rel = "%s/%s.html" % (section, slug)
        kicker = {
            "sports": "Sports",
            "tesla": "Tesla",
            "books": "Books",
            "dogs": "Dogs",
            "christian": "Christian",
            "tools": "Tools",
        }[section]
        inner = '<p class="kicker">%s</p>\n%s' % (kicker, body_html)
        (ROOT / rel).write_text(page(rel, title, inner, section, measure=True), encoding="utf-8")
        by_cat.setdefault(section, []).append((slug, title, blurb, rel))
    return by_cat


def build_category_pages(by_cat):
    book_priority = [
        "true-crime-shortlist",
        "2026-gift-shortlist",
        "mysteries-whodunits-shortlist",
        "history-shortlist",
        "audiobook-starter-list",
        "genre-starter-shortlists",
        "historical-fiction-shortlist",
        "business-shortlist",
        "self-help-shortlist",
    ]
    sports_priority = [
        "gift-guide-uk-bengals-reds",
        "official-vs-bootleg",
        "hats-and-casual-gear",
    ]
    tesla_priority = [
        "kentucky-winter-tesla-kit",
        "floor-mats-model-3-y",
        "home-level-2-charger",
        "cabin-organizers",
        "wheel-tire-care",
    ]

    def sort_items(section, items):
        order = {"books": book_priority, "sports": sports_priority, "tesla": tesla_priority}.get(section)
        if not order:
            return items
        rank = {s: i for i, s in enumerate(order)}
        return sorted(items, key=lambda it: rank.get(it[0], 99))

    for section, (heading, intro) in CATEGORY_INTRO.items():
        items = sort_items(section, by_cat.get(section, []))
        lis = "\n".join(
            '<li><a href="%s.html">%s</a><p>%s</p></li>'
            % (slug, htmlmod.escape(title), htmlmod.escape(blurb))
            for slug, title, blurb, _rel in items
        )
        body = (
            '<p class="kicker">Section</p>\n'
            "<h1>%s</h1>\n"
            '<p class="lede">%s</p>\n'
            '<p class="disclosure">I may earn a commission if you buy through an affiliate link, at no extra cost to you. '
            "Until affiliate programs are approved, product links go to ordinary store pages. See the "
            '<a href="../disclosure.html">disclosure</a>.</p>\n'
            '<ul class="article-list">\n%s\n</ul>'
        ) % (htmlmod.escape(heading), htmlmod.escape(intro), lis)
        rel = "%s/index.html" % section
        (ROOT / rel).write_text(page(rel, heading, body, section, measure=True), encoding="utf-8")


def build_home():
    body = (
        '<div class="hero">\n'
        "  <h1>" + SITE + "</h1>\n"
        '  <p class="lede">Short, plain buying guides and book lists, written from Villa Hills, Kentucky. I am Max. '
        "I root for Kentucky, the Bengals, and the Reds; I drive Teslas in this winter weather; and I read more true crime "
        'than I probably should. If a link later becomes an affiliate link, I may earn a commission — details are on the '
        '<a href="disclosure.html">disclosure</a> page.</p>\n'
        "</div>\n\n"
        '<p class="featured-label">Featured</p>\n'
        '<div class="grid featured">\n'
        '  <a class="card" href="sports/gift-guide-uk-bengals-reds.html">\n'
        '    <div class="kicker">Sports · UK first</div>\n'
        "    <h2>A gift guide for UK, Bengals, and Reds fans</h2>\n"
        "    <p>Start with Kentucky, then Cincinnati. Hats and shirts if you do not know a jersey size.</p>\n"
        "  </a>\n"
        '  <a class="card" href="sports/official-vs-bootleg.html">\n'
        '    <div class="kicker">Sports</div>\n'
        "    <h2>Official vs. bootleg fan gear</h2>\n"
        "    <p>What to check so a Wildcats, Bengals, or Reds gift is actually licensed.</p>\n"
        "  </a>\n"
        '  <a class="card" href="books/true-crime-shortlist.html">\n'
        '    <div class="kicker">Books · True crime</div>\n'
        "    <h2>A true crime shortlist</h2>\n"
        "    <p>Sober books, and the library as a fair first stop. No jokey tone.</p>\n"
        "  </a>\n"
        '  <a class="card" href="tesla/kentucky-winter-tesla-kit.html">\n'
        '    <div class="kicker">Tesla · Kentucky / Ohio</div>\n'
        "    <h2>A practical winter kit for a Tesla</h2>\n"
        "    <p>The unglamorous kit that actually gets used in this weather.</p>\n"
        "  </a>\n"
        "</div>\n\n"
        '<p class="note">More UK, Bengals, and Reds gear — including '
        '<a href="sports/hats-and-casual-gear.html">hats and casual wear</a> — is in the '
        '<a href="sports/index.html">Sports</a> section.</p>\n\n'
        '<section class="more-section">\n'
        "  <h2>More shortlists</h2>\n"
        '  <p class="note">These stay on the site and will get their own posts over the launch weeks. They are just not the front of the line.</p>\n'
        '  <div class="grid">\n'
        '    <a class="card" href="sports/index.html"><h3>Sports</h3><p>UK Wildcats, Bengals, and Reds licensed gear.</p></a>\n'
        '    <a class="card" href="tesla/index.html"><h3>Tesla</h3><p>Mats, a home charger, organizers, and wheel care — plus the winter kit above.</p></a>\n'
        '    <a class="card" href="books/index.html"><h3>Books</h3><p>True crime first, then 2026 gifts, mysteries, history, and the other shelves.</p></a>\n'
        '    <a class="card" href="dogs/index.html"><h3>Dogs</h3><p>Shedding gear, beds, crates, and harnesses for large dogs.</p></a>\n'
        '    <a class="card" href="christian/index.html"><h3>Christian</h3><p>Choosing a Bible, books worth giving, and gifts that are not junk.</p></a>\n'
        '    <a class="card" href="tools/index.html"><h3>Tools</h3><p>NordVPN and Hostinger, without the scare tactics. Shopify can wait.</p></a>\n'
        "  </div>\n"
        "</section>\n"
    )
    (ROOT / "index.html").write_text(page("index.html", "Home", body, "home", measure=False), encoding="utf-8")


def build_about():
    body = (
        "<h1>About " + SITE + "</h1>\n"
        '<p class="disclosure">I may earn a commission if you buy through an affiliate link, at no extra cost to you. '
        "Until programs are approved, product links go to ordinary store pages. See the "
        '<a href="disclosure.html">disclosure</a>.</p>\n'
        "<p>I’m Max. I live in Villa Hills, Kentucky, just south of Cincinnati. This site is a set of short, plain lists — "
        "things I would actually tell a neighbor to check before they buy, and books I would put on a table and let someone pick up.</p>\n"
        "<p>I drive a Tesla Model 3 Performance and a 2026 Model S Plaid, so the Tesla pages are written for people who own "
        "the cars, not for people who want a rental-host kit. I will not recommend car-sharing, Turo, or short-term rental "
        "tools here. That would compete with work I already do.</p>\n"
        "<p>We have two large dogs, both around two and a half years old: Red, a ~55 lb female, and Snowball, a ~65 lb white male. "
        "One of them sheds a lot. The dog articles start from that household, not from a show-ring catalog.</p>\n"
        "<p>I follow Kentucky Wildcats basketball first, and I also follow the Cincinnati Bengals and the Cincinnati Reds. "
        "The sports pages start with official UK gear and then the two Cincinnati teams. I like true crime as a reader — "
        "the book list in that genre is written in a sober voice, and the library is a fair first stop.</p>\n"
        "<p>Where it is relevant, I prefer to point people toward conservative, Christian-owned, or plainly run businesses I can "
        "stand behind. I will not pretend a product is something it isn’t, and I will not invent a price, a rating, or a review I did not see.</p>\n"
        "<p>This is not investment advice, and it is not a bourbon or whiskey guide. If those subjects ever appear later, it will be after I decide they belong here.</p>\n"
        '<p>You can find me on X at <a href="https://x.com/Maxbps8">@Maxbps8</a>.</p>\n'
    )
    (ROOT / "about.html").write_text(page("about.html", "About", body, "about", measure=True), encoding="utf-8")


def build_disclosure():
    body = (
        "<h1>Affiliate disclosure</h1>\n"
        "<p>I want this to be obvious, not buried.</p>\n"
        "<p><strong>" + SITE + " uses affiliate links, or will use them once programs are approved.</strong> "
        "That means if you click a link and buy something, I may earn a commission. It does not change the price you pay. "
        "Until those programs are approved, links on this site go to ordinary official or retailer product pages and are not "
        "tracking links. When a tracking link is swapped in, this same disclosure still applies.</p>\n"
        "<p>I also put a short disclosure near the top of each article that includes product links. If a post on X points at one "
        "of those articles or includes a product link, it will say so with “#ad” or the words “affiliate link.”</p>\n"
        "<h2>Amazon Associates statement</h2>\n"
        "<p><em>Placeholder — to be used once an Amazon Associates account is approved. This site is not yet claiming participation.</em></p>\n"
        "<blockquote>\n"
        "<p>" + SITE + " is a participant in the Amazon Services LLC Associates Program, an affiliate advertising program "
        "designed to provide a means for sites to earn advertising fees by advertising and linking to Amazon.com.</p>\n"
        "</blockquote>\n"
        "<p>Similar arrangements may apply with Bookshop.org, Audible, Libro.fm, Christianbook, Fanatics, Lids, Rally House, "
        "NordVPN, Hostinger, Shopify, and other retailers named in the setup notes. Public pages always carry this disclosure.</p>\n"
        "<h2>What I will not do</h2>\n"
        "<ul>\n"
        "<li>I will not invent a price, a star rating, or a review quote.</li>\n"
        "<li>I will not recommend car-sharing, Turo, short-term rental platforms, or other products that compete with businesses I already run.</li>\n"
        "<li>Nothing on this site is investment advice.</li>\n"
        "</ul>\n"
        '<p>Questions: <a href="about.html">About</a>, or X at <a href="https://x.com/Maxbps8">@Maxbps8</a>.</p>\n'
    )
    (ROOT / "disclosure.html").write_text(page("disclosure.html", "Disclosure", body, "about", measure=True), encoding="utf-8")


def build_privacy():
    body = (
        "<h1>Privacy</h1>\n"
        "<p>" + SITE + " is a static website. I do not ask you to create an account, and I do not run a comment form or a checkout on this site.</p>\n"
        "<p>The site is meant to be hosted on GitHub Pages. GitHub may collect standard server logs (such as IP address, browser type, "
        "and the pages requested) as described in GitHub’s own privacy policy. I do not currently add a separate analytics script, "
        "advertising pixel, or tracking cookie of my own. If that changes, I will update this page.</p>\n"
        "<p>Links to Amazon, Bookshop.org, Fanatics, NordVPN, Hostinger, and other third-party sites go to those companies’ websites. "
        "Once affiliate programs are approved, some of those links will include tracking codes so a commission can be credited. "
        "Those retailers have their own privacy policies and may set cookies when you visit them. I do not control that.</p>\n"
        "<p>If you email me or message me on X, I will use that conversation to reply to you and not for a mailing list, unless you ask to be added to one.</p>\n"
        "<p>This page was written November 27, 2026 (America/New_York).</p>\n"
    )
    (ROOT / "privacy.html").write_text(page("privacy.html", "Privacy", body, "about", measure=True), encoding="utf-8")


def build_favicon():
    svg = (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">\n'
        '  <rect width="64" height="64" fill="#7a2e22"/>\n'
        '  <text x="32" y="46" text-anchor="middle" font-size="36" font-family="Georgia, serif" fill="#fffaf2">M</text>\n'
        "</svg>\n"
    )
    (ROOT / "favicon.svg").write_text(svg, encoding="utf-8")


def build_nojekyll():
    (ROOT / ".nojekyll").write_text("", encoding="utf-8")
    (ROOT / ".gitignore").write_text(".DS_Store\n__pycache__/\n*.pyc\n.idea/\n", encoding="utf-8")


def main():
    for d in ["tesla", "dogs", "sports", "books", "christian", "tools", "css"]:
        (ROOT / d).mkdir(parents=True, exist_ok=True)
    by_cat = build_articles()
    build_category_pages(by_cat)
    build_home()
    build_about()
    build_disclosure()
    build_privacy()
    build_favicon()
    build_nojekyll()
    leftover = []
    for path in ROOT.rglob("*.html"):
        t = path.read_text(encoding="utf-8")
        if "AFFILIATE_LINK" in t or "{{AFF" in t or "Plain Picks" in t:
            leftover.append(str(path))
    n_html = len(list(ROOT.rglob("*.html")))
    print("Wrote %d HTML files, %d unique source links." % (n_html, len(USED_SOURCES)))
    if leftover:
        print("LEFTOVER PLACEHOLDERS OR OLD NAME:", leftover)
        raise SystemExit(1)
    print("OK")


if __name__ == "__main__":
    main()
