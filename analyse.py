import pandas as pd
import jieba
from wordcloud import WordCloud

font = '../font/msyh.ttf'

def word_cloud():
    content = pd.read_csv('movie_comment_1211270.csv',  encoding='utf_8_sig')
    df_list = content['content'].tolist()
    comment = jieba.cut(str(df_list), cut_all=False)
    comment = ' '.join(comment)
    wc = WordCloud(width=2000, height=1800, background_color='white', font_path=font, contour_width=3, contour_color='steelblue').generate(comment)
    wc.to_file('img.png')

if __name__ == '__main__':
    word_cloud()