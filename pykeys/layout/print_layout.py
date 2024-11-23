# pyright: reportUnknownMemberType=false
# pyright: reportUnknownVariableType=false
# pyright: reportMissingTypeStubs=false
# pyright: reportUnknownArgumentType=false
import re
from beautifultable import BeautifulTable, ALIGN_CENTER, ALIGN_LEFT, ALIGN_RIGHT


from pykeys.keys.key import Key
from pykeys.layout.layout import Layout


def get_magic_marker(inner: str):
    return f"@@@{inner}@@@"


_magic_marker_regex = re.compile(rf"^.*@@@(.+)@@@.*$", re.MULTILINE)
_newline_regex = re.compile(r"\n")


def get_layout_table(layout: Layout):
    table = BeautifulTable()
    table.border = ""
    table.junction = ""
    table.rows.separator = ""

    for key_binding in layout:
        key = key_binding.key
        table.rows.append([get_magic_marker(key.id), "", ""])
        less_specific_first = sorted(
            key_binding, key=lambda binding: binding.trigger.specificity
        )
        for binding in less_specific_first:
            trigger_char = binding.trigger.type.char
            modifiers = 
            combo_str = " + ".join((trigger_char, str(binding.trigger.modifiers)))
            table.rows.append([combo_str, binding.act.label, binding.act.description])

    def replacement_function(match: re.Match[str]):
        key_id = match.group(1)
        return f"{Key(key_id).label} ::"

    table.columns.alignment = ALIGN_LEFT, ALIGN_LEFT, ALIGN_LEFT
    table_string = str(table)
    indented_table_string = _newline_regex.sub("\n    ", table_string)
    table_with_headings = _magic_marker_regex.sub(
        replacement_function, indented_table_string
    )
    return table_with_headings
