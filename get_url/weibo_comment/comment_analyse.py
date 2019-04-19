"""
分析微博评论
"""
import re

comment_file = open('comment_demo', 'rb')
for i in range(1, 5):
    comment_file.readline()
comment = comment_file.readline().decode('unicode_escape')
comment = comment.replace('\\', '')

str = ' <div comment_id="(.*?)" class="list_li S_line1 clearfix" >' \
      '<div class="WB_face W_fl"><a target="_blank" href="(.*?)">' \
      '<img width="30" height="30" alt=".*?" src=".*?" usercard=".*?" ucardconf=".*?"></a></div>' \
      '<div class="list_con" node-type="replywrap">' \
      '<div class="WB_text">' \
      '<a target="_blank" href=".*?" usercard=".*?" ucardconf=".*?">(.*?)</a>(.*?)</div>' \
      '<div class="WB_expand_media_box" style="display: none;" node-type="comment_media_disp">.*?</div>' \
      '<div class="WB_func clearfix">' \
      '<div class="WB_handle W_fr">' \
      '<ul class="clearfix">.*?</ul></div>' \
      '<div class="WB_from S_txt2">(.*?)</div></div></div></div>'

str = str.replace(' ', '')

print(str)

print(comment)

comment = comment.replace(' ', '')
comment = comment.replace('\n', '')

print(comment)

pattern = re.compile(str)
items = re.findall(pattern, comment)
for item in items:
    print(item)


comment_file.close()
