from retriever.version import get_module_version


def test_script_version():
    """Test if script version specifed in version.txt match."""
    script = get_module_version()
    with open("version.txt", "r") as version_file:
        version_file.readline()
        for counter, line in enumerate(version_file.readlines()):
            if line[-1] == '\n':
                assert line[:-1] == script[counter]
            else:
                assert line == script[counter]
