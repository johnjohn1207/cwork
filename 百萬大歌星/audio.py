from pydub import AudioSegment
import os

def make_silence_challenge(karaoke_path, cut_off_sec, output_path):
    if not os.path.exists(karaoke_path):
        print(f"❌ 找不到原始檔：{karaoke_path}")
        return

    # 載入伴奏
    song = AudioSegment.from_file(karaoke_path)
    cut_off_ms = int(cut_off_sec * 1000)
    
    # 前半段保留聲音，後半段改為靜音
    audible_part = song[:cut_off_ms]
    silent_part = AudioSegment.silent(duration=len(song) - cut_off_ms)
    
    challenge = audible_part + silent_part
    challenge.export(output_path, format="mp3")
    print(f"✅ 消音挑戰檔已生成：{output_path} (消音點：{cut_off_sec}秒)")

if __name__ == "__main__":
    # 請確保資料夾下有一個 test.mp3 (鄭中基-太難 的伴奏)
    # 我們設定在 111.97 秒 (真的愛心太亂) 之前消音，或你自己選個點
    make_silence_challenge("test.mp3", 71.0, "q1_challenge.mp3")