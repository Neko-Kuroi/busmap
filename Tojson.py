import json

place = [
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu481.htm",
    "lat": "35.0307370000",
    "long": "135.7697330000",
    "name": "あおいばしにしづめ",
    "name2": "葵橋西詰"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu472.htm",
    "lat": "35.0609533400",
    "long": "135.7499049000",
    "name": "あさつゆがはらちょう",
    "name2": "朝露ヶ原町"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu285.htm",
    "lat": "34.9463820000",
    "long": "135.7430170000",
    "name": "あかいけ",
    "name2": "赤池"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu906.htm",
    "lat": "35.0324901402",
    "long": "135.7801802884",
    "name": "あすかいちょう",
    "name2": "飛鳥井町"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu025.htm",
    "lat": "35.0468428233",
    "long": "135.7395999872",
    "name": "あさひがおか",
    "name2": "旭ケ丘"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu384.htm",
    "lat": "34.9399522501",
    "long": "135.7513991000",
    "name": "あぶらのこうじたんばばし　あくときょうとまえ",
    "name2": "油小路丹波橋・アクト京都前"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu217.htm",
    "lat": "35.0137098800",
    "long": "135.6791088000",
    "name": "あらしやま",
    "name2": "嵐山"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu422.htm",
    "lat": "35.0118071432",
    "long": "135.6775459067",
    "name": "あらしやまこうえん",
    "name2": "嵐山公園"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu423.htm",
    "lat": "35.0153097376",
    "long": "135.6773276908",
    "name": "あらしやまてんりゅうじまえ",
    "name2": "嵐山天龍寺前（嵐電嵐山駅）"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu679.htm",
    "lat": "35.0367540000",
    "long": "135.7878200000",
    "name": "いおりちょう",
    "name2": "伊織町"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu214.htm",
    "lat": "35.0143360300",
    "long": "135.6915687000",
    "name": "ありすがわ",
    "name2": "有栖川"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu480.htm",
    "lat": "35.0348640000",
    "long": "135.7676940000",
    "name": "いずもじかぐらちょう",
    "name2": "出雲路神楽町"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu828.htm",
    "lat": "34.9624800000",
    "long": "135.7269560000",
    "name": "いしはらだんちまえ",
    "name2": "石原団地前"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu479.htm",
    "lat": "35.0368780000",
    "long": "135.7664220000",
    "name": "いずもじたわらちょう",
    "name2": "出雲路俵町"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu601.htm",
    "lat": "34.9373075900",
    "long": "135.7673749000",
    "name": "いたばし",
    "name2": "板橋"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu478.htm",
    "lat": "35.0378678100",
    "long": "135.7656555000",
    "name": "いずもじばし",
    "name2": "出雲路橋"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu444.htm",
    "lat": "35.0421827241",
    "long": "135.7831878601",
    "name": "いちじょうじあかのみやちょう",
    "name2": "一乗寺赤ノ宮町"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu449.htm",
    "lat": "35.0460820000",
    "long": "135.7888700000",
    "name": "いちじょうじあおしろちょう",
    "name2": "一乗寺青城町"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu450.htm",
    "lat": "35.0461560000",
    "long": "135.7867200000",
    "name": "いちじょうじきたおおまるちょう",
    "name2": "一乗寺北大丸町"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu469.htm",
    "lat": "35.0403992048",
    "long": "135.7877706276",
    "name": "いちじょうじうめのきちょう",
    "name2": "一乗寺梅ノ木町"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu099.htm",
    "lat": "35.0437086400",
    "long": "135.7918650000",
    "name": "いちじょうじさがりまつちょう",
    "name2": "一乗寺下り松町"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu100.htm",
    "lat": "35.0401888931",
    "long": "135.7917678442",
    "name": "いちじょうじきのもとちょう",
    "name2": "一乗寺木ノ本町"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu098.htm",
    "lat": "35.0464320082",
    "long": "135.7919514577",
    "name": "いちじょうじしみずちょう",
    "name2": "一乗寺清水町"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu470.htm",
    "lat": "35.0405498600",
    "long": "135.7851237000",
    "name": "いちじょうじじぞうもとちょう",
    "name2": "一乗寺地蔵本町"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu443.htm",
    "lat": "35.0437590000",
    "long": "135.7837180000",
    "name": "いちじょうじたかつきちょう",
    "name2": "一乗寺高槻町"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu013.htm",
    "lat": "35.0412020000",
    "long": "135.7708690000",
    "name": "いっぽんまつ",
    "name2": "一本松"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu261.htm",
    "lat": "34.9685010000",
    "long": "135.7684550000",
    "name": "いなりたいしゃまえ",
    "name2": "稲荷大社前"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu121.htm",
    "lat": "34.9856652099",
    "long": "135.7741100761",
    "name": "いまぐまの",
    "name2": "今熊野"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu180.htm",
    "lat": "35.0266570000",
    "long": "135.7517520000",
    "name": "いちじょうもどりばしせいめいじんじゃまえ",
    "name2": "一条戻橋・晴明神社前"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu627.htm",
    "lat": "35.0298070000",
    "long": "135.7493920000",
    "name": "いまでがわおおみや",
    "name2": "今出川大宮"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu397.htm",
    "lat": "35.0298070000",
    "long": "135.7458220000",
    "name": "いまでがわじょうふくじ",
    "name2": "今出川浄福寺"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu554.htm",
    "lat": "35.0449290000",
    "long": "135.7415720000",
    "name": "いまみやじんじゃまえ",
    "name2": "今宮神社前"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu092.htm",
    "lat": "35.0643792843",
    "long": "135.7870835423",
    "name": "いわくらおおさぎちょう",
    "name2": "岩倉大鷺町"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu290.htm",
    "lat": "34.9607760000",
    "long": "135.7425470000",
    "name": "いわのもとちょう",
    "name2": "岩ノ本町"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu841.htm",
    "lat": "35.0651779700",
    "long": "135.7813188000",
    "name": "いわくらそうしゃじょうまえ",
    "name2": "岩倉操車場前"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu811.htm",
    "lat": "34.9513157100",
    "long": "135.6880819000",
    "name": "うきょうのさと",
    "name2": "右京の里"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu911.htm",
    "lat": "35.0155500000",
    "long": "135.7166030000",
    "name": "うきょうふれあいぶんかかいかんまえ",
    "name2": "右京ふれあい文化会館前"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu408.htm",
    "lat": "34.9707090000",
    "long": "135.7166890000",
    "name": "うしがせ",
    "name2": "牛ヶ瀬"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu551.htm",
    "lat": "35.0499820000",
    "long": "135.7441410000",
    "name": "うしわか",
    "name2": "牛若"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu717.htm",
    "lat": "35.0193800000",
    "long": "135.7099560000",
    "name": "うずまさえいがむらみち",
    "name2": "太秦映画村道"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu721.htm",
    "lat": "35.0210019000",
    "long": "135.6967628000",
    "name": "うずまさかいにちちょう",
    "name2": "太秦開日町"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu720.htm",
    "lat": "35.0209799363",
    "long": "135.6991687000",
    "name": "うずまさきたろちょう",
    "name2": "太秦北路町"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu210.htm",
    "lat": "35.0139153300",
    "long": "135.7064295000",
    "name": "うずまさこうりゅうじまえ",
    "name2": "太秦広隆寺前"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu325.htm",
    "lat": "35.0116090000",
    "long": "135.7081770000",
    "name": "うずまさしょうがっこうまえ",
    "name2": "太秦小学校前"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu863.htm",
    "lat": "35.0103570000",
    "long": "135.7154420000",
    "name": "うずまさてんじんがわえきまえ",
    "name2": "太秦天神川駅前"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu209.htm",
    "lat": "35.0136694400",
    "long": "135.7108821000",
    "name": "うずまさひがしぐち",
    "name2": "太秦東口"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu211.htm",
    "lat": "35.0146382200",
    "long": "135.7044406000",
    "name": "うずまさひらきちょう",
    "name2": "太秦開町"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu613.htm",
    "lat": "35.0248569700",
    "long": "135.7099103000",
    "name": "うたのおやしきちょう",
    "name2": "宇多野御屋敷町"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu196.htm",
    "lat": "35.0276080000",
    "long": "135.7028400000",
    "name": "うたのびょういんまえ",
    "name2": "宇多野病院前"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu419.htm",
    "lat": "35.0041290000",
    "long": "135.6847667000",
    "name": "うちだちょう",
    "name2": "内田町"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu123.htm",
    "lat": "34.9917684486",
    "long": "135.7747817202",
    "name": "うままち",
    "name2": "馬町"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu753.htm",
    "lat": "35.0152780000",
    "long": "135.7204580000",
    "name": "うまつかちょう",
    "name2": "馬塚町"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu169.htm",
    "lat": "35.0406890000",
    "long": "135.6869040000",
    "name": "うめがはたしみずしょう",
    "name2": "梅ケ畑清水町"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu357.htm",
    "lat": "34.9876435600",
    "long": "135.7428488000",
    "name": "うめこうじこうえん・きょうとてつどうはくぶつかんまえ",
    "name2": "梅小路公園・京都鉄道博物館前"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu689.htm",
    "lat": "35.0021950000",
    "long": "135.7057930000",
    "name": "うめづいしなだちょう",
    "name2": "梅津石灘町"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu413.htm",
    "lat": "35.0036530000",
    "long": "135.7061140000",
    "name": "うめづだんまち",
    "name2": "梅津段町"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu356.htm",
    "lat": "34.9891352400",
    "long": "135.7436481000",
    "name": "うめこうじこうえん・じぇいあーるきょうとにしえきまえ",
    "name2": "梅小路公園・ＪＲ梅小路京都西駅前"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu415.htm",
    "lat": "35.0031830000",
    "long": "135.6987750000",
    "name": "うめづにしうらちょう",
    "name2": "梅津西浦町"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu416.htm",
    "lat": "35.0024670000",
    "long": "135.6955510000",
    "name": "うめのみやたいしゃまえ",
    "name2": "梅宮大社前"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu452.htm",
    "lat": "35.0342600189",
    "long": "135.7807165509",
    "name": "えいでんもとたなか",
    "name2": "叡電元田中"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu118.htm",
    "lat": "34.9796155100",
    "long": "135.7611397000",
    "name": "おおいしばし（ちかてつ　くじょうえき）",
    "name2": "大石橋《地下鉄九条駅》"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu213.htm",
    "lat": "35.0142730800",
    "long": "135.6942815000",
    "name": "おいたぐち",
    "name2": "生田口"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu849.htm",
    "lat": "34.9854195500",
    "long": "135.6589387000",
    "name": "おおえやまちょうにし",
    "name2": "大枝山町西"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu855.htm",
    "lat": "34.9859028875",
    "long": "135.6705140553",
    "name": "おおえやまちょうひがし",
    "name2": "大枝山町東"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu815.htm",
    "lat": "34.9543790200",
    "long": "135.6674764000",
    "name": "おおはらのしょうがっこうまえ",
    "name2": "大原野小学校前"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu824.htm",
    "lat": "34.9510710000",
    "long": "135.6911150000",
    "name": "おおはらのかみざときたのちょう",
    "name2": "大原野上里北ノ町"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu547.htm",
    "lat": "35.0551390000",
    "long": "135.7440320000",
    "name": "おおみやおのぼりちょう",
    "name2": "大宮小野堀町"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu550.htm",
    "lat": "35.0525400000",
    "long": "135.7440920000",
    "name": "おおみやこうつうこうえんまえ",
    "name2": "大宮交通公園前"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu302.htm",
    "lat": "34.9962917889",
    "long": "135.7491736442",
    "name": "おおみやごじょう",
    "name2": "大宮五条"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu036.htm",
    "lat": "35.0583180000",
    "long": "135.7440380000",
    "name": "おおみやそうもんぐちちょう",
    "name2": "大宮総門口町"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu549.htm",
    "lat": "35.0525770000",
    "long": "135.7460690000",
    "name": "おおみやだいもんちょう",
    "name2": "大宮大門町"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu037.htm",
    "lat": "35.0570080000",
    "long": "135.7469900000",
    "name": "おおみやたじりちょう",
    "name2": "大宮田尻町"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu580.htm",
    "lat": "35.0250010000",
    "long": "135.7483300000",
    "name": "おおみやなかだちうり",
    "name2": "大宮中立売"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu303.htm",
    "lat": "34.9990870000",
    "long": "135.7491320000",
    "name": "おおみやまつばら",
    "name2": "大宮松原"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu110.htm",
    "lat": "35.0136437200",
    "long": "135.7840130000",
    "name": "おかざきこうえん　どうぶつえんまえ",
    "name2": "岡崎公園動物園前"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu111.htm",
    "lat": "35.0123790000",
    "long": "135.7826800000",
    "name": "おかざきこうえん　びじゅつかん･へいあんじんぐうまえ",
    "name2": "岡崎公園 美術館・平安神宮前"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu304.htm",
    "lat": "35.0136584200",
    "long": "135.7812718000",
    "name": "おかざきこうえん　ろーむしあたーきょうと・みやこめっせまえ",
    "name2": "岡崎公園 ロームシアター京都・みやこめっせ前"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu463.htm",
    "lat": "35.0166854265",
    "long": "135.7881283142",
    "name": "おかざきじんじゃまえ",
    "name2": "岡崎神社前"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu109.htm",
    "lat": "35.0135150000",
    "long": "135.7875110000",
    "name": "おかざきほっしょうじちょう",
    "name2": "岡崎法勝寺町"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu462.htm",
    "lat": "35.0169587726",
    "long": "135.7856966528",
    "name": "おかざきみち",
    "name2": "岡崎道"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu524.htm",
    "lat": "34.9733280000",
    "long": "135.7389150000",
    "name": "おちあいちょう",
    "name2": "落合町"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu134.htm",
    "lat": "34.9817410000",
    "long": "135.7441410000",
    "name": "おどい",
    "name2": "御土居"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu624.htm",
    "lat": "35.0283990000",
    "long": "135.7161460000",
    "name": "おむろ",
    "name2": "御室"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu776.htm",
    "lat": "34.9678980000",
    "long": "135.6756470000",
    "name": "おばたがわこうえんきたぐち",
    "name2": "小畑川公園北口"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu163.htm",
    "lat": "35.0280160000",
    "long": "135.7138230000",
    "name": "おむろにんなじ",
    "name2": "御室仁和寺"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu208.htm",
    "lat": "35.0113000000",
    "long": "135.7139220000",
    "name": "かいこのやしろ",
    "name2": "蚕ノ社"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu380.htm",
    "lat": "34.9745616049",
    "long": "135.6941632620",
    "name": "かたぎはら",
    "name2": "樫原"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu789.htm",
    "lat": "34.9752322900",
    "long": "135.6866696000",
    "name": "かたぎはらしぎたに",
    "name2": "樫原鴫谷"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu796.htm",
    "lat": "34.9731245300",
    "long": "135.6966872000",
    "name": "かたぎはらしょうがっこうまえ",
    "name2": "樫原小学校前"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu825.htm",
    "lat": "34.973142",
    "long": "135.691726",
    "name": "かたぎはらつかのもとちょう",
    "name2": "樫原塚ノ本町"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu827.htm",
    "lat": "34.971999",
    "long": "135.686114",
    "name": "かたぎはらはかりだにちょう",
    "name2": "樫原秤谷町"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu795.htm",
    "lat": "34.9731543489",
    "long": "135.6941299976",
    "name": "かたぎはらみずつきちょう",
    "name2": "樫原水築町"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu212.htm",
    "lat": "35.0148090000",
    "long": "135.7007400000",
    "name": "かたびらのつじ",
    "name2": "帷子ノ辻"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu814.htm",
    "lat": "34.9474080000",
    "long": "135.6911770000",
    "name": "かつやまちょう",
    "name2": "勝山町"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu886.htm",
    "lat": "34.9782608000",
    "long": "135.6829897000",
    "name": "かつらいのべーしょんぱーくまえ",
    "name2": "桂イノベーションパーク前"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu798.htm",
    "lat": "34.9793260000",
    "long": "135.7025530000",
    "name": "かつらえきにしぐち",
    "name2": "桂駅西口"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu378.htm",
    "lat": "34.9798459300",
    "long": "135.7037593000",
    "name": "かつらえきひがしぐち",
    "name2": "桂駅東口"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu374.htm",
    "lat": "34.9841894600",
    "long": "135.7152396000",
    "name": "かつらおおはし",
    "name2": "桂大橋"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu690.htm",
    "lat": "34.9943025900",
    "long": "135.7013789000",
    "name": "かつらがわしょうがっこうまえ",
    "name2": "桂川小学校前"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu637.htm",
    "lat": "34.9731180000",
    "long": "135.7032600000",
    "name": "かつらこうこうまえ",
    "name2": "桂高校前"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu638.htm",
    "lat": "34.9842022600",
    "long": "135.7175562000",
    "name": "かつらこばし",
    "name2": "桂小橋"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu854.htm",
    "lat": "34.9819514003",
    "long": "135.6780808460",
    "name": "かつらごりょうざか",
    "name2": "桂御陵坂"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu386.htm",
    "lat": "34.9766167654",
    "long": "135.6669650681",
    "name": "かつらざかぐち",
    "name2": "桂坂口"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu851.htm",
    "lat": "34.9856406200",
    "long": "135.6642303000",
    "name": "かつらざかしょうがっこうまえ",
    "name2": "桂坂小学校前"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu843.htm",
    "lat": "34.9824549900",
    "long": "135.6656633000",
    "name": "かつらざかせんたーまえ",
    "name2": "桂坂センター前"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu950.htm",
    "lat": "34.9843597800",
    "long": "135.6654992000",
    "name": "かつらざかちゅうおう",
    "name2": "桂坂中央"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu377.htm",
    "lat": "34.9800157400",
    "long": "135.7072790000",
    "name": "かつらしょうぼうしょまえ",
    "name2": "桂消防署前"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu401.htm",
    "lat": "34.9768120000",
    "long": "135.7129090000",
    "name": "かつらたきがわちょう",
    "name2": "桂滝川町"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu437.htm",
    "lat": "34.9877210000",
    "long": "135.6929680000",
    "name": "かつらちゅうがくまえ",
    "name2": "桂中学前"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu388.htm",
    "lat": "34.9884130000",
    "long": "135.7046692712",
    "name": "かつらとくだいじ",
    "name2": "桂徳大寺"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu375.htm",
    "lat": "34.9829377300",
    "long": "135.7112455000",
    "name": "かつらりきゅうまえ",
    "name2": "桂離宮前"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu782.htm",
    "lat": "35.0003910000",
    "long": "135.7197040000",
    "name": "かどのおおじたかつじ",
    "name2": "葛野大路高辻"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu772.htm",
    "lat": "34.9753910000",
    "long": "135.7261530000",
    "name": "かどのおおじくじょう",
    "name2": "葛野大路九条"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu784.htm",
    "lat": "34.9909870200",
    "long": "135.7198064000",
    "name": "かどのおおじはなやちょう",
    "name2": "葛野大路花屋町"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu558.htm",
    "lat": "34.9847810000",
    "long": "135.7198520000",
    "name": "かどのおおじはちじょう",
    "name2": "葛野大路八条"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu080.htm",
    "lat": "35.0327066000",
    "long": "135.7935456000",
    "name": "かみいけだちょう",
    "name2": "上池田町"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu686.htm",
    "lat": "34.9906610000",
    "long": "135.6986760000",
    "name": "かみかつらにしいちょう",
    "name2": "上桂西居町"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu685.htm",
    "lat": "34.9905750000",
    "long": "135.6958960000",
    "name": "かみかつらえきまえ",
    "name2": "上桂駅前"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu389.htm",
    "lat": "34.9903770000",
    "long": "135.7039140000",
    "name": "かみかつらひがしのくち",
    "name2": "上桂東ノ口"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu433.htm",
    "lat": "34.9906357500",
    "long": "135.7023399000",
    "name": "かみかつらみしょうちょう",
    "name2": "上桂御正町"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu434.htm",
    "lat": "34.9888511515",
    "long": "135.6997463865",
    "name": "かみかつらまえだちょう",
    "name2": "上桂前田町"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu060.htm",
    "lat": "35.0538280000",
    "long": "135.7604050000",
    "name": "かみがもいしかずちょう",
    "name2": "上賀茂石計町"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu088.htm",
    "lat": "35.0543470000",
    "long": "135.7671630000",
    "name": "かみがもさかきだちょう",
    "name2": "上賀茂榊田町"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu745.htm",
    "lat": "35.0560846200",
    "long": "135.7599503000",
    "name": "かみがもしょうがっこうまえ",
    "name2": "上賀茂小学校前"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu041.htm",
    "lat": "35.0539388259",
    "long": "135.7564986270",
    "name": "かみがもしょうぶえんちょう",
    "name2": "上賀茂菖蒲園町"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu129.htm",
    "lat": "35.0577570000",
    "long": "135.7519910000",
    "name": "かみがもじんじゃまえ",
    "name2": "上賀茂神社前"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu743.htm",
    "lat": "35.0561390000",
    "long": "135.7640870000",
    "name": "かみがもとよだちょう",
    "name2": "上賀茂豊田町"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu708.htm",
    "lat": "35.0531697414",
    "long": "135.7549198331",
    "name": "かみがもばし",
    "name2": "上賀茂橋"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu744.htm",
    "lat": "35.0546930000",
    "long": "135.7632960000",
    "name": "かみがもまつもとちょう",
    "name2": "上賀茂松本町"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu038.htm",
    "lat": "35.0570081300",
    "long": "135.7506440000",
    "name": "かみがもみそのばし",
    "name2": "上賀茂御薗橋"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu365.htm",
    "lat": "34.9394760000",
    "long": "135.7325280000",
    "name": "かみかわしょうがっこうまえ",
    "name2": "神川小学校前"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu628.htm",
    "lat": "35.0292430000",
    "long": "135.7565870000",
    "name": "かみぎょうくそうごうちょうしゃまえ",
    "name2": "上京区総合庁舎前"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu812.htm",
    "lat": "34.9536140500",
    "long": "135.6840424000",
    "name": "かみざとしょうがっこうまえ",
    "name2": "上里小学校前"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu156.htm",
    "lat": "35.0293260000",
    "long": "135.7391130000",
    "name": "かみしちけん",
    "name2": "上七軒"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu093.htm",
    "lat": "35.0638104800",
    "long": "135.7914841000",
    "name": "かみたかの",
    "name2": "上高野"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu309.htm",
    "lat": "34.9655940000",
    "long": "135.7451910000",
    "name": "かみとば",
    "name2": "上鳥羽"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu830.htm",
    "lat": "34.9623820000",
    "long": "135.7359130000",
    "name": "かみとばうままわし",
    "name2": "上鳥羽馬廻"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu292.htm",
    "lat": "34.9643710000",
    "long": "135.7424610000",
    "name": "かみとばしょうがっこうまえ",
    "name2": "上鳥羽小学校前"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu842.htm",
    "lat": "34.9463580000",
    "long": "135.7392610000",
    "name": "かみとばとうのもり",
    "name2": "上鳥羽塔ノ森"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu293.htm",
    "lat": "34.9656680000",
    "long": "135.7409660000",
    "name": "かみとばむらやまちょう",
    "name2": "上鳥羽村山町"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu294.htm",
    "lat": "34.9683528000",
    "long": "135.7410240000",
    "name": "かみのちょう",
    "name2": "上ノ町"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu687.htm",
    "lat": "34.9967503300",
    "long": "135.7036051000",
    "name": "かみのばし",
    "name2": "上野橋"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu101.htm",
    "lat": "35.0365940000",
    "long": "135.7916870000",
    "name": "かみはてちょう・うりゅうやまがくえん きょうとげいじゅつだいがくまえ",
    "name2": "上終町・瓜生山学園 京都芸術大学前"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu360.htm",
    "lat": "34.9221060000",
    "long": "135.7223970000",
    "name": "かみひづめ",
    "name2": "上樋爪"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu021.htm",
    "lat": "35.0499330000",
    "long": "135.7514680000",
    "name": "かみほりかわ",
    "name2": "上堀川"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu467.htm",
    "lat": "35.0201120000",
    "long": "135.7932060000",
    "name": "かみみやのまえちょう",
    "name2": "上宮ノ前町"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu039.htm",
    "lat": "35.0543178000",
    "long": "135.7513549000",
    "name": "かもがわちゅうがくまえ",
    "name2": "加茂川中学前"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu049.htm",
    "lat": "35.0256190000",
    "long": "135.7594670000",
    "name": "からすまいちじょう",
    "name2": "烏丸一条"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu048.htm",
    "lat": "35.0290563300",
    "long": "135.7600468000",
    "name": "からすまいまでがわ（ちかてつ　いまでがわえきまえ）",
    "name2": "烏丸今出川《地下鉄今出川駅》"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu053.htm",
    "lat": "35.0108136000",
    "long": "135.7596702000",
    "name": "からすまおいけ",
    "name2": "烏丸御池"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu017.htm",
    "lat": "35.0436254316",
    "long": "135.7593114288",
    "name": "からすまきたおおじ",
    "name2": "烏丸北大路"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu057.htm",
    "lat": "34.9962051600",
    "long": "135.7597339000",
    "name": "からすまごじょう（ちかてつ　ごじょうえき）",
    "name2": "烏丸五条《地下鉄五条駅》"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu054.htm",
    "lat": "35.0078939000",
    "long": "135.7596177000",
    "name": "からすまさんじょう",
    "name2": "烏丸三条"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu831.htm",
    "lat": "35.0197770000",
    "long": "135.7594870000",
    "name": "からすましもだちうり",
    "name2": "烏丸下立売"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu050.htm",
    "lat": "35.0221583800",
    "long": "135.7593227000",
    "name": "からすましもちょうじゃまち",
    "name2": "烏丸下長者町"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu059.htm",
    "lat": "34.9892889000",
    "long": "135.7596682000",
    "name": "からすまななじょう",
    "name2": "烏丸七条"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu052.htm",
    "lat": "35.0142312300",
    "long": "135.7596040000",
    "name": "からすまにじょう",
    "name2": "烏丸二条"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu391.htm",
    "lat": "34.9762350000",
    "long": "135.7596960000",
    "name": "からすまふだのつじ",
    "name2": "烏丸札ノ辻"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu056.htm",
    "lat": "34.9995847000",
    "long": "135.7596928000",
    "name": "からすままつばら",
    "name2": "烏丸松原"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu051.htm",
    "lat": "35.0173750000",
    "long": "135.7595420000",
    "name": "からすままるたまち（ちかてつ　まるたまちえき）",
    "name2": "烏丸丸太町《地下鉄丸太町駅》"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu297.htm",
    "lat": "34.9760330000",
    "long": "135.7414230000",
    "name": "からとちょう",
    "name2": "唐戸町"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu058.htm",
    "lat": "34.992705",
    "long": "135.759835",
    "name": "からすまろくじょう",
    "name2": "烏丸六条"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu826.htm",
    "lat": "34.9763476100",
    "long": "135.6982200000",
    "name": "かわしまあわたちょう",
    "name2": "川島粟田町"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu379.htm",
    "lat": "34.9765131800",
    "long": "135.7009827000",
    "name": "かわしまちょう",
    "name2": "川島町"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu634.htm",
    "lat": "34.9650930000",
    "long": "135.7033830000",
    "name": "かわしまろくのつぼちょう",
    "name2": "川島六ノ坪町"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu393.htm",
    "lat": "35.0131922147",
    "long": "135.7724138859",
    "name": "かわばたにじょう",
    "name2": "川端二条"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu008.htm",
    "lat": "35.0291749600",
    "long": "135.7696821601",
    "name": "かわらまちいまでがわ",
    "name2": "河原町今出川"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu496.htm",
    "lat": "34.9959113000",
    "long": "135.7661763000",
    "name": "かわらまちごじょう",
    "name2": "河原町五条"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu003.htm",
    "lat": "35.0087710000",
    "long": "135.7690040000",
    "name": "かわらまちさんじょう",
    "name2": "河原町三条"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu529.htm",
    "lat": "34.9747030000",
    "long": "135.7638840000",
    "name": "かわらまちじゅうじょう",
    "name2": "河原町十条"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu535.htm",
    "lat": "34.9929140000",
    "long": "135.7645390000",
    "name": "かわらまちしょうめん",
    "name2": "河原町正面"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu329.htm",
    "lat": "34.9819279200",
    "long": "135.7641989000",
    "name": "かわらまちとうじみち",
    "name2": "河原町東寺道"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu539.htm",
    "lat": "34.9843614500",
    "long": "135.7642794000",
    "name": "かわらまちはちじょう",
    "name2": "河原町八条"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu495.htm",
    "lat": "34.9989830000",
    "long": "135.7676111000",
    "name": "かわらまちまつばら",
    "name2": "河原町松原"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu005.htm",
    "lat": "35.0175567033",
    "long": "135.7690174110",
    "name": "かわらまちまるたまち",
    "name2": "河原町丸太町"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu619.htm",
    "lat": "34.9694400000",
    "long": "135.7629700000",
    "name": "かんじんばし",
    "name2": "勧進橋"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu127.htm",
    "lat": "35.0038176500",
    "long": "135.7771711000",
    "name": "ぎおん",
    "name2": "祇園"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu044.htm",
    "lat": "35.0406918000",
    "long": "135.7517216000",
    "name": "きたおおじほりかわ",
    "name2": "北大路堀川"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu707.htm",
    "lat": "35.0442976300",
    "long": "135.7582176000",
    "name": "きたおおじばすたーみなる（ちかてつ　きたおおじえき）",
    "name2": "北大路バスターミナル《地下鉄北大路駅》"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu018.htm",
    "lat": "35.0427550000",
    "long": "135.7555570000",
    "name": "きたおおじしんまち",
    "name2": "北大路新町"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu555.htm",
    "lat": "34.9662120000",
    "long": "135.7135020000",
    "name": "きたかみくぜ",
    "name2": "北上久世"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu725.htm",
    "lat": "35.0288652000",
    "long": "135.7863020000",
    "name": "きたしらかわ",
    "name2": "北白川"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu846.htm",
    "lat": "34.9792035497",
    "long": "135.6662753557",
    "name": "きたくつかけちょうろくちょうめ",
    "name2": "北沓掛町六丁目"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu027.htm",
    "lat": "35.0467330000",
    "long": "135.7370250000",
    "name": "きたこのはたちょう",
    "name2": "北木ノ畑町"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu078.htm",
    "lat": "35.0331710000",
    "long": "135.7869300000",
    "name": "きたしらかわおぐらちょう",
    "name2": "北白川小倉町"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu102.htm",
    "lat": "35.0301410800",
    "long": "135.7914837000",
    "name": "きたしらかわこうまえ",
    "name2": "北白川校前"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu081.htm",
    "lat": "35.0321939400",
    "long": "135.7957962000",
    "name": "きたしらかわしぶせちょう",
    "name2": "北白川仕伏町"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu079.htm",
    "lat": "35.0329127987",
    "long": "135.7915828467",
    "name": "きたしらかわべっとうちょう",
    "name2": "北白川別当町"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu084.htm",
    "lat": "35.0475849135",
    "long": "135.7707002356",
    "name": "きたぞのちょう",
    "name2": "北園町"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu688.htm",
    "lat": "34.9666032600",
    "long": "135.6940672000",
    "name": "きたのぐち",
    "name2": "北ノ口"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu248.htm",
    "lat": "35.0213440000",
    "long": "135.7317250000",
    "name": "きたのちゅうがくまえ",
    "name2": "北野中学前"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu157.htm",
    "lat": "35.0278430000",
    "long": "135.7353330000",
    "name": "きたのてんまんぐうまえ",
    "name2": "北野天満宮前"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu158.htm",
    "lat": "35.0273360000",
    "long": "135.7314410000",
    "name": "きたのはくばいちょう",
    "name2": "北野白梅町"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu810.htm",
    "lat": "34.9624430000",
    "long": "135.6823310000",
    "name": "きたふくにしちょう",
    "name2": "北福西町"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu087.htm",
    "lat": "35.0514289300",
    "long": "135.7673277000",
    "name": "きたやまえきまえ",
    "name2": "北山駅前"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu793.htm",
    "lat": "34.9648391100",
    "long": "135.6792920000",
    "name": "きたふくにしちょういっちょうめ",
    "name2": "北福西町一丁目"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu590.htm",
    "lat": "35.0505540000",
    "long": "135.7589720000",
    "name": "きたやまばしひがしづめ",
    "name2": "北山橋東詰"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu520.htm",
    "lat": "34.9658290000",
    "long": "135.7351840000",
    "name": "きっしょういんいけだちょう",
    "name2": "吉祥院池田町"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu771.htm",
    "lat": "34.9788750000",
    "long": "135.7236570000",
    "name": "きっしょういんいちのだんちょう",
    "name2": "吉祥院壱ノ段町"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu559.htm",
    "lat": "34.9692880000",
    "long": "135.7265230000",
    "name": "きっしょういんうんどうこうえんまえ",
    "name2": "吉祥院運動公園前"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu236.htm",
    "lat": "34.9760950000",
    "long": "135.7292540000",
    "name": "きっしょういんくるまみちちょう",
    "name2": "吉祥院車道町"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu829.htm",
    "lat": "34.9600100000",
    "long": "135.7296000000",
    "name": "きっしょういんしまたかまち",
    "name2": "吉祥院嶋高町"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu522.htm",
    "lat": "34.9705730000",
    "long": "135.7354560000",
    "name": "きっしょういんたかはたちょう",
    "name2": "吉祥院高畑町"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu523.htm",
    "lat": "34.9734270000",
    "long": "135.7363210000",
    "name": "きっしょういんてんまんぐうまえ",
    "name2": "吉祥院天満宮前"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu519.htm",
    "lat": "34.9659270000",
    "long": "135.7305760000",
    "name": "きっしょういんどうのあとちょう",
    "name2": "吉祥院堂ノ後町"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu234.htm",
    "lat": "34.9674470000",
    "long": "135.7264860000",
    "name": "きっしょういんながたちょう",
    "name2": "吉祥院長田町"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu235.htm",
    "lat": "34.9732290000",
    "long": "135.7266590000",
    "name": "きっしょういんにしのちゃやちょう",
    "name2": "吉祥院西ノ茶屋町"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu536.htm",
    "lat": "34.9657920000",
    "long": "135.7370000000",
    "name": "きっしょういんまきえちょう",
    "name2": "吉祥院蒔絵町"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu770.htm",
    "lat": "34.9828660000",
    "long": "135.7208770000",
    "name": "きっしょういんみやのにしちょう",
    "name2": "吉祥院宮ノ西町"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu608.htm",
    "lat": "35.0194796600",
    "long": "135.7233059000",
    "name": "きつじみなみちょう",
    "name2": "木辻南町"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu247.htm",
    "lat": "35.0303020000",
    "long": "135.7314410000",
    "name": "きぬがさこうまえ",
    "name2": "衣笠校前"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu775.htm",
    "lat": "35.0411370000",
    "long": "135.7244480000",
    "name": "きぬがさひむろちょう",
    "name2": "衣笠氷室町"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu271.htm",
    "lat": "34.9485221763",
    "long": "135.7736784577",
    "name": "きょういくだいがくまえ",
    "name2": "教育大学前"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu885.htm",
    "lat": "34.9800585200",
    "long": "135.6810585000",
    "name": "きょうだいかつらきゃんぱすまえ",
    "name2": "京大桂キャンパス前"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu726.htm",
    "lat": "35.0285750000",
    "long": "135.7836930000",
    "name": "きょうだいのうがくぶまえ",
    "name2": "京大農学部前"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu453.htm",
    "lat": "35.0254870000",
    "long": "135.7786400000",
    "name": "きょうだいせいもんまえ",
    "name2": "京大正門前"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu699.htm",
    "lat": "35.0195191968",
    "long": "135.7784735865",
    "name": "きょうだいびょういんまえ",
    "name2": "京大病院前"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu115.htm",
    "lat": "34.9840884300",
    "long": "135.7585785000",
    "name": "きょうとえきはちじょうぐち",
    "name2": "京都駅八条口"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu532.htm",
    "lat": "34.9839910000",
    "long": "135.7611210000",
    "name": "きょうとえきはちじょうぐちあばんてぃまえ",
    "name2": "京都駅八条口アバンティ前"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu061.htm",
    "lat": "34.9866600600",
    "long": "135.7586650000",
    "name": "きょうとえきまえ",
    "name2": "京都駅前"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu062.htm",
    "lat": "35.0036900000",
    "long": "135.7167140000",
    "name": "きょうとがいだいまえ",
    "name2": "京都外大前"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu475.htm",
    "lat": "35.0718200000",
    "long": "135.7563870000",
    "name": "きょうとさんだいまえ",
    "name2": "京都産大前"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu004.htm",
    "lat": "35.0109827000",
    "long": "135.7688760000",
    "name": "きょうとしやくしょまえ",
    "name2": "京都市役所前"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu405.htm",
    "lat": "35.0108680000",
    "long": "135.7194690000",
    "name": "きょうとせんたんかがくだいがくまえ",
    "name2": "京都先端科学大学前"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu800.htm",
    "lat": "34.9687010000",
    "long": "135.6809600000",
    "name": "きょうとめいとくこうこうまえ",
    "name2": "京都明徳高校前"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu459.htm",
    "lat": "34.9962228442",
    "long": "135.7411760000",
    "name": "きょうとりさーちぱーくまえ",
    "name2": "京都リサーチパーク前"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu317.htm",
    "lat": "34.9308200000",
    "long": "135.7588060000",
    "name": "きょうばし",
    "name2": "京橋"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu125.htm",
    "lat": "34.9979456173",
    "long": "135.7770734644",
    "name": "きよみずみち",
    "name2": "清水道"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu221.htm",
    "lat": "35.0398760000",
    "long": "135.7336150000",
    "name": "きんかくじみち",
    "name2": "金閣寺道"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu578.htm",
    "lat": "34.9659690000",
    "long": "135.7520730000",
    "name": "きんてつかみとばぐちえきまえ",
    "name2": "近鉄上鳥羽口駅前"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu105.htm",
    "lat": "35.0212490000",
    "long": "135.7922670000",
    "name": "きんりんしゃこまえ",
    "name2": "錦林車庫前"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu464.htm",
    "lat": "35.0273520000",
    "long": "135.7939720000",
    "name": "ぎんかくじまえ",
    "name2": "銀閣寺前"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu350.htm",
    "lat": "34.9796210000",
    "long": "135.7597450000",
    "name": "くじょうえきまえ",
    "name2": "九条駅前"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu131.htm",
    "lat": "34.9793570000",
    "long": "135.7492930000",
    "name": "くじょうおおみや",
    "name2": "九条大宮"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu103.htm",
    "lat": "35.0278840000",
    "long": "135.7914770000",
    "name": "ぎんかくじみち",
    "name2": "銀閣寺道"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu137.htm",
    "lat": "34.9781830000",
    "long": "135.7361480000",
    "name": "くじょうおんまえどおり",
    "name2": "九条御前通"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu531.htm",
    "lat": "34.9796330000",
    "long": "135.7641190000",
    "name": "くじょうかわらまち",
    "name2": "九条河原町"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu130.htm",
    "lat": "34.9794230000",
    "long": "135.7530370000",
    "name": "くじょうきんてつまえ",
    "name2": "九条近鉄前"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu731.htm",
    "lat": "34.9785290000",
    "long": "135.7391870000",
    "name": "くじょうしちほんまつ",
    "name2": "九条七本松"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu117.htm",
    "lat": "34.9795090000",
    "long": "135.7565450000",
    "name": "くじょうしゃこまえ",
    "name2": "九条車庫前"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu623.htm",
    "lat": "34.9516450000",
    "long": "135.7210750000",
    "name": "くぜおおやぶちょう",
    "name2": "久世大薮町"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu622.htm",
    "lat": "34.9516210000",
    "long": "135.7274250000",
    "name": "くぜこうぎょうだんちまえ",
    "name2": "久世工業団地前"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu229.htm",
    "lat": "34.9513120000",
    "long": "135.7167390000",
    "name": "くぜとのしろちょう",
    "name2": "久世殿城町"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu632.htm",
    "lat": "34.9641377700",
    "long": "135.7130412000",
    "name": "くぜしちほんまつ",
    "name2": "久世七本松"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu819.htm",
    "lat": "34.9669450000",
    "long": "135.7543590000",
    "name": "くぜばしどおりあぶらのこうじ",
    "name2": "久世橋通油小路"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu818.htm",
    "lat": "34.9655940000",
    "long": "135.7492560000",
    "name": "くぜばしどおりおおみや",
    "name2": "久世橋通大宮"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu820.htm",
    "lat": "34.9696750000",
    "long": "135.7578920000",
    "name": "くぜばしどおりしんまち",
    "name2": "久世橋通新町"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu232.htm",
    "lat": "34.9644080000",
    "long": "135.7206920000",
    "name": "くぜばしにしづめ",
    "name2": "久世橋西詰"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu233.htm",
    "lat": "34.9660510000",
    "long": "135.7264620000",
    "name": "くぜばしひがしづめ",
    "name2": "久世橋東詰"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu455.htm",
    "lat": "35.0173992200",
    "long": "135.7784013000",
    "name": "くまのじんじゃまえ",
    "name2": "熊野神社前"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu215.htm",
    "lat": "35.0143449800",
    "long": "135.6890189000",
    "name": "くるまざきじんじゃまえ",
    "name2": "車折神社前"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu593.htm",
    "lat": "35.0160200000",
    "long": "135.7155410000",
    "name": "くろばし",
    "name2": "黒橋"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu262.htm",
    "lat": "34.9651160000",
    "long": "135.7684180000",
    "name": "けいさつがっこうまえ",
    "name2": "警察学校前"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu883.htm",
    "lat": "34.9261121595",
    "long": "135.7590974907",
    "name": "けいはんちゅうしょじま・ふしみこうこうえん",
    "name2": "京阪中書島・伏見港公園"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu324.htm",
    "lat": "34.9059191200",
    "long": "135.7201248000",
    "name": "けいはんよどえき",
    "name2": "京阪淀駅"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu395.htm",
    "lat": "35.0341734043",
    "long": "135.7412742798",
    "name": "けんりゅうこうまえ",
    "name2": "乾隆校前"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu032.htm",
    "lat": "35.0527447615",
    "long": "135.7366999067",
    "name": "げんたく",
    "name2": "玄琢"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu033.htm",
    "lat": "35.0517551234",
    "long": "135.7410989067",
    "name": "げんたくした",
    "name2": "玄琢下"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu224.htm",
    "lat": "35.0407780000",
    "long": "135.7447960000",
    "name": "けんくんじんじゃまえ",
    "name2": "建勲神社前"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu381.htm",
    "lat": "34.9744462900",
    "long": "135.6910806000",
    "name": "こうかいどうまえ",
    "name2": "公会堂前"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu564.htm",
    "lat": "34.9270628200",
    "long": "135.7176305000",
    "name": "こうぎょうだんちまえ",
    "name2": "工業団地前"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu429.htm",
    "lat": "34.9960711559",
    "long": "135.7197601865",
    "name": "こうかじょしがくえんまえ",
    "name2": "光華女子学園前"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu206.htm",
    "lat": "35.0082731600",
    "long": "135.7194217000",
    "name": "こうしんまえ",
    "name2": "庚申前"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu902.htm",
    "lat": "35.0213775100",
    "long": "135.7693595000",
    "name": "こうじんぐち",
    "name2": "荒神口"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu085.htm",
    "lat": "35.0493426700",
    "long": "135.7706205000",
    "name": "こうどのちょう",
    "name2": "神殿町"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu287.htm",
    "lat": "34.9541660000",
    "long": "135.7416210000",
    "name": "こえだばし",
    "name2": "小枝橋"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu284.htm",
    "lat": "34.9455050000",
    "long": "135.7335280000",
    "name": "こが",
    "name2": "久我"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu226.htm",
    "lat": "34.9476800000",
    "long": "135.7247810000",
    "name": "こがいしはらちょう",
    "name2": "久我石原町"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu364.htm",
    "lat": "34.9420090000",
    "long": "135.7329230000",
    "name": "こがおたびちょう",
    "name2": "久我御旅町"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu373.htm",
    "lat": "34.9345470000",
    "long": "135.7270050000",
    "name": "こがのもり",
    "name2": "久我の杜"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu091.htm",
    "lat": "35.0637689600",
    "long": "135.7851771000",
    "name": "こくさいかいかんえきまえ",
    "name2": "国際会館駅前"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu311.htm",
    "lat": "34.9462840000",
    "long": "135.7453150000",
    "name": "こくどうあかいけ",
    "name2": "国道赤池"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu314.htm",
    "lat": "34.9326875000",
    "long": "135.7459186000",
    "name": "こくどうおおてすじ",
    "name2": "国道大手筋"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu343.htm",
    "lat": "34.9735820000",
    "long": "135.6690924000",
    "name": "こくどうくつかけぐち",
    "name2": "国道沓掛口"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu313.htm",
    "lat": "34.9379320000",
    "long": "135.7451170000",
    "name": "こくどうしもとば",
    "name2": "国道下鳥羽"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu706.htm",
    "lat": "34.9760089055",
    "long": "135.6883385307",
    "name": "こくどうさんのみや",
    "name2": "国道三ノ宮"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu664.htm",
    "lat": "34.9710323400",
    "long": "135.6734742000",
    "name": "こくどうつかはら",
    "name2": "国道塚原"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu663.htm",
    "lat": "34.9703405000",
    "long": "135.6779488000",
    "name": "こくどうなかやま",
    "name2": "国道中山"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu228.htm",
    "lat": "34.9487170000",
    "long": "135.7167510000",
    "name": "こくどうひがしつちかわ",
    "name2": "国道東土川"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu347.htm",
    "lat": "34.9812636426",
    "long": "135.8140358026",
    "name": "こくどうひがしの",
    "name2": "国道東野"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu600.htm",
    "lat": "34.9331690000",
    "long": "135.7680290000",
    "name": "ごこうのみやまえ",
    "name2": "御香宮前"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu173.htm",
    "lat": "35.0546840000",
    "long": "135.6756870000",
    "name": "ごしょのぐち",
    "name2": "御所ノ口"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu497.htm",
    "lat": "34.9954960000",
    "long": "135.7693570000",
    "name": "ごじょうけいはんまえ",
    "name2": "五条京阪前"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu124.htm",
    "lat": "34.9950545700",
    "long": "135.7764055000",
    "name": "ごじょうざか",
    "name2": "五条坂"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu538.htm",
    "lat": "34.9960982300",
    "long": "135.7631306000",
    "name": "ごじょうたかくら",
    "name2": "五条高倉"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu305.htm",
    "lat": "34.9962870000",
    "long": "135.7551740000",
    "name": "ごじょうにしのとういん",
    "name2": "五条西洞院"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu460.htm",
    "lat": "34.9962603216",
    "long": "135.7466120000",
    "name": "ごじょうみぶがわ",
    "name2": "五条壬生川"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu498.htm",
    "lat": "34.9948694901",
    "long": "135.7728329693",
    "name": "ごじょうやまとおおじひがしやまかいせいかんまえ",
    "name2": "五条大和大路・東山開睛館前"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu295.htm",
    "lat": "34.9701900000",
    "long": "135.7410890000",
    "name": "ごちょうばし",
    "name2": "五丁橋"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu427.htm",
    "lat": "35.0239007700",
    "long": "135.6779914000",
    "name": "こぶちちょう",
    "name2": "小渕町"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu454.htm",
    "lat": "35.0210140000",
    "long": "135.7785188221",
    "name": "このえどおり",
    "name2": "近衛通"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu705.htm",
    "lat": "34.9795722208",
    "long": "135.6903645423",
    "name": "ごりょうちょう",
    "name2": "御陵町"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu822.htm",
    "lat": "35.0318830000",
    "long": "135.7285250000",
    "name": "こまつばらじどうこうえんまえ",
    "name2": "小松原児童公園前"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu064.htm",
    "lat": "35.0035170000",
    "long": "135.7281050000",
    "name": "さいいんたつみちょう",
    "name2": "西院巽町"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu474.htm",
    "lat": "35.0675153900",
    "long": "135.7516602000",
    "name": "ごるふじょうまえ",
    "name2": "ゴルフ場前"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu202.htm",
    "lat": "35.0174070000",
    "long": "135.7641240000",
    "name": "さいばんしょまえ",
    "name2": "裁判所前"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu136.htm",
    "lat": "34.9816920000",
    "long": "135.7373210000",
    "name": "さいじまえ",
    "name2": "西寺前"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu791.htm",
    "lat": "34.9615612700",
    "long": "135.6685620000",
    "name": "さかいだにせんたーまえ",
    "name2": "境谷センター前"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu799.htm",
    "lat": "34.9651610000",
    "long": "135.6756470000",
    "name": "さかいだにおおはし",
    "name2": "境谷大橋"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu254.htm",
    "lat": "35.0107966600",
    "long": "135.7631889000",
    "name": "さかいまちおいけ",
    "name2": "堺町御池"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu727.htm",
    "lat": "35.0205801500",
    "long": "135.6808841000",
    "name": "さがあらしやまえきまえ",
    "name2": "嵯峨嵐山駅前"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu426.htm",
    "lat": "35.0226588700",
    "long": "135.6763666000",
    "name": "さがしゃかどうまえ",
    "name2": "嵯峨釈迦堂前"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu425.htm",
    "lat": "35.0198271800",
    "long": "135.6763707000",
    "name": "さがしょうがっこうまえ",
    "name2": "嵯峨小学校前"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu724.htm",
    "lat": "35.0202792200",
    "long": "135.6789744000",
    "name": "さがせとがわちょう",
    "name2": "嵯峨瀬戸川町"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu723.htm",
    "lat": "35.0209382000",
    "long": "135.6856450000",
    "name": "さがちゅうがくまえ",
    "name2": "嵯峨中学前"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu615.htm",
    "lat": "35.0142719136",
    "long": "135.6968211756",
    "name": "さがのあきかいどうちょう",
    "name2": "嵯峨野秋街道町"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu335.htm",
    "lat": "35.04823",
    "long": "135.779595",
    "name": "さきょううくそうごうちょうしゃ・きょうとこうげいせんいだいがくまえ",
    "name2": "左京区総合庁舎・京都工芸繊維大学前"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu242.htm",
    "lat": "35.0486030800",
    "long": "135.7763590000",
    "name": "さきょうくそうごうちょうしゃまえ",
    "name2": "左京区総合庁舎前"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu245.htm",
    "lat": "35.0350830000",
    "long": "135.7296000000",
    "name": "さくらぎちょう",
    "name2": "桜木町"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu557.htm",
    "lat": "35.0095829800",
    "long": "135.7166228000",
    "name": "さるたひこばし",
    "name2": "猿田彦橋"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu255.htm",
    "lat": "35.0083376700",
    "long": "135.7290459000",
    "name": "さんじょうかすが",
    "name2": "三条春日"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu114.htm",
    "lat": "35.0092060000",
    "long": "135.7730802000",
    "name": "さんじょうけいはんまえ",
    "name2": "三条京阪前"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu353.htm",
    "lat": "34.9349420000",
    "long": "135.7422140000",
    "name": "さんちょう",
    "name2": "三町"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu382.htm",
    "lat": "34.9738343100",
    "long": "135.6888078000",
    "name": "さんのみや",
    "name2": "三ノ宮"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu794.htm",
    "lat": "34.9725144600",
    "long": "135.6891668000",
    "name": "さんのみやかいどう",
    "name2": "三ノ宮街道"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu165.htm",
    "lat": "35.0317080000",
    "long": "135.7036250000",
    "name": "さんぽうじ",
    "name2": "三宝寺"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu572.htm",
    "lat": "34.9642887000",
    "long": "135.7094590000",
    "name": "じぇいあーるかつらがわえきまえ",
    "name2": "ＪＲ桂川駅前"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu561.htm",
    "lat": "34.9231429500",
    "long": "135.7013371000",
    "name": "じぇいあーるながおかきょうひがしぐち",
    "name2": "ＪＲ長岡京東口"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu579.htm",
    "lat": "34.9480670000",
    "long": "135.7758310000",
    "name": "じぇいあーるふじのもりえきまえ",
    "name2": "ＪＲ藤森駅前"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu635.htm",
    "lat": "34.9670460000",
    "long": "135.7032840000",
    "name": "じえいたいまえ",
    "name2": "自衛隊前"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu533.htm",
    "lat": "34.9872560000",
    "long": "135.7626860000",
    "name": "しおこうじたかくら",
    "name2": "塩小路高倉"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu257.htm",
    "lat": "34.9865760000",
    "long": "135.7680720000",
    "name": "しおこうじばし",
    "name2": "塩小路橋"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu542.htm",
    "lat": "35.0712286700",
    "long": "135.7435445000",
    "name": "しくろばし",
    "name2": "志久呂橋"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu541.htm",
    "lat": "35.0697271200",
    "long": "135.7426272000",
    "name": "しくろばしにしづめ",
    "name2": "志久呂橋西詰"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu069.htm",
    "lat": "35.0037020000",
    "long": "135.7490220000",
    "name": "しじょうおおみや",
    "name2": "四条大宮"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu066.htm",
    "lat": "35.0035790000",
    "long": "135.7368280000",
    "name": "しじょうおんまえどおり",
    "name2": "四条御前通"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu832.htm",
    "lat": "35.0035920000",
    "long": "135.7196670000",
    "name": "しじょうかどのおおじ",
    "name2": "四条葛野大路"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu055.htm",
    "lat": "35.0036753304",
    "long": "135.7596547116",
    "name": "しじょうからすま",
    "name2": "四条烏丸《地下鉄四条駅》"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu626.htm",
    "lat": "35.0324880000",
    "long": "135.7197160000",
    "name": "りょうあんじまえ",
    "name2": "竜安寺前"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu073.htm",
    "lat": "35.0038105100",
    "long": "135.7692857000",
    "name": "しじょうかわらまち",
    "name2": "四条河原町"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu128.htm",
    "lat": "35.0038159500",
    "long": "135.7724794000",
    "name": "しじょうけいはんまえ",
    "name2": "四条京阪前"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu072.htm",
    "lat": "35.0036976600",
    "long": "135.7619137000",
    "name": "しじょうたかくら",
    "name2": "四条高倉"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu063.htm",
    "lat": "35.0034670000",
    "long": "135.7243740000",
    "name": "しじょうちゅうがくまえ",
    "name2": "四条中学前"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu067.htm",
    "lat": "35.0036031000",
    "long": "135.7397850000",
    "name": "しじょうなかしんみち",
    "name2": "四条中新道"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu071.htm",
    "lat": "35.0036842711",
    "long": "135.7557420000",
    "name": "しじょうにしのとういん",
    "name2": "四条西洞院"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu070.htm",
    "lat": "35.0037520000",
    "long": "135.7519620000",
    "name": "しじょうほりかわ",
    "name2": "四条堀川"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu682.htm",
    "lat": "34.9699378200",
    "long": "135.6940295000",
    "name": "しせきこうえんまえ",
    "name2": "史跡公園前"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu289.htm",
    "lat": "34.9580080000",
    "long": "135.7424860000",
    "name": "じぞうまえ",
    "name2": "地蔵前"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu595.htm",
    "lat": "34.9474740000",
    "long": "135.7663670000",
    "name": "したまち",
    "name2": "下町"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu331.htm",
    "lat": "35.0215795900",
    "long": "135.7393885000",
    "name": "しちほんまつでみず",
    "name2": "七本松出水"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu330.htm",
    "lat": "35.0240353100",
    "long": "135.7393992000",
    "name": "しちほんまつにんなじかいどう",
    "name2": "七本松仁和寺街道"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu562.htm",
    "lat": "34.9212272700",
    "long": "135.7078366000",
    "name": "しばもと",
    "name2": "芝本"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu301.htm",
    "lat": "34.9933180000",
    "long": "135.7491570000",
    "name": "しまばらぐち",
    "name2": "島原口"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu308.htm",
    "lat": "34.9735750000",
    "long": "135.7460440000",
    "name": "しみんぼうさいせんたーまえ",
    "name2": "市民防災センター前"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu376.htm",
    "lat": "34.9813053245",
    "long": "135.7091601865",
    "name": "しもかつら",
    "name2": "下桂"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu012.htm",
    "lat": "35.0390030000",
    "long": "135.7709060000",
    "name": "しもがもじんじゃまえ",
    "name2": "下鴨神社前"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu448.htm",
    "lat": "35.0440834253",
    "long": "135.7741022460",
    "name": "しもがもひがしほんまち",
    "name2": "下鴨東本町"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu040.htm",
    "lat": "35.0527428000",
    "long": "135.7514284000",
    "name": "しもぎしちょう",
    "name2": "下岸町"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu082.htm",
    "lat": "34.9871820000",
    "long": "135.7555780000",
    "name": "しもぎょうくそうごうちょうしゃまえ",
    "name2": "下京区総合庁舎前"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu230.htm",
    "lat": "34.9566370000",
    "long": "135.7167630000",
    "name": "しもくぜ",
    "name2": "下久世"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu366.htm",
    "lat": "34.9369310000",
    "long": "135.7295260000",
    "name": "しもこが",
    "name2": "下久我"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu216.htm",
    "lat": "35.0142529000",
    "long": "135.6837283000",
    "name": "しもさが",
    "name2": "下嵯峨"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu548.htm",
    "lat": "35.0526510000",
    "long": "135.7489600000",
    "name": "しもたけどのちょう",
    "name2": "下竹殿町"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu848.htm",
    "lat": "34.9738710000",
    "long": "135.7144900000",
    "name": "しもつばやしだいはんにゃちょう",
    "name2": "下津林大般若町"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu553.htm",
    "lat": "34.9687320000",
    "long": "135.7142550000",
    "name": "しもつばやしなかじま",
    "name2": "下津林中島"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu402.htm",
    "lat": "34.9731180000",
    "long": "135.7090660000",
    "name": "しもつばやしろくたんだ",
    "name2": "下津林六反田"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu352.htm",
    "lat": "34.9377710000",
    "long": "135.7424360000",
    "name": "しもとば",
    "name2": "下鳥羽"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu312.htm",
    "lat": "34.9406130000",
    "long": "135.7460070000",
    "name": "しもとばしろのこしちょう",
    "name2": "下鳥羽城ノ越町"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu043.htm",
    "lat": "35.0440569000",
    "long": "135.7516493000",
    "name": "しもとりだちょう",
    "name2": "下鳥田町"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu045.htm",
    "lat": "35.0407600000",
    "long": "135.7593820000",
    "name": "しもふさちょう",
    "name2": "下総町"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu748.htm",
    "lat": "34.9266440000",
    "long": "135.7501700000",
    "name": "しもみす",
    "name2": "下三栖"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu022.htm",
    "lat": "35.0497480000",
    "long": "135.7489600000",
    "name": "しもみどりちょう",
    "name2": "下緑町"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu031.htm",
    "lat": "35.0541710000",
    "long": "135.7342950000",
    "name": "しゃかだにぐち",
    "name2": "釈迦谷口"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu243.htm",
    "lat": "35.0503274763",
    "long": "135.7910397798",
    "name": "しゅうがくいんえきまえ",
    "name2": "修学院駅前"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu097.htm",
    "lat": "35.0498870000",
    "long": "135.7920820000",
    "name": "しゅうがくいんみち",
    "name2": "修学院道"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu096.htm",
    "lat": "35.0526420000",
    "long": "135.7926880000",
    "name": "しゅうがくいんりきゅうみち",
    "name2": "修学院離宮道"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu526.htm",
    "lat": "34.9732815100",
    "long": "135.7539454000",
    "name": "じゅうじょうあぶらのこうじ",
    "name2": "十条油小路"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu260.htm",
    "lat": "34.9737157000",
    "long": "135.7679700000",
    "name": "じゅうじょうあいふかちょう",
    "name2": "十条相深町"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu525.htm",
    "lat": "34.9733530000",
    "long": "135.7496880000",
    "name": "じゅうじょうおおみや",
    "name2": "十条大宮"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu527.htm",
    "lat": "34.9733070000",
    "long": "135.7574720000",
    "name": "じゅうじょうしんまち",
    "name2": "十条新町"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu528.htm",
    "lat": "34.9732580000",
    "long": "135.7617960000",
    "name": "じゅうじょうたけだかいどう",
    "name2": "十条竹田街道"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu591.htm",
    "lat": "35.0511683800",
    "long": "135.7645515000",
    "name": "しょくぶつえんきたもんまえ",
    "name2": "植物園北門前"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu016.htm",
    "lat": "35.0437812954",
    "long": "135.7643963000",
    "name": "しょくぶつえんまえ",
    "name2": "植物園前"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu023.htm",
    "lat": "35.0494020000",
    "long": "135.7459330000",
    "name": "じょうとくじまえ",
    "name2": "常徳寺前"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu104.htm",
    "lat": "35.0250540000",
    "long": "135.7919340000",
    "name": "じょうどじ",
    "name2": "浄土寺"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu385.htm",
    "lat": "34.9515140000",
    "long": "135.7520610000",
    "name": "じょうなんぐうひがしぐち",
    "name2": "城南宮東口"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu286.htm",
    "lat": "34.9499650000",
    "long": "135.7431400000",
    "name": "じょうなんぐうみち",
    "name2": "城南宮道"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu310.htm",
    "lat": "34.9499932400",
    "long": "135.7454047000",
    "name": "じょうなんぐう",
    "name2": "城南宮"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu144.htm",
    "lat": "34.9961567500",
    "long": "135.7358678000",
    "name": "しりつびょういんまえ",
    "name2": "市立病院前"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu291.htm",
    "lat": "34.9624430000",
    "long": "135.7424980000",
    "name": "しろがまえちょう",
    "name2": "城ケ前町"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu461.htm",
    "lat": "35.0136501645",
    "long": "135.7757834527",
    "name": "しんあいのまちにじょう",
    "name2": "新間ノ町二条"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu010.htm",
    "lat": "35.0329980000",
    "long": "135.7706590000",
    "name": "しんあおいばし",
    "name2": "新葵橋"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu252.htm",
    "lat": "35.0109790000",
    "long": "135.7479220000",
    "name": "しんせんえんまえ",
    "name2": "神泉苑前"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu106.htm",
    "lat": "35.0194656068",
    "long": "135.7916160933",
    "name": "しんにょどうまえ",
    "name2": "真如堂前"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu779.htm",
    "lat": "34.9710110000",
    "long": "135.6673320000",
    "name": "しんばやしいけこうえん",
    "name2": "新林池公園"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu777.htm",
    "lat": "34.9662610000",
    "long": "135.6701860000",
    "name": "しんばやしこうだんじゅうたくまえ",
    "name2": "新林公団住宅前"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu778.htm",
    "lat": "34.9685530000",
    "long": "135.6664800000",
    "name": "しんばやしせんたーまえ",
    "name2": "新林センター前"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu780.htm",
    "lat": "34.9703570000",
    "long": "135.6719040000",
    "name": "しんばやしなかどおり",
    "name2": "新林中通"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu253.htm",
    "lat": "35.0108195400",
    "long": "135.7566234000",
    "name": "しんまちおいけ",
    "name2": "新町御池"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu112.htm",
    "lat": "35.0092559121",
    "long": "135.7827927288",
    "name": "じんぐうみち",
    "name2": "神宮道"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu035.htm",
    "lat": "35.0613410000",
    "long": "135.7439500000",
    "name": "じんこういんまえ",
    "name2": "神光院前"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu274.htm",
    "lat": "34.9542669700",
    "long": "135.7710493000",
    "name": "すじかいばしいっちょうめ",
    "name2": "直違橋一丁目"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu439.htm",
    "lat": "34.9930675055",
    "long": "135.6924313314",
    "name": "すずむしでら・こけでらみち",
    "name2": "鈴虫寺・苔寺道"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu605.htm",
    "lat": "34.9482520000",
    "long": "135.7697400000",
    "name": "すみぞめ",
    "name2": "墨染"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu752.htm",
    "lat": "35.0139589000",
    "long": "135.6816085000",
    "name": "すみのくらちょう",
    "name2": "角倉町"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu714.htm",
    "lat": "34.9431370000",
    "long": "135.7573730000",
    "name": "すみよし",
    "name2": "住吉"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu265.htm",
    "lat": "34.9595690000",
    "long": "135.7716241521",
    "name": "せいぼじょがくいんまえ",
    "name2": "聖母女学院前"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu372.htm",
    "lat": "34.9887422400",
    "long": "135.7189266000",
    "name": "せんしょうじ",
    "name2": "川勝寺"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu398.htm",
    "lat": "34.9572220000",
    "long": "135.7671090000",
    "name": "せいしょうねんかがくせんたーまえ",
    "name2": "青少年科学センター前"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu120.htm",
    "lat": "34.9829320000",
    "long": "135.7738623558",
    "name": "せんにゅうじみち",
    "name2": "泉涌寺道"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu155.htm",
    "lat": "35.0296470000",
    "long": "135.7424610000",
    "name": "せんぼんいまでがわ",
    "name2": "千本今出川"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu396.htm",
    "lat": "35.0325280374",
    "long": "135.7417779067",
    "name": "せんぼんかみだちうり",
    "name2": "千本上立売"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu222.htm",
    "lat": "35.0408280000",
    "long": "135.7385450000",
    "name": "せんぼんきたおおじ",
    "name2": "千本北大路"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu151.htm",
    "lat": "35.0160570000",
    "long": "135.7425970000",
    "name": "せんぼんきゅうにじょう",
    "name2": "千本旧二条"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu394.htm",
    "lat": "35.0365472693",
    "long": "135.7401771019",
    "name": "せんぼんくらまぐち",
    "name2": "千本鞍馬口"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu149.htm",
    "lat": "35.0084830000",
    "long": "135.7427700000",
    "name": "せんぼんさんじょう・すざくりつめいかんまえ",
    "name2": "千本三条・朱雀立命館前"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu296.htm",
    "lat": "34.9732660000",
    "long": "135.7412250000",
    "name": "せんぼんじゅうじょう",
    "name2": "千本十条"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu153.htm",
    "lat": "35.0216780000",
    "long": "135.7425350000",
    "name": "せんぼんでみず",
    "name2": "千本出水"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu154.htm",
    "lat": "35.0257296418",
    "long": "135.7424680847",
    "name": "せんぼんなかだちうり",
    "name2": "千本中立売"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu152.htm",
    "lat": "35.0182925061",
    "long": "135.7426153644",
    "name": "せんぼんまるたまち",
    "name2": "千本丸太町"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu267.htm",
    "lat": "34.9577530000",
    "long": "135.7760900000",
    "name": "そうぼうちょう",
    "name2": "僧坊町"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu404.htm",
    "lat": "35.0155630000",
    "long": "135.7318860000",
    "name": "たいしみち",
    "name2": "太子道"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu199.htm",
    "lat": "35.0238900000",
    "long": "135.7315890000",
    "name": "たいしょうぐん",
    "name2": "大将軍"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu428.htm",
    "lat": "35.0271718100",
    "long": "135.6780118000",
    "name": "だいかくじ",
    "name2": "大覚寺"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu225.htm",
    "lat": "35.0407170000",
    "long": "135.7478600000",
    "name": "だいとくじまえ",
    "name2": "大徳寺前"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu371.htm",
    "lat": "34.9888843300",
    "long": "135.7248321000",
    "name": "だいもんちょう",
    "name2": "大門町"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu174.htm",
    "lat": "35.0564490000",
    "long": "135.6740450000",
    "name": "たかお",
    "name2": "高雄"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu171.htm",
    "lat": "35.0463850000",
    "long": "135.6825360000",
    "name": "たかおしょうがっこうまえ",
    "name2": "高雄小学校前"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu167.htm",
    "lat": "35.0370890000",
    "long": "135.6929490000",
    "name": "たかおびょういんまえ",
    "name2": "高雄病院前"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu028.htm",
    "lat": "35.0484195875",
    "long": "135.7360691865",
    "name": "たかがみねかみのちょう",
    "name2": "鷹峯上ノ町"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu030.htm",
    "lat": "35.0543003926",
    "long": "135.7323867080",
    "name": "たかがみねげんこうあんまえ",
    "name2": "鷹峯源光庵前"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu447.htm",
    "lat": "35.0438823600",
    "long": "135.7770062000",
    "name": "たかぎちょう",
    "name2": "高木町"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu633.htm",
    "lat": "34.9645606100",
    "long": "135.7064207000",
    "name": "たかだちょう",
    "name2": "高田町"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu445.htm",
    "lat": "35.0406854668",
    "long": "135.7826650460",
    "name": "たかの",
    "name2": "高野"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu446.htm",
    "lat": "35.0423082280",
    "long": "135.7798272779",
    "name": "たかのばしひがしづめ",
    "name2": "高野橋東詰"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu567.htm",
    "lat": "35.07831",
    "long": "135.74067",
    "name": "たかばしみなみ",
    "name2": "高橋南"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu166.htm",
    "lat": "35.0350980000",
    "long": "135.6973350000",
    "name": "たかはなちょう",
    "name2": "高鼻町"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu680.htm",
    "lat": "35.0368650000",
    "long": "135.7859420000",
    "name": "たかはらちょう",
    "name2": "高原町"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu095.htm",
    "lat": "35.0583373000",
    "long": "135.7918364000",
    "name": "たからがいけ",
    "name2": "宝ヶ池"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu616.htm",
    "lat": "34.9573699400",
    "long": "135.7606841900",
    "name": "たけだいでばし",
    "name2": "竹田出橋"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu390.htm",
    "lat": "34.9544780100",
    "long": "135.7521236000",
    "name": "たけだうちはたちょう",
    "name2": "竹田内畑町"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu617.htm",
    "lat": "34.9623610000",
    "long": "135.7618210000",
    "name": "たけだくぼちょう",
    "name2": "竹田久保町"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu147.htm",
    "lat": "34.9569599200",
    "long": "135.7564929000",
    "name": "たけだえきひがしぐち",
    "name2": "竹田駅東口"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu146.htm",
    "lat": "34.9567840600",
    "long": "135.7557017000",
    "name": "たけだえきにしぐち",
    "name2": "竹田駅西口"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu207.htm",
    "lat": "34.9513934593",
    "long": "135.7554580000",
    "name": "たけだじょうぼだいいんちょう",
    "name2": "竹田浄菩堤院町"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu802.htm",
    "lat": "34.9577980000",
    "long": "135.6779940000",
    "name": "たけのさとしょうがっこうまえ",
    "name2": "竹の里小学校前"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu711.htm",
    "lat": "34.9516430313",
    "long": "135.7591525509",
    "name": "たけだじょうなんぐうみち",
    "name2": "竹田城南宮道"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu011.htm",
    "lat": "35.0369390000",
    "long": "135.7710420000",
    "name": "ただすのもり",
    "name2": "糺ノ森"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu077.htm",
    "lat": "35.0333320000",
    "long": "135.7840270000",
    "name": "たなかひのくちちょう",
    "name2": "田中樋ノ口町"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu451.htm",
    "lat": "35.0370688248",
    "long": "135.7815956123",
    "name": "たなかおおくぼちょう",
    "name2": "田中大久保町"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu602.htm",
    "lat": "34.9401930000",
    "long": "135.7681160000",
    "name": "たんばばし",
    "name2": "丹波橋"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu420.htm",
    "lat": "35.0068540944",
    "long": "135.6826553129",
    "name": "たにがつじちょう",
    "name2": "谷ケ辻町"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu400.htm",
    "lat": "35.0249890000",
    "long": "135.7455870000",
    "name": "ちえこういんなかだちうり",
    "name2": "智恵光院中立売"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu203.htm",
    "lat": "35.0064610000",
    "long": "135.7777750000",
    "name": "ちおいんまえ",
    "name2": "知恩院前"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu787.htm",
    "lat": "34.9732830000",
    "long": "135.7597210000",
    "name": "ちかてつじゅうじょうえきまえ",
    "name2": "地下鉄十条駅前"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu806.htm",
    "lat": "34.9565990100",
    "long": "135.6802623000",
    "name": "ちゅうおうこうえんみなみぐち",
    "name2": "中央公園南口"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu318.htm",
    "lat": "34.9280230951",
    "long": "135.7588290865",
    "name": "ちゅうしょじま",
    "name2": "中書島"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu414.htm",
    "lat": "35.0035040000",
    "long": "135.7014930000",
    "name": "ちょうふくじみち",
    "name2": "長福寺道"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu436.htm",
    "lat": "34.9823840000",
    "long": "135.6932030000",
    "name": "ちよはらぐち",
    "name2": "千代原口"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu259.htm",
    "lat": "34.9768265002",
    "long": "135.7681717877",
    "name": "つきのわ",
    "name2": "月輪"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu621.htm",
    "lat": "34.9595340000",
    "long": "135.7236200000",
    "name": "つきやま",
    "name2": "築山"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu684.htm",
    "lat": "34.9795050000",
    "long": "135.6936230000",
    "name": "つきみがおか",
    "name2": "月見ケ丘"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu009.htm",
    "lat": "35.0289278800",
    "long": "135.7724333000",
    "name": "でまちやなぎえきまえ",
    "name2": "出町柳駅前"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu370.htm",
    "lat": "34.9889303900",
    "long": "135.7282478000",
    "name": "つきよみばし",
    "name2": "月読橋"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu176.htm",
    "lat": "35.0362690000",
    "long": "135.7514310000",
    "name": "てんじんこうえんまえ",
    "name2": "天神公園前"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu844.htm",
    "lat": "34.9824219000",
    "long": "135.6604577000",
    "name": "てんがいこうえんまえ",
    "name2": "天蓋公園前"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu276.htm",
    "lat": "35.02927597",
    "long": "135.7277772",
    "name": "とうじいんひがしまち",
    "name2": "等持院東町"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu159.htm",
    "lat": "35.0247420000",
    "long": "135.7269070000",
    "name": "とうじいんみち",
    "name2": "等持院道"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu160.htm",
    "lat": "35.0259650000",
    "long": "135.7247450000",
    "name": "とうじいんみなみまち",
    "name2": "等持院南町"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu133.htm",
    "lat": "34.9823100000",
    "long": "135.7462040000",
    "name": "とうじにしもんまえ",
    "name2": "東寺西門前"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu299.htm",
    "lat": "34.9814260000",
    "long": "135.7493050000",
    "name": "とうじひがしもんまえ",
    "name2": "東寺東門前"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu116.htm",
    "lat": "34.9819155800",
    "long": "135.7537300000",
    "name": "とうじみち",
    "name2": "東寺道"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu132.htm",
    "lat": "34.9791840000",
    "long": "135.7465500000",
    "name": "とうじみなみもんまえ",
    "name2": "東寺南門前"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu521.htm",
    "lat": "34.9683240000",
    "long": "135.7352950000",
    "name": "とうなんこうこうまえ",
    "name2": "塔南高校前"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu625.htm",
    "lat": "35.0304130000",
    "long": "135.7166150000",
    "name": "とうのしたちょう",
    "name2": "塔ノ下町"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu119.htm",
    "lat": "34.9811198613",
    "long": "135.7720368981",
    "name": "とうふくじ",
    "name2": "東福寺"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu258.htm",
    "lat": "34.9801869073",
    "long": "135.7692173558",
    "name": "とうふくじみち",
    "name2": "東福寺道"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu349.htm",
    "lat": "34.9301530000",
    "long": "135.7680100000",
    "name": "とうりょうだんちまえ",
    "name2": "桃陵団地前"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu629.htm",
    "lat": "35.0291310000",
    "long": "135.7631480000",
    "name": "どうししゃまえ",
    "name2": "同志社前"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu334.htm",
    "lat": "35.060141",
    "long": "135.679164",
    "name": "とがのお",
    "name2": "栂ノ尾"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu718.htm",
    "lat": "35.0209074500",
    "long": "135.7047343000",
    "name": "ときわ・さがのこうこうまえ",
    "name2": "常盤・嵯峨野高校前"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu612.htm",
    "lat": "35.0236300000",
    "long": "135.7110930000",
    "name": "ときわおいけちょう",
    "name2": "常盤御池町"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu719.htm",
    "lat": "35.0209733400",
    "long": "135.7016739000",
    "name": "ときわのしょうがっこうまえ",
    "name2": "常磐野小学校前"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu029.htm",
    "lat": "35.0509206879",
    "long": "135.7343898393",
    "name": "どてんじょうちょう",
    "name2": "土天井町"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu783.htm",
    "lat": "34.9569950000",
    "long": "135.7455990000",
    "name": "とばおおはしきたづめ",
    "name2": "鳥羽大橋北詰"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu321.htm",
    "lat": "34.9168521000",
    "long": "135.7283151000",
    "name": "とみのもり",
    "name2": "富ノ森"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu387.htm",
    "lat": "34.9839530000",
    "long": "135.7073860000",
    "name": "なかかつら",
    "name2": "中桂"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu231.htm",
    "lat": "34.9592190000",
    "long": "135.7169490000",
    "name": "なかくぜ",
    "name2": "中久世"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu383.htm",
    "lat": "34.9600022100",
    "long": "135.7127774000",
    "name": "なかくぜいっちょうめ",
    "name2": "中久世一丁目"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu458.htm",
    "lat": "34.9960600000",
    "long": "135.7270550000",
    "name": "なかのはしごじょう",
    "name2": "中ノ橋五条"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu288.htm",
    "lat": "34.9562170000",
    "long": "135.7420280000",
    "name": "なすの",
    "name2": "奈須野"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu300.htm",
    "lat": "34.9891660000",
    "long": "135.7491820000",
    "name": "ななじょうおおみや・きょうとすいぞくかんまえ",
    "name2": "七条大宮・京都水族館前"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu142.htm",
    "lat": "34.9891525000",
    "long": "135.7362161000",
    "name": "ななじょうおんまえどおり",
    "name2": "七条御前通"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu534.htm",
    "lat": "34.9893070000",
    "long": "135.7642420000",
    "name": "ななじょうかわらまち",
    "name2": "七条河原町"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu256.htm",
    "lat": "34.9892882200",
    "long": "135.7684743000",
    "name": "ななじょうけいはんまえ",
    "name2": "七条京阪前"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu369.htm",
    "lat": "34.9891245800",
    "long": "135.7407108000",
    "name": "ななじょうせんぼん",
    "name2": "七条千本"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu193.htm",
    "lat": "34.9892320000",
    "long": "135.7552480000",
    "name": "ななじょうにしのとういん",
    "name2": "七条西洞院"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu192.htm",
    "lat": "34.9892080000",
    "long": "135.7530610000",
    "name": "ななじょうほりかわ",
    "name2": "七条堀川"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu368.htm",
    "lat": "34.9891646700",
    "long": "135.7455994000",
    "name": "ななじょうみぶがわ",
    "name2": "七条壬生川"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu710.htm",
    "lat": "34.9539288863",
    "long": "135.7597568307",
    "name": "ななせがわちょう",
    "name2": "七瀬川町"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu611.htm",
    "lat": "35.0199850000",
    "long": "135.7129210000",
    "name": "ならびがおか",
    "name2": "双ヶ丘"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu197.htm",
    "lat": "35.0280650000",
    "long": "135.7060650000",
    "name": "なるたきほんまち",
    "name2": "鳴滝本町"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu328.htm",
    "lat": "35.0338701013",
    "long": "135.6998572068",
    "name": "なるたきまつもとちょう",
    "name2": "鳴滝松本町"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu108.htm",
    "lat": "35.0140830000",
    "long": "135.7904640000",
    "name": "なんぜんじ・えいかんどうみち",
    "name2": "南禅寺・永観堂道"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu773.htm",
    "lat": "34.9373930000",
    "long": "135.7565700000",
    "name": "にしいたばし",
    "name2": "西板橋"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu823.htm",
    "lat": "34.9796290000",
    "long": "135.7327500000",
    "name": "にしおおじえきまえ",
    "name2": "西大路駅前"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu403.htm",
    "lat": "35.0108180000",
    "long": "135.7319230000",
    "name": "にしおおじおいけ",
    "name2": "西大路御池"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu138.htm",
    "lat": "34.9780840000",
    "long": "135.7328370000",
    "name": "にしおおじくじょう",
    "name2": "西大路九条"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu239.htm",
    "lat": "34.9961470000",
    "long": "135.7321570000",
    "name": "にしおおじごじょう",
    "name2": "西大路五条"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu204.htm",
    "lat": "35.0084340000",
    "long": "135.7319230000",
    "name": "にしおおじさんじょう",
    "name2": "西大路三条"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu065.htm",
    "lat": "35.0035410000",
    "long": "135.7319720000",
    "name": "にしおおじしじょう（はんきゅうさいいんえき,らんでんさいえき）",
    "name2": "西大路四条《阪急･嵐電西院駅》"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu237.htm",
    "lat": "34.9891790000",
    "long": "135.7324040000",
    "name": "にしおおじななじょう",
    "name2": "西大路七条"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu139.htm",
    "lat": "34.9842860000",
    "long": "135.7325030000",
    "name": "にしおおじはちじょう",
    "name2": "西大路八条"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu238.htm",
    "lat": "34.9928480000",
    "long": "135.7322930000",
    "name": "にしおおじはなやちょう",
    "name2": "西大路花屋町"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu240.htm",
    "lat": "34.9991370000",
    "long": "135.7320950000",
    "name": "にしおおじまつばら",
    "name2": "西大路松原"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu316.htm",
    "lat": "34.9329274085",
    "long": "135.7583453558",
    "name": "にしおおてすじ",
    "name2": "西大手筋"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu432.htm",
    "lat": "34.9922430000",
    "long": "135.7055580000",
    "name": "にしおおはしにしづめ",
    "name2": "西大橋西詰"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu845.htm",
    "lat": "34.9855286999",
    "long": "135.6559859239",
    "name": "にしかつらざか",
    "name2": "西桂坂"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu540.htm",
    "lat": "35.0674989000",
    "long": "135.7440542000",
    "name": "にしがもいのくちちょう",
    "name2": "西賀茂井ノ口町"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu568.htm",
    "lat": "35.076889",
    "long": "135.740773",
    "name": "にしがもしょうだちょう",
    "name2": "西賀茂庄田町"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu034.htm",
    "lat": "35.0641204501",
    "long": "135.7456534590",
    "name": "にしがもしゃこまえ",
    "name2": "西賀茂車庫前"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu569.htm",
    "lat": "35.072727",
    "long": "135.740461",
    "name": "にしがもちゅうがくきた",
    "name2": "西賀茂中学北"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu268.htm",
    "lat": "34.9542044294",
    "long": "135.7763884110",
    "name": "にしきゅうほうじちょう",
    "name2": "西久宝寺町"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu476.htm",
    "lat": "35.064444",
    "long": "135.747706",
    "name": "にしがもばしひがしづめ",
    "name2": "西賀茂橋東詰"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu441.htm",
    "lat": "34.9851086100",
    "long": "135.6929594000",
    "name": "にしきょうくやくしょまえ",
    "name2": "西京区役所前"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu431.htm",
    "lat": "34.9952988400",
    "long": "135.7125943000",
    "name": "にしきょうごく",
    "name2": "西京極"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu457.htm",
    "lat": "34.9990010000",
    "long": "135.7117840000",
    "name": "にしきょうごくうまつかちょう",
    "name2": "西京極午塚町"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu430.htm",
    "lat": "34.9959990000",
    "long": "135.7147370000",
    "name": "にしきょうごくうんどうこうえんまえ",
    "name2": "西京極運動公園前"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu785.htm",
    "lat": "34.9921404300",
    "long": "135.7188320000",
    "name": "にしきょうごくえきまえ",
    "name2": "西京極駅前"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu817.htm",
    "lat": "34.9880300000",
    "long": "135.7198400000",
    "name": "にしきょうごくしょうがっこうまえ",
    "name2": "西京極小学校前"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu407.htm",
    "lat": "35.0109420000",
    "long": "135.7249180000",
    "name": "にしこうじおいけ",
    "name2": "西小路御池"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu279.htm",
    "lat": "34.9924700300",
    "long": "135.7251848000",
    "name": "にしこうじはなやちょうう",
    "name2": "西小路花屋町"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu840.htm",
    "lat": "34.9602197749",
    "long": "135.6719492159",
    "name": "にしさかいだにちょうさんちょうめ",
    "name2": "西境谷町三丁目"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu712.htm",
    "lat": "34.9492427082",
    "long": "135.7584755423",
    "name": "にしすみぞめどおり",
    "name2": "西墨染通"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu792.htm",
    "lat": "34.9570007800",
    "long": "135.6699561000",
    "name": "にしたけのさとちょう",
    "name2": "西竹の里町"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu715.htm",
    "lat": "34.9403210000",
    "long": "135.7571750000",
    "name": "にしたんばばし",
    "name2": "西丹波橋"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu269.htm",
    "lat": "34.9523326507",
    "long": "135.7764075976",
    "name": "にしてらまち",
    "name2": "西寺町"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu249.htm",
    "lat": "35.0186197647",
    "long": "135.7318120000",
    "name": "にしのきょうえんまち（じぇいあーるえんまちえき）",
    "name2": "西ノ京円町《ＪＲ円町駅》"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu410.htm",
    "lat": "35.0154760000",
    "long": "135.7278580000",
    "name": "にしのきょうつかもとちょう",
    "name2": "西ノ京塚本町"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu607.htm",
    "lat": "35.0192294608",
    "long": "135.7251770000",
    "name": "にしのきょうばだいちょう",
    "name2": "西ノ京馬代町"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu409.htm",
    "lat": "35.0153770000",
    "long": "135.7233240000",
    "name": "にしのきょうふじのきちょう",
    "name2": "西ノ京藤ノ木町"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu307.htm",
    "lat": "34.9914690000",
    "long": "135.7551860000",
    "name": "にしのとういんしょうめん",
    "name2": "西洞院正面"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu581.htm",
    "lat": "35.0009880000",
    "long": "135.7551670000",
    "name": "にしのとういんぶっこうじ",
    "name2": "西洞院仏光寺"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu582.htm",
    "lat": "34.9984610000",
    "long": "135.7551620000",
    "name": "にしのとういんまつばら",
    "name2": "西洞院松原"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu306.htm",
    "lat": "34.9938160000",
    "long": "135.7551860000",
    "name": "にしのとういんろくじょう",
    "name2": "西洞院六条"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu191.htm",
    "lat": "34.9924980000",
    "long": "135.7529770000",
    "name": "にしほんがんじまえ",
    "name2": "西本願寺前"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu774.htm",
    "lat": "35.0112140000",
    "long": "135.7411520000",
    "name": "にじょうえきにしぐち",
    "name2": "二条駅西口"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu150.htm",
    "lat": "35.0115970000",
    "long": "135.7425970000",
    "name": "にじょうえきまえ",
    "name2": "二条駅前"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu185.htm",
    "lat": "35.0139320000",
    "long": "135.7517640000",
    "name": "にじょうじょうまえ",
    "name2": "二条城前"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu412.htm",
    "lat": "35.0038010000",
    "long": "135.7096470000",
    "name": "にっしんでんきまえ",
    "name2": "日新電機前"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu599.htm",
    "lat": "34.9146520000",
    "long": "135.7260180000",
    "name": "のうそきしのした",
    "name2": "納所岸ノ下"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu322.htm",
    "lat": "34.9109586200",
    "long": "135.7222289000",
    "name": "のうそきたしろほり",
    "name2": "納所北城堀"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu323.htm",
    "lat": "34.9079838800",
    "long": "135.7190723000",
    "name": "のうそちょう",
    "name2": "納所町"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu797.htm",
    "lat": "34.9731006100",
    "long": "135.7013208000",
    "name": "のだちょう",
    "name2": "野田町"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu086.htm",
    "lat": "35.0514852300",
    "long": "135.7705326000",
    "name": "ののがみちょう",
    "name2": "野々神町"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu424.htm",
    "lat": "35.0176939035",
    "long": "135.6765509620",
    "name": "ののみや",
    "name2": "野々宮"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu910.htm",
    "lat": "34.9892480000",
    "long": "135.7709440000",
    "name": "はくぶつかんさんじゅうさんげんどうまえ",
    "name2": "博物館三十三間堂前"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu606.htm",
    "lat": "35.0188558200",
    "long": "135.7280535000",
    "name": "はくらくちょう",
    "name2": "伯楽町"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu145.htm",
    "lat": "34.9842660000",
    "long": "135.7524560000",
    "name": "はちじょうあぶらのこうじ",
    "name2": "八条油小路"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu141.htm",
    "lat": "34.9842620000",
    "long": "135.7499350000",
    "name": "はちじょうおおみや",
    "name2": "八条大宮"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu135.htm",
    "lat": "34.9816920000",
    "long": "135.7398170000",
    "name": "はちじょうちゅうがくまえ",
    "name2": "八条中学前"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu319.htm",
    "lat": "34.9302991000",
    "long": "135.7425749000",
    "name": "はっちょうなわて",
    "name2": "八丁畷"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu560.htm",
    "lat": "34.9309760000",
    "long": "135.7272150000",
    "name": "はづかししみずちょう",
    "name2": "羽束師志水町"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu610.htm",
    "lat": "35.0189117360",
    "long": "135.7176248509",
    "name": "はなぞのえきまえ",
    "name2": "花園駅前"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu765.htm",
    "lat": "35.0184659882",
    "long": "135.7155251435",
    "name": "はなぞのおうぎのちょう",
    "name2": "花園扇野町"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu816.htm",
    "lat": "34.9858765159",
    "long": "135.6674987296",
    "name": "はなのまいこうえんまえ",
    "name2": "花の舞公園前"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu766.htm",
    "lat": "35.0429030000",
    "long": "135.7135140000",
    "name": "はらだに",
    "name2": "原谷"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu094.htm",
    "lat": "35.0600008900",
    "long": "135.7915853000",
    "name": "はなぞのばし",
    "name2": "花園橋"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu563.htm",
    "lat": "34.9270137200",
    "long": "135.7115840000",
    "name": "ばば",
    "name2": "馬場"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu769.htm",
    "lat": "35.0443360000",
    "long": "135.7167140000",
    "name": "はらだにのうきょうまえ",
    "name2": "原谷農協前"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu143.htm",
    "lat": "34.9474165800",
    "long": "135.7517803000",
    "name": "ぱるすぷらざまえ",
    "name2": "パルスプラザ前"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu767.htm",
    "lat": "35.0456710000",
    "long": "135.7185800000",
    "name": "はらだにぐち",
    "name2": "原谷口"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu421.htm",
    "lat": "35.0096386362",
    "long": "135.6807565841",
    "name": "はんきゅうあらしやまえきまえ",
    "name2": "阪急嵐山駅前"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu853.htm",
    "lat": "34.9840176708",
    "long": "135.6754184719",
    "name": "ひがしかつらざか",
    "name2": "東桂坂"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu503.htm",
    "lat": "34.9869883700",
    "long": "135.7152270000",
    "name": "ひがしがわちょう",
    "name2": "東側町"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu241.htm",
    "lat": "35.0480340000",
    "long": "135.7736740000",
    "name": "ひがしきたぞのちょう",
    "name2": "東北園町"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu781.htm",
    "lat": "34.9680590000",
    "long": "135.6736090000",
    "name": "ひがししんばやしちょう",
    "name2": "東新林町"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu042.htm",
    "lat": "35.0471415700",
    "long": "135.7515202000",
    "name": "ひがしたかなわちょう",
    "name2": "東高縄町"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu803.htm",
    "lat": "34.9556220400",
    "long": "135.6760627000",
    "name": "ひがしたけのさとちょう",
    "name2": "東竹の里町"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu227.htm",
    "lat": "34.9476670000",
    "long": "135.7196170000",
    "name": "ひがしつちかわばし",
    "name2": "東土川橋"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu270.htm",
    "lat": "34.9500897939",
    "long": "135.7763225595",
    "name": "ひがしてらまち",
    "name2": "東寺町"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu107.htm",
    "lat": "35.0166514451",
    "long": "135.7907546356",
    "name": "ひがしてんのうちょう",
    "name2": "東天王町"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu589.htm",
    "lat": "35.0500127500",
    "long": "135.7575518000",
    "name": "ひがしもとまち",
    "name2": "東元町"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu113.htm",
    "lat": "35.0094677252",
    "long": "135.7781527374",
    "name": "ひがしやまさんじょう（ちかてつ　ひがしやまえき）",
    "name2": "東山三条《地下鉄東山駅》"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu122.htm",
    "lat": "34.9890708154",
    "long": "135.7744535337",
    "name": "ひがしやまななじょう",
    "name2": "東山七条"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu905.htm",
    "lat": "35.0117762348",
    "long": "135.7784459239",
    "name": "ひがしやまにおうもん",
    "name2": "東山仁王門"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu456.htm",
    "lat": "35.0136630000",
    "long": "135.7783190000",
    "name": "ひがしやまにじょう・おかざきこうえんぐち",
    "name2": "東山二条・岡崎公園口"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu126.htm",
    "lat": "35.0001164100",
    "long": "135.7774436000",
    "name": "ひがしやまやすい",
    "name2": "東山安井"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu716.htm",
    "lat": "34.9361320000",
    "long": "135.7583860000",
    "name": "ひごまち",
    "name2": "肥後町"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu358.htm",
    "lat": "34.9316394400",
    "long": "135.7239598000",
    "name": "ひしかわ",
    "name2": "菱川"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu283.htm",
    "lat": "34.9476670000",
    "long": "135.7294140000",
    "name": "ひしづまじんじゃまえ",
    "name2": "菱妻神社前"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu359.htm",
    "lat": "34.9269209200",
    "long": "135.7226161000",
    "name": "ひづめぐち",
    "name2": "樋爪口"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu361.htm",
    "lat": "34.9167680000",
    "long": "135.7206800000",
    "name": "ひづめちょう",
    "name2": "樋爪町"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu075.htm",
    "lat": "35.0287953855",
    "long": "135.7792230117",
    "name": "ひゃくまんべん",
    "name2": "百万遍"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu168.htm",
    "lat": "35.0379280000",
    "long": "135.6893680000",
    "name": "ひらおかはちまんまえ",
    "name2": "平岡八幡前"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu543.htm",
    "lat": "35.0732087400",
    "long": "135.7439328000",
    "name": "ひらぎの",
    "name2": "柊野"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu566.htm",
    "lat": "35.078388",
    "long": "135.742306",
    "name": "ひらぎのぐらんどまえ",
    "name2": "柊野グラウンド前"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu473.htm",
    "lat": "35.0647965700",
    "long": "135.7504172000",
    "name": "ひらぎのわかれ",
    "name2": "柊野別れ"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu683.htm",
    "lat": "34.9718676200",
    "long": "135.6940754000",
    "name": "ひらたちょう",
    "name2": "平田町"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu722.htm",
    "lat": "35.0210831700",
    "long": "135.6903255000",
    "name": "ひろさわごしょのうちちょう",
    "name2": "広沢御所ノ内町"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu786.htm",
    "lat": "35.0257482600",
    "long": "135.6877145000",
    "name": "ひろさわのいけ・ぶつだいひろさわこうまえ",
    "name2": "広沢池・佛大広沢校前"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu170.htm",
    "lat": "35.0451970000",
    "long": "135.6840390000",
    "name": "ひろしばちょう",
    "name2": "広芝町"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu594.htm",
    "lat": "34.9518720000",
    "long": "135.7677140000",
    "name": "ふかくさきたはすいけちょう",
    "name2": "深草北蓮池町"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu618.htm",
    "lat": "34.9657590000",
    "long": "135.7623030000",
    "name": "ふかくさしもかわらちょう",
    "name2": "深草下川原町"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu264.htm",
    "lat": "34.9583830000",
    "long": "135.7682580000",
    "name": "ふかくさにしうらちょう",
    "name2": "深草西浦町"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu164.htm",
    "lat": "35.0286500000",
    "long": "135.7089010000",
    "name": "ふくおうじ",
    "name2": "福王子"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu804.htm",
    "lat": "34.9629144888",
    "long": "135.6782293951",
    "name": "ふくにしいせきこうえんまえ",
    "name2": "福西遺跡公園前"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu839.htm",
    "lat": "34.9552141600",
    "long": "135.6802543000",
    "name": "ふくにしたけのさと",
    "name2": "福西竹の里"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu596.htm",
    "lat": "34.9461890000",
    "long": "135.7659470000",
    "name": "ふしみいんくらいんまえ",
    "name2": "伏見インクライン前"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu351.htm",
    "lat": "34.9355115000",
    "long": "135.7512363153",
    "name": "ふしみけいさつしょまえ",
    "name2": "伏見警察署前"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu275.htm",
    "lat": "34.9554892500",
    "long": "135.7685602000",
    "name": "ふじのもり",
    "name2": "藤ノ森"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu272.htm",
    "lat": "34.9489865880",
    "long": "135.7709385509",
    "name": "ふじのもりじんじゃ",
    "name2": "藤森神社"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu273.htm",
    "lat": "34.9508807023",
    "long": "135.7705371546",
    "name": "ふじのもりじんじゃまえ",
    "name2": "藤森神社前"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu620.htm",
    "lat": "34.9761240000",
    "long": "135.7618950000",
    "name": "ふだのつじ",
    "name2": "札ノ辻"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu201.htm",
    "lat": "35.0173820000",
    "long": "135.7558340000",
    "name": "ふちょうまえ",
    "name2": "府庁前"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu026.htm",
    "lat": "35.0440520000",
    "long": "135.7382509914",
    "name": "ぶっきょうだいがくまえ",
    "name2": "佛教大学前"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu320.htm",
    "lat": "34.9267390000",
    "long": "135.7387790000",
    "name": "ふどうよこおおじ",
    "name2": "府道横大路"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu223.htm",
    "lat": "35.0411980000",
    "long": "135.7419050000",
    "name": "ふなおかやま",
    "name2": "船岡山"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu537.htm",
    "lat": "34.9759720000",
    "long": "135.7344180000",
    "name": "ふなとちょう",
    "name2": "船戸町"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu006.htm",
    "lat": "35.0239188933",
    "long": "135.7692173399",
    "name": "ふりついだいびょういんまえ",
    "name2": "府立医大病院前"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu198.htm",
    "lat": "35.0237290000",
    "long": "135.7283280000",
    "name": "ふりつたいいくかんまえ",
    "name2": "府立体育館前《島津アリーナ京都前》"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu015.htm",
    "lat": "35.0438741900",
    "long": "135.7674060000",
    "name": "ふりつだいがくまえ",
    "name2": "府立大学前"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu850.htm",
    "lat": "34.9872809230",
    "long": "135.6560016080",
    "name": "ふれあいのさと",
    "name2": "ふれあいの里"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu435.htm",
    "lat": "34.9848420000",
    "long": "135.6956370000",
    "name": "へいわだいちょう",
    "name2": "平和台町"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu466.htm",
    "lat": "35.0219553586",
    "long": "135.7934983558",
    "name": "ほうねんいんちょう",
    "name2": "法然院町"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu713.htm",
    "lat": "34.9465600000",
    "long": "135.7583000000",
    "name": "ぼうばな",
    "name2": "棒鼻"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu266.htm",
    "lat": "34.9593208106",
    "long": "135.7744309067",
    "name": "ぼうちょう",
    "name2": "坊町"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu179.htm",
    "lat": "35.0297260000",
    "long": "135.7518720000",
    "name": "ほりかわいまでがわ",
    "name2": "堀川今出川"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu178.htm",
    "lat": "35.0322290000",
    "long": "135.7519000000",
    "name": "ほりかわかみだちうり",
    "name2": "堀川上立売"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu186.htm",
    "lat": "35.0109210000",
    "long": "135.7518560000",
    "name": "ほりかわおいけ",
    "name2": "堀川御池"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu175.htm",
    "lat": "35.0385790000",
    "long": "135.7517770000",
    "name": "ほりかわくらまぐち",
    "name2": "堀川鞍馬口"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu187.htm",
    "lat": "35.0085240000",
    "long": "135.7518180000",
    "name": "ほりかわさんじょう",
    "name2": "堀川三条"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu190.htm",
    "lat": "34.9962550000",
    "long": "135.7522994405",
    "name": "ほりかわごじょう",
    "name2": "堀川五条"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu183.htm",
    "lat": "35.0202200000",
    "long": "135.7517770000",
    "name": "ほりかわしもだちうり",
    "name2": "堀川下立売"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu182.htm",
    "lat": "35.0221970000",
    "long": "135.7518010000",
    "name": "ほりかわしもちょうじゃまち",
    "name2": "堀川下長者町"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu188.htm",
    "lat": "35.0060650000",
    "long": "135.7518310000",
    "name": "ほりかわたこやくし",
    "name2": "堀川蛸薬師"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu177.htm",
    "lat": "35.0339560000",
    "long": "135.7516820000",
    "name": "ほりかわてらのうち",
    "name2": "堀川寺ノ内"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu181.htm",
    "lat": "35.0246430000",
    "long": "135.7517640000",
    "name": "ほりかわなかだちうり",
    "name2": "堀川中立売"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu189.htm",
    "lat": "34.9995220000",
    "long": "135.7519770000",
    "name": "ほりかわまつばら",
    "name2": "堀川松原"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu184.htm",
    "lat": "35.0173420000",
    "long": "135.7517640000",
    "name": "ほりかわまるたまち",
    "name2": "堀川丸太町"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu333.htm",
    "lat": "35.056505",
    "long": "135.6765",
    "name": "まきのお",
    "name2": "槇ノ尾"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu418.htm",
    "lat": "35.0005784300",
    "long": "135.6877536000",
    "name": "まつおたいしゃまえ",
    "name2": "松尾大社前"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu438.htm",
    "lat": "34.9906175791",
    "long": "135.6929670380",
    "name": "まつおだいりちょう",
    "name2": "松尾大利町"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu417.htm",
    "lat": "35.0022070000",
    "long": "135.6917700000",
    "name": "まつおばし",
    "name2": "松尾橋"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu704.htm",
    "lat": "35.0515648000",
    "long": "135.7746642000",
    "name": "まつがさきえきまえ",
    "name2": "松ヶ崎駅前"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu244.htm",
    "lat": "35.0516605600",
    "long": "135.7788967000",
    "name": "まつがさきかいじりちょう",
    "name2": "松ヶ崎海尻町"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu837.htm",
    "lat": "35.0517056700",
    "long": "135.7850972000",
    "name": "まつがさきだいこくてん",
    "name2": "松ヶ崎大黒天"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu836.htm",
    "lat": "35.0515364127",
    "long": "135.7885157841",
    "name": "まつがさきばし",
    "name2": "松ヶ崎橋"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu477.htm",
    "lat": "35.0416470000",
    "long": "135.7621840000",
    "name": "まつのしたちょう",
    "name2": "松ノ下町"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu440.htm",
    "lat": "34.9961720000",
    "long": "135.6895460000",
    "name": "まつむろきたかわらちょう",
    "name2": "松室北河原町"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu250.htm",
    "lat": "35.0186229700",
    "long": "135.7358801000",
    "name": "まるたまちおんまえどおり",
    "name2": "丸太町御前通"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu392.htm",
    "lat": "35.0175430000",
    "long": "135.7738840000",
    "name": "まるたまちけいはんまえ",
    "name2": "丸太町京阪前"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu251.htm",
    "lat": "35.0184516400",
    "long": "135.7393133142",
    "name": "まるたまちしちほんまつ",
    "name2": "丸太町七本松"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu200.htm",
    "lat": "35.0181450000",
    "long": "135.7466120000",
    "name": "まるたまちちえこういん",
    "name2": "丸太町智恵光院"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu172.htm",
    "lat": "35.0512420000",
    "long": "135.6793740000",
    "name": "みきょうざか",
    "name2": "御経坂"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu315.htm",
    "lat": "34.9327606233",
    "long": "135.7511363730",
    "name": "みすこうえんまえ",
    "name2": "三栖公園前"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu821.htm",
    "lat": "34.9328784900",
    "long": "135.7540870000",
    "name": "みすだいこくちょう",
    "name2": "三栖大黒町"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu362.htm",
    "lat": "34.9123630000",
    "long": "135.7155880000",
    "name": "みずたれちょう",
    "name2": "水垂町"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu471.htm",
    "lat": "35.0587090000",
    "long": "135.7506451000",
    "name": "みそのぐちちょう",
    "name2": "御薗口町"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu090.htm",
    "lat": "35.0557180000",
    "long": "135.7670760000",
    "name": "みどろがいけ",
    "name2": "深泥池"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu326.htm",
    "lat": "35.0084340000",
    "long": "135.7066450000",
    "name": "みなみうずまさ",
    "name2": "南太秦"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu565.htm",
    "lat": "34.9766140000",
    "long": "135.7461550000",
    "name": "みなみくそうごうちょうしゃまえ",
    "name2": "南区総合庁舎前"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu672.htm",
    "lat": "34.9573655900",
    "long": "135.6608179000",
    "name": "みなみかすがちょう",
    "name2": "南春日町"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu847.htm",
    "lat": "34.9459380000",
    "long": "135.7224960000",
    "name": "みなみこうぎょうだんちまえ",
    "name2": "南工業団地前"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu465.htm",
    "lat": "35.0234047511",
    "long": "135.7950821779",
    "name": "みなみだちょう",
    "name2": "南田町"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu411.htm",
    "lat": "35.0037140000",
    "long": "135.7127360000",
    "name": "みなみひろまち",
    "name2": "南広町"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu809.htm",
    "lat": "34.9590340000",
    "long": "135.6855560000",
    "name": "みなみふくにしちょう（竹林公園前）",
    "name2": "南福西町（竹林公園前）"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu807.htm",
    "lat": "34.9546720000",
    "long": "135.6849750000",
    "name": "みなみふくにしちょうさんちょうめ",
    "name2": "南福西町三丁目"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu808.htm",
    "lat": "34.9566610000",
    "long": "135.6869640000",
    "name": "みなみふくにしちょうにちょうめ",
    "name2": "南福西町二丁目"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu530.htm",
    "lat": "34.9763220000",
    "long": "135.7639210000",
    "name": "みなみまつのきちょう",
    "name2": "南松ノ木町"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu751.htm",
    "lat": "34.9202328000",
    "long": "135.7318947000",
    "name": "みなみよこおおじ",
    "name2": "南横大路（さすてな京都前）"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu858.htm",
    "lat": "34.9845524147",
    "long": "135.6736886552",
    "name": "みねがどうちょういっちょうめ",
    "name2": "峰ケ堂町一丁目"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu852.htm",
    "lat": "34.9826240900",
    "long": "135.6724137000",
    "name": "みねがどうちょうさんちょうめ",
    "name2": "峰ケ堂町三丁目"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu148.htm",
    "lat": "35.0061610000",
    "long": "135.7457850000",
    "name": "みぶそうしゃじょうまえ",
    "name2": "みぶ操車場前"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu068.htm",
    "lat": "35.0035636000",
    "long": "135.7443930000",
    "name": "みぶでらみち",
    "name2": "壬生寺道"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu468.htm",
    "lat": "35.0176290000",
    "long": "135.7934040000",
    "name": "みやのまえちょう",
    "name2": "宮ノ前町"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu363.htm",
    "lat": "34.9100070000",
    "long": "135.7146850000",
    "name": "みやまえばしにしづめ",
    "name2": "宮前橋西詰"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu161.htm",
    "lat": "35.0258344800",
    "long": "135.7209572000",
    "name": "みょうしんじきたもんまえ",
    "name2": "妙心寺北門前"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu609.htm",
    "lat": "35.0197629500",
    "long": "135.7203350000",
    "name": "みょうしんじまえ",
    "name2": "妙心寺前"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu636.htm",
    "lat": "34.9705230000",
    "long": "135.7032470000",
    "name": "むしろだちょう",
    "name2": "莚田町"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu665.htm",
    "lat": "34.9635589265",
    "long": "135.6914386485",
    "name": "むこうかいせいびょういんまえ",
    "name2": "向日回生病院前"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu552.htm",
    "lat": "35.0472770000",
    "long": "135.7441540000",
    "name": "むらさきのうえのちょう",
    "name2": "紫野上野町"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu024.htm",
    "lat": "35.0491420000",
    "long": "135.7412130000",
    "name": "むらさきのせんどうちょう",
    "name2": "紫野泉堂町"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu750.htm",
    "lat": "34.9244061900",
    "long": "135.7225973000",
    "name": "めんきょしけんじょうまえ",
    "name2": "免許試験場前"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu604.htm",
    "lat": "34.9434220000",
    "long": "135.7686040000",
    "name": "もがみちょう",
    "name2": "最上町"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu681.htm",
    "lat": "34.9641730600",
    "long": "135.6956986000",
    "name": "もずめ",
    "name2": "物集女"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu020.htm",
    "lat": "35.0499450000",
    "long": "135.7536170000",
    "name": "もとまち",
    "name2": "元町"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu813.htm",
    "lat": "34.9479390000",
    "long": "135.6884710000",
    "name": "もみじちょう",
    "name2": "紅葉町"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu603.htm",
    "lat": "34.9413460000",
    "long": "135.7682910000",
    "name": "ももやまちゅうがくまえ",
    "name2": "桃山中学前"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu592.htm",
    "lat": "35.0131040000",
    "long": "135.7166030000",
    "name": "やすいにしぐち",
    "name2": "安井西口"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu194.htm",
    "lat": "35.0272500000",
    "long": "135.6959960000",
    "name": "やまごえ",
    "name2": "山越"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu857.htm",
    "lat": "35.0322740000",
    "long": "135.6955930000",
    "name": "やまごえおんすいぷーるまえ",
    "name2": "やまごえ温水プール前"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu856.htm",
    "lat": "35.0256930000",
    "long": "135.6961070000",
    "name": "やまごえなかちょう",
    "name2": "山越中町"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu709.htm",
    "lat": "35.0233210000",
    "long": "135.6983180000",
    "name": "やまごえひがしちょう",
    "name2": "山越東町"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu205.htm",
    "lat": "35.0083720000",
    "long": "135.7237440000",
    "name": "やまのうち",
    "name2": "山ノ内"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu406.htm",
    "lat": "35.0109050000",
    "long": "135.7216190000",
    "name": "やまのうちおいけ",
    "name2": "山ノ内御池"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu742.htm",
    "lat": "35.0559639813",
    "long": "135.7411051166",
    "name": "やまのまえちょう",
    "name2": "山ノ前町"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu195.htm",
    "lat": "35.0260640000",
    "long": "135.7001100000",
    "name": "ゆーすほすてるまえ",
    "name2": "ユースホステル前"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu355.htm",
    "lat": "34.9307540000",
    "long": "135.7403480000",
    "name": "よこおおじ",
    "name2": "横大路"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu749.htm",
    "lat": "34.9266770000",
    "long": "135.7438690000",
    "name": "よこおおじしゃこまえ",
    "name2": "横大路車庫前"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu860.htm",
    "lat": "35.0395217058",
    "long": "135.7390210847",
    "name": "らいとはうすまえ",
    "name2": "ライトハウス前"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu805.htm",
    "lat": "34.9602306100",
    "long": "135.6796262000",
    "name": "らくさいおおはし",
    "name2": "洛西大橋"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu630.htm",
    "lat": "34.9638007200",
    "long": "135.7030298000",
    "name": "らくさいぐちえきまえ",
    "name2": "洛西口駅前"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu790.htm",
    "lat": "34.9645379400",
    "long": "135.6676160000",
    "name": "らくさいこうこうまえ",
    "name2": "洛西高校前"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu801.htm",
    "lat": "34.9629250000",
    "long": "135.6760180000",
    "name": "らくさいばすたーみなる",
    "name2": "洛西バスターミナル"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu761.htm",
    "lat": "34.9232670000",
    "long": "135.7351470000",
    "name": "らくすいこうこうまえ",
    "name2": "洛水高校前"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu083.htm",
    "lat": "35.0458514535",
    "long": "135.7707795221",
    "name": "らくほくこうこうせいもんまえ",
    "name2": "洛北高校正門前"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu014.htm",
    "lat": "35.0440046319",
    "long": "135.7708813908",
    "name": "らくほくこうこうまえ",
    "name2": "洛北高校前"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu298.htm",
    "lat": "34.9789490000",
    "long": "135.7429670000",
    "name": "らじょうもん",
    "name2": "羅城門"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu614.htm",
    "lat": "35.027626",
    "long": "135.70902",
    "name": "らんでんうたのえきまえ",
    "name2": "嵐電宇多野駅前"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu768.htm",
    "lat": "35.0395430000",
    "long": "135.7264250000",
    "name": "りつめいかんさいおんじきねんかんまえ",
    "name2": "立命館西園寺記念館前"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu162.htm",
    "lat": "35.0266008500",
    "long": "135.7182770000",
    "name": "らんでんみょうしんじえきまえ",
    "name2": "嵐電妙心寺駅前"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu218.htm",
    "lat": "35.0347996200",
    "long": "135.7260479000",
    "name": "りつめいかんだいがくまえ",
    "name2": "立命館大学前"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu263.htm",
    "lat": "34.9637106000",
    "long": "135.7684636000",
    "name": "りゅうこくだいがくまえ",
    "name2": "龍谷大学前"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu327.htm",
    "lat": "35.0334512137",
    "long": "135.7253068686",
    "name": "りつめいかんだいがくまえ（きゃんぱすない）",
    "name2": "立命館大学前（キャンパス内）"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu140.htm",
    "lat": "34.9842860000",
    "long": "135.7474520000",
    "name": "ろくそんのうじんじゃまえ",
    "name2": "六孫王神社前"
  },
  {
    "URL": "https://www2.city.kyoto.lg.jp/kotsu/busdia/hyperdia/menu246.htm",
    "lat": "35.0350090000",
    "long": "135.7321200000",
    "name": "わらてんじんまえ",
    "name2": "わら天神前"
  }
]

# GeoJSON形式にデータを変換
features = []
for item in place:
    feature = {
        "type": "Feature",
        "geometry": {
            "type": "Point",
            "coordinates": [float(item['long']), float(item['lat'])] # GeoJSONは [経度, 緯度] の順
        },
        "properties": {
            "name": item['name'],
            "name2": item['name2'],
            "url": item['URL']
        }
    }
    features.append(feature)

geojson = {
    "type": "FeatureCollection",
    "features": features
}

# 確認用：コンソールに出力
print(json.dumps(geojson, indent=2, ensure_ascii=False))
