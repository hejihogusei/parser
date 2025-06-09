# src/parser/comp/sheets/model_card.py
from __future__ import annotations

import json
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Optional


# ─────────────────── helpers ───────────────────

class _CardState(Enum):
    VISIBLE = auto()
    HIDDEN = auto()
    DISABLED = auto()


@dataclass(frozen=True, slots=True)
class _CardSize:
    min: int
    avg: int
    max: int


@dataclass(slots=True)
class _CardOrder:
    default: int
    _current: int = field(init=False)
    _previous: int = field(init=False)

    def __post_init__(self) -> None:
        self._current = self.default
        self._previous = self.default

    # internal mutators
    def _set_current(self, pos: int) -> None:
        #   set new order position, store previous
        if pos != self._current:
            self._previous = self._current
            self._current = pos

    def _reset(self) -> None:
        #   reset order position to previous
        self._current, self._previous = self._previous, self._current


# ───────────────────── Card ─────────────────────

@dataclass(slots=True)
class Card:
    id: int
    title: str
    size: _CardSize
    _order: _CardOrder
    _state: _CardState = _CardState.VISIBLE

    # read-only ----------------------------
    @property
    def order(self) -> int:
        return self._order._current

    @property
    def is_visible(self) -> bool:
        return self._state is _CardState.VISIBLE

    @property
    def disabled(self) -> bool:
        return self._state is _CardState.DISABLED

    # visibility --------------------------
    @property
    def show(self) -> bool:
        return self._state is _CardState.VISIBLE

    @show.setter
    def show(self, value: bool) -> None:
        if self._state is _CardState.DISABLED:
            return
        self._state = _CardState.VISIBLE if value else _CardState.HIDDEN

    # enable / disable --------------------
    def set_disabled(self, value: bool) -> None:
        if value:
            self._state = _CardState.DISABLED
        else:
            if self._state is _CardState.DISABLED:
                self._state = _CardState.VISIBLE

    # order (package-private) -------------
    def _move_to(self, pos: int) -> None:
        self._order._set_current(pos)

    def _restore_order(self) -> None:
        self._order._reset()

    # serialisation ----------------------------------------------------
    def to_dict(self) -> dict:
        as_int = int        # shorthand

        return {
            "id":        as_int(self.id),
            "title":     self.title,
            "show":      self.show,
            "disable":   self.disabled,
            "order": {
                "default":  as_int(self._order.default),
                "current":  as_int(self._order._current),
                "previous": as_int(self._order._previous),
            },
            "size": {
                "min":  as_int(self.size.min),
                "avg":  as_int(self.size.avg),
                "max":  as_int(self.size.max),
            },
        }

    def to_json(self, indent: int | None = 2) -> str:
        return json.dumps(self.to_dict(), indent=indent, ensure_ascii=False)

    # print(card) → short one-liner, repr(card) → JSON
    def __str__(self) -> str:
        return (
            f"<Card #{self.id} '{self.title}' "
            f"state={self._state.name} order={self.order} size={self.size}>"
        )

    def __repr__(self) -> str:
        return self.to_json(indent=2)

__all__ = ["Card"]