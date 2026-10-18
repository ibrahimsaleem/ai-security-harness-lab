import pickle
import yaml

def load_session(blob: bytes):
    # VULN: untrusted pickle
    return pickle.loads(blob)

def load_config(text: str):
    # VULN: yaml.load without SafeLoader
    return yaml.load(text, Loader=yaml.Loader)
