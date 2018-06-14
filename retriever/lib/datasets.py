from retriever.lib.scripts import SCRIPT_LIST, get_script


def datasets(keywords=None, licenses=None):
    """Search all datasets by keywords and licenses."""
    script_list = SCRIPT_LIST()

    if not keywords and not licenses:
        return sorted(script_list, key=lambda s: s.name.lower())

    result_scripts = set()
    if licenses:
        licenses = [l.lower() for l in licenses]
    for script in script_list:
        if script.name:
            if licenses:
                script_license = [licence_map['name'].lower()
                                  for licence_map in script.licenses
                                  if licence_map['name']]
                if script_license and set(script_license).intersection(set(licenses)):
                    result_scripts.add(script)
                    continue
            if keywords:
                script_keywords = script.title + ' ' + script.name
                if script.keywords:
                    script_keywords = script_keywords + ' ' + '-'.join(script.keywords)
                script_keywords = script_keywords.lower()
                for k in keywords:
                    if script_keywords.find(k.lower()) != -1:
                        result_scripts.add(script)
                        break
    return sorted(list(result_scripts), key=lambda s: s.name.lower())


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


def dataset_licenses():
    """Return set with all available licenses."""
    license_values = [str(script.licenses[0]['name']).lower()
                      for script in SCRIPT_LIST()]
    return set(license_values)
