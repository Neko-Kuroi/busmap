# -*- coding: utf-8 -*-
"""
停留所名・系統名・POI名の「ハイブリッド英語化」変換ロジック（JSON出力版）。
mlit_stops.json を読み込み、romaji フィールドを追加して mlit_stops_en.json を出力します。
"""
import re
import sys
import os
import subprocess
import glob
import json # JSON処理用に追加

# ==========================================
# 0. 必要なライブラリのインストールと初期化
# ==========================================
try:
    import pykakasi
except ImportError:
    print("pykakasi not found. Installing...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pykakasi"])
    import pykakasi

try:
    import MeCab
except ImportError:
    print("MeCab not found. Installing...")
    subprocess.check_call(["apt-get", "-q", "-y", "update"])
    subprocess.check_call(["apt-get", "-q", "-y", "install", "mecab", "libmecab-dev", "mecab-ipadic-utf8"])
    subprocess.check_call([sys.executable, "-m", "pip", "install", "mecab-python3"])
    subprocess.check_call([sys.executable, "-m", "pip", "install", "mecab-ipadic-neologd"])
    import MeCab

kks = pykakasi.kakasi()
_mecab_tagger = None

# MeCab の辞書探索と初期化（neologd -> ipadic の順）
try:
    mecab_dict_dir = None
    candidate_paths = []
    for p in sys.path:
        candidate_paths.append(os.path.join(p, 'mecab_dict', 'ipadic-neologd'))
    candidate_paths.extend([
        '/usr/lib/mecab/dic/mecab-ipadic-neologd',
        '/usr/local/lib/python3.10/dist-packages/mecab_dict/ipadic-neologd'
    ])
    candidate_paths.extend(glob.glob('/usr/local/lib/python*/dist-packages/mecab_dict/ipadic-neologd'))

    for path_cand in candidate_paths:
        if os.path.exists(path_cand) and os.path.isdir(path_cand):
            try:
                temp_tagger = MeCab.Tagger(f"-d {path_cand}")
                temp_tagger.parse('テスト')
                mecab_dict_dir = path_cand
                break
            except: pass

    if mecab_dict_dir:
        _mecab_tagger = MeCab.Tagger(f"-d {mecab_dict_dir}")
    else:
        _mecab_tagger = MeCab.Tagger() # デフォルト辞書でフォールバック
except Exception as e:
    print(f"MeCab initialization warning: {e}")

# ==========================================
# 1. 辞書の定義（前回と同じ）
# ==========================================
CATEGORY_DICT = {
    "駅前": "Station", "駅": "Station", "線": "Line",
    "道路元標": "Road Distance Marker", "参道": "Sando (Approach)",
    "小学校前": "Elementary School", "小学校": "Elementary School",
    "中学校前": "Junior High School", "中学校": "Junior High School",
    "中学前": "Junior High School", "中学": "Junior High School",
    "高等学校前": "High School", "高等学校": "High School",
    "高校前": "High School", "高校": "High School",
    "大学前": "University", "大学": "University",
    "学校前": "School", "学校": "School",
    "幼稚園": "Kindergarten", "保育園": "Nursery",
    "病院前": "Hospital", "病院": "Hospital",
    "医院": "Clinic", "診療所": "Clinic",
    "市役所前": "City Hall", "市役所": "City Hall",
    "町役場": "Town Hall", "役場前": "Town Hall", "役場": "Town Hall",
    "郵便局前": "Post Office", "郵便局": "Post Office",
    "出張所": "Branch Office", "案内所": "Information Center",
    "観光案内図": "Tourist Information Map", "案内図": "Information Map",
    "図書館前": "Library", "図書館": "Library",
    "体育館前": "Gymnasium", "体育館": "Gymnasium",
    "公民館前": "Community Center", "公民館": "Community Center",
    "コミュニティセンター": "Community Center",
    "会館前": "Hall", "会館": "Hall",
    "児童公園": "Children's Park", "公園前": "Park", "公園": "Park",
    "神社前": "Shrine", "神社": "Shrine",
    "寺院": "Temple", "教会前": "Church", "教会": "Church",
    "美術館": "Art Museum", "博物館": "Museum", "資料館": "Museum",
    "記念碑": "Monument", "庭園": "Garden", "地蔵尊": "Jizo Statue",
    "橋": "Bridge", "自然歩道": "Nature Trail", "保存地区": "Preservation District",
    "均一系統": "Flat Fare", "均一区間": "Flat Fare Zone",
    "多区間系統": "Multi-Zone Fare", "号系統": "Route", "系統": "Route",
    "循環": "Loop", "ループ": "Loop", "ルート": "Route",
    "エクスプレス": "Express", "バス": "Bus",
    # 地名
    "京都": "Kyoto", "大阪": "Osaka", "東京": "Tokyo", "神戸": "Kobe", "大津": "Otsu",
    "亀岡": "Kameoka", "舞鶴": "Maizuru", "福知山": "Fukuchiyama", "宮津": "Miyazu",
    "京丹後": "Kyotango", "南丹": "Nantan", "木津川": "Kizugawa", "城陽": "Joyo",
    "向日": "Muko", "長岡京": "Nagaokakyo", "八幡": "Yawata", "京田辺": "Kyotanabe",
    "宇治": "Uji", "与謝野": "Yosano", "向島": "Mukojima",
}
PLACE_NAME_DICT = {
    "京都": "Kyoto", "大阪": "Osaka", "東京": "Tokyo", "神戸": "Kobe", "大津": "Otsu",
    "亀岡": "Kameoka", "舞鶴": "Maizuru", "福知山": "Fukuchiyama", "宮津": "Miyazu",
    "京丹後": "Kyotango", "南丹": "Nantan", "木津川": "Kizugawa", "城陽": "Joyo",
    "向日": "Muko", "長岡京": "Nagaokakyo", "八幡": "Yawata", "京田辺": "Kyotanabe",
    "宇治": "Uji", "与謝野": "Yosano", "向島": "Mukojima",
}
CATEGORY_DICT.update(PLACE_NAME_DICT)

CATEGORY_READINGS = {
    "駅前": ["えきまえ"], "駅": ["えき"], "線": ["せん"],
    "小学校前": ["しょうがっこうまえ"], "小学校": ["しょうがっこう"],
    "中学校前": ["ちゅうがっこうまえ"], "中学校": ["ちゅうがっこう"],
    "中学前": ["ちゅうがくまえ"], "中学": ["ちゅうがく"],
    "高等学校前": ["こうとうがっこうまえ"], "高等学校": ["こうとうがっこう"],
    "高校前": ["こうこうまえ"], "高校": ["こうこう"],
    "大学前": ["だいがくまえ"], "大学": ["だいがく"],
    "学校前": ["がっこうまえ"], "学校": ["がっこう"],
    "幼稚園": ["ようちえん"], "保育園": ["ほいくえん"],
    "病院前": ["びょういんまえ"], "病院": ["びょういん"],
    "医院": ["いいん"], "診療所": ["しんりょうじょ"],
    "市役所前": ["しやくしょまえ"], "市役所": ["しやくしょ"],
    "町役場": ["まちやくば", "ちょうやくば"], "役場前": ["やくばまえ"], "役場": ["やくば"],
    "郵便局前": ["ゆうびんきょくまえ"], "郵便局": ["ゆうびんきょく"],
    "出張所": ["しゅっちょうじょ"], "案内所": ["あんないじょ"],
    "観光案内図": ["かんこうあんないず"], "案内図": ["あんないず"],
    "図書館前": ["としょかんまえ"], "図書館": ["としょかん"],
    "体育館前": ["たいいくかんまえ"], "体育館": ["たいいくかん"],
    "公民館前": ["こうみんかんまえ"], "公民館": ["こうみんかん"],
    "コミュニティセンター": ["こみゅにてぃせんたー"],
    "会館前": ["かいかんまえ"], "会館": ["かいかん"],
    "児童公園": ["じどうこうえん"], "公園前": ["こうえんまえ"], "公園": ["こうえん"],
    "神社前": ["じんじゃまえ"], "神社": ["じんじゃ"],
    "寺院": ["じいん"], "教会前": ["きょうかいまえ"], "教会": ["きょうかい"],
    "美術館": ["びじゅつかん"], "博物館": ["はくぶつかん"], "資料館": ["しりょうかん"],
    "記念碑": ["きねんひ"], "庭園": ["ていえん"], "地蔵尊": ["じぞうそん"],
    "均一区間": ["きんいつくかん"], "橋": ["ばし", "はし"],
    "自然歩道": ["しぜんほどう"], "保存地区": ["ほぞんちく"],
    "道路元標": ["どうろげんぴょう"], "参道": ["さんどう"],
}
_TEMPLE_READINGS = ["でら", "てら"]
TEMPLE_SUFFIX = "寺"
TEMPLE_SUFFIX_EN = "Temple"

_SORTED_KEYS = sorted(CATEGORY_DICT.keys(), key=len, reverse=True)
_GLOBAL_UNSAFE_KEYS = {"橋", "会館前", "会館"}
_GLOBAL_KEYS = [k for k in _SORTED_KEYS if k not in _GLOBAL_UNSAFE_KEYS]
_PATTERN = re.compile("|".join(re.escape(k) for k in _GLOBAL_KEYS))

# ==========================================
# 2. 前処理・難読地名フォールバック
# ==========================================
def _normalize_text(text: str) -> str:
    if not text: return ""
    text = re.sub(r'(.)々', r'\1\1', text)
    text = re.sub(r'[「」『』［］【】（）\(\)\[\]]', ' ', text)
    return re.sub(r'\s+', ' ', text).strip()

_ATEJI_FALLBACK = {
    "宇豆貴": "うづき", "加悦谷": "かやだに", "加悦": "かや", "筈巻": "はずまき",
    "深泥池": "みどろがいけ", "椥辻": "なぎつじ", "柊野": "ひらぎの",
    "栂ノ尾": "とがのお", "木幡": "こばた", "上狛": "かみこま", "下狛": "しもこま",
    "弥栄": "よさ", "夜久野": "やくの", "菟原": "うばら", "丹海": "たんかい", "白瀬橋": "しらせばし",
}

def _apply_ateji_fallback(text: str) -> str:
    for kanji, kana in _ATEJI_FALLBACK.items():
        if kanji in text: text = text.replace(kanji, kana)
    return text

# ==========================================
# 3. 変換ロジック本体
# ==========================================
def _apply_category_dict(text: str) -> str:
    replaced = _PATTERN.sub(lambda m: " " + CATEGORY_DICT[m.group(0)] + " ", text)
    if replaced.endswith(TEMPLE_SUFFIX):
        replaced = replaced[:-1] + " " + TEMPLE_SUFFIX_EN + " "
    for key in ("会館前", "会館", "橋"):
        if replaced.endswith(key):
            replaced = replaced[: -len(key)] + " " + CATEGORY_DICT[key] + " "
            break
    return replaced

def _simplify_long_vowels(h: str) -> str:
    return re.sub(r"uu", "u", re.sub(r"oo", "o", re.sub(r"ou", "o", h)))

def kana_romanize(kana_text: str) -> str:
    if not kana_text: return ""
    parts = []
    for tok in kks.convert(kana_text):
        h = tok["hepburn"].strip()
        if h:
            h = _simplify_long_vowels(h)
            parts.append(h[0].upper() + h[1:])
    return re.sub(r"\s+", " ", " ".join(parts)).strip()

def _mecab_reading_lengths(kanji_text: str):
    if _mecab_tagger is None: return None
    node = _mecab_tagger.parseToNode(kanji_text)
    if node is None: return None
    tokens = []
    node = node.next
    while node and node.surface:
        cols = node.feature.split(",")
        reading = cols[6] if len(cols) > 6 and cols[6] != "*" else (cols[7] if len(cols) > 7 and cols[7] != "*" else None)
        if reading is None: return None
        tokens.append((node.surface, len(reading)))
        node = node.next
    return tokens

_DIRECTION_KANJI = {"東", "西", "南", "北", "前"}
_KNOWN_COMPOUND_READINGS = {"同志社": "どうししゃ", "吉祥院": "きっしょういん"}

def _merge_lone_kanji_tokens(tokens):
    merged, pending_len = [], 0
    for surface, length in tokens:
        if len(surface) == 1 and surface not in _DIRECTION_KANJI:
            pending_len += length
        else:
            merged.append(pending_len + length)
            pending_len = 0
    if pending_len:
        if merged: merged[-1] += pending_len
        else: merged.append(pending_len)
    return merged

def kana_romanize_segmented(kanji_text: str, kana_text: str) -> str:
    if not kanji_text: return kana_romanize(kana_text)
    for compound, reading in _KNOWN_COMPOUND_READINGS.items():
        if kanji_text.startswith(compound) and kana_text.startswith(reading):
            head = kana_romanize(reading)
            rest_kanji, rest_kana = kanji_text[len(compound):], kana_text[len(reading):]
            if not rest_kanji: return head
            if rest_kanji == "前": return head + kana_romanize(rest_kana).lower()
            return f"{head} {kana_romanize_segmented(rest_kanji, rest_kana)}".strip()

    tokens = _mecab_reading_lengths(kanji_text)
    if not tokens: return kana_romanize(kana_text)
    lengths = _merge_lone_kanji_tokens(tokens)
    if not lengths or sum(lengths) != len(kana_text): return kana_romanize(kana_text)

    parts, pos = [], 0
    for length in lengths:
        r = kana_romanize(kana_text[pos: pos + length])
        if r: parts.append(r)
        pos += length
    return " ".join(parts) if parts else kana_romanize(kana_text)

def hybrid_romanize_with_kana(kanji_text: str, kana_text: str) -> str:
    if not kana_text: return hybrid_romanize(kanji_text)
    for cat_word in _SORTED_KEYS:
        if cat_word in PLACE_NAME_DICT or not kanji_text.endswith(cat_word): continue
        readings = CATEGORY_READINGS.get(cat_word) or (_TEMPLE_READINGS if cat_word == TEMPLE_SUFFIX else [])
        for reading in readings:
            if kana_text.endswith(reading) and len(kana_text) > len(reading):
                rem_kanji = _apply_ateji_fallback(kanji_text[: -len(cat_word)])
                rem_kana = kana_text[: -len(reading)]
                label = CATEGORY_DICT[cat_word] if cat_word in CATEGORY_DICT else TEMPLE_SUFFIX_EN
                return f"{kana_romanize_segmented(rem_kanji, rem_kana)} {label}".strip()
    return kana_romanize_segmented(_apply_ateji_fallback(kanji_text), kana_text)

def _normalize_dash(text: str) -> str:
    katakana = "\u30A0-\u30FF"
    def _sub(m):
        b, a = m.group(1), m.group(2)
        if re.match(f"[{katakana}]", b or "") and re.match(f"[{katakana}]", a or ""):
            return m.group(0)
        return (b or "") + " - " + (a or "")
    return re.sub(r"(.)ー(.)", _sub, text)

def hybrid_romanize(text: str) -> str:
    if not text: return ""
    text = _normalize_text(text)
    text = _apply_ateji_fallback(text)
    text = text.replace("・", " / ")
    text = _normalize_dash(text)
    substituted = _apply_category_dict(text)

    parts, merge_next = [], False
    for tok in kks.convert(substituted):
        orig = tok["orig"].strip()
        if not orig: continue
        if orig.isascii():
            parts.append(orig)
            merge_next = False
        else:
            if orig == "ヶ" and tok["hepburn"].strip() == "ke":
                if parts: parts[-1] += "ga"
                else: parts.append("Ga")
                merge_next = True
                continue
            h = tok["hepburn"].strip()
            if h:
                h = _simplify_long_vowels(h)
                if merge_next and parts: parts[-1] += h
                else: parts.append(h[0].upper() + h[1:])
            merge_next = False

    result = re.sub(r"\s+", " ", " ".join(parts)).strip()
    result = re.sub(r"\(\s+", "(", result)
    return re.sub(r"\s+([,)\]])", r"\1", result)

# ==========================================
# 4. メイン処理: JSONの読み込みと出力
# ==========================================
if __name__ == "__main__":
    input_file = "mlit_stops.json"
    output_file = "mlit_stops_en_2_.json"

    if not os.path.exists(input_file):
        print(f"Error: {input_file} が見つかりません。")
        sys.exit(1)

    print(f"Loading data from {input_file}...")
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    print(f"Loaded {len(data)} stops. Starting conversion...")

    # 変換処理
    for i, stop in enumerate(data):
        name = stop.get("name", "")
        kana = stop.get("kana", "")

        # kana フィールドの有無で変換関数を切り替え
        if kana:
            romaji = hybrid_romanize_with_kana(name, kana)
        else:
            romaji = hybrid_romanize(name)

        # 変換結果を romaji フィールドとして追加
        stop["romaji"] = romaji

        # 進捗表示 (1000件ごと)
        if (i + 1) % 1000 == 0:
            print(f"  Processed {i + 1} / {len(data)} stops...")

    ## ファイル書き出し
    #print(f"Saving to {output_file}...")
    #with open(output_file, 'w', encoding='utf-8') as f:
    #    json.dump(data, f, ensure_ascii=False, indent=2)
    #
    #print("="*50)
    #print(f"✅ 完了しました！ {output_file} に保存しました。")
    #print("="*50)
    #
    ## 動作確認サンプルの表示
    #print("\n--- 変換結果サンプル (先頭5件) ---")
    #for stop in data[:5]:
    #    kana_info = f" (kana: {stop['kana']})" if stop.get('kana') else ""
    #    print(f"[ID {stop['id']}] {stop['name']}{kana_info}  ->  {stop['romaji']}")
    # ==========================================
    # 4. メイン処理: JSONの読み込みと出力
    # ==========================================
    # ... (前半の読み込み・変換処理は同じ) ...

    # ファイル書き出し（辞書形式に変換）
    print(f"Saving to {output_file}...")
    
    # IDをキー、ローマ字を値とする辞書を作成
    output_dict = {str(stop["id"]): stop["romaji"] for stop in data}
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output_dict, f, ensure_ascii=False, indent=2)
        
    print("="*50)
    print(f"✅ 完了しました！ {output_file} に保存しました。")
    print("="*50)
