import requests
import sys
import time
import re

link_body = 'http://ocw.nthu.edu.tw/videosite/index.php?op=watch&id={}&filename=640_480_768.MP4&type=download'

info = [
    # [[237],             '第01讲 课程介绍与上课方式说明'],
    # [[240, 241],        '第02讲 电影《梦游交易所》欣赏与相关概念'],
    # [[242, 243, 244],   '第03讲 何谓科幻？科幻概论之总论篇'],
    # [[245, 246, 247],   '第04讲 科幻的10+1堂入门必修课之「人」、「空」、「时」、「灾」、「战」、「政」'],
    # [[248, 249],        '第05讲 科幻的10+1堂入门必修课之「力」，「界」，「创」，「神」，「变」'],
    # [[250, 251],        '第06讲 古典科幻篇'],
    # [[252],             '第07讲 社会科幻篇与电影《重装任务》'],
    # [[253],             '第08讲 社会科幻篇与电影《千钧一发》'],
    # [[378, 383],        '第09讲 社会科幻篇与反乌托邦'],
    # [[380],             '第10讲 美国科幻黄金时期与电影《星战毁灭者》'],
    # [[384, 385, 386],   '第11讲 英语科幻三大家'],
    # [[387, 388],        '第12讲 英语科幻三大家之艾西莫夫与电影《魔鬼总动员》'],
    [[389, 390],        '第13讲 菲利浦．狄克和他的异想世界'],
    [[473],             '第14讲 菲利浦．狄克与电影《异次元骇客》'],
    [[465, 466],        '第15讲 Cyber​​punk 驭电飞行'],
    [[467, 468],        '第16讲 Cyber​​punk与电影《Tron》'],
    [[472],             '第17讲 骇客任务影片欣赏'],
    [[471],             '第18讲 日本的幻想科学'],
]

for i in range(0, len(info)):
    top_id = info[i][0]
    top_title = info[i][1]
    for j in range(0, len(top_id)):
        file_id = top_id[j]
        if len(top_id) <= 1:
            file_title = top_title
        else:
            # course_num = int(re.findall(r'\d+', top_title)[0])
            # char_mark = (4, 3)[course_num<=9]
            char_mark = 4
            file_title = top_title[0:char_mark] + '_' + chr(ord('A')+j) + top_title[char_mark:]
        file_link = link_body.format(file_id) 

        print('>>> Downloading ' + file_title + ' ...')

        start_time = time.clock()
        req = requests.get(file_link, stream=True)
        file_length = req.headers.get('content-length')

        with open(file_title + '.mp4', 'wb') as outfile:
            if file_length is None: # no content length header
                outfile.write(req.content)
            else:
                dl_num = 0
                segs_num = 50
                chunk_size = 1024 * 1024 * 10 # 10 Mb per chunk
                file_length = int(file_length)
                for chunk in req.iter_content(chunk_size=chunk_size):
                    dl_num += len(chunk)
                    outfile.write(chunk)
                    dl_progress = int(segs_num * dl_num / file_length)
                    used_time = time.clock() - start_time
                    sys.stdout.write('\r {:>3}{} [{} {}] {} {}'.format(
                        str(int(dl_progress*100/segs_num)), '/'+str(100), 
                        '='*dl_progress, ' '*(segs_num-dl_progress),
                        round(dl_num/(2**20)/used_time,2), ' Mb/s'))
                    sys.stdout.flush()
                print('')

        print(file_title + ' downloaded!')
        elapsed_time = time.clock() - start_time
        print('Elapsed time: {} s'.format(round(elapsed_time, 1)))
