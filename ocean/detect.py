"""Tech-stack detection for the jellyfish field: pull recognizable
languages and tools out of repo languages + manifest files."""

import json
import re

# Recognized dependency names, grouped loosely so the list stays readable.
DEP_MAP = {
    "ai": {
        "torch", "pytorch", "tensorflow", "keras", "scikit-learn", "sklearn",
        "transformers", "langchain", "openai", "anthropic", "xgboost",
        "lightgbm", "huggingface-hub", "sentence-transformers", "llama-index",
        "onnxruntime", "ultralytics", "opencv-python", "spacy", "nltk",
    },
    "data": {
        "pandas", "numpy", "matplotlib", "seaborn", "plotly", "polars",
        "duckdb", "pyspark", "airflow", "dbt-core", "sqlalchemy", "psycopg2",
        "pymongo", "redis", "elasticsearch", "kafka-python", "scipy",
    },
    "frontend": {
        "react", "react-dom", "next", "vue", "svelte", "angular", "tailwindcss",
        "styled-components", "vite", "three", "framer-motion", "bootstrap",
        "sass", "webpack", "chart.js", "d3",
    },
    "js": {
        "express", "fastify", "koa", "nestjs", "axios", "node-fetch",
        "socket.io", "lodash", "jest", "mocha", "eslint", "prisma", "mongoose",
    },
    "python": {
        "flask", "django", "fastapi", "uvicorn", "gunicorn", "requests",
        "httpx", "pydantic", "celery", "pytest", "jinja2", "beautifulsoup4",
        "aiohttp", "streamlit", "gradio",
    },
    "cli": {
        "click", "typer", "argparse", "rich", "textual", "commander", "yargs",
        "inquirer", "chalk", "ora", "fire", "docopt",
    },
    "devops": {
        "docker", "kubernetes", "terraform", "ansible", "boto3", "awscli",
        "google-cloud", "azure", "pulumi", "helm", "prometheus-client",
        "grafana", "nginx", "supervisor", "paramiko", "fabric",
    },
    "mobile": {
        "react-native", "expo", "flutter", "ionic", "capacitor", "kivy",
        "@react-navigation/native",
    },
    "docs": {
        "mkdocs", "sphinx", "docusaurus", "vuepress", "jsdoc", "pdoc",
    },
}

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


def detected_techs(languages: dict[str, int], deps: set[str]) -> tuple[list[str], list[str]]:
    """(languages, tools) lists for the jellyfish field.

    Languages ordered by byte count; tools are recognized dependency names.
    """
    langs = [l for l, _ in sorted(languages.items(), key=lambda kv: -kv[1])
             if l not in ("Markdown", "TeX")]
    known = set().union(*DEP_MAP.values())
    tools = sorted(d for d in deps if d in known)
    return langs, tools
