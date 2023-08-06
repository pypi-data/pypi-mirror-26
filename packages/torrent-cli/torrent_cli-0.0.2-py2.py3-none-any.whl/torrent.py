import csv
import json
from pprint import pprint
import argparse

import requests
from bs4 import BeautifulSoup


HEADERS = {
    'X-Requested-With': 'XMLHttpRequest',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 '
                  '(KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
}

VERSION = "VERSION 0.0.2"


def get_parser():
    """
    解析命令行参数
    """
    parser = argparse.ArgumentParser(description='Magnets-Getter CLI Tools.')
    parser.add_argument('-k', '--keyword', type=str,
                        help='magnet keyword.')
    parser.add_argument('-n', '--num', type=int, default=20,
                        help='magnet number.(default 20)')
    parser.add_argument('-s', '--sort-by', type=int, default=0,
                        help='0: Sort by date，1: Sort by size.(default 0)')
    parser.add_argument('-o', '--output', type=str,
                        help='output file path, supports csv and json format.')
    parser.add_argument('-p', '--pretty-oneline', action='store_true',
                        help='show magnets info with one line.')
    parser.add_argument('-v', '--version', action='store_true',
                        help='version information.')
    return parser


def command_line_runner():
    """ 执行命令行操作
    """
    parser = get_parser()
    args = vars(parser.parse_args())

    if args['version']:
        print(VERSION)
        return

    if not args["keyword"]:
        parser.print_help()
    else:
        magnets = run(kw=args["keyword"],
                      num=args["num"], sort_by=args["sort_by"])
        if args["output"]:
            _output(magnets, args["output"])
        else:
            _print(magnets, args["pretty_oneline"])


def run(kw, num, sort_by):
    """ 爬虫入口

    :param kw: 资源名称
    :param num: 资源数量
    :param sort_by: 排序方式。0：按磁力时间排序，1：按磁力大小排序
    """
    print("Crawling data for you.....")
    domain = "http://bt2.bt87.cc"

    # 确保 num 有效
    if num < 0 or num > 200:
        num = 20
    # 每页最多 20 条磁力信息
    page = num // 20

    urls = []
    for p in range(1, page + 1):
        url = domain + "/index.php?r=files%2Findex&kw={kw}&page={p}".\
            format(kw=kw, p=p)
        try:
            resp = requests.get(url, headers=HEADERS).text
            try:
                bs = BeautifulSoup(resp, "lxml").find(
                    "ul", class_="row list-group").find_all("li")
                urls.extend([domain + b.find("a")["href"] for b in bs])
            except:
                pass
        except Exception:
            print("Crawling Exception, may be you should check your network!")

    magnets = []
    if not urls:
        print("Sorry, found nothing :(")

    for url in urls:
        try:
            resp = requests.get(url, headers=HEADERS).text
            magnet = BeautifulSoup(resp, 'lxml').find("h4", id="magnet").text[8:]
            magnet_name = BeautifulSoup(resp, 'lxml').find("h3").text
            magnet_date, magnet_size = (
                str(BeautifulSoup(resp, 'lxml').find("h4").text).split(maxsplit=1))
            magnets.append({
                "magnet": magnet,               # 磁力链接
                "magnet_name": magnet_name,     # 磁力名称
                "magnet_date": magnet_date,     # 磁力日期
                "magnet_size": magnet_size      # 磁力大小
            })
        except Exception:
            print("Crawling Exception, may be you should check your network!")
    return sort_magnets(magnets, sort_by)


def sort_magnets(magnets, sort_by):
    """ 排序磁力

    :param magnets: 磁力列表
    :param sort_by: 排序方式
    """
    # 按日期排序，默认
    if sort_by == 0:
        _magnets = sorted(magnets,
                          key=lambda x: x["magnet_date"],
                          reverse=True)
    # 按大小排序，统一单位为 kb
    else:
        for m in magnets:
            unit = m["magnet_size"].split()
            if unit[1] == "GB":
                _size = float(unit[0]) * 1024 * 1024
            elif unit[1] == "MB":
                _size = float(unit[0]) * 1024
            else:
                _size = float(unit[0])
            m["magnet_size_kb"] = _size
        _magnets = sorted(magnets,
                          key=lambda x: x["magnet_size_kb"],
                          reverse=True)
    return _magnets


def _print(magnets, is_show_magnet_only):
    """ 在终端界面输出结果

    :param magnets: 磁力列表
    :param is_show_magnet_only: 单行输出
    """
    if is_show_magnet_only:
        for row in magnets:
            print(row["magnet"], row["magnet_size"], row["magnet_date"])
    else:
        for row in magnets:
            if "magnet_size_kb" in row:
                row.pop("magnet_size_kb")
            pprint(row)


def _output(magnets, path):
    """ 将数据保存到本地文件

    :param magnets: 磁力列表
    :param path: 文件路径，支持 csv 和 json 两种文件格式
    """
    if path:
        if str(path).endswith("csv"):
            try:
                with open(path, mode="w+", encoding="utf-8") as fout:
                    f_csv = csv.writer(fout)
                    f_csv.writerow((
                        "magnet_name", "magnet_date", "magnet_size", "magnet"))
                    for row in magnets:
                        f_csv.writerow((
                            row["magnet_name"], row["magnet_date"],
                            row["magnet_size"], row["magnet"]))
            except Exception:
                print("Failed to save the file!")
        if str(path).endswith("json"):
            try:
                with open(path, mode="w+", encoding="utf-8") as fout:
                    fout.write(json.dumps(magnets))
            except Exception:
                print("Failed to save the file!")


if __name__ == "__main__":
    command_line_runner()
