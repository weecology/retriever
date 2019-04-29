import cProfile
import retriever as rt
import requests
from tqdm import tqdm
from math import ceil
# import urllib.request

# def sum(a, b):
#     return a+b

if __name__ == '__main__':
    # pr = cProfile.Profile()
    # pr.enable()
    # sum(2, 3)
    # with open("./nameData.txt", 'r') as f:
    #     for line in f:
    # url = "http://ourairports.com/data/airports.csv"
    # filename = "airport.csv"
    # # progbar = tqdm(unit='B',
    # #                unit_scale=True,
    # #                unit_divisor=1024,
    # #                miniters=1,
    # #                desc='Downloading {}'.format(filename))
    #
    # resume_header = {'Range': 'bytes=%s-' % (10001),'Accept-Encoding': 'deflate'}
    # req = requests.get(url, headers=resume_header, allow_redirects=True,
    #              stream=True,
    #              )
    #
    # # total_size = int(req.headers['content-length'])
    # # progbar.total = ceil(total_size // (2 * 1024))
    # #
    # # with open(filename, 'wb') as f:
    # #     for chunk in req.iter_content(2 * 1024):
    # #         f.write(chunk)
    # #         progbar.update(1)
    #
    # print(req)
    # with open("file", 'ab') as f:
    #     f.write(req.content)

    rt.install_csv("breed-bird-survey")
    # rt.install_csv("breed-bird-survey")
    # rt.install_sqlite('airports')
    # rt.download("gdp")
    # rt.fetch("breed-bird-survey")

    # pr.disable()
    # pr.print_stats()
    # pr.dump_stats("result.prof")
    # fw = open("./nameData.txt",'w')
    # with open("./dataName.txt",'r') as f:
    #     for line in f:
    #         tmp = list(set(line.strip().split(" ")))
    #         tmp.remove('')
    #         print(tmp)
    #         for item in tmp:
    #             fw.write(item+'\n')




