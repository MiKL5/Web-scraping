from pathlib import Path

def csv_name(json_name: str) -> str:
    """
    Génère le nom du fichier CSV à partir du nom du fichier JSON.
    """
    try:
        p = Path(json_name)
        return str(p.with_suffix(".csv"))
    except Exception:
        return (json_name.rsplit(".", 1)[0] if "." in json_name else json_name) + ".csv"
