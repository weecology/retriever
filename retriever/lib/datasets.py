from retriever.lib.scripts import SCRIPT_LIST, get_script, get_dataset_names_upstream
from retriever.lib.defaults import RETRIEVER_REPOSITORY

def datasets(keywords=None, licenses=None):
    """Search all datasets by keywords and licenses."""
    script_list = SCRIPT_LIST()

    if not keywords and not licenses:
        offline_scripts = sorted(script_list, key=lambda s: s.name.lower())
        online_retriever_script_names = get_dataset_names_upstream(repo=RETRIEVER_REPOSITORY)
        online_script_names = get_dataset_names_upstream()
        return dict({'online': sorted(online_retriever_script_names + online_script_names), 'offline': offline_scripts})

    result_scripts_offline = set()
    if licenses:
        licenses = [l.lower() for l in licenses]
    for script in script_list:
        if script.name:
            if licenses:
                script_license = [licence_map['name'].lower()
                                  for licence_map in script.licenses
                                  if licence_map['name']]
                if script_license and set(script_license).intersection(set(licenses)):
                    result_scripts_offline.add(script)
                    continue
            if keywords:
                script_keywords = script.title + ' ' + script.name
                if script.keywords:
                    script_keywords = script_keywords + ' ' + '-'.join(script.keywords)
                script_keywords = script_keywords.lower()
                for k in keywords:
                    if script_keywords.find(k.lower()) != -1:
                        result_scripts_offline.add(script)
                        break
    result_scripts_offline = sorted(list(result_scripts_offline), key=lambda s: s.name.lower())
    result_retriever_scripts_online = get_dataset_names_upstream(keywords, licenses, repo=RETRIEVER_REPOSITORY)
    result_scripts_online = get_dataset_names_upstream(keywords, licenses)
    return dict({'online': sorted(result_retriever_scripts_online + result_scripts_online), 'offline': result_scripts_offline})


def dataset_names():
    """Return list of all available dataset names."""
    all_scripts = datasets()
    scripts_name = dict()
    scripts_name['offline'] = []
    scripts_name['online'] = []
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
    license_values = [str(script.licenses[0]['name']).lower()
                      for script in SCRIPT_LIST()]
    return set(license_values)
