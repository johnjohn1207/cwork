import requests
import csv
import time
import json

# 你的 90 首歌完整曲目資料庫
song_data = {
    "秋天來了！": [
        {"title": "楓", "singer": "周杰倫"}, {"title": "秋意濃", "singer": "張學友"}, {"title": "秋天別來", "singer": "侯湘婷"}
    ],
    "經典秀場金曲": [
        {"title": "舞女", "singer": "陳小雲"}, {"title": "愛情恰恰", "singer": "陳小雲"}, {"title": "一代女皇", "singer": "金佩姍"}
    ],
    "花之歌": [
        {"title": "玫瑰玫瑰我愛你", "singer": "姚莉"}, {"title": "魯冰花", "singer": "曾淑勤"}, {"title": "夜來香", "singer": "鄧麗君"}
    ],
    "經典台語歌曲": [
        {"title": "愛拚才會贏", "singer": "葉啟田"}, {"title": "家後", "singer": "江蕙"}, {"title": "浪子回頭", "singer": "茄子蛋"}
    ],
    "70-80經典國語": [
        {"title": "太難", "singer": "鄭中基"}, {"title": "恰似你的溫柔", "singer": "蔡琴"}, {"title": "一場遊戲一場夢", "singer": "王傑"}
    ],
    "懷舊電影主題曲": [
        {"title": "那些年", "singer": "胡夏"}, {"title": "酒矸倘賣無", "singer": "蘇芮"}, {"title": "新不了情", "singer": "萬芳"}
    ],
    "台灣味飲料歌曲": [
        {"title": "爺爺泡的茶", "singer": "周杰倫"}, {"title": "半糖主義", "singer": "S.H.E"}, {"title": "咖啡", "singer": "張學友"}
    ],
    "懷舊民謠": [
        {"title": "丟丟銅仔", "singer": "台灣民謠"}, {"title": "望春風", "singer": "台灣民謠"}, {"title": "雨夜花", "singer": "台灣民謠"}
    ],
    "小鄧金曲": [
        {"title": "月亮代表我的心", "singer": "鄧麗君"}, {"title": "甜蜜蜜", "singer": "鄧麗君"}, {"title": "我只在乎你", "singer": "鄧麗君"}
    ],
    "動漫熱血魂": [
        {"title": "紅蓮華", "singer": "LiSA"}, {"title": "直到世界的盡頭", "singer": "WANDS"}, {"title": "Butter-Fly", "singer": "和田光司"}
    ],
    "情歌對唱": [
        {"title": "屋頂", "singer": "吳宗憲"}, {"title": "珊瑚海", "singer": "周杰倫"}, {"title": "今天妳要嫁給我", "singer": "陶喆"}
    ],
    "數字歌": [
        {"title": "十年", "singer": "陳奕迅"}, {"title": "七里香", "singer": "周杰倫"}, {"title": "零", "singer": "柯有倫"}
    ],
    "地名歌曲": [
        {"title": "鹿港小鎮", "singer": "羅大佑"}, {"title": "忠孝東路走九遍", "singer": "動力火車"}, {"title": "挪威的森林", "singer": "伍佰"}
    ],
    "顏色歌曲": [
        {"title": "紅豆", "singer": "王菲"}, {"title": "白月光", "singer": "張信哲"}, {"title": "黑色幽默", "singer": "周杰倫"}
    ],
    "天氣系列": [
        {"title": "聽海", "singer": "張惠妹"}, {"title": "晴天", "singer": "周杰倫"}, {"title": "雨一直下", "singer": "張宇"}
    ],
    "校園民歌": [
        {"title": "外婆的澎湖灣", "singer": "潘安邦"}, {"title": "童年", "singer": "張艾嘉"}, {"title": "鄉間的小路", "singer": "葉佳修"}
    ],
    "舞曲大帝國": [
        {"title": "不如跳舞", "singer": "陳慧琳"}, {"title": "眉飛色舞", "singer": "鄭秀文"}, {"title": "姐姐", "singer": "謝金燕"}
    ],
    "失戀陣線聯盟": [
        {"title": "失戀陣線聯盟", "singer": "草蜢"}, {"title": "分手快樂", "singer": "梁靜茹"}, {"title": "說謊", "singer": "林宥嘉"}
    ],
    "勵志金曲": [
        {"title": "隱形的翅膀", "singer": "張韶涵"}, {"title": "我的未來不是夢", "singer": "張雨生"}, {"title": "倔強", "singer": "五月天"}
    ],
    "搖滾之夜": [
        {"title": "離歌", "singer": "信樂團"}, {"title": "自由", "singer": "張震嶽"}, {"title": "派對動物", "singer": "五月天"}
    ],
    "超級英雄": [
        {"title": "孤勇者", "singer": "陳奕迅"}, {"title": "超人", "singer": "五月天"}, {"title": "無敵鐵金剛", "singer": "盧廣仲"}
    ],
    "迪士尼系列": [
        {"title": "Let It Go", "singer": "Idina Menzel"}, {"title": "A Whole New World", "singer": "Peabo Bryson"}, {"title": "Under the Sea", "singer": "Samuel E. Wright"}
    ],
    "周杰倫專場": [
        {"title": "告白氣球", "singer": "周杰倫"}, {"title": "稻香", "singer": "周杰倫"}, {"title": "青花瓷", "singer": "周杰倫"}
    ],
    "五月天專場": [
        {"title": "突然好想你", "singer": "五月天"}, {"title": "溫柔", "singer": "五月天"}, {"title": "傷心的人別聽慢歌", "singer": "五月天"}
    ],
    "四大天王": [
        {"title": "吻別", "singer": "張學友"}, {"title": "忘情水", "singer": "劉德華"}, {"title": "對你愛不完", "singer": "郭富城"}
    ],
    "名字歌曲": [
        {"title": "小薇", "singer": "黃品源"}, {"title": "志明與春嬌", "singer": "五月天"}, {"title": "曹操", "singer": "林俊傑"}
    ],
    "食物歌曲": [
        {"title": "豆漿油條", "singer": "林俊傑"}, {"title": "麥芽糖", "singer": "周杰倫"}, {"title": "咖哩咖哩", "singer": "牛奶咖啡"}
    ],
    "交通工具": [
        {"title": "單車", "singer": "陳奕迅"}, {"title": "腳踏車", "singer": "王識賢"}, {"title": "火車", "singer": "羅大佑"}
    ],
    "動物世界": [
        {"title": "蝸牛", "singer": "周杰倫"}, {"title": "蝴蝶飛呀", "singer": "小虎隊"}, {"title": "學貓叫", "singer": "小潘潘"}
    ],
    "星空系列": [
        {"title": "星星點燈", "singer": "鄭智化"}, {"title": "星晴", "singer": "周杰倫"}, {"title": "夜空中最亮的星", "singer": "逃跑計劃"}
    ]
}

def fetch_lrc_lyrics(title, singer):
    # 使用免費的 lrclib API 搜尋歌詞
    url = "https://lrclib.net/api/search"
    params = {
        'track_name': title,
        'artist_name': singer
    }
    
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        if data and len(data) > 0:
            # 優先拿帶有時間軸的歌詞 (syncedLyrics)，若無則拿純文字歌詞 (plainLyrics)
            lrc = data[0].get('syncedLyrics')
            if lrc:
                return lrc
            elif data[0].get('plainLyrics'):
                return "[00:00.00]本首歌曲僅有純文字歌詞，無時間軸\n" + data[0].get('plainLyrics')
            
        return "[00:00.00]抱歉，資料庫中未找到此歌曲的歌詞"
    
    except Exception as e:
        return f"[00:00.00]搜尋時發生錯誤: {e}"

def generate_lyrics_database(data):
    total_songs = sum(len(songs) for songs in data.values())
    current_count = 1
    
    csv_data = []
    dict_output = "FULL_LRC_DATABASE = {\n"
    
    print(f"🚀 開始抓取歌詞，共計 {total_songs} 首...\n")
    
    for category, songs in data.items():
        for song in songs:
            title = song['title']
            singer = song['singer']
            
            # 對唱或合唱歌曲，只取第一位歌手搜尋比較容易找到
            search_singer = singer.split('/')[0] 
            
            print(f"⏳ ({current_count}/{total_songs}) 正在搜尋: {singer} - {title} ...")
            lyrics = fetch_lrc_lyrics(title, search_singer)
            
            # 1. 準備存入 CSV 的資料
            csv_data.append([category, title, singer, lyrics])
            
            # 2. 準備存入 Python Dictionary 的字串
            # 使用三重引號包住歌詞，保留換行符號
            dict_output += f'    "{title}": """\n{lyrics}\n""",\n'
            
            current_count += 1
            # 暫停 1.5 秒，避免發送過多請求被 API 伺服器封鎖
            time.sleep(1.5)
            
    dict_output += "}\n"
    
    # 將資料寫入 CSV 檔案
    with open("lyrics_database.csv", "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerow(["分類", "歌名", "歌手", "LRC歌詞"])
        writer.writerows(csv_data)
        
    # 將 Python 字典寫入文字檔
    with open("FULL_LRC_DATABASE.txt", "w", encoding="utf-8") as f:
        f.write(dict_output)
        
    print("\n🎉 歌詞抓取完畢！")
    print("📁 已生成 'lyrics_database.csv' (可用 Excel 開啟)")
    print("📁 已生成 'FULL_LRC_DATABASE.txt' (裡面就是你要的程式碼格式)")

if __name__ == "__main__":
    generate_lyrics_database(song_data)