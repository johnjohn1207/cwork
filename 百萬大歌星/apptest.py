import streamlit as st
import random
import base64
import io
import re
import json
import os
import speech_recognition as sr
from streamlit_mic_recorder import mic_recorder

# --- 完整繁體歌詞庫 ---
FULL_LRC_DATABASE = {
    "太難": """
[00:19.49]愛太難 真心也難完美
[00:25.32]在愛情的世界最怕有人說累
[00:30.45]動了心容易醉 愛的深容易碎
[00:35.06]寂寞的滋味 為了誰
[00:40.22]情太難 真心話難婉轉
[00:45.60]看往事如煙片刻清醒的消散
[00:50.56]你的心在不在 還願不願等待
[00:55.22]原諒那對錯重新再來
[01:01.97]要忘記你太難
[01:04.46]一顆心相思難耐
[01:06.95]我不願讓等待變成一種遺憾
[01:11.97]真的愛心太亂
[01:14.62]一段情不必散
[01:17.71]我的愛願意為你而存在
[01:22.17]要忘記你太難
[01:24.70]一份愛何苦聚散
[01:27.19]我不願讓沉默變成一種寂寞
[01:32.26]愛情一旦落空
[01:34.80]還有什麼藉口
[01:38.00]能讓我再擁有你的笑容和天空
[02:10.51]情太難 真心話難婉轉
[02:16.40]看往事如煙片刻清醒的消散
[02:21.54]你的心在不在 還願不願等待
[02:26.21]原諒那對錯重新再來
[02:32.90]要忘記你太難
[02:35.39]一顆心相思難耐
[02:37.87]我不願讓等待變成一種遺憾
[02:43.10]真的愛心太亂
[02:45.48]一段情不必散
[02:48.63]我的愛願意為你而存在
[02:53.14]要忘記你太難
[02:55.68]一份愛何苦聚散
[02:58.11]我不願讓沉默變成一種寂寞
[03:03.13]愛情一旦落空
[03:05.67]還有什麼藉口
[03:08.87]能讓我再擁有你的笑容和天空
[03:18.30]要忘記你太難
[03:20.79]一顆心相思難耐
[03:23.38]我不願讓等待變成一種遺憾
[03:28.50]真的愛心太亂
[03:30.94]一段情不必散
[03:34.13]我的愛願意為你而存在
[03:38.55]要忘記你太難
[03:40.99]一份愛何苦聚散
[03:43.63]我不願讓沉默變成一種寂寞
[03:48.65]愛情一旦落空
[03:51.14]還有什麼藉口
[03:54.38]能讓我再擁有你的笑容和天空
"""
}

# --- 解析 LRC 成清單格式 ---
st.set_page_config(page_title="百萬大歌星", layout="wide")

# ==========================================
# 1. 遊戲資料庫與輔助函數 (請保留你完整的 90 首歌與 LRC)
# ==========================================
if 'SONG_DATABASE' not in st.session_state:
    st.session_state.SONG_DATABASE = {
        "秋天來了！": [
            {"title": "楓", "singer": "周杰倫", "year": "2005", "ans": "緩緩飄落的楓葉像思念", "file": "autumn_1.mp3"},
            {"title": "秋意濃", "singer": "張學友", "year": "1993", "ans": "離人心上秋意濃", "file": "autumn_2.mp3"},
            {"title": "秋天別來", "singer": "侯湘婷", "year": "1999", "ans": "秋天別來我還沒忘了你", "file": "autumn_3.mp3"}
        ],
        "經典秀場金曲": [
            {"title": "舞女", "singer": "陳小雲", "year": "1985", "ans": "搖來搖去", "file": "show_1.mp3"},
            {"title": "愛情恰恰", "singer": "陳小雲", "year": "1992", "ans": "繁華的夜都市", "file": "show_2.mp3"},
            {"title": "一代女皇", "singer": "金佩姍", "year": "1985", "ans": "娥眉聳參天", "file": "show_3.mp3"}
        ],
        "花之歌": [
            {"title": "玫瑰玫瑰我愛你", "singer": "姚莉", "year": "1940", "ans": "玫瑰玫瑰最嬌美", "file": "flower_1.mp3"},
            {"title": "魯冰花", "singer": "曾淑勤", "year": "1989", "ans": "閃閃的淚光魯冰花", "file": "flower_2.mp3"},
            {"title": "夜來香", "singer": "鄧麗君", "year": "1978", "ans": "我愛這夜色茫茫", "file": "flower_3.mp3"}
        ],
        "經典台語歌曲": [
            {"title": "愛拚才會贏", "singer": "葉啟田", "year": "1988", "ans": "三分天注定", "file": "tw_1.mp3"},
            {"title": "家後", "singer": "江蕙", "year": "2001", "ans": "有一工咱若老", "file": "tw_2.mp3"},
            {"title": "浪子回頭", "singer": "茄子蛋", "year": "2017", "ans": "菸一支一支一支的點", "file": "tw_3.mp3"}
        ],
        "70-80經典國語": [
            {"title": "太難", "singer": "鄭中基", "year": "1996", "ans": "一段情不必散", "file": "q1_challenge.mp3"},
            {"title": "恰似你的溫柔", "singer": "蔡琴", "year": "1980", "ans": "某年某月的某一天", "file": "old_2.mp3"},
            {"title": "一場遊戲一場夢", "singer": "王傑", "year": "1987", "ans": "為什麼道別離", "file": "old_3.mp3"}
        ],
        "懷舊電影主題曲": [
            {"title": "那些年", "singer": "胡夏", "year": "2011", "ans": "那些年錯過的大雨", "file": "movie_1.mp3"},
            {"title": "酒矸倘賣無", "singer": "蘇芮", "year": "1983", "ans": "多麼熟悉的聲音", "file": "movie_2.mp3"},
            {"title": "新不了情", "singer": "萬芳", "year": "1993", "ans": "回憶過去痛苦的相思忘不了", "file": "movie_3.mp3"}
        ],
        "台灣味飲料歌曲": [
            {"title": "爺爺泡的茶", "singer": "周杰倫", "year": "2002", "ans": "有一種味道叫做家", "file": "drink_1.mp3"},
            {"title": "半糖主義", "singer": "S.H.E", "year": "2003", "ans": "只要半糖的溫柔", "file": "drink_2.mp3"},
            {"title": "咖啡", "singer": "張學友", "year": "2002", "ans": "太濃了吧", "file": "drink_3.mp3"}
        ],
        "懷舊民謠": [
            {"title": "丟丟銅仔", "singer": "台灣民謠", "year": "1943", "ans": "火車行到伊都", "file": "folk_1.mp3"},
            {"title": "望春風", "singer": "台灣民謠", "year": "1933", "ans": "獨夜無伴守燈下", "file": "folk_2.mp3"},
            {"title": "雨夜花", "singer": "台灣民謠", "year": "1934", "ans": "受風雨吹落地", "file": "folk_3.mp3"}
        ],
        "小鄧金曲": [
            {"title": "月亮代表我的心", "singer": "鄧麗君", "year": "1977", "ans": "月亮代表我的心", "file": "teresa_1.mp3"},
            {"title": "甜蜜蜜", "singer": "鄧麗君", "year": "1979", "ans": "你笑得甜蜜蜜", "file": "teresa_2.mp3"},
            {"title": "我只在乎你", "singer": "鄧麗君", "year": "1987", "ans": "心甘情願感染你的氣息", "file": "teresa_3.mp3"}
        ],
        "動漫熱血魂": [
            {"title": "紅蓮華", "singer": "LiSA", "year": "2019", "ans": "ありがとう 悲しみよ", "file": "anime_1.mp3"},
            {"title": "直到世界的盡頭", "singer": "WANDS", "year": "1994", "ans": "世界が終るまでは", "file": "anime_2.mp3"},
            {"title": "Butter-Fly", "singer": "和田光司", "year": "1999", "ans": "無限大な夢のあとの", "file": "anime_3.mp3"}
        ],
        "情歌對唱": [
            {"title": "屋頂", "singer": "吳宗憲/溫嵐", "year": "1999", "ans": "在屋頂唱著你的歌", "file": "duet_1.mp3"},
            {"title": "珊瑚海", "singer": "周杰倫/Lara", "year": "2005", "ans": "海鳥跟魚相愛", "file": "duet_2.mp3"},
            {"title": "今天妳要嫁給我", "singer": "陶喆/蔡依林", "year": "2006", "ans": "聽我說手牽手", "file": "duet_3.mp3"}
        ],
        "數字歌": [
            {"title": "十年", "singer": "陳奕迅", "year": "2003", "ans": "十年之前", "file": "num_1.mp3"},
            {"title": "七里香", "singer": "周杰倫", "year": "2004", "ans": "雨下整夜", "file": "num_2.mp3"},
            {"title": "零", "singer": "柯有倫", "year": "2005", "ans": "零的溫存", "file": "num_3.mp3"}
        ],
        "地名歌曲": [
            {"title": "鹿港小鎮", "singer": "羅大佑", "year": "1982", "ans": "台北不是我的家", "file": "place_1.mp3"},
            {"title": "忠孝東路走九遍", "singer": "動力火車", "year": "2001", "ans": "忠孝東路走九遍", "file": "place_2.mp3"},
            {"title": "挪威的森林", "singer": "伍佰", "year": "1996", "ans": "讓我將妳心兒摘下", "file": "place_3.mp3"}
        ],
        "顏色歌曲": [
            {"title": "紅豆", "singer": "王菲", "year": "1998", "ans": "還沒為你把紅豆", "file": "color_1.mp3"},
            {"title": "白月光", "singer": "張信哲", "year": "2004", "ans": "白月光心裡某個地方", "file": "color_2.mp3"},
            {"title": "黑色幽默", "singer": "周杰倫", "year": "2000", "ans": "不懂你的黑色幽默", "file": "color_3.mp3"}
        ],
        "天氣系列": [
            {"title": "聽海", "singer": "張惠妹", "year": "1997", "ans": "寫信告訴我今天海是什麼顏色", "file": "weather_1.mp3"},
            {"title": "晴天", "singer": "周杰倫", "year": "2003", "ans": "故事的小黃花", "file": "weather_2.mp3"},
            {"title": "雨一直下", "singer": "張宇", "year": "1999", "ans": "雨一直下氣氛不算融洽", "file": "weather_3.mp3"}
        ],
        "校園民歌": [
            {"title": "外婆的澎湖灣", "singer": "潘安邦", "year": "1979", "ans": "陽光沙灘海浪仙人掌", "file": "campus_1.mp3"},
            {"title": "童年", "singer": "張艾嘉", "year": "1981", "ans": "池塘邊的榕樹上", "file": "campus_2.mp3"},
            {"title": "鄉間的小路", "singer": "葉佳修", "year": "1979", "ans": "走在鄉間的小路上", "file": "campus_3.mp3"}
        ],
        "舞曲大帝國": [
            {"title": "不如跳舞", "singer": "陳慧琳", "year": "2000", "ans": "聊天倒不如跳舞", "file": "dance_1.mp3"},
            {"title": "眉飛色舞", "singer": "鄭秀文", "year": "2000", "ans": "愛的是非對錯已太多", "file": "dance_2.mp3"},
            {"title": "姐姐", "singer": "謝金燕", "year": "2013", "ans": "叫我姐姐", "file": "dance_3.mp3"}
        ],
        "失戀陣線聯盟": [
            {"title": "失戀陣線聯盟", "singer": "草蜢", "year": "1990", "ans": "找一個承認失戀的方法", "file": "breakup_1.mp3"},
            {"title": "分手快樂", "singer": "梁靜茹", "year": "2002", "ans": "分手快樂祝妳快樂", "file": "breakup_2.mp3"},
            {"title": "說謊", "singer": "林宥嘉", "year": "2009", "ans": "我沒有說謊", "file": "breakup_3.mp3"}
        ],
        "勵志金曲": [
            {"title": "隱形的翅膀", "singer": "張韶涵", "year": "2006", "ans": "我知道我一直有雙隱形的翅膀", "file": "inspire_1.mp3"},
            {"title": "我的未來不是夢", "singer": "張雨生", "year": "1988", "ans": "我知道我的未來不是夢", "file": "inspire_2.mp3"},
            {"title": "倔強", "singer": "五月天", "year": "2004", "ans": "我就是我自己的神", "file": "inspire_3.mp3"}
        ],
        "搖滾之夜": [
            {"title": "離歌", "singer": "信樂團", "year": "2003", "ans": "想留不能留才最寂寞", "file": "rock_1.mp3"},
            {"title": "自由", "singer": "張震嶽", "year": "1998", "ans": "說愛我說愛我", "file": "rock_2.mp3"},
            {"title": "派對動物", "singer": "五月天", "year": "2016", "ans": "Let's go party party all night", "file": "rock_3.mp3"}
        ],
        "超級英雄": [
            {"title": "孤勇者", "singer": "陳奕迅", "year": "2021", "ans": "誰說站在光裡的才算英雄", "file": "hero_1.mp3"},
            {"title": "超人", "singer": "五月天", "year": "2004", "ans": "為什麼拯救地球是那麼容易", "file": "hero_2.mp3"},
            {"title": "無敵鐵金剛", "singer": "盧廣仲", "year": "2009", "ans": "我要變身無敵鐵金剛", "file": "hero_3.mp3"}
        ],
        "迪士尼系列": [
            {"title": "Let It Go", "singer": "Idina Menzel", "year": "2013", "ans": "Let it go let it go", "file": "disney_1.mp3"},
            {"title": "A Whole New World", "singer": "Peabo Bryson", "year": "1992", "ans": "A whole new world", "file": "disney_2.mp3"},
            {"title": "Under the Sea", "singer": "Samuel E. Wright", "year": "1989", "ans": "Under the sea", "file": "disney_3.mp3"}
        ],
        "周杰倫專場": [
            {"title": "告白氣球", "singer": "周杰倫", "year": "2016", "ans": "親愛的愛上你從那天起", "file": "jay_1.mp3"},
            {"title": "稻香", "singer": "周杰倫", "year": "2008", "ans": "回到最初的美好", "file": "jay_2.mp3"},
            {"title": "青花瓷", "singer": "周杰倫", "year": "2007", "ans": "天青色等煙雨", "file": "jay_3.mp3"}
        ],
        "五月天專場": [
            {"title": "突然好想你", "singer": "五月天", "year": "2008", "ans": "突然好想你", "file": "mayday_1.mp3"},
            {"title": "溫柔", "singer": "五月天", "year": "2000", "ans": "不打擾是我的溫柔", "file": "mayday_2.mp3"},
            {"title": "傷心的人別聽慢歌", "singer": "五月天", "year": "2013", "ans": "我不管你是誰的誰", "file": "mayday_3.mp3"}
        ],
        "四大天王": [
            {"title": "吻別", "singer": "張學友", "year": "1993", "ans": "我和你吻別", "file": "king_1.mp3"},
            {"title": "忘情水", "singer": "劉德華", "year": "1994", "ans": "給我一杯忘情水", "file": "king_2.mp3"},
            {"title": "對你愛不完", "singer": "郭富城", "year": "1990", "ans": "對你愛愛愛不完", "file": "king_3.mp3"}
        ],
        "名字歌曲": [
            {"title": "小薇", "singer": "黃品源", "year": "2002", "ans": "有一個美麗的小女孩", "file": "name_1.mp3"},
            {"title": "志明與春嬌", "singer": "五月天", "year": "1999", "ans": "走到淡水的海岸", "file": "name_2.mp3"},
            {"title": "曹操", "singer": "林俊傑", "year": "2006", "ans": "說曹操曹操就到", "file": "name_3.mp3"}
        ],
        "食物歌曲": [
            {"title": "豆漿油條", "singer": "林俊傑", "year": "2004", "ans": "喝純白的豆漿", "file": "food_1.mp3"},
            {"title": "麥芽糖", "singer": "周杰倫", "year": "2005", "ans": "我牽著你的手經過", "file": "food_2.mp3"},
            {"title": "咖哩咖哩", "singer": "牛奶咖啡", "year": "2017", "ans": "泰國新加坡印度尼西亞", "file": "food_3.mp3"}
        ],
        "交通工具": [
            {"title": "單車", "singer": "陳奕迅", "year": "2001", "ans": "任世間怨我壞", "file": "transport_1.mp3"},
            {"title": "腳踏車", "singer": "王識賢", "year": "2004", "ans": "繞來繞去騎", "file": "transport_2.mp3"},
            {"title": "火車", "singer": "羅大佑", "year": "1991", "ans": "火車火車行崎腳", "file": "transport_3.mp3"}
        ],
        "動物世界": [
            {"title": "蝸牛", "singer": "周杰倫", "year": "1999", "ans": "我要一步一步往上爬", "file": "animal_1.mp3"},
            {"title": "蝴蝶飛呀", "singer": "小虎隊", "year": "1991", "ans": "蝴蝶飛呀", "file": "animal_2.mp3"},
            {"title": "學貓叫", "singer": "小潘潘", "year": "2018", "ans": "我們一起學貓叫", "file": "animal_3.mp3"}
        ],
        "星空系列": [
            {"title": "星星點燈", "singer": "鄭智化", "year": "1992", "ans": "星星點燈照亮我的家門", "file": "star_1.mp3"},
            {"title": "星晴", "singer": "周杰倫", "year": "2000", "ans": "一步兩步三步四步望著天", "file": "star_2.mp3"},
            {"title": "夜空中最亮的星", "singer": "逃跑計劃", "year": "2011", "ans": "夜空中最亮的星", "file": "star_3.mp3"}
        ]
    }

if 'all_themes' not in st.session_state:
    st.session_state.all_themes = {
        "秋天來了！": "🍂", "經典秀場金曲": "💃", "花之歌": "🌸", "經典台語歌曲": "📻",
        "70-80經典國語": "🎙️", "懷舊電影主題曲": "🎬", "台灣味飲料歌曲": "🥤", "懷舊民謠": "🪕",
        "小鄧金曲": "🌹", "動漫熱血魂": "🔥", "情歌對唱": "👩‍❤️‍👨", "數字歌": "1️⃣",
        "地名歌曲": "🗺️", "顏色歌曲": "🎨", "天氣系列": "☁️", "校園民歌": "🎸",
        "舞曲大帝國": "🕺", "失戀陣線聯盟": "💔", "勵志金曲": "🌈", "搖滾之夜": "🤘",
        "超級英雄": "🦸", "迪士尼系列": "🏰", "周杰倫專場": "🎹", "五月天專場": "🖐️",
        "四大天王": "👑", "名字歌曲": "🆔", "食物歌曲": "🍕", "交通工具": "🚲",
        "動物世界": "🐼", "星空系列": "✨"
    }

def parse_lrc_to_list(lrc_text):
    lyrics = []
    pattern = r"\[(\d+):(\d+\.\d+)\](.*)"
    for line in lrc_text.strip().split('\n'):
        match = re.search(pattern, line)
        if match:
            m, s, text = match.groups()
            lyrics.append({"time": int(m)*60 + float(s), "text": text.strip()})
    return lyrics

# 獎金階梯陣列 (從第一關到第十關)
PRIZES = [3000, 6000, 9000, 12000, 20000, 30000, 60000, 100000, 150000, 300000]

# ==========================================
# 2. 狀態初始化 (新增過關紀錄)
# ==========================================
if 'display_themes' not in st.session_state:
    st.session_state.display_themes = random.sample(list(st.session_state.all_themes.keys()), 10)
if 'page' not in st.session_state:
    st.session_state.page = "lobby"
if 'selected_song' not in st.session_state:
    st.session_state.selected_song = None
    
# 🌟 新增：遊戲闖關進度變數
if 'current_level' not in st.session_state:
    st.session_state.current_level = 0 # 0代表準備挑戰 $3000，9代表準備挑戰 $300,000
if 'completed_themes' not in st.session_state:
    st.session_state.completed_themes = [] # 儲存已經過關的主題
if 'answered' not in st.session_state:
    st.session_state.answered = False # 記錄是否已經按下交卷

st.markdown("<style>.stApp { background-color: #B2225F; }</style>", unsafe_allow_html=True)

# ==========================================
# 【第一層：大廳】 (動態獎金梯 + 主題反灰)
# ==========================================
def show_lobby():
    st.markdown("<h1 style='text-align: center; color: white; text-shadow: 2px 2px 4px #000;'>🌟 百萬大歌星 🌟</h1>", unsafe_allow_html=True)
    main_col1, main_col2 = st.columns([1, 4])
    
    with main_col1:
        # 🌟 動態生成獎金階梯
        ladder_html = ""
        for i in range(9, -1, -1):
            if i == st.session_state.current_level:
                # 當前挑戰關卡：變大、變金黃色
                ladder_html += f'<div style="background-color: #FFD700; color: #8B0000; font-weight: bold; font-size: 20px; text-align: center; border: 3px solid white; padding: 8px; border-radius: 5px; margin: 3px 0; transform: scale(1.05); box-shadow: 0 0 10px #FFD700;">${PRIZES[i]:,}</div>'
            elif i < st.session_state.current_level:
                # 已經通過的關卡：變成綠色顯示達成
                ladder_html += f'<div style="background-color: #2E8B57; color: white; text-align: center; border: 1px solid white; padding: 5px; border-radius: 5px; margin: 2px 0; opacity: 0.8;">${PRIZES[i]:,} (達成)</div>'
            else:
                # 還沒到的關卡：深紅色
                ladder_html += f'<div style="background-color: #8B0000; color: white; text-align: center; border: 1px solid white; padding: 5px; border-radius: 5px; margin: 2px 0;">${PRIZES[i]:,}</div>'
                
        st.markdown(f"""
            <div style="background-color: #E9967A; padding: 10px; border-radius: 10px; border: 4px solid #8B4513; height: 600px; display: flex; flex-direction: column; justify-content: space-around;">
                <div style="color: #8B4513; text-align: center; font-weight: bold; font-size: 20px;">獎金累積</div>
                {ladder_html}
            </div>
        """, unsafe_allow_html=True)
        
        st.write("")
        if st.button("🔄 換一批 (已過關不會重置)"):
            # 確保換一批時，把已經過關的也算進去，不影響機制
            st.session_state.display_themes = random.sample(list(st.session_state.all_themes.keys()), 10)
            st.rerun()

    with main_col2:
        st.markdown("""
            <style>
            div.stButton > button { background-color: #FF69B4 !important; color: white !important; border-radius: 15px !important; border: 3px solid #FFC0CB !important; font-size: 22px !important; font-weight: bold !important; height: 80px !important; width: 100% !important; margin-bottom: 10px !important; box-shadow: 2px 2px 5px rgba(0,0,0,0.3) !important; display: flex !important; align-items: center !important; justify-content: center !important; transition: 0.2s;}
            div.stButton > button:hover:not(:disabled) { background-color: #FF1493 !important; color: yellow !important; transform: scale(1.02); }
            [data-testid="column"] { flex: 1 1 0% !important; min-width: 0 !important; }
            </style>
        """, unsafe_allow_html=True)
        st.markdown("<h2 style='text-align: center; color: #FFD700; margin-bottom: 20px;'>請選擇挑戰主題</h2>", unsafe_allow_html=True)
        
        display_keys = st.session_state.display_themes
        for i in range(0, 10, 2):
            c1, c2 = st.columns(2)
            with c1:
                t1 = display_keys[i]
                # 🌟 核心：如果這個主題在 completed_themes 裡，按鈕就 disabled (變暗且不能點)
                is_disabled1 = t1 in st.session_state.completed_themes
                if st.button(f"{st.session_state.all_themes[t1]} {t1}", key=f"t{i}", disabled=is_disabled1):
                    st.session_state.selected_theme = t1
                    st.session_state.page = "song_list"
                    st.rerun()
            with c2:
                if i+1 < 10:
                    t2 = display_keys[i+1]
                    is_disabled2 = t2 in st.session_state.completed_themes
                    if st.button(f"{st.session_state.all_themes[t2]} {t2}", key=f"t{i+1}", disabled=is_disabled2):
                        st.session_state.selected_theme = t2
                        st.session_state.page = "song_list"
                        st.rerun()

# ==========================================
# 【第二層：歌曲清單】
# ==========================================
def show_song_list():
    theme = st.session_state.selected_theme
    songs = st.session_state.SONG_DATABASE.get(theme, [])

    col_l, col_m, col_r = st.columns([1, 2, 1])
    with col_m:
        if st.button("⬅️ 返回大廳", key="back_to_lobby"):
            st.session_state.page = "lobby"
            st.rerun()
            
        st.write("") 
        st.markdown("""
            <style>
            div.stButton > button { background: linear-gradient(180deg, #E85A9F 0%, #C71585 100%) !important; border: 3px solid #FFC0CB !important; border-radius: 15px !important; padding: 20px 0 !important; height: auto !important; width: 100% !important; box-shadow: 3px 3px 8px rgba(0,0,0,0.4) !important; }
            div.stButton > button:hover { background: #FF1493 !important; border-color: #FFFFFF !important; transform: scale(1.03); }
            div.stButton > button p, div.stButton > button div { white-space: pre-line !important; font-size: 22px !important; font-weight: bold !important; line-height: 1.5 !important; text-shadow: 2px 2px 4px rgba(0,0,0,0.6) !important; margin: 0 !important; }
            </style>
        """, unsafe_allow_html=True)

        for i, song in enumerate(songs):
            btn_text = f"🎵 {song['title']}\n🎤 {song['singer']}\n💿 {song['year']}"
            if st.button(btn_text, key=f"song_btn_{i}"):
                st.session_state.selected_song = song
                st.session_state.use_hint = False
                
                # 🎲 隨機接唱引擎啟動！
                if song["title"] in FULL_LRC_DATABASE:
                    full_lrc = FULL_LRC_DATABASE[song["title"]]
                    lrc_list = parse_lrc_to_list(full_lrc)
                    
                    # 從第 4 句到最後一句之間隨機挑一個「目標接唱句」
                    target_idx = random.randint(3, len(lrc_list) - 1)
                    
                    # 記錄隨機抽出的結果
                    st.session_state.target_ans = lrc_list[target_idx]["text"]
                    st.session_state.stop_time = lrc_list[target_idx]["time"]
                    # 往前抓 3 句當作前奏起點
                    st.session_state.start_time = lrc_list[target_idx - 3]["time"] 
                    st.session_state.lyrics_json = json.dumps(lrc_list, ensure_ascii=False)
                else:
                    # 如果該首歌還沒建好完整歌詞，走預設邏輯
                    st.session_state.target_ans = song["ans"]
                    st.session_state.stop_time = 999
                    st.session_state.start_time = 0
                    st.session_state.lyrics_json = "[]"
                
                st.session_state.page = "game"
                st.rerun()


# ==========================================
# 【第三層：遊戲畫面 (過關/失敗結算版)】
# ==========================================
def show_game():
    song = st.session_state.selected_song
    st.markdown(f"<h1 style='color: white; text-align: center;'>🎤 挑戰：{song['title']}</h1>", unsafe_allow_html=True)
    st.markdown(f"<h4 style='color: #FFD700; text-align: center;'>挑戰獎金：${PRIZES[st.session_state.current_level]:,}</h4>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("⬅️ 放棄挑戰，重選歌曲", use_container_width=True):
            st.session_state.page = "song_list"
            st.session_state.hint_data = None
            st.session_state.answered = False # 確保重置交卷狀態
            
            # 🧹 清空輸入框的殘留記憶！
            if 'final_ans_input' in st.session_state: 
                del st.session_state['final_ans_input']
            if 'hidden_ans_input' in st.session_state: 
                del st.session_state['hidden_ans_input']
                
            st.rerun()

    # 如果還沒按交卷，才顯示遊戲與語音畫面
    if not st.session_state.answered:
        user_voice_raw = st.text_input("hidden_ans", key="hidden_ans_input", label_visibility="collapsed")
        
        audio_file = song["file"]
        if os.path.exists(audio_file):
            with open(audio_file, "rb") as f:
                audio_base64 = base64.b64encode(f.read()).decode()
                
            start_time = st.session_state.get("start_time", 0)
            stop_time = st.session_state.get("stop_time", 999)
            target_ans = st.session_state.get("target_ans", song["ans"])
            lyrics_json = st.session_state.get("lyrics_json", "[]")
            
            # 處理提示資料
            ans_clean = target_ans.replace(" ", "")
            ans_length = len(ans_clean)
            
            hint_data_json = "null"
            if st.session_state.get("hint_data"):
                hint_data_json = json.dumps(st.session_state.hint_data)

            # ⚡ 結合掃描動畫與即時語音的超級 JS 面板
            st.components.v1.html(f"""
                <div style="background-color: #1E1E1E; padding: 20px; border-radius: 15px; text-align: center; border: 3px solid #FF9800; box-shadow: 0 0 15px #FF9800;">
                    <audio id="myAudio" controls style="width: 100%; margin-bottom: 15px;">
                        <source src="data:audio/mp3;base64,{audio_base64}" type="audio/mp3">
                    </audio>
                    
                    <div style="min-height: 80px; display: flex; align-items: center; justify-content: center;">
                        <h1 id="lyricText" style="color: #FFFFFF; font-family: '微軟正黑體'; font-size: 36px; margin: 0; text-shadow: 2px 2px 4px #000; letter-spacing: 5px;">🎵 準備開始...</h1>
                    </div>
                    
                    <div style="min-height: 50px; margin-top: 10px;">
                        <h2 id="singingText" style="color: #00FF00; font-family: '微軟正黑體'; font-size: 28px; margin: 0; text-shadow: 1px 1px 3px #000;"></h2>
                    </div>
                    
                    <button id="micBtn" style="margin-top: 15px; background-color: #DC143C; color: white; border: 2px solid white; border-radius: 25px; padding: 10px 30px; font-size: 20px; font-weight: bold; cursor: pointer; display: none;">
                        🎙️ 點擊開始接唱
                    </button>
                </div>

                <script>
                    const lyrics = {lyrics_json};
                    const audio = document.getElementById('myAudio');
                    const lyricText = document.getElementById('lyricText');
                    const singingText = document.getElementById('singingText');
                    const micBtn = document.getElementById('micBtn');
                    
                    const stopTime = {stop_time};
                    const targetAns = "{target_ans}";
                    const ansLength = {ans_length};
                    const hintData = {hint_data_json}; 
                    
                    let isStopped = false;
                    if (!window.currentStarsArray) {{
                        window.currentStarsArray = Array(ansLength).fill("★");
                    }}

                    audio.addEventListener('loadedmetadata', () => {{ audio.currentTime = {start_time}; }});

                    audio.ontimeupdate = function() {{
                        if (audio.currentTime >= stopTime && !isStopped) {{
                            audio.pause();
                            isStopped = true;
                            micBtn.style.display = "inline-block";
                            
                            if (hintData) {{
                                playScanningHint(hintData.idx, hintData.char);
                            }} else {{
                                lyricText.innerText = window.currentStarsArray.join(" ");
                                lyricText.style.color = "#FFFFFF";
                            }}
                            return;
                        }}

                        if (!isStopped) {{
                            let currentText = "🎵 請點擊播放...";
                            for (let i = 0; i < lyrics.length; i++) {{
                                if (audio.currentTime >= lyrics[i].time) currentText = lyrics[i].text;
                                else break;
                            }}
                            if (currentText === targetAns) {{
                                currentText = window.currentStarsArray.join(" ");
                                lyricText.style.color = "#FFFFFF";
                            }} else {{
                                lyricText.style.color = "#FF9800";
                            }}
                            lyricText.innerText = currentText;
                        }}
                    }};

                    // --- 🌟 輪迴掃描動畫 ---
                    function playScanningHint(targetIdx, finalChar) {{
                        let currentPos = 0;
                        let loops = 3; 
                        let totalSteps = (loops * ansLength) + targetIdx; 
                        let step = 0;
                        
                        let interval = setInterval(() => {{
                            let htmlStr = "";
                            for(let i = 0; i < ansLength; i++) {{
                                if (step === totalSteps && i === targetIdx) {{
                                    htmlStr += `<span style='color: #FFD700; text-shadow: 0 0 10px #FFD700;'>${{finalChar}}</span> `;
                                }} else if (step < totalSteps && i === currentPos) {{
                                    htmlStr += `<span style='color: #FFD700;'>★</span> `;
                                }} else {{
                                    let charColor = window.currentStarsArray[i] === "★" ? "#FFFFFF" : "#FFD700";
                                    htmlStr += `<span style='color: ${{charColor}};'>${{window.currentStarsArray[i]}}</span> `;
                                }}
                            }}
                            lyricText.innerHTML = htmlStr;

                            if (step === totalSteps) {{
                                clearInterval(interval);
                                window.currentStarsArray[targetIdx] = finalChar; 
                            }} else {{
                                currentPos = (currentPos + 1) % ansLength; 
                                step++;
                            }}
                        }}, 80);
                    }}

                    // --- 🎙️ 語音辨識與畫面互動 ---
                    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
                    if (SpeechRecognition) {{
                        const recognition = new SpeechRecognition();
                        recognition.continuous = true;  
                        recognition.interimResults = true; 
                        recognition.lang = 'zh-TW';

                        micBtn.onclick = () => {{
                            recognition.start();
                            micBtn.innerText = "🔴 收音中... (唱完再次點擊)";
                            micBtn.style.backgroundColor = "#8B0000";
                            micBtn.onclick = () => {{ recognition.stop(); }};
                        }};

                        recognition.onresult = (event) => {{
                            let interimTranscript = '';
                            let finalTranscript = '';
                            for (let i = event.resultIndex; i < event.results.length; ++i) {{
                                if (event.results[i].isFinal) finalTranscript += event.results[i][0].transcript;
                                else interimTranscript += event.results[i][0].transcript;
                            }}
                            singingText.innerText = finalTranscript + interimTranscript;
                        }};

                        recognition.onend = () => {{
                            micBtn.innerText = "✅ 已記錄！請在下方確認並交卷";
                            micBtn.style.backgroundColor = "#228B22";
                            const finalResult = singingText.innerText;
                            
                            // 💡 把唱出來的字，安全地丟進下方的 Streamlit 輸入框
                            const inputs = window.parent.document.querySelectorAll('input');
                            for (let i = 0; i < inputs.length; i++) {{
                                if (inputs[i].getAttribute('aria-label') === '你的接唱答案：') {{
                                    let nativeInputValueSetter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, "value").set;
                                    nativeInputValueSetter.call(inputs[i], finalResult);
                                    inputs[i].dispatchEvent(new Event('input', {{ bubbles: true }}));
                                    break;
                                }}
                            }}
                        }};
                    }} else {{
                        micBtn.innerText = "⚠️ 你的瀏覽器不支援即時語音";
                    }}
                </script>
            """, height=380)
        else:
            st.error(f"❌ 找不到音檔 `{audio_file}`。")


        st.divider()
        ans_col, tool_col = st.columns([2, 1])
        with tool_col:
            st.markdown("<h3 style='color: white;'>🛠️ 求救錦囊</h3>", unsafe_allow_html=True)
            if st.button("🔤 一字提示", use_container_width=True):
                ans_clean = target_ans.replace(" ", "")
                random_idx = random.randint(0, len(ans_clean) - 1)
                st.session_state.hint_data = {"idx": random_idx, "char": ans_clean[random_idx]}
                st.rerun()# ... (老虎機提示邏輯)
                pass

        with ans_col:
            st.markdown("<h3 style='color: #FFD700;'>🤔 確定嗎？這就是你的答案？</h3>", unsafe_allow_html=True)
            user_final_ans = st.text_input("你的接唱答案：", key="final_ans_input")
            
            # 🌟 確定交卷按鈕
            if st.button("✅ 確定交卷！", use_container_width=True):
                if user_final_ans:
                    target_ans = st.session_state.target_ans
                    target_ans_clean = target_ans.replace(" ", "")
                    
                    # 進行判定，並記錄結果
                    st.session_state.answered = True
                    if target_ans_clean in user_final_ans.replace(" ", ""):
                        st.session_state.is_correct = True
                        # 答對了：加入已挑戰清單、等級 +1
                        st.session_state.completed_themes.append(st.session_state.selected_theme)
                        st.session_state.current_level += 1
                    else:
                        st.session_state.is_correct = False
                        
                    st.rerun() # 重新整理畫面進入結算區
                else:
                    st.warning("⚠️ 你還沒有填寫答案喔！")
    
    # 🌟 玩家已交卷，進入結算畫面
    else:
        st.divider()
        target_ans = st.session_state.target_ans
        
        # 🟢 答對邏輯
        if st.session_state.is_correct:
            st.markdown(f"""
                <div style='background-color: #2E8B57; color: white; padding: 30px; border-radius: 15px; text-align: center; border: 5px solid #FFD700;'>
                    <h1 style='font-size: 50px;'>🎉 恭喜過關！</h1>
                    <h3>正確歌詞：『{target_ans}』</h3>
                    <h2 style='color: #FFD700;'>準備挑戰下一階段獎金！</h2>
                </div>
            """, unsafe_allow_html=True)
            st.balloons()
            
            # 判斷是否已經全破 (10關全過)
            # 判斷是否已經全破 (10關全過)
            if st.session_state.current_level >= 10:
                st.markdown("<h1 style='color: yellow; text-align: center;'>🏆 太神啦！你贏得了三十萬大獎！ 🏆</h1>", unsafe_allow_html=True)
            else:
                st.write("")
                col_b1, col_b2, col_b3 = st.columns([1, 2, 1])
                with col_b2:
                    if st.button("➡️ 返回大廳挑選下一關", use_container_width=True):
                        st.session_state.page = "lobby"
                        st.session_state.hint_data = None
                        st.session_state.answered = False # 確保重置交卷狀態
                        
                        # 🧹 清空輸入框的殘留記憶！
                        if 'final_ans_input' in st.session_state: 
                            del st.session_state['final_ans_input']
                        if 'hidden_ans_input' in st.session_state: 
                            del st.session_state['hidden_ans_input']
                            
                        st.rerun()
                        
        # 🔴 答錯邏輯 (獎金折半)
        else:
            # 計算折半獎金
            if st.session_state.current_level == 0:
                final_prize = 0 # 第一關就錯，獎金 0
            else:
                # 拿前一關的獎金折半
                final_prize = PRIZES[st.session_state.current_level - 1] // 2
                
            st.markdown(f"""
                <div style='background-color: #8B0000; color: white; padding: 30px; border-radius: 15px; text-align: center; border: 5px solid white;'>
                    <h1 style='font-size: 50px;'>❌ 挑戰失敗！</h1>
                    <h3>正確歌詞應該是：『{target_ans}』</h3>
                    <h2 style='color: #FFD700;'>結算獎金：${final_prize:,}</h2>
                </div>
            """, unsafe_allow_html=True)
            
            st.write("")
            col_b1, col_b2, col_b3 = st.columns([1, 2, 1])
            with col_b2:
                if st.button("🏠 遊戲結束，返回大廳重新開始", use_container_width=True):
                    # 重新開始，把所有狀態歸零！
                    st.session_state.current_level = 0
                    st.session_state.completed_themes = []
                    st.session_state.page = "lobby"
                    st.session_state.hint_data = None
                    st.session_state.display_themes = random.sample(list(st.session_state.all_themes.keys()), 10)
                    
                    st.session_state.answered = False # 徹底重置交卷狀態
                    
                    # 🧹 清空輸入框的殘留記憶！(最關鍵的就是這裡)
                    if 'final_ans_input' in st.session_state: 
                        del st.session_state['final_ans_input']
                    if 'hidden_ans_input' in st.session_state: 
                        del st.session_state['hidden_ans_input']
                        
                    st.rerun()

# --- 路由執行 ---
if st.session_state.page == "lobby":
    show_lobby()
elif st.session_state.page == "song_list":
    show_song_list()
else:
    show_game()