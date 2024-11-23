import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from pykeys.keys.cmd import Act
from pykeys.layout.layout import Layout
from pykeys.keys import keys
from pykeys.layout.print_layout import get_layout_table


def a():
    print("num 1 down with num 0")


lt = Layout("messing_with_keys")
lt += keys.num_1.down.with_modifiers(keys.num_0).bind(
    Act("action", a, "something something")
)
lt += keys.num_1.down.with_modifiers(keys.num_dot).bind(
    Act("action", a, "something something")
)
lt += keys.num_1.down.bind(Act("action", a, "something something"))
lt += keys.num_2.down.bind(Act("action", a, "something something"))

print(get_layout_table(lt))
