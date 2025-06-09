# src/parser/comp/sheets/model.py
from __future__ import annotations

import pandas as pd

from .model_row import RowModel
from .model_card_table import CardTableModel

__ALL__ = ["SheetsModel"]

class SheetsModel:
    """
    Aggregates a RowModel + CardTable.
    Controllers read only from this façade.
    """

    def __init__(self, path_or_df):
        df = path_or_df if isinstance(path_or_df, pd.DataFrame) else pd.read_excel(path_or_df)
        self.rows = RowModel(df)    #   pandas row management model
        self.cardtable = CardTableModel.load_from_df(df)  #   card view management model

    # convenience projections -------------------------------------------
    @property
    def cards(self):
        #   expose cards list
        return self.cardtable.cards

    @property
    def cards_count(self) -> int:
        return len(list(self.cardtable.cards))

    @property
    def current_items(self) -> list[tuple[str, object]]:
        #   current row list of items (column/field, value)
        return self.rows.items()

    @property
    def row_count(self) -> int:
        #   total pandas df row count
        return self.rows.row_count

    # expose column stats (read-only) -----------------------------------
    @property
    def value_len(self) -> int:
        #   card view value column size in chars
        return self.cardtable.value_len

    @property
    def title_len(self) -> int:
        #   card view column titles size in chars
        return self.cardtable.title_len