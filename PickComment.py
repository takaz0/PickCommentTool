import bs4
import requests
from bs4 import BeautifulSoup
import csv
import os
import re
from requests_html import HTMLSession

# バージョンを定義
version = "Pick Comment Tool - ver:1.0"

# 1つのコメントリストをcsvに出力する
def Export_Csv1(title, comments):
    # 出力先フォルダのパスを指定する
    output_dir = ".\output"

    # 出力先フォルダが存在しない場合は作成する
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # 空文字を除外
    new_list = [s for s in comments if s != ""]

    # コメントをcsvに書き込む
    with open(os.path.join(output_dir, title), 'w', encoding='UTF-8', newline='') as file:
        writer = csv.writer(file)
        for comment in new_list:
            writer.writerow([comment])

# 2つのコメントリストをcsvに出力する
def Export_Csv2(title, comments, comments2):
    # 出力先フォルダのパスを指定する
    output_dir = "./output"

    # 出力先フォルダが存在しない場合は作成する
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # 空文字を除外
    new_list = [s for s in comments if s != ""]
    new_list2 = [s for s in comments2 if s != ""]

    # コメントをcsvに書き込む
    with open(os.path.join(output_dir, title), 'w', encoding='UTF-8', newline='') as file:
        writer = csv.writer(file)
        for comment in new_list:
            writer.writerow([comment])
        for comment in new_list2:
            writer.writerow([comment])

# コメントをリストで抽出してcsvに出力する（2ch (5ch) :https://find.5ch.net/）
def pick_comment_5ch(url):
    # ページのHTMLを取得
    response = requests.get(url)
    response.encoding = 'UTF-8'
    html = response.content

    # BeautifulSoupで解析
    soup = BeautifulSoup(html, 'html.parser')

    # Winでファイルに使用できない文字を置換する
    title = re.sub(r'[\\/:*?"<>|]', '', soup.title.text) + '.csv'
    title = title.replace('\n', '').replace('\r', '')

    # 条件で抽出
    comment_elements = soup.select('div.message')
    comments = [re.sub('>>\d{1,4}', "", comment.get_text(strip=True)) for comment in comment_elements]

    # 現行スレが0件の場合は過去スレの条件で検索
    if not comments:
        comment_elements = soup.select('dd')

        # get_textで取得するとスレッド番号が上位のものを全て含んだテキストになってしまうため
        # 原因となっているcontentsの末尾を削除してから取得する
        for comment in comment_elements:
            comment.contents = comment.contents[:-1]
            comments.append(re.sub('>>\d{1,4}', "", comment.get_text(strip=True)))
    
    # CSVで出力
    Export_Csv1(title, comments)

# # コメントをリストで抽出してcsvに出力する（Twitter:https://twitter.com/home）
# def pick_comment_twitter(url):
#     # ページのHTMLを取得
#     response = requests.get(url)
#     response.encoding = 'UTF-8'
#     html = response.content

#     # BeautifulSoupで解析
#     soup = BeautifulSoup(html, 'html.parser')

#     # Winでファイルに使用できない文字を置換する
#     title = re.sub(r'[\\/:*?"<>|]', '', soup.title.text) + '.csv'
#     title = title.replace('\n', '').replace('\r', '')

#     # 条件で抽出
#     comment_elements = soup.select('div#content.style-scope.ytd-expander') # なぜか取れない
#     comments = [re.sub('>>\d{1,4}', "", comment.get_text(strip=True)) for comment in comment_elements]
    
#     # CSVで出力
#     Export_Csv1(title, comments)

# コメントをリストで抽出してcsvに出力する（YouTubeコメント欄:https://www.youtube.com/）
def pick_comment_youtube(url):
    # ページのHTMLを取得
    response = requests.get(url)
    response.encoding = 'UTF-8'
    html = response.content

    # BeautifulSoupで解析
    soup = BeautifulSoup(html, 'html.parser')

    # Winでファイルに使用できない文字を置換する
    title = re.sub(r'[\\/:*?"<>|]', '', soup.title.text) + '.csv'
    title = title.replace('\n', '').replace('\r', '')
    
    # 条件で抽出
    comment_elements = soup.select('yt-formatted-string#content-text.style-scope.ytd-comment-renderer') # なぜか取れない
    comments = [re.sub('>>\d{1,4}', "", comment.get_text(strip=True)) for comment in comment_elements]

    # sample youtube video url
    video_url = url
    # init an HTML Session
    session = HTMLSession()
    # get the html content
    response = session.get(video_url)
    # execute Java-script
    response.html.render(sleep=1)
    # create bs object to parse HTML
    soup = bs4(response.html.html, "html.parser")
    
    # CSVで出力
    Export_Csv1(title, comments)

# コメントをリストで抽出してcsvに出力する（あにまん掲示板:https://bbs.animanch.com/）
def pick_comment_animanch_bbs(url):
    # ページのHTMLを取得
    response = requests.get(url)
    response.encoding = 'UTF-8'
    html = response.content

    # BeautifulSoupで解析
    soup = BeautifulSoup(html, 'html.parser')

    # Winでファイルに使用できない文字を置換する
    title = re.sub(r'[\\/:*?"<>|]', '', soup.title.text) + '.csv'
    title = title.replace('\n', '').replace('\r', '')
    
    # 条件で抽出
    comment_elements = soup.select('div.resbody')
    comments = [re.sub('>>\d{1,4}', "", comment.get_text(strip=True)) for comment in comment_elements]
    
    # CSVで出力
    Export_Csv1(title, comments)

# コメントをリストで抽出してcsvに出力する（あにまんch（あにまん掲示板のまとめサイト）:https://animanch.com/）
def pick_comment_animanch(url):
    # ページのHTMLを取得
    response = requests.get(url)
    response.encoding = 'UTF-8'
    html = response.content

    # BeautifulSoupで解析
    soup = BeautifulSoup(html, 'html.parser')
    
    # Winでファイルに使用できない文字を置換する
    title = re.sub(r'[\\/:*?"<>|]', '', soup.title.text) + '.csv'
    title = title.replace('\n', '').replace('\r', '')
    
    # 条件で抽出
    comment_elements = soup.select('div.t_b')
    comments = [re.sub('>>\d{1,4}', "", comment.get_text(strip=True)) for comment in comment_elements]
    comment_elements2 = soup.select('div.commentbody')
    comments2 = [re.sub('>>\d{1,4}', "", comment.get_text(strip=True)) for comment in comment_elements2]
    
    # CSVで出力
    Export_Csv2(title, comments, comments2)

# コメントをリストで抽出してcsvに出力する（ねいろ速報:http://animesoku.com/）
def pick_comment_animesoku(url):
    # ページのHTMLを取得
    response = requests.get(url)
    response.encoding = 'UTF-8'
    html = response.content

    # BeautifulSoupで解析
    soup = BeautifulSoup(html, 'html.parser')
    
    # Winでファイルに使用できない文字を置換する
    title = re.sub(r'[\\/:*?"<>|]', '', soup.title.text) + '.csv'
    title = title.replace('\n', '').replace('\r', '')
    
    # 条件で抽出
    comment_elements = soup.select('div.t_h')
    comments = [re.sub('>>\d{1,4}', "", comment.get_text(strip=True)) for comment in comment_elements]
    
    # CSVで出力
    Export_Csv1(title, comments)

# コメントをリストで抽出してcsvに出力する（最強ジャンプ放送局:http://www.saikyo-jump.com/）
def pick_comment_saikyo_jump(url):

    # ページのHTMLを取得
    response = requests.get(url)
    response.encoding = 'UTF-8'
    html = response.content
    
    # BeautifulSoupで解析
    soup = BeautifulSoup(html, 'html.parser')
    
    # Winでファイルに使用できない文字を置換する
    title = re.sub(r'[\\/:*?"<>|]', '', soup.title.text) + '.csv'
    title = title.replace('\n', '').replace('\r', '')
    
    # 条件で抽出
    comment_elements = soup.select('div.t_b')
    comments = [re.sub('>>\d{1,4}', "", comment.get_text(strip=True)) for comment in comment_elements]
    comment_elements2 = soup.select('li.comment-body')
    comments2 = [re.sub('>>\d{1,4}', "", comment.get_text(strip=True)) for comment in comment_elements2]
    
    # CSVで出力
    Export_Csv2(title, comments, comments2)

# コメントをリストで抽出してcsvに出力する（ジャンプまとめ速報:https://jumpmatome2ch.biz/）
def pick_comment_jumpmatome2ch(url):
    # ページのHTMLを取得
    response = requests.get(url)
    response.encoding = 'UTF-8'
    html = response.content

    # BeautifulSoupで解析
    soup = BeautifulSoup(html, 'html.parser')

    # Winでファイルに使用できない文字を置換する
    title = re.sub(r'[\\/:*?"<>|]', '', soup.title.text) + '.csv'
    title = title.replace('\n', '').replace('\r', '')
    
    # 条件で抽出
    comment_elements = soup.select('div.t_b')
    comments = [re.sub('>>\d{1,4}', "", comment.get_text(strip=True)) for comment in comment_elements]

    commonlistcon = soup.select('div.comment-listCon')
    p_texts = []
    for con in commonlistcon:
        p_elements = con.select('p')
        for p in p_elements:
            p_texts.append(p.get_text(strip=True))
    comments2 = [re.sub('>>\d{1,4}', "", comment) for comment in p_texts]

    # CSVで出力
    Export_Csv2(title, comments, comments2)

# コメントをリストで抽出してcsvに出力する（ウマ娘BBS:https://umabbs.com/patio.cgi）
def pick_comment_umabbs(url):
    # ページのHTMLを取得
    response = requests.get(url)
    response.encoding = 'UTF-8'
    html = response.content

    # BeautifulSoupで解析
    soup = BeautifulSoup(html, 'html.parser')
    
    # Winでファイルに使用できない文字を置換する
    title = re.sub(r'[\\/:*?"<>|]', '', soup.title.text) + '.csv'
    title = title.replace('\n', '').replace('\r', '')
    
    # 条件で抽出
    comment_elements = soup.select('div.com-top')
    comments = [re.sub('>>\d{1,4}', "", comment.get_text(strip=True)) for comment in comment_elements]
    comment_elements2 = soup.select('div.com-res')
    comments2 = [re.sub('>>\d{1,4}', "", comment.get_text(strip=True)) for comment in comment_elements2]
    
    # CSVで出力
    Export_Csv2(title, comments, comments2)

# コメントをリストで抽出してcsvに出力する（うまぴょいチャンネル:http://umapch.blog.jp/）
def pick_comment_umapch(url):
    # ページのHTMLを取得
    response = requests.get(url)
    response.encoding = 'UTF-8'
    html = response.content

    # BeautifulSoupで解析
    soup = BeautifulSoup(html, 'html.parser')
    
    # Winでファイルに使用できない文字を置換する
    title = re.sub(r'[\\/:*?"<>|]', '', soup.title.text) + '.csv'
    title = title.replace('\n', '').replace('\r', '')
    
    # 条件で抽出
    comment_elements = soup.select('div.t_b')
    comments = [re.sub('>>\d{1,4}', "", comment.get_text(strip=True)) for comment in comment_elements]
    comment_elements2 = soup.select('li.comment-body')
    comments2 = [re.sub('>>\d{1,4}', "", comment.get_text(strip=True)) for comment in comment_elements2]
    
    # CSVで出力
    Export_Csv2(title, comments, comments2)

# コメントをリストで抽出してcsvに出力する（サカラボ:http://sakarabo.blog.jp/）
def pick_comment_sakarabo(url):
    # ページのHTMLを取得
    response = requests.get(url)
    response.encoding = 'UTF-8'
    html = response.content

    # BeautifulSoupで解析
    soup = BeautifulSoup(html, 'html.parser')
    
    # Winでファイルに使用できない文字を置換する
    title = re.sub(r'[\\/:*?"<>|]', '', soup.title.text) + '.csv'
    title = title.replace('\n', '').replace('\r', '')
    
    # 条件で抽出
    comment_elements = soup.select('div.t_b')
    comments = [re.sub('>>\d{1,4}', "", comment.get_text(strip=True)) for comment in comment_elements]
    comment_elements2 = soup.select('li.comment-body')
    comments2 = [re.sub('>>\d{1,4}', "", comment.get_text(strip=True)) for comment in comment_elements2]
    
    # CSVで出力
    Export_Csv2(title, comments, comments2)

# コメントをリストで抽出してcsvに出力する（ぽけりん:https://pokemon-matome.net/）
def pick_comment_pokemon_matome(url):
    # ページのHTMLを取得
    response = requests.get(url)
    response.encoding = 'UTF-8'
    html = response.content

    # BeautifulSoupで解析
    soup = BeautifulSoup(html, 'html.parser')
    
    # Winでファイルに使用できない文字を置換する
    title = re.sub(r'[\\/:*?"<>|]', '', soup.title.text) + '.csv'
    title = title.replace('\n', '').replace('\r', '')
    
    # 条件で抽出
    comment_elements = soup.select('div.a-b')
    comments = [re.sub('>>\d{1,4}', "", comment.get_text(strip=True)) for comment in comment_elements]
    comment_elements2 = soup.select('div.commentleft')
    comments2 = [re.sub('>>\d{1,4}', "", comment.get_text(strip=True)) for comment in comment_elements2]
    
    # CSVで出力
    Export_Csv2(title, comments, comments2)

# コメントをリストで抽出してcsvに出力する（ウマ娘まとめちゃんねる:https://umamusume.net/）
def pick_comment_umamusume(url):
    # ページのHTMLを取得
    response = requests.get(url)
    response.encoding = 'UTF-8'
    html = response.content

    # BeautifulSoupで解析
    soup = BeautifulSoup(html, 'html.parser')
    
    # Winでファイルに使用できない文字を置換する
    title = re.sub(r'[\\/:*?"<>|]', '', soup.title.text) + '.csv'
    title = title.replace('\n', '').replace('\r', '')
    
    # 条件で抽出
    comment_elements = soup.select('div.t_b')
    comments = [re.sub('>>\d{1,4}', "", comment.get_text(strip=True)) for comment in comment_elements]
    comment_elements2 = soup.select('li.body')
    comments2 = [re.sub('>>\d{1,4}', "", comment.get_text(strip=True)) for comment in comment_elements2]

    libody = soup.select('li.body')
    p_texts = []
    for body in libody:
        p_elements = body.select('p')
        for p in p_elements:
            p_texts.append(p.get_text(strip=True))
    comments2 = [re.sub(r"[>> \d{1,4}, >>\d{1,4}]", "", comment) for comment in p_texts]
    
    # CSVで出力
    Export_Csv2(title, comments, comments2)

def pick_comment(url):
    # ページのHTMLを取得
    response = requests.get(url)
    response.encoding = 'UTF-8'
    html = response.content

    # BeautifulSoupで解析
    soup = BeautifulSoup(html, 'html.parser')
    
    # Winでファイルに使用できない文字を置換する
    title = re.sub(r'[\\/:*?"<>|]', '', soup.title.text) + '.csv'
    title = title.replace('\n', '').replace('\r', '')
    
    # 条件で抽出
    comment_elements = soup.select('div.t_b')
    comments = [re.sub('>>\d{1,4}', "", comment.get_text(strip=True)) for comment in comment_elements]
    comment_elements2 = soup.select('div.commentbody')
    comments2 = [re.sub('>>\d{1,4}', "", comment.get_text(strip=True)) for comment in comment_elements2]
    
    # CSVで出力
    Export_Csv2(title, comments, comments2)

# URLのチェック
def CheckUrl(url):
    # ★2ch（5ch）:https://find.5ch.net/
    if "https://" in url and ".5ch.net/" in url:
        pick_comment_5ch(url)
        return True
    
    # ★Twitter:https://twitter.com/home -- 後で対応
    # elif "https://" in url and "https://twitter.com/" in url:
    #     pick_comment_twitter(url)
    #     return True

    # ★YouTubeコメント欄:https://www.youtube.com/ -- 後で対応
    elif "https://" in url and "https://www.youtube.com/" in url:
        pick_comment_youtube(url)
        return True
    
    # ★あにまん掲示板:https://bbs.animanch.com/
    elif "https://" in url and "https://bbs.animanch.com/" in url:
        pick_comment_animanch_bbs(url)
        return True
    
    # ★かころぐβ:https://kakolog.jp/ -- リンク先が5ch　過去記事は別途対応済み
    # elif "https://" in url and "https://kakolog.jp/" in url:
    #     pick_comment(url)
    
    # ★あにまんch（あにまん掲示板のまとめサイト）:https://animanch.com/
    elif "https://" in url and "https://animanch.com/" in url:
        pick_comment_animanch(url)
        return True
    
    # ★ねいろ速報:http://animesoku.com/
    elif "http://animesoku.com/" in url:
        pick_comment_animesoku(url)
        return True
    
    # ★5ちゃんねる:https://nova.5ch.net/livegalileo/ -- 5ch同様
    # elif "https://" in url and "https://nova.5ch.net/livegalileo/" in url:
    #     pick_comment(url)
    
    # ★5ちゃんねる/2ちゃんねる掲示板全文検索:https://www.zzzsearch.com/2ch/
        # 5ch.net（旧2ch.net)：
        # ５ちゃんねるを検索
        # おーぷん2ch：
        # おーぷん２ちゃんねるを検索
        # 2ch.sc：
        # 2ch.scを検索
        # 過去ログサイト：
        # mimizun.com等の複数の過去ログ保存サイトを検索
    # elif "https://" in url and "https://www.zzzsearch.com/2ch/" in url:
    #     pick_comment(url)

    # ★最強ジャンプ放送局:http://www.saikyo-jump.com/
    elif "http://www.saikyo-jump.com/" in url:
        pick_comment_saikyo_jump(url)
        return True
    
    # ★ジャンプまとめ速報:https://jumpmatome2ch.biz/
    elif "https://" in url and "https://jumpmatome2ch.biz/" in url:
        pick_comment_jumpmatome2ch(url)
        return True
    
    # ★ウマ娘BBS:https://umabbs.com/patio.cgi
    elif "https://" in url and "https://umabbs.com/patio.cgi" in url:
        pick_comment_umabbs(url)
        return True
    
    # ★うまぴょいチャンネル:http://umapch.blog.jp/
    elif "http://umapch.blog.jp/" in url:
        pick_comment_umapch(url)
        return True
    
    # ★サカラボ:http://sakarabo.blog.jp/
    elif "http://sakarabo.blog.jp/" in url:
        pick_comment_sakarabo(url)
        return True
    
    # ★ぽけりん:https://pokemon-matome.net/
    elif "https://" in url and "https://pokemon-matome.net/" in url:
        pick_comment_pokemon_matome(url)
        return True
    
    # ★ウマ娘まとめちゃんねる:https://umamusume.net/
    elif "https://" in url and "https://umamusume.net/" in url:
        pick_comment_umamusume(url)
        return True
    else:
        return False

# ユーザからの入力を受け付ける
print(version)
print("************************************************************************")
print("** 現在コメントの抽出に対応しているサイトは下記の通りです。")
print("**   - あにまんch:https://animanch.com/ -")
print("**   - あにまん掲示板 :https://bbs.animanch.com/ -")
print("**   - ねいろ速報:http://animesoku.com/ -")
print("**   - 5ちゃんねる:https://find.5ch.net/ -")
print("**   - かころぐβ:https://kakolog.jp/ -")
# print("**   - Youtubeコメント欄: -")
print("**   - 最強ジャンプ放送局:http://www.saikyo-jump.com/ -")
print("**   - ジャンプまとめ速報:https://jumpmatome2ch.biz/ -")
print("**   - うまぴょいチャンネル:http://umapch.blog.jp/ -")
print("**   - ウマ娘まとめちゃんねる:https://umamusume.net/ -")
print("**   - ウマ娘BBS:https://umabbs.com/patio.cgi -")
print("**   - ぽけりん:https://pokemon-matome.net/ -")
print("**   - サカラボ:http://sakarabo.blog.jp/ -")
print("************************************************************************")
url = input("抽出対象ページのURLを入力してください（URLをコピペしてEnterキーを押下してください）->")
# URLが抽出可能な対象かチェックする
if CheckUrl(url):
    print("抽出が完了しました。outputフォルダを確認してください")
    input("Enterキーを押下で終了します。")
else:
    print("対応していないURLです。抽出に失敗しました。")
    input("Enterキーを押下で終了します。")
