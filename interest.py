# -*- coding:UTF-8 -*-
# @Author Liwz
# @Create 2024/8/12 10:11
# -*- coding:UTF-8 -*-
# @Author Liwz
# @Create 2024/8/12 9:53
"""
月份1         月份2      月份3
4000
4000*1.01    4000
4000*1.01^2  4000*1.01  4000
……
"""
import webbrowser

from pyecharts import options as opts
from pyecharts.charts import Line, Bar, Page
from pyecharts.commons.utils import JsCode


def count(base, rate, month):
    account = 0.0
    account_ls = []
    interest_ls = []
    ori_account_ls = []
    interest_account = 0.0
    interest_account_ls = []
    for i in range(month):
        ori = base * (i + 1)
        ori_account_ls.append(ori)
        curr = round(base * ((1 + rate) ** i), 2)
        interest = round((curr * 1000 - base * 1000) / 1000, 2)
        interest_ls.append(interest)
        account = round((account * 1000 + curr * 1000) / 1000, 2)
        account_ls.append(account)
        interest_account = round((interest_account * 1000 + interest * 1000) / 1000, 2)
        interest_account_ls.append(interest_account)
        print(f'{i + 1}月时第一个月存入的资金已增长至 {curr}, 利息为:{interest}')
    print(f"当基础资金为 {base} , 月利率为 {rate} 时, 你将在 {month} 个月后获得 {account} , 其中利息部分为 {interest_account}")
    return ori_account_ls, interest_ls, account_ls, interest_account_ls


def generate_bar(x, ori_account_ls, account_ls, title):
    js = """
    function(params){
        if (params.dataIndex % 2 === 0){
            return params.value > 10000 ? (params.value/10000).toFixed(1)+'w' : (params.value/1000).toFixed(1)+'k';
        } else {
            return '';
        }
    }
    """
    js2 = """
    function(params){
        if (params.dataIndex % 2 === 0){
            return params.value > 100000 ? (params.value/10000).toFixed(1)+'w' : '';
        } else {
            return '';
        }
    }
    """

    bar = (
        Bar(init_opts=opts.InitOpts(width="2000px", height="500px"))
        .add_xaxis(x)
        .add_yaxis(
            series_name="总金额", y_axis=account_ls, label_opts=opts.LabelOpts(formatter=JsCode(js), position='top')
        )
        .add_yaxis(
            series_name="原金额", y_axis=ori_account_ls,
            label_opts=opts.LabelOpts(formatter=JsCode(js2), position='top')
        )
        .set_global_opts(
            title_opts=opts.TitleOpts(
                title=f"{title}",
                # pos_left="center"
            ),
            # legend_opts=opts.LegendOpts(
            #     is_show=False
            # )
        )
    )
    return bar


def generate_line(x, interest_account_ls, series_name):
    js = """
    function(params){
        console.log(params);
        if (params.dataIndex % 2 === 0){
            return params.value[1] > 10000 ? (params.value[1]/10000).toFixed(1)+'w' : (params.value[1]/1000).toFixed(1)+'k';
        } else {
            return '';
        }
    }
    """
    line = (
        Line()
        .add_xaxis(x)
        .add_yaxis(
            series_name=series_name, y_axis=interest_account_ls, z_level=1,
            label_opts=opts.LabelOpts(formatter=JsCode(js), position='top')
        )
    )
    return line


def run(base, month, year_rate):
    rate = round(year_rate / 12, 4)
    x = [f'{i}月' for i in range(month + 1)]
    title = f"基本资金={base} | 年化={year_rate * 100}%"

    ori_account_ls, interest_ls, account_ls, interest_account_ls = count(base, rate, month + 1)
    bar = generate_bar(x, ori_account_ls, account_ls, title)
    line = generate_line(x, interest_account_ls, "总利息")
    line2 = generate_line(x, interest_ls, "月利息")

    page = Page(layout=Page.SimplePageLayout)
    page.add(bar)
    page.add(line)
    page.add(line2)
    return page


if __name__ == '__main__':
    base = 4000.00
    month = 36
    year_rate = 0.24

    page = run(base, month, year_rate)
    path = page.render()
    webbrowser.open(path)
