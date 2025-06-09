# src/parser/comp/sheets/model_card_table.py
from __future__ import annotations

import json
from typing import Iterable, List
import pandas as pd
from PySide6.QtCore import QObject, Signal, Qt
from .model_card import Card, _CardSize, _CardOrder


class CardTableModel(QObject):
    """
    Column metadata holder.

    • Keeps original order and tri-state visibility for every column.
    • Computes once:
         - _title_len   – longest header (chars) → widget “Field” width
         - _col_len   – typical cell len  (chars) → widget “Value” width
    • Emits orderChanged / visibilityChanged when columns are reordered
      or disabled/enabled.
    """

    orderChanged: Signal = Signal()
    visibilityChanged: Signal = Signal()

    # -----------------------------------------------------------------
    def __init__(self, cards: List[Card]) -> None:
        super().__init__()
        self._cards = cards

        # pre-computed stats for the whole table
        self._title_len: int = max((len(c.title) for c in cards), default=0)
        self._value_len: int = self._calc_avg_value_len()

    #   signal updates
    def update_visibility(self, row: int, state: Qt.CheckState) -> None:
        """
        Updates the card's .show and .disabled flags based on tri-state checkbox.
        Emits visibilityChanged if the state changes.
        """
        print(f"row {row}, state {state}")

        card = self._cards[row]
        prev_show = card.show
        prev_disabled = card.disabled

        if state == Qt.Checked:
            card.set_disabled(False)
            card.show = True
        elif state == Qt.Unchecked:
            card.set_disabled(False)
            card.show = False
        elif state == Qt.PartiallyChecked:
            card.set_disabled(True)
            card.show = False

        if (card.show != prev_show) or (card.disabled != prev_disabled):
            self.visibilityChanged.emit()


    # ---------- factory ------------------------------------------------
    @classmethod
    def load_from_df(cls, df: pd.DataFrame) -> "CardTableModel":
        #   populates CardTable object with column data from dataframe
        cards: list[Card] = []
        for idx, col in enumerate(df.columns):
            lens = df[col].astype(str).str.rstrip().str.len()
            size = _CardSize(min=lens.min(), avg=int(lens.mean()), max=lens.max())
            cards.append(
                Card(id=idx, title=str(col), size=size, _order=_CardOrder(default=idx))
            )
        #print(*cards, sep="\n")        #   print all cards
        return cls(cards)

    # ---------- public projections ------------------------------------
    @property
    def cards(self) -> Iterable[Card]:
        return self._cards

    @property
    def title_len(self) -> int:
        """Length (chars) of the widest column header."""
        return self._title_len

    @property
    def value_len(self) -> int:
        """Typical ‘Value’ width in characters (outliers trimmed)."""
        return self._value_len

    # ---------- helpers ------------------------------------------------
    def _calc_avg_value_len(self, gap: int = 50) -> int:
        """
        Average of per-column max lengths, ignoring the long-text block
        that starts with the first jump ≥ gap.
        """
        maxima = sorted(c.size.max for c in self._cards)
        cut = next(
            (i + 1 for i, (a, b) in enumerate(zip(maxima, maxima[1:])) if b - a >= gap),
            len(maxima),
        )
        return int(sum(maxima[:cut]) / cut) if cut else 0

    # ---------- mutation API ------------------------------------------
    def reorder(self, card_id: int, pos: int) -> None:
        #   re-orders position of column within list of columns in card table object
        self._cards[card_id]._move_to(pos)
        self.orderChanged.emit()

    def disable(self, card_id: int) -> None:
        #   marks column as disabled, considered out of order and skipped
        card = self._cards[card_id]
        if card.disabled:
            return
        card._move_to(len(self._cards) - 1)     #   move to the last position
        card.set_disabled(True)
        self.orderChanged.emit()    #   order at the bottom of the stack
        self.visibilityChanged.emit()   # no more visible

    def enable(self, card_id: int) -> None:
        card = self._cards[card_id]
        if not card.disabled:
            return
        card.set_disabled(False)
        card._restore_order()
        self.orderChanged.emit()
        self.visibilityChanged.emit()

    # ---------- serialisation -----------------------------------------
    def to_dict(self) -> dict:
        return {"cards": [c.to_dict() for c in self._cards]}

    def to_json(self, indent: int | None = 2) -> str:
        return json.dumps(self.to_dict(), indent=indent)


__all__ = ["CardTableModel"]