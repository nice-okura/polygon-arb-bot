from web3 import Web3
import yaml
from pathlib import Path

_cfg_path = Path(__file__).resolve().parents[2] / "config" / "settings.yaml"
with open(_cfg_path, "r", encoding="utf-8") as f:
    _CFG = yaml.safe_load(f)

def get_web3():
    """Singleton Web3 provider."""
    return Web3(Web3.HTTPProvider(_CFG["polygon_rpc"]))
