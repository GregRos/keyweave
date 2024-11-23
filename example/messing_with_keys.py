from pykeys.layout.layout import Layout
from pykeys.keys import keys

lt = Layout("messing_with_keys")
lt += keys.num_1.down.with_modifiers(keys.num_0).bind(lambda: print("num_1 + num_0"))
