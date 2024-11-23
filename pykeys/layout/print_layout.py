# pyright: reportUnknownMemberType=false
# pyright: reportUnknownVariableType=false
# pyright: reportMissingTypeStubs=false
# pyright: reportUnknownArgumentType=false
import re
from beautifultable import BeautifulTable


from pykeys.keys.key import Key
from pykeys.layout.layout import Layout


def get_magic_marker(inner: str):
    return f"@@@{inner}@@@"


_magic_marker_regex = re.compile(rf"^.*@@@(.+)@@@.*$", re.MULTILINE)
_newline_regex = re.compile(r"\n")


def get_layout_table(layout: Layout):
    table = BeautifulTable()
    for key_binding in layout:
        key = key_binding.key
        table.rows.append([get_magic_marker(key.id)])
        less_specific_first = sorted(
            key_binding, key=lambda binding: binding.trigger.specificity
        )
        for binding in less_specific_first:
            trigger_char = binding.trigger.type.char
            combo_str = " + ".join((trigger_char, str(binding.trigger.modifiers)))
            table.rows.append([combo_str, binding.label, binding.description])

    def replacement_function(match: re.Match[str]):
        key_id = match.group(1)
        return f"{Key(key_id).label} ::"

    table_string = str(table)
    indented_table_string = _newline_regex.sub("\n    ", table_string)
    table_with_headings = _magic_marker_regex.sub(
        replacement_function, indented_table_string
    )
    return table_with_headings
