from retriever.lib.scripts import reload_scripts


def compile():
    """Reload scripts for CLI"""
    print("Compiling retriever scripts...")
    reload_scripts()
    print("done.")


if __name__ == "__main__":
    compile()
