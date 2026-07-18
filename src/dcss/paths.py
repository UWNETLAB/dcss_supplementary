from pyprojroot import here

try:
    # pyprojroot >= 0.3 finds the project root (.git, pyproject.toml, ...)
    # automatically and no longer accepts project_files.
    root = here()
except TypeError:  # pragma: no cover - pyprojroot < 0.3
    root = here(project_files=[".git"])

british_hansards_path = root / "data" / "british_hansards"
vdem_path = root / "data" / "vdem"
canadian_hansards_path = root / "data" / "canadian_hansards" / "lipad"
vdem_combined_path = root / "data" / "vdem_internet_freedom_combined"
enron_path = root / "data" / "enron"
russian_troll_tweets_path = root / "data" / "russian-troll-tweets"
internet_freedom_path = root / "data" / "freedom_house"
sociopatterns_path = root / "data" / "SocioPatterns"
copenhagen_networks_path = root / "data" / "copenhagen_networks_study"
election_path = root / "data" / "2020_election"
