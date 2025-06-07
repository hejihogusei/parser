
# src/parser/comp/sheets/card_table_mdl.py
from __future__ import annotations

import json
from typing import Iterable, List

import pandas as pd
from PySide6.QtCore import QObject, Signal   # ← PySide6 substitutes

from .card_mdl import Card, _CardSize, _CardOrder


class CardTable(QObject):
    """
    Central source-of-truth for column order & visibility.
    Views listen to its Qt signals; only CardTable mutates order.
    """

    orderChanged: Signal          = Signal()   # ← was pyqtSignal()
    visibilityChanged: Signal     = Signal()

    # -----------------------------------------------------------------
    def __init__(self, cards: List[Card]) -> None:
        super().__init__()
        self._cards: List[Card] = cards

    # factory ----------------------------------------------------------
    @classmethod
    def from_dataframe(cls, df: pd.DataFrame) -> "CardTable":
        cards: List[Card] = []
        for idx, col in enumerate(df.columns):
            lens = df[col].astype(str).str.rstrip().str.len()
            size = _CardSize(min=lens.min(), avg=int(lens.mean()), max=lens.max())
            cards.append(Card(id=idx, title=str(col),
                              size=size,
                              _order=_CardOrder(default=idx)))
        return cls(cards)

    @property
    def col_width(self) -> int:
        """
        Typical column width based on per-column max lengths.
        Re-computed only once because card sizes don’t change after build.
        """
        GAP = 50
        vals = sorted(c.size.avg for c in self._cards)
        print(vals)
        cut = next((i + 1 for i, (a, b) in enumerate(zip(vals, vals[1:]))
                    if b - a >= GAP), len(vals))
        return int(sum(vals[:cut]) / cut) if cut else 0

    @property
    def title_width(self) -> int:
        """Number of characters in the longest column title."""
        return max((len(c.title) for c in self._cards), default=0)

    # read-only --------------------------------------------------------
    @property
    def cards(self) -> Iterable[Card]:
        return self._cards

    def by_id(self, card_id: int) -> Card:
        return self._cards[card_id]

    # mutators ---------------------------------------------------------
    def reorder(self, card_id: int, pos: int) -> None:
        self.by_id(card_id)._move_to(pos)
        self.orderChanged.emit()

    def disable(self, card_id: int) -> None:
        card = self.by_id(card_id)
        if card.disabled:
            return
        card._drop_to_end(len(self._cards) - 1)
        card.set_disabled(True)
        self.orderChanged.emit()
        self.visibilityChanged.emit()

    def enable(self, card_id: int) -> None:
        card = self.by_id(card_id)
        if not card.disabled:
            return
        card.set_disabled(False)
        card._restore_order()
        self.orderChanged.emit()
        self.visibilityChanged.emit()

    # serialisation ---------------------------------------------------
    def to_dict(self) -> dict:
        return {"cards": [c.to_dict() for c in self._cards]}

    def to_json(self, indent: int | None = 2) -> str:
        return json.dumps(self.to_dict(), indent=indent)


__all__ = ["CardTable"]