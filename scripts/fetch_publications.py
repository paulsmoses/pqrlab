#!/usr/bin/env python3
"""
Fetch Dr. Paul Moses's publications from ORCID and Semantic Scholar, merge and
de-duplicate them, and write assets/publications.json for the Publications page.

Runs with only the Python standard library (no pip installs), so it works in a
GitHub Actions runner as-is. See .github/workflows/update-publications.yml.
"""
import json, re, ssl, time, urllib.request, urllib.error, urllib.parse, pathlib

ORCID_ID = "0000-0002-0438-7527"
S2_AUTHOR_ID = "2899496"            # Semantic Scholar author: P. Moses
OUT = pathlib.Path(__file__).resolve().parent.parent / "assets" / "publications.json"

CTX = ssl.create_default_context()
UA = {"User-Agent": "pqr-lab-site/1.0 (publications updater)"}


def get(url, headers=None, tries=4):
    h = dict(UA)
    if headers:
        h.update(headers)
    last = None
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers=h)
            with urllib.request.urlopen(req, timeout=40, context=CTX) as r:
                return json.load(r)
        except urllib.error.HTTPError as e:
            last = e
            # 429 = rate limited (common on Semantic Scholar's free tier): back off
            if e.code in (429, 500, 502, 503):
                time.sleep(3 * (i + 1))
                continue
            raise
        except Exception as e:            # network hiccup: retry
            last = e
            time.sleep(2 * (i + 1))
    raise last


def norm(title):
    return re.sub(r"[^a-z0-9]", "", (title or "").lower())


def year_of(pub):
    return pub.get("year") or 0


# ---------- Semantic Scholar (rich: authors + venue) ----------
def from_semantic_scholar():
    out = []
    url = (f"https://api.semanticscholar.org/graph/v1/author/{S2_AUTHOR_ID}/papers"
           f"?fields=title,year,venue,externalIds,authors&limit=500")
    try:
        data = get(url).get("data", [])
    except Exception as e:
        print("Semantic Scholar fetch failed:", e)
        return out
    for p in data:
        title = (p.get("title") or "").strip()
        if not title:
            continue
        authors = ", ".join(a.get("name", "") for a in (p.get("authors") or []) if a.get("name"))
        doi = (p.get("externalIds") or {}).get("DOI")
        out.append({
            "title": title,
            "year": p.get("year") or 0,
            "venue": (p.get("venue") or "").strip(),
            "authors": authors,
            "doi": doi,
            "url": f"https://doi.org/{doi}" if doi else f"https://www.semanticscholar.org/paper/{p.get('paperId')}",
            "source": "semantic-scholar",
        })
    return out


# ---------- ORCID (authoritative; catches ones S2 misses) ----------
def from_orcid():
    out = []
    url = f"https://pub.orcid.org/v3.0/{ORCID_ID}/works"
    try:
        groups = get(url, headers={"Accept": "application/json"}).get("group", [])
    except Exception as e:
        print("ORCID fetch failed:", e)
        return out
    for g in groups:
        s = (g.get("work-summary") or [{}])[0]
        title = (((s.get("title") or {}).get("title") or {}).get("value") or "").strip()
        if not title:
            continue
        year = (((s.get("publication-date") or {}) or {}).get("year") or {})
        year = int(year.get("value")) if year and year.get("value") else 0
        venue = (s.get("journal-title") or {}).get("value") or ""
        doi = None
        for eid in ((s.get("external-ids") or {}).get("external-id") or []):
            if (eid.get("external-id-type") or "").lower() == "doi":
                doi = eid.get("external-id-value")
                break
        url_val = ((s.get("url") or {}) or {}).get("value")
        out.append({
            "title": title,
            "year": year,
            "venue": venue.strip(),
            "authors": "",
            "doi": doi,
            "url": (f"https://doi.org/{doi}" if doi else url_val) or
                   f"https://scholar.google.com/scholar?q={urllib.parse.quote(title)}",
            "source": "orcid",
        })
    return out


def merge(*lists):
    merged = []
    by_doi = {}
    by_title = {}

    def find(pub):
        doi = (pub.get("doi") or "").lower()
        if doi and doi in by_doi:
            return by_doi[doi]
        return by_title.get(norm(pub["title"]))

    for lst in lists:
        for pub in lst:
            cur = find(pub)
            if cur is None:
                cur = dict(pub)
                merged.append(cur)
            else:
                # merge: prefer the record with more display info
                if not cur.get("authors") and pub.get("authors"):
                    cur["authors"] = pub["authors"]
                if not cur.get("venue") and pub.get("venue"):
                    cur["venue"] = pub["venue"]
                if not cur.get("doi") and pub.get("doi"):
                    cur["doi"] = pub["doi"]
                    cur["url"] = pub["url"]
                if cur.get("source") != pub.get("source"):
                    cur["source"] = "both"
                cur["year"] = max(cur.get("year") or 0, pub.get("year") or 0)
            # register keys so later entries dedupe against this record
            if cur.get("doi"):
                by_doi[cur["doi"].lower()] = cur
            by_title[norm(cur["title"])] = cur

    merged.sort(key=year_of, reverse=True)
    return merged


def main():
    s2 = from_semantic_scholar()
    orcid = from_orcid()
    print(f"Semantic Scholar: {len(s2)}   ORCID: {len(orcid)}")
    merged = merge(s2, orcid)
    print(f"Merged unique: {len(merged)}")
    payload = {
        "updated": time.strftime("%Y-%m-%d", time.gmtime()),
        "count": len(merged),
        "sources": {"semantic_scholar": len(s2), "orcid": len(orcid)},
        "publications": merged,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=1, ensure_ascii=False))
    print("Wrote", OUT)


if __name__ == "__main__":
    main()
