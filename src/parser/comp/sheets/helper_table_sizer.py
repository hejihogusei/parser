# src/parser/comp/sheets/helper_table_sizer.py
from __future__ import annotations
from PySide6.QtGui import QFontMetrics

def set_initial_sizing(view, model) -> None:
    tbl = view.table  # now a QTableView
    hdr = tbl.horizontalHeader()

    # row heights
    row_h = hdr.height()
    tbl.verticalHeader().setDefaultSectionSize(row_h)
    tbl.resizeRowsToContents()

    # fixed “select” column
    tbl.setColumnWidth(view.COL_SELECT, 30)

    # compute Field-column width using header font
    fm_field = hdr.fontMetrics()
    field_w = int(fm_field.averageCharWidth() * 0.85 * model.title_len)
    tbl.setColumnWidth(view.COL_FIELD, field_w)

    # compute Value-column width using table’s font
    fm_value = tbl.fontMetrics()
    val_w    = int(fm_value.averageCharWidth() * 0.85 * model.value_len)
    tbl.setColumnWidth(view.COL_VALUE, val_w)

    hdr.setStretchLastSection(True)

    # overall width +10%
    tbl.setMinimumWidth(int((field_w + val_w) * 1.1))

    # overall height = (rows + header) × row_h + frame
    rows   = model.cards_count
    frame  = tbl.frameWidth() * 2
    height = row_h * (rows + 1) + frame
    tbl.setMinimumHeight(int(height * 0.95))

