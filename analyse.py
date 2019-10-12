import pandas as pd
import jieba
import os
from wordcloud import WordCloud
from pyecharts.charts import Pie
from pyecharts import options as opts

sex = ['未填写','男','女']#性别对应关系
font = '../font/msyh.ttf'

#生成词云
def word_cloud(data, movie_id):
    data = data['content'].tolist()
    comment = jieba.cut(str(data), cut_all=False)
    comment = ' '.join(comment)
    wc = WordCloud(width=2000, height=1800, background_color='white', font_path=font, contour_width=3, contour_color='steelblue').generate(comment)
    wc.to_file('word_cloud_' + movie_id +'.png')

#评论用户性别饼图
def sex_chart(data, movie_id):
    list = []
    data = data['gender'].value_counts()
    for key,v in enumerate(data):
        list.append([sex[key],v])
    pie = Pie()
    pie.add("", list)
    pie.set_global_opts(title_opts=opts.TitleOpts(title="评论用户性别分布饼图"))
    pie.set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))
    pie.render('user_sex_' + movie_id + '.html')

def choose_func(data, movie_id):
    print ("[1] 生成词云")
    print ("[2] 生成性别饼图")
    func_id = input('请选择您要的分析功能,输入编号:')

    if func_id != '1' and func_id != '2' :
        print ('请输入正确的功能编号')
        choose_func(data, movie_id)
    else:
        if func_id == '1':
            word_cloud(data, movie_id)
        elif func_id == '2':
            sex_chart(data, movie_id)

def init():
    movie_id = input('请输入电影ID:')
    if os.path.exists('movie_comment_' + movie_id + '.csv') == True:
        content = pd.read_csv('movie_comment_' + movie_id + '.csv', encoding='utf_8_sig')
        choose_func(content, movie_id)
    else:
        print ('请先获取该电影的评论数据!')
        init()

if __name__ == '__main__':
    init()
