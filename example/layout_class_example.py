from pykeys import LayoutClass, Key, hotkey


class MyLayout(metaclass=LayoutClass):
    @hotkey(Key("A"))
    def a(self):
        print("A")


x = MyLayout()
