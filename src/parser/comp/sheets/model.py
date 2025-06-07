# src/parser/comp/sheets/model.py
import pandas as pd
from .card_table_mdl import CardTable   # ← the new column-state engine

class SheetModel:
    """Model for navigating one row at a time, transposed vertically as field-value pairs."""

    def __init__(self, path_or_df):
        if isinstance(path_or_df, pd.DataFrame):
            self.df = path_or_df
        else:
            self.df = pd.read_excel(path_or_df)

        self.current_index = 0

        # loading cardtable
        self.card_table: CardTable = CardTable.from_dataframe(self.df)
        # debug: show how CardTable parsed the DataFrame
        self.col_width = self.card_table.col_width
        self.title_width = self.card_table.title_width
        #self._print_card_info()

    @property
    def row_count(self):
        return len(self.df)

    @property
    def current_row(self):
        if not (0 <= self.current_index < len(self.df)):
            return None, None
        row = self.df.iloc[self.current_index]
        items = list(row.items())
        return row, items

    def next(self):
        if self.current_index < self.row_count - 1:
            self.current_index += 1

    def prev(self):
        if self.current_index > 0:
            self.current_index -= 1

    # ────────── helpers ──────────
    def _print_card_info(self) -> None:
        """Dump CardTable state once at load-time."""
        print("== CardTable snapshot ==")
        for card in self.card_table.cards:
            print(card)
        print()  # newline for readability


