# src/parser/comp/sheets/helper_table_sizer.py
from __future__ import annotations
from PySide6.QtGui import QFontMetrics

def chars_to_px(widget, n: int, pad: int = 0) -> int:
    #   converts characters len to pixel width for UI widget
    fm: QFontMetrics = widget.fontMetrics()
    return fm.averageCharWidth() * int(0.95 * n) + pad


def set_initial_sizing(widget, model) -> None:
    """
    One-off sizing: sets default row height, column widths, min widget width.
    called from the main controller
    """
    tbl = widget.table
    hdr = tbl.horizontalHeader()
    tbl.resizeRowsToContents()

    # row height equals header height
    row_h = hdr.height()
    tbl.verticalHeader().setDefaultSectionSize(row_h)

    # fixed columns for 'Select'
    tbl.setColumnWidth(widget.COL_SELECT, 30)

    # 'Field' column px from title len
    field_width = chars_to_px(widget, model.title_len)
    #print(f"field_width: {field_width}")
    tbl.setColumnWidth(widget.COL_FIELD, field_width)

    # 'Value' column px from average cell size; still stretch last section
    value_width= chars_to_px(widget, model.value_len)
    #print(f"value_width: {value_width}")
    tbl.setColumnWidth(widget.COL_VALUE, value_width)
    hdr.setStretchLastSection(True)

    # min overall width plus 10%
    tbl.setMinimumWidth( int((field_width + value_width)*1.10) )

    # ─────── min overall height (rows × row_h) ───────
    row_count   = model.cards_count       # total columns = card rows
    #print(f"row_count: {row_count}")
    frame       = tbl.frameWidth() * 2          # top + bottom frame
    #print(f"frame: {frame}")
    total       = row_h * row_count + row_h + frame
    #print(f"table height: {total}")
    tbl.setMinimumHeight( int(total * 1.00) )
