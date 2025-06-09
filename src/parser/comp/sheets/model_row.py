# src/parser/comp/sheets/model_row.py
from __future__ import annotations

import pandas as pd


class RowModel:
    """Holds the DataFrame and the current-row index."""

    def __init__(self, df: pd.DataFrame) -> None:
        self._df = df.reset_index(drop=True)
        self._idx: int = 0

    # ── navigation ──────────────────────────────────────────────
    @property
    def index(self) -> int:              # current row number
        return self._idx

    @index.setter
    def index(self, i: int) -> None:
        if 0 <= i < len(self._df):
            self._idx = i

    @property
    def row_count(self) -> int:
        return len(self._df)

    def items(self) -> list[tuple[str, object]]:
        """Return (column/field, value) pairs for the current row."""
        return list(self._df.iloc[self._idx].items())