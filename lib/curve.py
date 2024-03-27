#!/usr/bin/env python
#  -*- coding:utf-8 -*-
import re
import time
import os
import sys
import _thread
import statistics
from matplotlib import pyplot as plt
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


def readcsv(filename,x_name,y_name):
    # 读取CSV数据文件
    df = pd.read_csv(filename)  # 将filename替换为你的CSV文件路径
    # 这里的 'Attenuation' 列是横坐标数据，'Throughput' 列是纵坐标数据
    x = df[x_name]
    y = df[y_name]
    return x, y

def figure(stringx,stringy,x1,x2,x_s,y1,y2,y_s,xmin, xmax,ymin, ymax,x_p,y_p):
    fig = go.Figure()
    #fig.add_trace(go.Scatter(x=[], y=[], mode='lines', name=''))
    fig.update_xaxes(title_text=stringx, tickvals=list(range(x1,x2,x_s)), ticktext=[], range=[xmin, xmax], dtick=x_p)
    fig.update_yaxes(title_text=stringy, tickvals=list(range(y1,y2,y_s)), ticktext=[], range=[ymin, ymax], dtick=y_p)
    # 设置图例
    #fig.update_layout(legend=dict(title='{}'.format(test_case)))
    # 设置布局
    fig.update_layout(title="2.4GHz RvR", xaxis=dict(showgrid=True, zeroline=True), yaxis=dict(showgrid=True, zeroline=True))
    return fig

def trace(fig,test_case,x_value,y_value):
    fig.add_trace(go.Scatter(x=x_value, y=y_value, mode='lines', name='RvR_Curve_{}'.format(test_case)))
     # 设置图例
    fig.update_layout(legend=dict(title='{}'.format(test_case)))
  
def wrfig(fig,htmlfile):
    fig.write_html(htmlfile)


# def readcsv(filename,test_case,htmlfile):
#     # 读取CSV数据文件
#     df = pd.read_csv(filename)  # 将filename替换为你的CSV文件路径
#     # 这里的 'Attenuation' 列是横坐标数据，'Throughput' 列是纵坐标数据
#     x_attenuation = df['Attenuation_{}'.format(test_case)]
#     y_throughput = df['Throughput_{}'.format(test_case)]
#     # 创建图表
#     fig = go.Figure()
#     # 添加曲线图
#     fig.add_trace(go.Scatter(x=x_attenuation, y=y_throughput, mode='lines', name='RvR_Curve_{}'.format(test_case)))
#     # 设置 x 轴和 y 轴的标题以及精度、最大值和最小值
#     # title_text：设置 x 轴的标题文本，例如 title_text="X轴标题"。
#     # tickvals：设置 x 轴的刻度值，传入一个列表，例如 tickvals=[1, 2, 3, 4, 5]。
#     # ticktext：设置 x 轴的刻度显示文字，传入一个与 tickvals 对应的列表，例如 ticktext=["点1", "点2", "点3", "点4", "点5"]。
#     # range：设置 x 轴的数值范围，传入一个包含两个元素的列表 [min_value, max_value]，例如 range=[1, 5]。
#     # dtick：设置 x 轴的刻度间隔，即精度，例如 dtick=1 表示刻度间隔为 1。
#     # showgrid：设置是否显示网格线，例如 showgrid=True 表示显示网格线。
#     # zeroline：设置是否显示零线（原点线），例如 zeroline=True 表示显示零线。
#     fig.update_xaxes(title_text="Attenuation(dB)", tickvals=list(range(0,101)), ticktext=[], range=[0, 110], dtick=1)
#     fig.update_yaxes(title_text="Throughput(Mbps)", tickvals=list(range(0,51,5)), ticktext=[], range=[0, 50], dtick=5)
#     # 设置图例
#     fig.update_layout(legend=dict(title='{}'.format(test_case)))
#     # 设置布局
#     fig.update_layout(title="2.4GHz RvR", xaxis=dict(showgrid=True, zeroline=True), yaxis=dict(showgrid=True, zeroline=True))
#     # fig = px.line(x=attenuation, y=throughput, title='Throughput vs Attenuation', labels={'x': 'Attenuation', 'y': 'Throughput'})
#     # fig.update_layout(
#     #     xaxis_title='Attenuation(dB)',
#     #     yaxis_title='Throughput(Mbps)',
#     #     legend_title='Legend'
#     # )
#     fig.write_html(htmlfile)

# # def getData(filename):
# #         if 'log'  in filename:
# #             #REGX = re.compile('.*Bytes\s*(.*)\s*([GMK])bits\/sec', re.I)
# #             REGX = re.compile('.*Bytes\s*(\d+.\d+)\s(\S*)\/sec', re.I)
# #             cmd = 'type {} | findstr "sec"'.format(filename)
# #             data = commands(cmd)
# #             if data is None or len(data) == 0:
# #                 print("Test case Failed!")
# #                 return None
# #             data = REGX.findall(data)
# #         else:
# #             REGX = re.compile('(\d+\.\d+)\(.*([GMK])bps', re.I)
# #             data = REGX.findall(filename)
# #         newdata = []
# #         for d in data:
# #             #if d[1] == 'K':
# #             if d[1] == 'Kbits':
# #                 nd = str(float(d[0].strip()) / 1024)
# #                 newdata.append(float(nd))
# #             else:
# #                 newdata.append(float(d[0]))
# #         return newdata

# # def table(data) :
# #     time = list(range(len(data)))
# #     fig = plt.figure(figsize=(10, 8.5))   # 创建绘图窗口，并设置窗口大小
# #     ax1 = fig.add_subplot(111)      # 将画面分割为1行1列选第一个
# #     ax1.plot(time, data, 'blue', label='Throughput')  # 画time-data的值，颜色蓝
# #     ax1.legend(loc='upper right')  # 绘制图例，plot()中的label值
# #     ax1.set_xlabel('Time')  # 设置X轴名称
# #     ax1.set_ylabel('Throughput (Mbps/sec)')  # 设置Y轴名称
# #     plt.ylim(0, max(data))    #设置y轴坐标从0开始
# #     plt.xlim(0, 180)
# #     plt.savefig(filename+'.png')     # 保存图表
# #     #plt.show()  # 显示绘制的图

if __name__ == '__main__':
    print('Hello, we are processing the data!')
#     # path = "C:\\Users\\dell\\Desktop\\ww\\log"  # 文件夹目录
#     # files = os.listdir(path)  # 得到文件夹下的所有文件名称
#     # txts = [path + '\\' + file for file in files]
#     # for txt in txts[0:]:
#     #     print(txt)
#     #     filename = txt
#     #     data = getData(filename)
#     #     #print(data)
#     #     #table1 = table(data)
#     #     # print(max(table_data))
#     #     print("平均值为：",statistics.mean(data))
#     #     print("最小值为：", min(data))

