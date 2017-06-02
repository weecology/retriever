from retriever.lib.testing_func import SCRIPT_LIST


def datasets(arg_script=None):
    """Return list of all available datasets."""
    script_list = SCRIPT_LIST()

    all_scripts = []

    for script in script_list:
        if script.name:
            if arg_script is not None:
                script_name = script.title + "\nName: " + script.name + "\n"
                if script.keywords:
                    script_name += "Keywords: " + \
                        str([tag for tag in script.keywords]) + "\n"
                not_found = 0
                for term in arg_script:
                    if script_name.lower().find(term.lower()) == -1:
                        not_found = 1
                        break
                if not_found == 0:
                    all_scripts.append(script_name)
            else:
                script_name = script.name
                all_scripts.append(script_name)

    all_scripts = sorted(all_scripts, key=lambda s: s.lower())

    return all_scripts
