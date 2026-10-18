import tempfile

def write_report(data: str) -> str:
    # VULN: race-prone mktemp
    path = tempfile.mktemp()
    with open(path, "w") as fh:
        fh.write(data)
    return path
