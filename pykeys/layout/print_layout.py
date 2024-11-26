# pyright: reportUnknownMemberType=false
# pyright: reportUnknownVariableType=false
# pyright: reportMissingTypeStubs=false
# pyright: reportUnknownArgumentType=false
from itertools import groupby
import re
from beautifultable import BeautifulTable, ALIGN_LEFT


from pykeys.layout.layout import Layout


def get_magic_marker(inner: str):
    return f"@{inner}@"


_magic_marker_regex = re.compile(rf"^.*@(.+)@.*$", re.MULTILINE)
_newline_regex = re.compile(r"\n")


def get_layout_table(layout: Layout):
    table = BeautifulTable()
    table.border.left = "|"
    table.border.right = "|"
    table.border.top = ""
    table.border.bottom = ""
    table.junction = ""
    table.rows.separator = ""
    headings_saved: list[str] = []
    for key_bindings in layout:
        for heading_line, of_type in groupby(
            key_bindings, key=lambda binding: binding.trigger.trigger_label
        ):
            index = len(headings_saved)
            headings_saved.append(heading_line)
            table.rows.append([get_magic_marker(str(index)), "", ""])
            less_specific_first = sorted(
                of_type, key=lambda binding: binding.trigger.specificity
            )
            for in_order in less_specific_first:
                table.rows.append(
                    [
                        in_order.trigger.modifiers,
                        in_order.act.metadata.label,
                        in_order.act.metadata.description,
                    ]
                )

    def replacement_function(match: re.Match[str]):
        heading_index = int(match.group(1))
        heading = headings_saved[heading_index]
        return f"{heading} +"

    table.columns.alignment = ALIGN_LEFT, ALIGN_LEFT, ALIGN_LEFT
    table_string = str(table)
    indented_table_string = _newline_regex.sub("\n    ", table_string)
    table_with_headings = _magic_marker_regex.sub(
        replacement_function, indented_table_string
    )
    active = "✅" if layout.active else "❎"
    return f"LAYOUT {layout.name} {active}\n{table_with_headings} "
