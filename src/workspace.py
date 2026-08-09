import json
import logging
from pathlib import Path
from typing import List, Dict, Any
from src.config import DATA_DIR

logger = logging.getLogger("workspace")

DEFAULT_PINS = [
    {"title": "⭐ Playwright Cheat Sheet", "path": "notes/21_CHEAT_SHEETS/cheat-sheet-playwright.md", "type": "doc"},
    {"title": "⭐ ERP Procure-to-Pay (P2P)", "path": "notes/03_ERP_TESTING/03_procure_to_pay_p2p_workflow.md", "type": "doc"},
    {"title": "⭐ RBAC & SOD Testing", "path": "notes/03_ERP_TESTING/08_rbac_security_and_sod_testing.md", "type": "doc"},
    {"title": "⭐ SQL Cheat Sheet", "path": "notes/21_CHEAT_SHEETS/cheat-sheet-sql.md", "type": "doc"},
    {"title": "⭐ API Status Codes", "path": "notes/21_CHEAT_SHEETS/cheat-sheet-http-status-codes.md", "type": "doc"}
]

class WorkspaceManager:
    def __init__(self, pins_file: Path = DATA_DIR / "user_pins.json"):
        self.pins_file = pins_file
        self.pins: List[Dict[str, Any]] = self._load_pins()

    def _load_pins(self) -> List[Dict[str, Any]]:
        if self.pins_file.exists():
            try:
                with open(self.pins_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception as e:
                logger.error(f"Failed to load user pins: {e}")
        return DEFAULT_PINS.copy()

    def _save_pins(self) -> None:
        try:
            with open(self.pins_file, "w", encoding="utf-8") as f:
                json.dump(self.pins, f, indent=2)
        except Exception as e:
            logger.error(f"Failed to save user pins: {e}")

    def add_pin(self, title: str, path: str, item_type: str = "doc") -> bool:
        for pin in self.pins:
            if pin["path"] == path:
                return False
        self.pins.append({"title": title, "path": path, "type": item_type})
        self._save_pins()
        return True

    def remove_pin(self, path: str) -> bool:
        initial = len(self.pins)
        self.pins = [p for p in self.pins if p["path"] != path]
        if len(self.pins) < initial:
            self._save_pins()
            return True
        return False

    def get_pins(self) -> List[Dict[str, Any]]:
        return self.pins
