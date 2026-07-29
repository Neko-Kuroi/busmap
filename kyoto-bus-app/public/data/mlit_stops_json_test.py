# -*- coding: utf-8 -*-
"""
停留所名・系統名・POI名の「ハイブリッド英語化」変換ロジック（修正版）。
修正点：
1. 「々（くりかえし）」の展開処理を追加
2. 括弧・記号の正規化処理を追加
3. 難読地名・当て字のフォールバック辞書（_ATEJI_FALLBACK）を追加
4. CATEGORY_DICT に「公民館」などを追加
TEST
"""
import re
import sys
import os # Import os for path checks
import subprocess
import glob # Import glob for path searching

# Install pykakasi if not already available
try:
    import pykakasi
except ImportError:
    print("pykakasi not found. Installing...")
    !pip install pykakasi
    import pykakasi

try:
    import MeCab
except ImportError:
    print("MeCab not found. Installing...")
    # Ensure fresh package list
    !apt-get -q -y update
    # Install MeCab system package and dictionaries
    !apt-get -q -y install mecab libmecab-dev mecab-ipadic-utf8
    # Install Python bindings for MeCab
    !pip install mecab-python3
    import MeCab
    # Install mecab-ipadic-neologd Python package (which contains the dictionary)
    !pip install mecab-ipadic-neologd
    print("MeCab and neologd Python bindings installed.")

kks = pykakasi.kakasi()

_mecab_tagger = None # Initialize to None

print("Attempting MeCab initialization...")
try:
    mecab_dict_dir = None

    # Search for mecab-ipadic-neologd in common Python site-packages locations
    candidate_paths = []
    # 1. Search in sys.path entries combined with mecab_dict/ipadic-neologd
    for p in sys.path:
        candidate_paths.append(os.path.join(p, 'mecab_dict', 'ipadic-neologd'))
    # 2. Add common Colab/Python installation paths directly
    candidate_paths.append('/usr/lib/mecab/dic/mecab-ipadic-neologd') # System-wide install if any
    candidate_paths.append('/usr/share/mecab/dic/mecab-ipadic-neologd') # Another system path
    candidate_paths.append('/usr/local/lib/python3.10/dist-packages/mecab_dict/ipadic-neologd') # Specific Colab path
    # Add a broader glob search as a last resort for neologd
    neologd_glob_paths = glob.glob('/usr/local/lib/python*/dist-packages/mecab_dict/ipadic-neologd')
    if neologd_glob_paths:
        candidate_paths.extend(neologd_glob_paths)

    for path_cand in candidate_paths:
        if os.path.exists(path_cand) and os.path.isdir(path_cand):
            # Test if it's a valid dictionary by attempting to parse
            try:
                temp_tagger = MeCab.Tagger(f"-d {path_cand}")
                # Ensure the tagger can parse without error
                temp_tagger.parse('テスト')
                mecab_dict_dir = path_cand
                print(f"Found and validated mecab-ipadic-neologd dictionary at: {mecab_dict_dir}")
                break
            except Exception as e:
                print(f"MeCab Tagger with neologd dictionary at {path_cand} failed to parse: {e}")

    if mecab_dict_dir:
        _mecab_tagger = MeCab.Tagger(f"-d {mecab_dict_dir}")
        print("MeCab initialized successfully with mecab-ipadic-neologd.")
    else:
        print("MeCab-ipadic-neologd dictionary not found or failed to load. Falling back to system ipadic.")
        # Fallback to default system dictionary (ipadic-utf8)
        default_ipadic_path = None
        system_ipadic_paths = [
            '/usr/lib/mecab/dic/mecab-ipadic-2.7.0-20070801',
            '/var/lib/mecab/dic/ipadic-utf8',
            '/usr/share/mecab/dic/ipadic',
            '/usr/share/mecab/dic/ipadic-utf8', # Adding this common path
        ]
        for path in system_ipadic_paths:
            if os.path.exists(path) and os.path.isdir(path):
                # Test if it's a valid dictionary
                try:
                    temp_tagger = MeCab.Tagger(f"-d {path}")
                    temp_tagger.parse('テスト')
                    default_ipadic_path = path
                    print(f"Found and validated default ipadic dictionary at: {default_ipadic_path}")
                    break
                except Exception as e:
                    print(f"Default MeCab Tagger with system ipadic dictionary at {path} failed to parse: {e}")

        if default_ipadic_path:
            _mecab_tagger = MeCab.Tagger(f"-d {default_ipadic_path}")
            print("MeCab initialized successfully with default system ipadic-utf8.")
        else:
            print("Default ipadic dictionary not found or failed to load. Attempting MeCab.Tagger() without arguments (last resort).")
            # Last resort - Try MeCab.Tagger() without args
            try:
                temp_tagger = MeCab.Tagger()
                temp_tagger.parse('テスト')
                _mecab_tagger = temp_tagger
                print("MeCab initialized successfully with default configuration.")
            except Exception as e:
                print(f"MeCab Tagger without arguments failed to parse: {e}")
                _mecab_tagger = None

except Exception as e:
    print(f"MeCab initialization error: {e}")
    _mecab_tagger = None

if _mecab_tagger is None:
    print("WARNING: MeCab could not be initialized. Romanization quality for segmented readings may be affected.")

# ==========================================
# 1. 辞書の定義と補強
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
# 2. 【新規追加】前処理関数
# ==========================================
def _normalize_text(text: str) -> str:
    """変換前にテキストを正規化する（々、括弧、スペース）"""
    if not text:
        return ""

    # 1. 「々」を直前の文字で置換 (例: 市野々 -> 市野野, 佐々木 -> 佐佐木)
    # ※バス停名のような短いテキストではこれで概ね対応可能
    text = re.sub(r'(.)々', r'\1\1', text)

    # 2. 括弧・記号をスペースに置換
    # MeCabのトークン崩れや、文字数カウントの不一致を防ぐため
    text = re.sub(r'[「」『』［］【】（）\(\)\[\]]', ' ', text)

    # 3. 連続するスペースを詰める
    text = re.sub(r'\s+', ' ', text).strip()
    return text

# ==========================================
# 3. 【新規追加】難読地名フォールバック辞書
# ==========================================
# pykakasiやMeCabが誤読みする可能性の高い、地域固有の難読地名・当て字
_ATEJI_FALLBACK = {
    "宇豆貴": "うづき",
    "加悦谷": "かやだに",
    "加悦": "かや",
    "筈巻": "はずまき",
    "深泥池": "みどろがいけ",
    "椥辻": "なぎつじ",
    "柊野": "ひらぎの",
    "栂ノ尾": "とがのお",
    "木幡": "こばた",
    "上狛": "かみこま",
    "下狛": "しもこま",
    "弥栄": "よさ",       # 野中［弥栄町］対策
    "夜久野": "やくの",   # 小畑［夜久野町］対策
    "菟原": "うばら",     # 小学校前［菟原小］対策
    "丹海": "たんかい",   # 野田川丹海前対策
    "白瀬橋": "しらせばし",
}

def _apply_ateji_fallback(text: str) -> str:
    """難読地名をかなに変換してからpykakasiに渡す"""
    for kanji, kana in _ATEJI_FALLBACK.items():
        if kanji in text:
            text = text.replace(kanji, kana)
    return text

# ==========================================
# 4. 変換ロジック本体
# ==========================================

def _apply_category_dict(text: str) -> str:
    def _sub(m):
        return " " + CATEGORY_DICT[m.group(0)] + " "
    replaced = _PATTERN.sub(_sub, text)
    if replaced.endswith(TEMPLE_SUFFIX):
        replaced = replaced[:-1] + " " + TEMPLE_SUFFIX_EN + " "
    for key in ("会館前", "会館", "橋"):
        if replaced.endswith(key):
            replaced = replaced[: -len(key)] + " " + CATEGORY_DICT[key] + " "
            break
    return replaced

def _simplify_long_vowels(h: str) -> str:
    h = re.sub(r"ou", "o", h)
    h = re.sub(r"oo", "o", h)
    h = re.sub(r"uu", "u", h)
    return h

def kana_romanize(kana_text: str) -> str:
    if not kana_text:
        return ""
    tokens = kks.convert(kana_text)
    parts = []
    for tok in tokens:
        h = tok["hepburn"].strip()
        if h:
            h = _simplify_long_vowels(h)
            parts.append(h[0].upper() + h[1:])
    # Corrected re.sub call: provide the string to be substituted
    return re.sub(r"\s+", " ", " ".join(parts)).strip()

def _mecab_reading_lengths(kanji_text: str):
    if _mecab_tagger is None: return None
    node = _mecab_tagger.parseToNode(kanji_text)
    if node is None: return None
    tokens = []
    node = node.next
    while node and node.surface:
        cols = node.feature.split(",")
        reading = cols[6] if len(cols) > 6 and cols[6] != "*" else None

        if reading is None and len(cols) > 7 and cols[7] != "*":
            reading = cols[7]

        if reading is None:
            return None
        tokens.append((node.surface, len(reading)))
        node = node.next
    return tokens

_DIRECTION_KANJI = {"東", "西", "南", "北", "前"}

_KNOWN_COMPOUND_READINGS = {
    "同志社": "どうししゃ",
    "吉祥院": "きっしょういん",
}

def _merge_lone_kanji_tokens(tokens):
    merged = []
    pending_len = 0
    for surface, length in tokens:
        is_lone_kanji = len(surface) == 1 and surface not in _DIRECTION_KANJI
        if is_lone_kanji:
            pending_len += length
            continue
        merged.append(pending_len + length)
        pending_len = 0
    if pending_len:
        if merged:
            merged[-1] += pending_len
        else:
            merged.append(pending_len)
    return merged

def kana_romanize_segmented(kanji_text: str, kana_text: str) -> str:
    if not kanji_text:
        return kana_romanize(kana_text)

    for compound, reading in _KNOWN_COMPOUND_READINGS.items():
        if kanji_text.startswith(compound) and kana_text.startswith(reading):
            head = kana_romanize(reading)
            rest_kanji = kanji_text[len(compound):]
            rest_kana = kana_text[len(reading):]
            if not rest_kanji: return head
            if rest_kanji == "前":
                return head + kana_romanize(rest_kana).lower()
            rest = kana_romanize_segmented(rest_kanji, rest_kana)
            return f"{head} {rest}".strip()

    tokens = _mecab_reading_lengths(kanji_text)
    if not tokens:
        return kana_romanize(kana_text)

    lengths = _merge_lone_kanji_tokens(tokens)
    if not lengths or sum(lengths) != len(kana_text):
        return kana_romanize(kana_text)

    parts = []
    pos = 0
    for length in lengths:
        segment = kana_text[pos: pos + length]
        pos += length
        r = kana_romanize(segment)
        if r: parts.append(r)
    return " ".join(parts) if parts else kana_romanize(kana_text)

def hybrid_romanize_with_kana(kanji_text: str, kana_text: str) -> str:
    if not kana_text:
        return hybrid_romanize(kanji_text)

    kanji_text_processed = _apply_ateji_fallback(kanji_text)

    for cat_word in _SORTED_KEYS:
        if cat_word in PLACE_NAME_DICT: continue
        if not kanji_text.endswith(cat_word): continue
        readings = CATEGORY_READINGS.get(cat_word) or (
            _TEMPLE_READINGS if cat_word == TEMPLE_SUFFIX else []
        )
        for reading in readings:
            if kana_text.endswith(reading) and len(kana_text) > len(reading):
                remaining_kanji = kanji_text[: -len(cat_word)]
                remaining_kana = kana_text[: -len(reading)]
                remaining_kanji = _apply_ateji_fallback(remaining_kanji)

                remaining_en = kana_romanize_segmented(remaining_kanji, remaining_kana)
                label = CATEGORY_DICT[cat_word] if cat_word in CATEGORY_DICT else TEMPLE_SUFFIX_EN
                return f"{remaining_en} {label}".strip()
        break

    return kana_romanize_segmented(kanji_text_processed, kana_text)

def _normalize_dash(text: str) -> str:
    katakana = "\u30A0-\u30FF"
    def _sub(m):
        before, after = m.group(1), m.group(2)
        if re.match(f"[{katakana}]", before or "") and re.match(f"[{katakana}]", after or ""):
            return m.group(0)
        return (before or "") + " - " + (after or "")
    return re.sub(r"(.)ー(.)", _sub, text)

def hybrid_romanize(text: str) -> str:
    if not text:
        return ""

    text = _normalize_text(text)
    text = _apply_ateji_fallback(text)

    text = text.replace("・", " / ")
    text = _normalize_dash(text)
    substituted = _apply_category_dict(text)

    tokens = kks.convert(substituted)
    parts = []
    merge_next = False
    for tok in tokens:
        orig = tok["orig"].strip()
        if not orig: continue
        if orig.isascii():
            parts.append(orig)
            merge_next = False
        else:
            if orig == "ヶ" and tok["hepburn"].strip() == "ke":
                if parts:
                    parts[-1] = parts[-1] + "ga"
                else:
                    parts.append("Ga")
                merge_next = True
                continue
            h = tok["hepburn"].strip()
            if h:
                h = _simplify_long_vowels(h)
                if merge_next and parts:
                    parts[-1] = parts[-1] + h
                else:
                    parts.append(h[0].upper() + h[1:])
            merge_next = False

    result = " ".join(parts)
    result = re.sub(r"\s+", " ", result).strip()
    result = re.sub(r"\(\s+", "(", result)
    result = re.sub(r"\s+([,)\]])", r"\1", result)
    return result


if __name__ == "__main__":
    test_cases = [
        ("市野々", None),
        ("宇豆貴公民館", None),
        ("野中［弥栄町］", None),
        ("小畑［夜久野町］", None),
        ("野田川丹海前", None),
        ("筈巻", None),
        ("深泥池", "みどろがいけ"),
        ("同志社前", "どうししゃまえ"),
    ]

    for kanji, kana in test_cases:
        if kana:
            res = hybrid_romanize_with_kana(kanji, kana)
        else:
            res = hybrid_romanize(kanji)
        print(f"{kanji} -> {res}")

#------------------------------------------------
#-------------------------------------------------
    import json

#if __name__ == "__main__":
    # ==========================================
    # 5. JSONデータの読み込みと全件変換・不具合検出
    # ==========================================
    json_file_path = "mlit_stops.json" # アップロードしたJSONのパスに合わせてください
    
    try:
        with open(json_file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"Error: {json_file_path} not found.")
        exit()

    # 不具合とみなす明らかなエラーパターン（小文字で比較）
    # pykakasiの誤変換や、記号処理の失敗を検出するためのキーワード
    ERROR_PATTERNS = [
        "kurikaesi", "repeat", "mame", "takashi", "kawai", 
        "tan umi", "yasaka", "sho no", "u mame"
    ]
    
    results = []
    errors = []

    print(f"Processing {len(data)} stops...")

    for stop in data:
        name = stop.get("name", "")
        kana = stop.get("kana", "")
        stop_id = stop.get("id", "N/A")
        
        # kanaフィールドの有無で変換関数を切り替え
        if kana:
            romaji = hybrid_romanize_with_kana(name, kana)
        else:
            romaji = hybrid_romanize(name)
            
        stop["romaji"] = romaji
        results.append(stop)
        
        # --- 不具合チェック ---
        is_error = False
        reason = []
        romaji_lower = romaji.lower()
        
        # 1. 既知のエラーパターンが含まれているか
        if any(p in romaji_lower for p in ERROR_PATTERNS):
            is_error = True
            reason.append("Known error pattern detected")
            
        # 2. 日本語（漢字・ひらがな・カタカナ）がそのままローマ字に混ざっているか
        if re.search(r'[\u3040-\u30FF\u4E00-\u9FFF]', romaji):
            is_error = True
            reason.append("Japanese characters remain")
            
        # 3. 括弧が不正に残っているか（スペース区切りなどで孤立している場合など）
        if "( " in romaji or " )" in romaji:
            is_error = True
            reason.append("Malformed brackets")

        if is_error:
            errors.append({
                "id": stop_id,
                "name": name,
                "kana": kana,
                "romaji": romaji,
                "reason": ", ".join(reason)
            })

    # --- 結果の出力 ---
    print("\n" + "="*50)
    print(f"Total stops processed: {len(data)}")
    print(f"Detected potential errors: {len(errors)}")
    print("="*50 + "\n")

    # 検出された不具合の表示（先頭50件）
    for i, e in enumerate(errors[:50]):
        print(f"[{i+1}] ID: {e['id']} | Reason: {e['reason']}")
        print(f"    JP  : {e['name']}")
        if e['kana']:
            print(f"    KANA: {e['kana']}")
        print(f"    EN  : {e['romaji']}\n")

    # 全件をCSVとして出力する場合は以下をコメントアウトして使用
    """
    import csv
    with open('romaji_converted_with_errors.csv', 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=["id", "name", "kana", "romaji", "operator", "lat", "lng"])
        # 必要なフィールドに合わせて書き込み
        # ...
    print("Saved to romaji_converted_with_errors.csv")
    """
