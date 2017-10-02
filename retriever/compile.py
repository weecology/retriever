from __future__ import absolute_import
from __future__ import print_function

from retriever.lib.scripts import MODULE_LIST


def compile():
    print("Compiling retriever scripts...")
    MODULE_LIST(force_compile=True)
    print("done.")


if __name__ == "__main__":
    compile()
