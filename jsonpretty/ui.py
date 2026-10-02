"""JSONPretty GUI."""

from __future__ import annotations

import ctypes
import tkinter as tk

from . import __version__
from .engine import minify, pretty
from .instance import WINDOW_TITLE

BG = "#111111"
FG = "#ffffff"
MUTED = "#999999"
CARD = "#1a1a1a"
OK = "#86efac"
BAD = "#fca5a5"
ACCENT = "#93c5fd"


class JSONPrettyApp(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title(WINDOW_TITLE)
        self.geometry("780x600")
        self.minsize(560, 440)
        self.configure(bg=BG)

        pad = tk.Frame(self, bg=BG)
        pad.pack(fill="both", expand=True, padx=22, pady=18)

        head = tk.Frame(pad, bg=BG)
        head.pack(fill="x")
        tk.Label(head, text="JSONPretty", bg=BG, fg=FG, font=("Segoe UI Semibold", 18)).pack(
            side="left"
        )
        tk.Label(
            head,
            text="неделя 6 · Текст · день 40",
            bg=BG,
            fg=MUTED,
            font=("Segoe UI", 9),
        ).pack(side="right")

        tk.Label(
            pad,
            text="Каша ↔ читаемый JSON",
            bg=BG,
            fg=MUTED,
            font=("Segoe UI", 9),
        ).pack(anchor="w", pady=(4, 12))

        self._footer = tk.Frame(pad, bg=BG)
        self._footer.pack(side="bottom", fill="x")

        row = tk.Frame(self._footer, bg=BG)
        row.pack(side="bottom", fill="x", pady=(10, 0))
        self._mk_btn(row, "Из буфера", self.from_clip).pack(side="left")
        self._mk_btn(row, "Красиво", self.do_pretty, accent=True).pack(side="left", padx=(8, 0))
        self._mk_btn(row, "Сжать", self.do_minify).pack(side="left", padx=(8, 0))
        self._mk_btn(row, "В буфер", self.to_clip).pack(side="left", padx=(8, 0))
        tk.Label(
            row,
            text=f"v{__version__} · darkshade",
            bg=BG,
            fg=MUTED,
            font=("Segoe UI", 9),
        ).pack(side="right")

        self._status = tk.Label(
            self._footer,
            text="Ctrl+Enter — красиво",
            bg=BG,
            fg=MUTED,
            font=("Segoe UI", 11),
            anchor="w",
            pady=4,
        )
        self._status.pack(side="bottom", fill="x")

        self._box = tk.Text(
            pad,
            height=18,
            bg=CARD,
            fg=FG,
            insertbackground=FG,
            relief="flat",
            font=("Consolas", 12),
            wrap="none",
            padx=12,
            pady=10,
            undo=True,
        )
        self._box.pack(fill="both", expand=True)

        self.bind("<Control-Return>", lambda _e: self.do_pretty())
        self.after(20, self._place)
        self.after(80, self._box.focus_set)

    def _mk_btn(self, parent, text, cmd, accent: bool = False) -> tk.Label:
        lbl = tk.Label(
            parent,
            text=text,
            bg=ACCENT if accent else "#333333",
            fg=BG if accent else FG,
            font=("Segoe UI", 10),
            padx=12,
            pady=7,
            cursor="hand2",
        )
        lbl.bind("<Button-1>", lambda _e: cmd())
        return lbl

    def _place(self) -> None:
        self.update_idletasks()
        w, h = self.winfo_width() or 780, self.winfo_height() or 600
        sw = ctypes.windll.user32.GetSystemMetrics(0)
        sh = ctypes.windll.user32.GetSystemMetrics(1)
        self.geometry(f"{w}x{h}+{(sw - w) // 2}+{(sh - h) // 4}")

    def _text(self) -> str:
        return self._box.get("1.0", "end-1c")

    def _set_text(self, text: str) -> None:
        self._box.delete("1.0", "end")
        self._box.insert("1.0", text)

    def _apply(self, result) -> None:
        if result.ok:
            self._set_text(result.text)
            self._status.configure(
                text=f"ок · {len(result.text)} симв.",
                fg=OK,
            )
        else:
            self._status.configure(text=result.error, fg=BAD)

    def from_clip(self) -> None:
        try:
            data = self.clipboard_get()
        except tk.TclError:
            self._status.configure(text="буфер пуст", fg=MUTED)
            return
        if not isinstance(data, str):
            data = str(data)
        self._set_text(data)
        self._status.configure(text=f"вставлено {len(data)} симв.", fg=ACCENT)

    def to_clip(self) -> None:
        text = self._text()
        self.clipboard_clear()
        self.clipboard_append(text)
        self.update_idletasks()
        self._status.configure(text=f"скопировано {len(text)} симв.", fg=OK)

    def do_pretty(self) -> None:
        self._apply(pretty(self._text()))

    def do_minify(self) -> None:
        self._apply(minify(self._text()))


def run() -> None:
    JSONPrettyApp().mainloop()
