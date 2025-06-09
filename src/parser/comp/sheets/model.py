# src/parser/comp/sheets/model.py
from __future__ import annotations

import pandas as pd

from .model_row import RowModel
from .model_card_table import CardTableModel

__all__ = ["SheetsModel"]    # lowercase per PEP8

class SheetsModel:
    """
    Aggregates a RowModel + CardTableModel.
    Controllers and the Qt‐table model read only from this façade.
    """

    def __init__(self, path_or_df):
        df = path_or_df if isinstance(path_or_df, pd.DataFrame) \
                        else pd.read_excel(path_or_df)
        self.rows      = RowModel(df)
        self.cardtable = CardTableModel.load_from_df(df)

    # ── convenience projections ────────────────────────────────────
    @property
    def cards(self):
        return self.cardtable.cards

    @property
    def cards_count(self) -> int:
        return len(list(self.cardtable.cards))

    @property
    def current_items(self) -> list[tuple[str, object]]:
        return self.rows.items()

    @property
    def row_count(self) -> int:
        return self.rows.row_count

    # ── expose column stats (read‐only) ─────────────────────────────
    @property
    def value_len(self) -> int:
        return self.cardtable.value_len

    @property
    def title_len(self) -> int:
        return self.cardtable.title_len