from retriever.lib.scripts import SCRIPT_LIST, get_script


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


def dataset_names():
    """Return list of all available dataset names."""
    all_scripts = datasets()
    scripts_name = []

    for script in all_scripts:
        scripts_name.append(script.name)

    return scripts_name


def license(dataset):
    """Get the license for a dataset."""
    return get_script(dataset).licenses[0]['name']
