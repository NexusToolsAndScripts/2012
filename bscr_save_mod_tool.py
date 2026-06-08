#!/usr/bin/env python3
"""
this is ai slop, for some other random ass game <3
"""

from __future__ import annotations

import hashlib
import json
import os
import shutil
import sys
import time
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, ttk
from typing import Any, Dict

SECRET_KEY = b"MySuperSecretKey2026!@#"
DEFAULT_SAVE_NAME = "bscr_save.dat"

RESOURCE_FIELDS = [
    ("money", "Money"),
    ("multiplier", "Multiplier"),
    ("rebirth_points", "Rebirth Points"),
    ("ultra_rebirth_points", "Ultra Rebirth Points"),
    ("mega_rebirth_points", "Mega Rebirth Points"),
    ("prestige_points", "Prestige Points"),
    ("ultra_prestige_points", "Ultra Prestige Points"),
    ("mega_prestige_points", "Mega Prestige Points"),
    ("evolution_points", "Evolution Points"),
    ("transcend_points", "Transcend Points"),
    ("ascension_points", "Ascension Points"),
]

ACHIEVEMENTS = {
    "first_money": "First Money",
    "first_multiplier": "First Multiplier",
    "first_rebirth": "First Rebirth",
    "money_1000": "Thousandaire",
    "multiplier_10": "Multiplier Master",
    "pay_respect": "Pay Respect (Secret)",
    "secret_clicker": "Secret Clicker (Secret)",
}

DEFAULT_SAVE: Dict[str, Any] = {
    "money": 0,
    "money_is_int": True,
    "multiplier": 1,
    "rebirth_points": 0,
    "ultra_rebirth_points": 0,
    "mega_rebirth_points": 0,
    "prestige_points": 0,
    "ultra_prestige_points": 0,
    "mega_prestige_points": 0,
    "evolution_points": 0,
    "transcend_points": 0,
    "ascension_points": 0,
    "achievements": {achievement_id: False for achievement_id in ACHIEVEMENTS},
}

PRESETS = {
    "Starter boost": {
        "money": 1_000_000,
        "multiplier": 100,
        "rebirth_points": 10,
    },
    "Mid game": {
        "money": 10**12,
        "multiplier": 10_000,
        "rebirth_points": 1_000,
        "ultra_rebirth_points": 100,
        "mega_rebirth_points": 10,
    },
    "End game": {
        "money": 10**30,
        "multiplier": 10**9,
        "rebirth_points": 10**7,
        "ultra_rebirth_points": 10**6,
        "mega_rebirth_points": 10**5,
        "prestige_points": 10**4,
        "ultra_prestige_points": 1_000,
        "mega_prestige_points": 500,
        "evolution_points": 100,
        "transcend_points": 25,
        "ascension_points": 5,
    },
    "Max-ish sandbox": {
        "money": 10**100,
        "multiplier": 10**50,
        "rebirth_points": 10**30,
        "ultra_rebirth_points": 10**25,
        "mega_rebirth_points": 10**20,
        "prestige_points": 10**15,
        "ultra_prestige_points": 10**12,
        "mega_prestige_points": 10**9,
        "evolution_points": 10**6,
        "transcend_points": 10**4,
        "ascension_points": 1_000,
    },
}


def xor_encrypt(data: bytes, key: bytes) -> bytes:
    return bytes(data[i] ^ key[i % len(key)] for i in range(len(data)))


def get_hash(data: bytes) -> bytes:
    return hashlib.sha256(data + SECRET_KEY).digest()


def read_save(path: Path) -> Dict[str, Any]:
    content = path.read_bytes()
    if len(content) < 32:
        raise ValueError("Save file is too short to be valid.")

    stored_hash = content[:32]
    encrypted_data = content[32:]
    decrypted_json = xor_encrypt(encrypted_data, SECRET_KEY)

    if get_hash(decrypted_json) != stored_hash:
        raise ValueError("Hash mismatch. Wrong file, damaged file, or unsupported game version.")

    data = json.loads(decrypted_json.decode("utf-8"))
    merged = json.loads(json.dumps(DEFAULT_SAVE))
    merged.update(data)
    merged["achievements"] = {**DEFAULT_SAVE["achievements"], **data.get("achievements", {})}
    return merged


def write_save(path: Path, data: Dict[str, Any], make_backup: bool = True) -> Path | None:
    path.parent.mkdir(parents=True, exist_ok=True)

    backup_path = None
    if make_backup and path.exists():
        stamp = time.strftime("%Y%m%d-%H%M%S")
        backup_path = path.with_name(f"{path.name}.backup-{stamp}")
        shutil.copy2(path, backup_path)

    # Match the original game's behavior: money_is_int tracks the saved money type.
    try:
        money_value = data.get("money", 0)
        data["money_is_int"] = isinstance(money_value, int) and not isinstance(money_value, bool)
    except Exception:
        data["money_is_int"] = False

    json_bytes = json.dumps(data, separators=(",", ":")).encode("utf-8")
    path.write_bytes(get_hash(json_bytes) + xor_encrypt(json_bytes, SECRET_KEY))
    return backup_path


def parse_number(text: str) -> int | float:
    text = text.strip().replace(",", "")
    if not text:
        return 0
    value = float(text) if any(ch in text.lower() for ch in [".", "e"]) else int(text)
    if isinstance(value, float) and value.is_integer():
        return int(value)
    return value


class SaveModTool(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("BSCR Save Mod Tool")
        self.geometry("760x720")
        self.minsize(680, 620)

        self.save_path = tk.StringVar(value=str(Path.cwd() / DEFAULT_SAVE_NAME))
        self.status = tk.StringVar(value="Choose or load a save file.")
        self.entries: Dict[str, tk.StringVar] = {}
        self.achievement_vars: Dict[str, tk.BooleanVar] = {}
        self.data: Dict[str, Any] = json.loads(json.dumps(DEFAULT_SAVE))

        self._build_ui()

    def _build_ui(self) -> None:
        root = ttk.Frame(self, padding=12)
        root.pack(fill="both", expand=True)

        file_box = ttk.LabelFrame(root, text="Save file")
        file_box.pack(fill="x", pady=(0, 10))

        path_entry = ttk.Entry(file_box, textvariable=self.save_path)
        path_entry.pack(side="left", fill="x", expand=True, padx=(8, 6), pady=8)
        ttk.Button(file_box, text="Browse", command=self.browse).pack(side="left", padx=4)
        ttk.Button(file_box, text="Load", command=self.load).pack(side="left", padx=4)
        ttk.Button(file_box, text="Create New", command=self.create_new).pack(side="left", padx=(4, 8))

        notebook = ttk.Notebook(root)
        notebook.pack(fill="both", expand=True)

        stats_tab = ttk.Frame(notebook, padding=10)
        ach_tab = ttk.Frame(notebook, padding=10)
        presets_tab = ttk.Frame(notebook, padding=10)
        raw_tab = ttk.Frame(notebook, padding=10)

        notebook.add(stats_tab, text="Stats")
        notebook.add(ach_tab, text="Achievements")
        notebook.add(presets_tab, text="Presets")
        notebook.add(raw_tab, text="Raw JSON")

        self._build_stats_tab(stats_tab)
        self._build_achievements_tab(ach_tab)
        self._build_presets_tab(presets_tab)
        self._build_raw_tab(raw_tab)

        bottom = ttk.Frame(root)
        bottom.pack(fill="x", pady=(10, 0))
        ttk.Button(bottom, text="Save Modded File", command=self.save).pack(side="right")
        ttk.Button(bottom, text="Reload", command=self.load).pack(side="right", padx=8)
        ttk.Label(bottom, textvariable=self.status).pack(side="left", fill="x", expand=True)

    def _build_stats_tab(self, parent: ttk.Frame) -> None:
        info = ttk.Label(
            parent,
            text="Edit values, then click Save Modded File. Big integers are okay, including 1e100.",
        )
        info.grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 10))

        for row, (key, label) in enumerate(RESOURCE_FIELDS, start=1):
            ttk.Label(parent, text=label).grid(row=row, column=0, sticky="w", padx=(0, 8), pady=4)
            var = tk.StringVar(value=str(DEFAULT_SAVE[key]))
            self.entries[key] = var
            ttk.Entry(parent, textvariable=var).grid(row=row, column=1, sticky="ew", pady=4)

        parent.columnconfigure(1, weight=1)

    def _build_achievements_tab(self, parent: ttk.Frame) -> None:
        buttons = ttk.Frame(parent)
        buttons.pack(fill="x", pady=(0, 10))
        ttk.Button(buttons, text="Unlock All", command=lambda: self.set_all_achievements(True)).pack(side="left")
        ttk.Button(buttons, text="Lock All", command=lambda: self.set_all_achievements(False)).pack(side="left", padx=8)

        for achievement_id, name in ACHIEVEMENTS.items():
            var = tk.BooleanVar(value=False)
            self.achievement_vars[achievement_id] = var
            ttk.Checkbutton(parent, text=name, variable=var).pack(anchor="w", pady=3)

    def _build_presets_tab(self, parent: ttk.Frame) -> None:
        ttk.Label(parent, text="Presets only fill the stat fields. They do not save until you click Save Modded File.").pack(anchor="w", pady=(0, 10))
        for name, values in PRESETS.items():
            frame = ttk.Frame(parent)
            frame.pack(fill="x", pady=4)
            ttk.Label(frame, text=name, width=18).pack(side="left")
            ttk.Button(frame, text="Apply", command=lambda v=values: self.apply_preset(v)).pack(side="left")

    def _build_raw_tab(self, parent: ttk.Frame) -> None:
        ttk.Label(parent, text="Advanced: current save JSON. Click Refresh after editing stats/achievements.").pack(anchor="w")
        buttons = ttk.Frame(parent)
        buttons.pack(fill="x", pady=8)
        ttk.Button(buttons, text="Refresh Raw JSON", command=self.refresh_raw).pack(side="left")
        ttk.Button(buttons, text="Apply Raw JSON To Fields", command=self.apply_raw).pack(side="left", padx=8)

        self.raw_text = tk.Text(parent, wrap="none", height=20)
        self.raw_text.pack(fill="both", expand=True)

    def browse(self) -> None:
        filename = filedialog.askopenfilename(
            title="Choose BSCR save file",
            filetypes=[("BSCR save", "bscr_save.dat"), ("DAT files", "*.dat"), ("All files", "*.*")],
        )
        if filename:
            self.save_path.set(filename)

    def create_new(self) -> None:
        self.data = json.loads(json.dumps(DEFAULT_SAVE))
        self.fill_fields()
        self.status.set("New default save loaded in editor. Click Save Modded File to write it.")

    def load(self) -> None:
        path = Path(self.save_path.get()).expanduser()
        try:
            self.data = read_save(path)
            self.fill_fields()
            self.status.set(f"Loaded {path}")
        except FileNotFoundError:
            messagebox.showerror("Not found", f"Could not find:\n{path}")
        except Exception as exc:
            messagebox.showerror("Load failed", str(exc))

    def save(self) -> None:
        path = Path(self.save_path.get()).expanduser()
        try:
            self.collect_fields()
            backup = write_save(path, self.data, make_backup=True)
            backup_msg = f"\nBackup created:\n{backup}" if backup else ""
            self.status.set(f"Saved {path}")
            messagebox.showinfo("Saved", f"Save file written successfully.{backup_msg}")
        except Exception as exc:
            messagebox.showerror("Save failed", str(exc))

    def fill_fields(self) -> None:
        for key, _label in RESOURCE_FIELDS:
            self.entries[key].set(str(self.data.get(key, DEFAULT_SAVE[key])))
        achievements = self.data.setdefault("achievements", {})
        for achievement_id, var in self.achievement_vars.items():
            var.set(bool(achievements.get(achievement_id, False)))
        self.refresh_raw()

    def collect_fields(self) -> None:
        for key, _label in RESOURCE_FIELDS:
            self.data[key] = parse_number(self.entries[key].get())
        achievements = self.data.setdefault("achievements", {})
        for achievement_id, var in self.achievement_vars.items():
            achievements[achievement_id] = bool(var.get())
        self.data["money_is_int"] = isinstance(self.data.get("money"), int)
        self.refresh_raw()

    def set_all_achievements(self, unlocked: bool) -> None:
        for var in self.achievement_vars.values():
            var.set(unlocked)

    def apply_preset(self, values: Dict[str, Any]) -> None:
        for key, value in values.items():
            if key in self.entries:
                self.entries[key].set(str(value))
        self.status.set("Preset applied to fields. Save when ready.")

    def refresh_raw(self) -> None:
        try:
            # Avoid recursion if fields are not fully built yet.
            data = json.loads(json.dumps(self.data))
            if self.entries:
                for key, _label in RESOURCE_FIELDS:
                    data[key] = parse_number(self.entries[key].get())
            if self.achievement_vars:
                data["achievements"] = {k: bool(v.get()) for k, v in self.achievement_vars.items()}
            data["money_is_int"] = isinstance(data.get("money"), int)
            self.raw_text.delete("1.0", "end")
            self.raw_text.insert("1.0", json.dumps(data, indent=2))
        except Exception as exc:
            self.status.set(f"Raw refresh failed: {exc}")

    def apply_raw(self) -> None:
        try:
            self.data = json.loads(self.raw_text.get("1.0", "end"))
            self.data["achievements"] = {**DEFAULT_SAVE["achievements"], **self.data.get("achievements", {})}
            self.fill_fields()
            self.status.set("Raw JSON applied to fields.")
        except Exception as exc:
            messagebox.showerror("Invalid JSON", str(exc))


def main() -> int:
    app = SaveModTool()
    app.mainloop()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
