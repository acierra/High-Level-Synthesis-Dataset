import os, requests, pandas as pd

# все упоминания GNWSIS в коде на GitHub
SEARCH_TERMS = [
    "GNWSIS",
    "GNWSIS.csv",
    "GNΩSIS"
]

def gh_headers():
    h = {"Accept": "application/vnd.github+json"}
    token = os.getenv("GITHUB_TOKEN")
    if token:
        h["Authorization"] = f"Bearer {token}"
    return h

def search_code(q, per_page=50, max_pages=2):
    url = "https://api.github.com/search/code"
    rows = []
    for page in range(1, max_pages + 1):
        r = requests.get(url, headers=gh_headers(),
                         params={"q": q, "per_page": per_page, "page": page},
                         timeout=30)
        r.raise_for_status()
        data = r.json()
        items = data.get("items", [])
        for it in items:
            repo = it.get("repository", {})
            rows.append({
                "repo_full_name": repo.get("full_name"),
                "repo_html_url": repo.get("html_url"),
                "repo_description": repo.get("description"),
                "repo_language": repo.get("language"),
                "repo_stars": repo.get("stargazers_count"),
                "repo_forks": repo.get("forks_count"),
                "repo_updated_at": repo.get("updated_at"),
                "file_path": it.get("path"),
                "file_html_url": it.get("html_url"),
                "search_query": q
            })
        if len(items) < per_page:
            break
    return pd.DataFrame(rows)

def enrich(df):
    if df.empty:
        return df
    df = df.drop_duplicates(subset=["repo_full_name", "file_path"])
    for col in ["repo_stars", "repo_forks"]:
        df[col] = pd.to_numeric(df[col], errors="coerce").astype("Int64")
    if "repo_updated_at" in df.columns:
        df["repo_updated_at"] = pd.to_datetime(df["repo_updated_at"], errors="coerce", utc=True)
    return df.reset_index(drop=True)

def main():
    frames = []
    for term in SEARCH_TERMS:
        print(f"Searching for: {term}")
        frames.append(search_code(term))
    df = pd.concat(frames, ignore_index=True) if frames else pd.DataFrame()
    df = enrich(df)
    cols = [
        "repo_full_name","repo_stars","repo_forks","repo_language","repo_updated_at",
        "repo_html_url","repo_description","file_path","file_html_url","search_query"
    ]
    df = df[[c for c in cols if c in df.columns]]
    print(df.head(10))

if __name__ == "__main__":
    main()
