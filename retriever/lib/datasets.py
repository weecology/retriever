from retriever.lib.scripts import SCRIPT_LIST, get_script, get_dataset_names_upstream
from retriever.lib.defaults import RETRIEVER_REPOSITORY


def datasets(keywords=None, licenses=None):
    """Search all datasets by keywords and licenses."""
    script_list = SCRIPT_LIST()
    if not keywords and not licenses:
        # The scripts present locally
        offline_scripts = sorted(script_list, key=lambda s: s.name.lower())
        # The scripts present in upstream retriever repository
        retriever_scripts = get_dataset_names_upstream(repo=RETRIEVER_REPOSITORY)
        # The scripts present in upstream recipes repository
        recipes_scripts = get_dataset_names_upstream()
        # Sorted list of all the online scripts
        native_scripts = sorted(list(set(retriever_scripts + recipes_scripts)))
        return {'online': native_scripts, 'offline': offline_scripts}

    offline_scripts = set()
    if licenses:
        licenses = [i.lower() for i in licenses]
    for script in script_list:
        if script.name:
            if licenses:
                script_license = [
                    licence_map['name'].lower()
                    for licence_map in script.licenses
                    if licence_map['name']
                ]
                if script_license and set(script_license).intersection(set(licenses)):
                    offline_scripts.add(script)
                    continue
            if keywords:
                script_keywords = script.title + ' ' + script.name
                if script.keywords:
                    script_keywords = script_keywords + ' ' + '-'.join(script.keywords)
                script_keywords = script_keywords.lower()
                for k in keywords:
                    if script_keywords.find(k.lower()) != -1:
                        offline_scripts.add(script)
                        break
    # The offline scripts filtered by params
    offline_scripts = sorted(list(offline_scripts), key=lambda s: s.name.lower())
    # The scripts present in upstream retriever repository filtered by params
    retriever_scripts = get_dataset_names_upstream(keywords,
                                                   licenses,
                                                   repo=RETRIEVER_REPOSITORY)
    # The scripts present in upstream recipes repository filtered by params
    recipes_scripts = get_dataset_names_upstream(keywords, licenses)
    native_scripts = sorted(list(set(retriever_scripts + recipes_scripts)))
    datasets_dict = {'online': native_scripts, 'offline': offline_scripts}
    return datasets_dict


def dataset_names():
    """Return list of all available dataset names."""
    all_scripts = datasets()
    scripts_name = {'online': [], 'offline': []}
    for offline_script in all_scripts['offline']:
        scripts_name['offline'].append(offline_script.name)
    for online_script in all_scripts['online']:
        scripts_name['online'].append(online_script)
    return scripts_name


def license(dataset):
    """Get the license for a dataset."""
    return get_script(dataset).licenses[0]['name']


def dataset_licenses():
    """Return set with all available licenses."""
    license_values = [str(script.licenses[0]['name']).lower() for script in SCRIPT_LIST()]
    return set(license_values)
