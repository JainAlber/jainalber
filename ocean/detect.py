"""Tech-stack detection: turn repo languages + manifest files into
category scores that species.resolve_species() can consume."""

import json
import re

from . import species as sp

# GitHub linguist language -> category
LANG_MAP = {
    "Python": sp.PYTHON,
    "JavaScript": sp.JS,
    "TypeScript": sp.JS,
    "Jupyter Notebook": sp.AI,
    "HTML": sp.FRONTEND,
    "CSS": sp.FRONTEND,
    "SCSS": sp.FRONTEND,
    "Vue": sp.FRONTEND,
    "Svelte": sp.FRONTEND,
    "Shell": sp.CLI,
    "PowerShell": sp.CLI,
    "Go": sp.CLI,
    "Rust": sp.CLI,
    "Dockerfile": sp.DEVOPS,
    "HCL": sp.DEVOPS,
    "Makefile": sp.DEVOPS,
    "Kotlin": sp.MOBILE,
    "Swift": sp.MOBILE,
    "Dart": sp.MOBILE,
    "Objective-C": sp.MOBILE,
    "R": sp.DATA,
    "TSQL": sp.DATA,
    "PLpgSQL": sp.DATA,
    "Markdown": sp.DOCS,
    "TeX": sp.DOCS,
}

# Dependency name (lowercased, matched on token) -> category
DEP_MAP = {
    sp.AI: {
        "torch", "pytorch", "tensorflow", "keras", "scikit-learn", "sklearn",
        "transformers", "langchain", "openai", "anthropic", "xgboost",
        "lightgbm", "huggingface-hub", "sentence-transformers", "llama-index",
        "onnxruntime", "ultralytics", "opencv-python", "spacy", "nltk",
    },
    sp.DATA: {
        "pandas", "numpy", "matplotlib", "seaborn", "plotly", "polars",
        "duckdb", "pyspark", "airflow", "dbt-core", "sqlalchemy", "psycopg2",
        "pymongo", "redis", "elasticsearch", "kafka-python", "scipy",
    },
    sp.FRONTEND: {
        "react", "react-dom", "next", "vue", "svelte", "angular", "tailwindcss",
        "styled-components", "vite", "three", "framer-motion", "bootstrap",
        "sass", "webpack", "chart.js", "d3",
    },
    sp.JS: {
        "express", "fastify", "koa", "nestjs", "axios", "node-fetch",
        "socket.io", "lodash", "jest", "mocha", "eslint", "prisma", "mongoose",
    },
    sp.PYTHON: {
        "flask", "django", "fastapi", "uvicorn", "gunicorn", "requests",
        "httpx", "pydantic", "celery", "pytest", "jinja2", "beautifulsoup4",
        "aiohttp", "streamlit", "gradio",
    },
    sp.CLI: {
        "click", "typer", "argparse", "rich", "textual", "commander", "yargs",
        "inquirer", "chalk", "ora", "fire", "docopt",
    },
    sp.DEVOPS: {
        "docker", "kubernetes", "terraform", "ansible", "boto3", "awscli",
        "google-cloud", "azure", "pulumi", "helm", "prometheus-client",
        "grafana", "nginx", "supervisor", "paramiko", "fabric",
    },
    sp.MOBILE: {
        "react-native", "expo", "flutter", "ionic", "capacitor", "kivy",
        "@react-navigation/native",
    },
    sp.DOCS: {
        "mkdocs", "sphinx", "docusaurus", "vuepress", "jsdoc", "pdoc",
    },
}

LANG_WEIGHT = 0.6   # share of score from language bytes
DEP_WEIGHT = 0.4    # share of score from dependency hits
DEVOPS_FILE_BONUS = 0.18  # Dockerfile / compose / workflows presence

_REQ_LINE = re.compile(r"^\s*([A-Za-z0-9_.@/\[\]-]+)")


def deps_from_package_json(text: str) -> set[str]:
    try:
        data = json.loads(text)
    except (json.JSONDecodeError, TypeError):
        return set()
    deps: set[str] = set()
    for key in ("dependencies", "devDependencies", "peerDependencies"):
        deps |= {d.lower() for d in (data.get(key) or {})}
    return deps


def deps_from_requirements(text: str) -> set[str]:
    deps = set()
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith(("#", "-")):
            continue
        m = _REQ_LINE.match(line)
        if m:
            deps.add(m.group(1).split("[")[0].lower())
    return deps


def deps_from_dockerfile(text: str) -> set[str]:
    """Pull obvious tool names out of FROM / RUN lines."""
    hits = set()
    for tool in ("nginx", "redis", "postgres", "node", "python", "terraform",
                 "kubectl", "helm", "prometheus", "grafana"):
        if re.search(rf"\b{tool}\b", text, re.IGNORECASE):
            hits.add(tool)
    return hits


def category_scores(languages: dict[str, int], deps: set[str],
                    has_docker: bool = False) -> dict[str, float]:
    """Blend language byte shares and dependency hits into category scores."""
    scores: dict[str, float] = {}

    total_bytes = sum(b for lang, b in languages.items() if lang in LANG_MAP)
    if total_bytes > 0:
        for lang, b in languages.items():
            cat = LANG_MAP.get(lang)
            if cat:
                scores[cat] = scores.get(cat, 0.0) + LANG_WEIGHT * b / total_bytes

    dep_hits: dict[str, int] = {}
    for dep in deps:
        for cat, names in DEP_MAP.items():
            if dep in names:
                dep_hits[cat] = dep_hits.get(cat, 0) + 1
    total_hits = sum(dep_hits.values())
    if total_hits > 0:
        for cat, n in dep_hits.items():
            scores[cat] = scores.get(cat, 0.0) + DEP_WEIGHT * n / total_hits

    if has_docker:
        scores[sp.DEVOPS] = scores.get(sp.DEVOPS, 0.0) + DEVOPS_FILE_BONUS

    return scores


def detected_techs(languages: dict[str, int], deps: set[str]) -> tuple[list[str], list[str]]:
    """(languages, tools) lists for the jellyfish field.

    Languages ordered by byte count; tools are recognized dependency names.
    """
    langs = [l for l, _ in sorted(languages.items(), key=lambda kv: -kv[1])
             if l not in ("Markdown", "TeX")]
    known = set().union(*DEP_MAP.values())
    tools = sorted(d for d in deps if d in known)
    return langs, tools
