from retriever.lib.scripts import SCRIPT_LIST


def datasets(arg_keyword=None):
    """Return list of all available datasets."""
    script_list = SCRIPT_LIST()

    all_scripts = []

    for script in script_list:
        if script.name:
            if arg_keyword:
                keywords = script.title + ',' + script.name
                if script.keywords:
                    keywords = keywords + ',' + ','.join(script.keywords)
                if keywords.lower().find(arg_keyword.lower()) != -1:
                    all_scripts.append(script)
            else:
                all_scripts.append(script)

    all_scripts = sorted(all_scripts, key=lambda s: s.name.lower())

    return all_scripts
