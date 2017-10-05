from __future__ import absolute_import
from retriever.lib.compile import MODULE_LIST


def compile():
    print("Compiling retriever scripts...")
    MODULE_LIST(force_compile=True)
    print("done.")


if __name__ == "__main__":
    compile()
