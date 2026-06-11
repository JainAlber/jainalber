"""GitHub data collection. Fail-soft: any single repo/API failure degrades
gracefully instead of killing the weekly sync."""

import base64
import datetime as dt
import json
import os
import re
import time
import urllib.parse
from dataclasses import dataclass, field

import requests

from . import detect

API = "https://api.github.com"
USER = "JainAlber"
MANIFESTS = ("package.json", "requirements.txt", "pyproject.toml",
             "Dockerfile", "docker-compose.yml")


@dataclass
class RepoState:
    name: str
    pushed_at: dt.datetime
    commits: int = 0
    languages: dict = field(default_factory=dict)
    deps: set = field(default_factory=set)
    has_docker: bool = False

    @property
    def scores(self) -> dict[str, float]:
        return detect.category_scores(self.languages, self.deps, self.has_docker)


@dataclass
class OceanState:
    repos: list[RepoState] = field(default_factory=list)
    total_commits: int = 0
    streak: int | None = None
    open_prs: int | None = None
    generated: dt.datetime = field(default_factory=lambda: dt.datetime.now(dt.timezone.utc))

    # tech -> days since last activity in any repo containing it
    lang_age: dict = field(default_factory=dict)
    tool_age: dict = field(default_factory=dict)


class Client:
    def __init__(self, token: str | None = None):
        self.s = requests.Session()
        self.s.headers["Accept"] = "application/vnd.github+json"
        self.s.headers["User-Agent"] = "ocean-sync"
        token = token or os.environ.get("GITHUB_TOKEN")
        self.token = token
        if token:
            self.s.headers["Authorization"] = f"Bearer {token}"

    def get(self, url: str, **params) -> requests.Response | None:
        for attempt in range(3):
            try:
                r = self.s.get(url, params=params or None, timeout=30)
            except requests.RequestException:
                time.sleep(2 ** attempt)
                continue
            if r.status_code == 200:
                return r
            if r.status_code in (403, 429) and attempt < 2:
                time.sleep(5 * (attempt + 1))
                continue
            return None
        return None

    def json(self, url: str, **params):
        r = self.get(url, **params)
        return r.json() if r is not None else None


def _commit_count(c: Client, repo: str) -> int:
    """Count commits authored by USER on the default branch via the Link
    header trick: per_page=1, read the last page number."""
    r = c.get(f"{API}/repos/{USER}/{repo}/commits", author=USER, per_page=1)
    if r is None:
        return 0
    link = r.headers.get("Link", "")
    m = re.search(r'[?&]page=(\d+)>; rel="last"', link)
    if m:
        return int(m.group(1))
    return len(r.json())  # 0 or 1, no pagination


def _file_text(c: Client, repo: str, path: str) -> str | None:
    data = c.json(f"{API}/repos/{USER}/{repo}/contents/{urllib.parse.quote(path)}")
    if not isinstance(data, dict) or data.get("encoding") != "base64":
        return None
    try:
        return base64.b64decode(data["content"]).decode("utf-8", errors="replace")
    except (ValueError, KeyError):
        return None


def _scan_repo(c: Client, info: dict) -> RepoState:
    name = info["name"]
    repo = RepoState(
        name=name,
        pushed_at=dt.datetime.fromisoformat(info["pushed_at"].replace("Z", "+00:00")),
    )
    repo.commits = _commit_count(c, name)
    repo.languages = c.json(f"{API}/repos/{USER}/{name}/languages") or {}

    for path in MANIFESTS:
        text = _file_text(c, name, path)
        if text is None:
            continue
        if path == "package.json":
            repo.deps |= detect.deps_from_package_json(text)
        elif path in ("requirements.txt",):
            repo.deps |= detect.deps_from_requirements(text)
        elif path == "pyproject.toml":
            repo.deps |= {d for d in detect.deps_from_requirements(text)
                          if d in set().union(*detect.DEP_MAP.values())}
        else:  # Dockerfile / compose
            repo.has_docker = True
            repo.deps |= detect.deps_from_dockerfile(text)
    return repo


def _streak(c: Client) -> int | None:
    """Current contribution streak from the GraphQL calendar (needs token)."""
    if not c.token:
        return None
    query = """
    query($login: String!) {
      user(login: $login) {
        contributionsCollection {
          contributionCalendar { weeks { contributionDays { date contributionCount } } }
        }
      }
    }"""
    try:
        r = c.s.post(f"{API}/graphql",
                     json={"query": query, "variables": {"login": USER}},
                     timeout=30)
        days = [d for w in r.json()["data"]["user"]["contributionsCollection"]
                ["contributionCalendar"]["weeks"] for d in w["contributionDays"]]
    except (requests.RequestException, KeyError, TypeError):
        return None
    days.sort(key=lambda d: d["date"])
    today = dt.date.today().isoformat()
    streak = 0
    for d in reversed(days):
        if d["date"] > today:
            continue
        if d["contributionCount"] > 0:
            streak += 1
        elif d["date"] == today:
            continue  # today empty doesn't break the streak yet
        else:
            break
    return streak


def fetch_ocean(token: str | None = None) -> OceanState:
    c = Client(token)
    state = OceanState()

    repos_raw = c.json(f"{API}/users/{USER}/repos", per_page=100, sort="pushed") or []
    repos_raw = [r for r in repos_raw if not r.get("fork")]

    now = dt.datetime.now(dt.timezone.utc)
    for info in repos_raw:
        repo = _scan_repo(c, info)
        state.repos.append(repo)
        age = (now - repo.pushed_at).days
        langs, tools = detect.detected_techs(repo.languages, repo.deps)
        for lang in langs:
            state.lang_age[lang] = min(state.lang_age.get(lang, 9999), age)
        for tool in tools:
            state.tool_age[tool] = min(state.tool_age.get(tool, 9999), age)

    state.total_commits = sum(r.commits for r in state.repos)
    state.streak = _streak(c)

    search = c.json(f"{API}/search/issues",
                    q=f"author:{USER} type:pr state:open", per_page=1)
    if isinstance(search, dict):
        state.open_prs = search.get("total_count")

    return state


def load_state(path: str) -> OceanState:
    """Rebuild an OceanState from a saved snapshot (offline re-rendering)."""
    with open(path, encoding="utf-8") as f:
        payload = json.load(f)
    state = OceanState(
        total_commits=payload["total_commits"],
        streak=payload["streak"],
        open_prs=payload["open_prs"],
        generated=dt.datetime.fromisoformat(payload["generated"]),
        lang_age=payload["lang_age"],
        tool_age=payload["tool_age"],
    )
    state.repos = [RepoState(
        name=r["name"],
        pushed_at=dt.datetime.fromisoformat(r["pushed_at"]),
        commits=r["commits"], languages=r["languages"],
        deps=set(r["deps"]), has_docker=r["has_docker"],
    ) for r in payload["repos"]]
    return state


def save_state(state: OceanState, path: str) -> None:
    """Persist a JSON snapshot (debugging / offline rendering)."""
    payload = {
        "generated": state.generated.isoformat(),
        "total_commits": state.total_commits,
        "streak": state.streak,
        "open_prs": state.open_prs,
        "lang_age": state.lang_age,
        "tool_age": state.tool_age,
        "repos": [{
            "name": r.name, "pushed_at": r.pushed_at.isoformat(),
            "commits": r.commits, "languages": r.languages,
            "deps": sorted(r.deps), "has_docker": r.has_docker,
        } for r in state.repos],
    }
    with open(path, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)
