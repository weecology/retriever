from retriever.lib.repository import check_for_updates
from retriever.lib.scripts import SCRIPT_LIST

def check(url):
    check_for_updates()

    script_list = SCRIPT_LIST()
    flag=0

    for script in script_list:
        if str(script) == url:
            flag=1
    
    if flag == 1:
        print("URL already in Retriever")
    else:
        print("Please download dataset")