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
         - _value_len   – typical cell len  (chars) → widget “Value” width
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

    def by_id(self, cid: int) -> Card:
        return next(c for c in self._cards if c.id == cid)

    # ── visibility API ─────────────────────────────────────────────
    def update_visibility(self, row: int, state: Qt.CheckState) -> None:
        """
        Updates the card's .show and .disabled flags based on tri-state checkbox.
        Emits visibilityChanged if the state changes.
        """
        card = self._cards[row]
        prev_show = card.show
        prev_disabled = card.disabled

        if state == Qt.Checked:
            card.set_disabled(False)
            card.show = True
        elif state == Qt.Unchecked:
            card.set_disabled(False)
            card.show = False
        else:  # Qt.PartiallyChecked
            card.set_disabled(True)
            card.show = False

        if (card.show != prev_show) or (card.disabled != prev_disabled):
            self.visibilityChanged.emit()

    def visible_cards(self, show_all: bool) -> list[Card]:
        """Return either all cards (if show_all) or only those with card.show."""
        return list(self._cards) if show_all else [c for c in self._cards if c.show]

    # ── ordering API ────────────────────────────────────────────────
    def reorder(self, card_id: int, pos: int) -> None:
        """Re-orders a single card by ID → position, emits orderChanged."""
        self._cards[card_id]._move_to(pos)
        self.orderChanged.emit()

    def reorder_by_list(self, new_id_order: List[int]) -> None:
        """
        Re-orders all cards to match the given list of IDs, updating each
        card’s ._order._current accordingly and emitting orderChanged.
        """
        id2card = {c.id: c for c in self._cards}
        for idx, cid in enumerate(new_id_order):
            id2card[cid]._move_to(idx)
        self.orderChanged.emit()

    def disable(self, card_id: int) -> None:
        """Disable a card (moves it to end) and emit both order and visibility signals."""
        card = next(c for c in self._cards if c.id == card_id)
        if card.disabled:
            return
        card._move_to(len(self._cards) - 1)
        card.set_disabled(True)
        self.orderChanged.emit()
        self.visibilityChanged.emit()

    def enable(self, card_id: int) -> None:
        """Re-enable a disabled card, restoring its previous order."""
        card = next(c for c in self._cards if c.id == card_id)
        if not card.disabled:
            return
        card.set_disabled(False)
        card._restore_order()
        self.orderChanged.emit()
        self.visibilityChanged.emit()

    # ── factory & projections ────────────────────────────────────────
    @classmethod
    def load_from_df(cls, df: pd.DataFrame) -> "CardTableModel":
        cards: list[Card] = []
        for idx, col in enumerate(df.columns):
            lens = df[col].astype(str).str.rstrip().str.len()
            size = _CardSize(min=lens.min(), avg=int(lens.mean()), max=lens.max())
            cards.append(Card(
                id=idx,
                title=str(col),
                size=size,
                _order=_CardOrder(default=idx),
            ))
        return cls(cards)

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

    # ── internal helpers ─────────────────────────────────────────────
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

    # ── serialization ───────────────────────────────────────────────
    def to_dict(self) -> dict:
        return {"cards": [c.to_dict() for c in self._cards]}

    def to_json(self, indent: int | None = 2) -> str:
        return json.dumps(self.to_dict(), indent=indent)


__all__ = ["CardTableModel"]