import streamlit as st
import datetime
import locale
from collections import Counter

# 日本語ロケール設定（ただしStreamlitのdate_inputでは効かない可能性あり）
try:
    locale.setlocale(locale.LC_TIME, 'ja_JP.UTF-8')
except:
    pass

# ピタゴラス変換表
def char_to_num(c):
    mapping = {
        'A':1, 'J':1, 'S':1,
        'B':2, 'K':2, 'T':2,
        'C':3, 'L':3, 'U':3,
        'D':4, 'M':4, 'V':4,
        'E':5, 'N':5, 'W':5,
        'F':6, 'O':6, 'X':6,
        'G':7, 'P':7, 'Y':7,
        'H':8, 'Q':8, 'Z':8,
        'I':9, 'R':9
    }
    return mapping.get(c.upper(), 0)

def reduce_number(n):
    while n > 9 and n not in [11, 22, 33]:
        n = sum(int(d) for d in str(n))
    return n

def calculate_life_path_number(birthdate):
    digits = [int(d) for d in birthdate.replace('-', '') if d.isdigit()]
    return reduce_number(sum(digits))

def calculate_birth_day_number(day):
    return reduce_number(day)

def calculate_expression_number(name):
    return reduce_number(sum(char_to_num(c) for c in name if c.isalpha()))

def calculate_soul_urge_number(name):
    vowels = "AEIOU"
    return reduce_number(sum(char_to_num(c) for c in name if c.upper() in vowels))

# 数字の意味の解説辞書（役割別）
def get_number_meaning(position, n):
    meanings = {
        "life_path": {
            1: "あなたの人生は『自立』と『リーダーシぶ』がテーマです。先頭に立って新しい道を切り開く運命にあります。",
            2: "あなたの人生は『調和』と『共感』がテーマです。人との関わりを通じて、優しさと受容の力を育みます。",
            3: "あなたの人生は『表現』と『創造性』がテーマです。楽しさを分かち合い、周囲に喜びを届ける存在です。",
            4: "あなたの人生は『安定』と『継続』がテーマです。地道な努力と信頼で、着実に基盤を築いていきます。",
            5: "あなたの人生は『自由』と『変化』がテーマです。新しい挑戦や刺激を求めて進むことで、道が開かれていくでしょう。",
            6: "あなたの人生は『愛』と『責任』がテーマです。家族や仲間を支え、安心と調和を広げていきます。",
            7: "あなたの人生は『探究』と『精神性』がテーマです。静けさの中で深い洞察を得て、真実を追い求めます。",
            8: "あなたの人生は『達成』と『現実的な成功』がテーマです。実行力と戦略的思考で目標を現実化していきます。",
            9: "あなたの人生は『奉仕』と『理想』がテーマです。広い視野で人や社会に貢献する使命があります。",
            11: "あなたの人生は『直感』と『インスピレーション』がテーマです。高次の気づきを伝えるスピリチュアルな導き手です。",
            22: "あなたの人生は『理想の具現化』がテーマです。大きなビジョンを現実に落とし込む使命があります。",
            33: "あなたの人生は『無条件の愛』がテーマです。周囲に愛と癒しを届ける教師的な存在です。"
        }
    }
    return meanings.get(position, {}).get(n, "この数と役割の組み合わせの意味はまだ用意されていません。")

# Streamlit UI
st.title("🔢 数秘術診断アプリ（PDFなし版）")
st.markdown("あなたの生年月日と名前から、基本的な4つの数を導き出します。")

name = st.text_input("名前（ローマ字）")
birthdate = st.date_input(
    "生年月日を選んでください",
    min_value=datetime.date(1925, 1, 1),
    max_value=datetime.date(2025, 12, 31),
    value=datetime.date(1980, 1, 1)
)

if st.button("診断する"):
    if name:
        birth_str = birthdate.strftime('%Y-%m-%d')
        life_path = calculate_life_path_number(birth_str)
        birth_day = calculate_birth_day_number(birthdate.day)
        expression = calculate_expression_number(name)
        soul = calculate_soul_urge_number(name)

        st.subheader("🔮 診断結果")
        st.write(f"**運命数：** {life_path} → {get_number_meaning('life_path', life_path)}")
        st.write(f"**誕生数：** {birth_day}")
        st.write(f"**表現数：** {expression}")
        st.write(f"**魂の欲求数：** {soul}")

        # 数字の重複検出と強調
        nums = [life_path, birth_day, expression, soul]
        count = Counter(nums)
        repeated = [n for n, c in count.items() if c > 1]
        if repeated:
            for num in repeated:
                st.info(f"{num} が複数の数に登場しています → この数字の影響があなたの中で強く現れるでしょう。")
    else:
        st.warning("名前をローマ字で入力してください。")
