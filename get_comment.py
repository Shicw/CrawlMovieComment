import requests
import json
import time

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36'}

def process_data(data):
    list = []
    for index,v in enumerate(data):
        content = v['content'].replace('\n', '').replace(',','，')
        gender = v['gender']
        user_level = v['userLevel']
        score = v['score']
        time = v['startTime'][:-2]
        list.append([content,time,gender,user_level,score])
    return list

def save_data(data,movie_id,page):
    filename = 'movie_comment_' + movie_id + '.csv'
    with open(filename, 'a+', encoding='utf_8_sig') as f:
        if page == '1':
            f.write('content,time,gender,user_level,score\n')
        for d in data:
            try:
                row = '{},{},{},{},{}'.format(d[0], d[1], d[2], d[3], d[4])
                f.write(row)
                f.write('\n')
            except:
                continue
    print ("保存成功")

def get_comment(movie_id):
    url = "https://m.maoyan.com/review/v2/comments.json?movieId=" + movie_id + "&limit=20&type=2&offset="
    for i in range(0,2500,20):
        page = str(int(i/20+1))
        new_url = url + str(i)
        res = requests.get(new_url, headers = headers).text
        comment_json = json.loads(res)
        if not comment_json['paging']['hasMore']:
            print ("-----全部评论爬取结束-----")
            break
        else:
            print ("开始爬取第" + page + "页评论")
            data = process_data(comment_json['data']['comments'])
            save_data(data,movie_id,page)
            time.sleep(1)

def init():
    keyword = input("请输入电影名称:")
    url = "https://maoyan.com/ajax/suggest?kw="
    list = requests.get(url + keyword, headers = headers).text
    list = json.loads(list)
    movie = list['movies']['list']
    print ("共搜索出" + str(list['movies']['total']) + "部电影")
    for key, v in enumerate(movie):
        desc = '[' + str(key) + ']' + '|' + str(v['id']) + '|' + v['nm'] + '|' + v['cat']
        if v.__contains__('star'):
            desc += '|' + v['star']
        print (desc)
    if list['movies']['total'] > 1:
        index = int(input("请输入序号确认:"))
        movie_id = movie[index]['id']
    else:
        movie_id = movie[0]['id']
    get_comment(str(movie_id))

if __name__ == '__main__':
    init()