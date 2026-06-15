// 门店决策卡
const STORE_DATA = [
  {p:"BBQ",n:"中式烧烤",e:"🔥",c:[{f:"catalog/BBQ/BBQ_M01_中式烧烤创业母卡.html",n:"BBQ_M01_中式烧烤创业母卡"},{f:"catalog/BBQ/BBQ_T01_中式烧烤总纲.html",n:"BBQ_T01_中式烧烤总纲"},{f:"catalog/BBQ/BBQ_V01_腌料体系.html",n:"BBQ_V01_腌料体系"},{f:"catalog/BBQ/BBQ_V02_酱料体系.html",n:"BBQ_V02_酱料体系"},{f:"catalog/BBQ/BBQ_V03_撒料体系.html",n:"BBQ_V03_撒料体系"},{f:"catalog/BBQ/BBQ_V04_味型体系.html",n:"BBQ_V04_味型体系"},{f:"catalog/BBQ/BBQ_V05_地摊自助烤肉模式.html",n:"BBQ_V05_地摊自助烤肉模式"},{f:"catalog/BBQ/BBQ_V06_纸上烤肉门店模式.html",n:"BBQ_V06_纸上烤肉门店模式"}]},
  {p:"SL",n:"烧腊体系",e:"🍗",c:[{f:"catalog/SL/SL_M01_烧腊创业母卡.html",n:"SL_M01_烧腊创业母卡"},{f:"catalog/SL/SL_T01_烧腊总纲.html",n:"SL_T01_烧腊总纲"},{f:"catalog/SL/SL_V01_腌制与皮水体系.html",n:"SL_V01_腌制与皮水体系"},{f:"catalog/SL/SL_V02_烘烤与火候体系.html",n:"SL_V02_烘烤与火候体系"},{f:"catalog/SL/SL_V03_蘸料与卤水体系.html",n:"SL_V03_蘸料与卤水体系"},{f:"catalog/SL/SL_V04_斩切与出品体系.html",n:"SL_V04_斩切与出品体系"}]},
  {p:"KR",n:"韩式烤肉",e:"🥩",c:[{f:"catalog/KR/KR_001_秘制大块肉.html",n:"KR_001_秘制大块肉"},{f:"catalog/KR/KR_002_厚切五花肉.html",n:"KR_002_厚切五花肉"},{f:"catalog/KR/KR_003_LA牛排.html",n:"KR_003_LA牛排"},{f:"catalog/KR/KR_004_烤护心肉.html",n:"KR_004_烤护心肉"},{f:"catalog/KR/KR_005_烤大肠.html",n:"KR_005_烤大肠"},{f:"catalog/KR/KR_006_烤猪皮.html",n:"KR_006_烤猪皮"},{f:"catalog/KR/KR_01_韩式肥牛系列.html",n:"KR_01_韩式肥牛系列"},{f:"catalog/KR/KR_02_韩式厚切系列.html",n:"KR_02_韩式厚切系列"},{f:"catalog/KR/KR_03_韩式猪羊特色系列.html",n:"KR_03_韩式猪羊特色系列"},{f:"catalog/KR/KR_S_地摊烤肉精简版.html",n:"KR_S_地摊烤肉精简版"},
    {f:"catalog/其他/KR_04 韩式秘制烤肉系列（母）.html",n:"KR_04 韩式秘制烤肉系列（母）"}]},
  {p:"J",n:"鸡系列",e:"🐔",c:[{f:"catalog/J/J01 五香整鸡（母）.html",n:"J01 五香整鸡（母）"},{f:"catalog/J/J02 德州扒鸡（母）.html",n:"J02 德州扒鸡（母）"},{f:"catalog/J/J03 五香烧鸡（母）.html",n:"J03 五香烧鸡（母）"},{f:"catalog/J/J04 风干鸡（母）.html",n:"J04 风干鸡（母）"},{f:"catalog/J/J05 八珍药膳鸡（母）.html",n:"J05 八珍药膳鸡（母）"},{f:"catalog/J/J06 五香鸡爪（母）.html",n:"J06 五香鸡爪（母）"},{f:"catalog/J/J07 五香鸡翅（母）.html",n:"J07 五香鸡翅（母）"},{f:"catalog/J/J08 五香鸡腿（母）.html",n:"J08 五香鸡腿（母）"},{f:"catalog/J/J09 五香鸡胗（母）.html",n:"J09 五香鸡胗（母）"},{f:"catalog/J/J10 五香虎皮风爪（母）.html",n:"J10 五香虎皮风爪（母）"},{f:"catalog/J/J11 五香虎皮鸡腿（母）.html",n:"J11 五香虎皮鸡腿（母）"},{f:"catalog/J/J12 五香虎皮鸡头（母）.html",n:"J12 五香虎皮鸡头（母）"},{f:"catalog/J/J13 五香鸡头（母）.html",n:"J13 五香鸡头（母）"},{f:"catalog/J/J14 五香鸡肝（母）.html",n:"J14 五香鸡肝（母）"},{f:"catalog/J/J15 五香鸡心（母）.html",n:"J15 五香鸡心（母）"},{f:"catalog/J/J16 五香鸡肚（母）.html",n:"J16 五香鸡肚（母）"}]},
  {p:"Z",n:"猪系列",e:"🐷",c:[{f:"catalog/Z/Z01 五香猪头肉（母）.html",n:"Z01 五香猪头肉（母）"},{f:"catalog/Z/Z02 五香猪蹄（母）.html",n:"Z02 五香猪蹄（母）"},{f:"catalog/Z/Z03 五香猪尾巴.html",n:"Z03 五香猪尾巴"},{f:"catalog/Z/Z04 五香猪肘子带骨.html",n:"Z04 五香猪肘子带骨"},{f:"catalog/Z/Z05 五香猪耳朵.html",n:"Z05 五香猪耳朵"},{f:"catalog/Z/Z06 五香猪皮卷.html",n:"Z06 五香猪皮卷"},{f:"catalog/Z/Z07 五香猪口条.html",n:"Z07 五香猪口条"},{f:"catalog/Z/Z08 五香猪肝.html",n:"Z08 五香猪肝"},{f:"catalog/Z/Z09 五香猪心.html",n:"Z09 五香猪心"},{f:"catalog/Z/Z10 五香猪大肠.html",n:"Z10 五香猪大肠"},{f:"catalog/Z/Z11 五香猪连心肉.html",n:"Z11 五香猪连心肉"}]},
  {p:"B",n:"牛系列",e:"🐮",c:[{f:"catalog/B/B01 五香牛腱.html",n:"B01 五香牛腱"},{f:"catalog/B/B02 酱香牛肉.html",n:"B02 酱香牛肉"},{f:"catalog/B/B03 五香牛头肉.html",n:"B03 五香牛头肉"},{f:"catalog/B/B04 五香牛肝.html",n:"B04 五香牛肝"},{f:"catalog/B/B05 五香牛肚.html",n:"B05 五香牛肚"},{f:"catalog/B/B06 五香黄喉.html",n:"B06 五香黄喉"},{f:"catalog/B/B07 五香牛腩.html",n:"B07 五香牛腩"},{f:"catalog/B/B08 五香牛蹄筋.html",n:"B08 五香牛蹄筋"},{f:"catalog/B/B09 夫妻肺片.html",n:"B09 夫妻肺片"}]},
  {p:"E",n:"鹅系列",e:"🦆",c:[{f:"catalog/E/E01 五香鹅翅.html",n:"E01 五香鹅翅"},{f:"catalog/E/E02 五香鹅掌.html",n:"E02 五香鹅掌"},{f:"catalog/E/E03 五香鹅头.html",n:"E03 五香鹅头"},{f:"catalog/E/E04 五香鹅肠.html",n:"E04 五香鹅肠"}]},
  {p:"LW",n:"卤味体系",e:"🫘",c:[{f:"catalog/LW/LW001 卤鸭脖（母）LW_001.html",n:"LW001 卤鸭脖（母）LW_001"},{f:"catalog/LW/LW001 卤鸭脖（母）样卡.html",n:"LW001 卤鸭脖（母）样卡"},{f:"catalog/LW/LW002 卤鸭翅（母）LW_002.html",n:"LW002 卤鸭翅（母）LW_002"},{f:"catalog/LW/LW003 卤鸭掌（母）LW_003.html",n:"LW003 卤鸭掌（母）LW_003"},{f:"catalog/LW/LW004 卤鸭头（母）LW_004.html",n:"LW004 卤鸭头（母）LW_004"},{f:"catalog/LW/LW005 卤鸭锁骨（母）LW_005.html",n:"LW005 卤鸭锁骨（母）LW_005"}]},
  {p:"VC",n:"卤味·变体",e:"🌶️",c:[{f:"catalog/VC/VC001 麻辣鸭脖.html",n:"VC001 麻辣鸭脖"},{f:"catalog/VC/VC002 酱香鸭脖.html",n:"VC002 酱香鸭脖"},{f:"catalog/VC/VC003 藤椒鸭脖.html",n:"VC003 藤椒鸭脖"},{f:"catalog/VC/VC004 麻辣鸭翅.html",n:"VC004 麻辣鸭翅"},{f:"catalog/VC/VC005 酱香鸭翅.html",n:"VC005 酱香鸭翅"},{f:"catalog/VC/VC006 藤椒鸭翅.html",n:"VC006 藤椒鸭翅"},{f:"catalog/VC/VC007 麻辣鸭掌.html",n:"VC007 麻辣鸭掌"},{f:"catalog/VC/VC008 酱香鸭掌.html",n:"VC008 酱香鸭掌"},{f:"catalog/VC/VC009 藤椒鸭掌.html",n:"VC009 藤椒鸭掌"},{f:"catalog/VC/VC010 麻辣鸭头.html",n:"VC010 麻辣鸭头"},{f:"catalog/VC/VC011 酱香鸭头.html",n:"VC011 酱香鸭头"},{f:"catalog/VC/VC012 藤椒鸭头.html",n:"VC012 藤椒鸭头"},{f:"catalog/VC/VC013 麻辣锁骨.html",n:"VC013 麻辣锁骨"},{f:"catalog/VC/VC014 酱香锁骨.html",n:"VC014 酱香锁骨"},{f:"catalog/VC/VC015 藤椒锁骨.html",n:"VC015 藤椒锁骨"},{f:"catalog/VC/VC016 麻辣鸭舌.html",n:"VC016 麻辣鸭舌"},{f:"catalog/VC/VC017 酱香鸭舌.html",n:"VC017 酱香鸭舌"},{f:"catalog/VC/VC018 藤椒鸭舌.html",n:"VC018 藤椒鸭舌"},{f:"catalog/VC/VC019 麻辣鸭肠.html",n:"VC019 麻辣鸭肠"},{f:"catalog/VC/VC020 酱香鸭肠.html",n:"VC020 酱香鸭肠"},{f:"catalog/VC/VC021 藤椒鸭肠.html",n:"VC021 藤椒鸭肠"},{f:"catalog/VC/VC022 麻辣板肠.html",n:"VC022 麻辣板肠"},{f:"catalog/VC/VC023 酱香板肠.html",n:"VC023 酱香板肠"},{f:"catalog/VC/VC024 藤椒板肠.html",n:"VC024 藤椒板肠"},{f:"catalog/VC/VC025 麻辣鸭腿.html",n:"VC025 麻辣鸭腿"},{f:"catalog/VC/VC026 酱香鸭腿.html",n:"VC026 酱香鸭腿"},{f:"catalog/VC/VC027 藤椒鸭腿.html",n:"VC027 藤椒鸭腿"},{f:"catalog/VC/VC028 麻辣鸭心.html",n:"VC028 麻辣鸭心"},{f:"catalog/VC/VC029 酱香鸭心.html",n:"VC029 酱香鸭心"},{f:"catalog/VC/VC030 藤椒鸭心.html",n:"VC030 藤椒鸭心"},{f:"catalog/VC/VC031 麻辣鸭胗.html",n:"VC031 麻辣鸭胗"},{f:"catalog/VC/VC032 酱香鸭胗.html",n:"VC032 酱香鸭胗"},{f:"catalog/VC/VC033 藤椒鸭胗.html",n:"VC033 藤椒鸭胗"}]},
  {p:"SC",n:"素菜系列",e:"🥗",c:[{f:"catalog/SC/SC01 甜辣藕片（素菜·免费）.html",n:"SC01 甜辣藕片（素菜·免费）"},{f:"catalog/SC/SC02 甜辣土豆片（素菜·免费）.html",n:"SC02 甜辣土豆片（素菜·免费）"},{f:"catalog/SC/SC03 麻辣红油腐竹（素菜·免费）.html",n:"SC03 麻辣红油腐竹（素菜·免费）"},{f:"catalog/SC/SC04 麻辣红油豆干（素菜·免费）.html",n:"SC04 麻辣红油豆干（素菜·免费）"},{f:"catalog/SC/SC05 五香鸡汤千张（素菜·免费）.html",n:"SC05 五香鸡汤千张（素菜·免费）"},{f:"catalog/SC/SC06 五香鸡汤海带丝（素菜·免费）.html",n:"SC06 五香鸡汤海带丝（素菜·免费）"}]},
  {p:"CJ",n:"炒鸡体系",e:"🍳",c:[{f:"catalog/CJ/CJ_M01_炒鸡创业母卡.html",n:"CJ_M01_炒鸡创业母卡"},{f:"catalog/CJ/CJ_T01_炒鸡总纲.html",n:"CJ_T01_炒鸡总纲"},{f:"catalog/CJ/CJ_V01_炒鸡工艺体系.html",n:"CJ_V01_炒鸡工艺体系"},{f:"catalog/CJ/CJ_V02_炒鸡配套体系.html",n:"CJ_V02_炒鸡配套体系"}]},
  {p:"GS",n:"贵州酸汤",e:"🥘",c:[{f:"catalog/GS/GS_M01_贵州酸汤创业母卡.html",n:"GS_M01_贵州酸汤创业母卡"},{f:"catalog/GS/GS_T01_贵州酸汤总纲.html",n:"GS_T01_贵州酸汤总纲"},{f:"catalog/GS/GS_V01_贵州酸汤发酵高汤体系.html",n:"GS_V01_贵州酸汤发酵高汤体系"},{f:"catalog/GS/GS_V02_贵州酸汤蘸水蘸料体系.html",n:"GS_V02_贵州酸汤蘸水蘸料体系"},{f:"catalog/GS/GS_V03_贵州酸汤涮品搭配体系.html",n:"GS_V03_贵州酸汤涮品搭配体系"}]},
  {p:"HG",n:"火锅体系",e:"🫕",c:[{f:"catalog/HG/HG_M01_火锅创业母卡.html",n:"HG_M01_火锅创业母卡"},{f:"catalog/HG/HG_T01_火锅总纲.html",n:"HG_T01_火锅总纲"},{f:"catalog/HG/HG_V01_火锅底料配方体系.html",n:"HG_V01_火锅底料配方体系"},{f:"catalog/HG/HG_V02_火锅蘸料体系.html",n:"HG_V02_火锅蘸料体系"},{f:"catalog/HG/HG_V03_火锅涮品搭配体系.html",n:"HG_V03_火锅涮品搭配体系"}]},
  {p:"HM",n:"河南烩面",e:"🍜",c:[{f:"catalog/HM/HM_M01_河南烩面创业母卡.html",n:"HM_M01_河南烩面创业母卡"},{f:"catalog/HM/HM_T01_河南烩面总纲.html",n:"HM_T01_河南烩面总纲"},{f:"catalog/HM/HM_V01_烩面汤底扯面工艺.html",n:"HM_V01_烩面汤底扯面工艺"},{f:"catalog/HM/HM_V02_烩面浇头配菜体系.html",n:"HM_V02_烩面浇头配菜体系"}]},
  {p:"KY",n:"烤鱼体系",e:"🐟",c:[{f:"catalog/KY/KY_M01_烤鱼创业母卡.html",n:"KY_M01_烤鱼创业母卡"},{f:"catalog/KY/KY_T01_烤鱼总纲.html",n:"KY_T01_烤鱼总纲"},{f:"catalog/KY/KY_V01_烤鱼底料酱料体系.html",n:"KY_V01_烤鱼底料酱料体系"},{f:"catalog/KY/KY_V02_烤鱼腌料撒料体系.html",n:"KY_V02_烤鱼腌料撒料体系"},{f:"catalog/KY/KY_V03_烤鱼浇头配菜体系.html",n:"KY_V03_烤鱼浇头配菜体系"}]},
  {p:"MLT",n:"麻辣烫冒菜",e:"🥘",c:[{f:"catalog/MLT/MLT_M01_麻辣烫冒菜创业母卡.html",n:"MLT_M01_麻辣烫冒菜创业母卡"},{f:"catalog/MLT/MLT_T01_麻辣烫冒菜总纲.html",n:"MLT_T01_麻辣烫冒菜总纲"},{f:"catalog/MLT/MLT_V01_麻辣烫冒菜底料体系.html",n:"MLT_V01_麻辣烫冒菜底料体系"},{f:"catalog/MLT/MLT_V02_麻辣烫冒菜碗底料体系.html",n:"MLT_V02_麻辣烫冒菜碗底料体系"},{f:"catalog/MLT/MLT_V03_麻辣烫冒菜蘸料干碟体系.html",n:"MLT_V03_麻辣烫冒菜蘸料干碟体系"}]},
  {p:"XLX",n:"小龙虾",e:"🦞",c:[{f:"catalog/XLX/XLX_M01_小龙虾创业母卡.html",n:"XLX_M01_小龙虾创业母卡"},{f:"catalog/XLX/XLX_T01_小龙虾总纲.html",n:"XLX_T01_小龙虾总纲"},{f:"catalog/XLX/XLX_V01_小龙虾底料调味体系.html",n:"XLX_V01_小龙虾底料调味体系"},{f:"catalog/XLX/XLX_V02_小龙虾清洗过油炒制工艺.html",n:"XLX_V02_小龙虾清洗过油炒制工艺"},{f:"catalog/XLX/XLX_V03_小龙虾配菜蘸料虾尾衍生品.html",n:"XLX_V03_小龙虾配菜蘸料虾尾衍生品"}]},
  {p:"YN",n:"云南米线",e:"🍜",c:[{f:"catalog/YN/YN_M01_云南米线创业母卡.html",n:"YN_M01_云南米线创业母卡"},{f:"catalog/YN/YN_T01_云南米线总纲.html",n:"YN_T01_云南米线总纲"},{f:"catalog/YN/YN_V01_云南米线汤底帽子体系.html",n:"YN_V01_云南米线汤底帽子体系"},{f:"catalog/YN/YN_V02_云南米线过桥小锅技法.html",n:"YN_V02_云南米线过桥小锅技法"},{f:"catalog/YN/YN_V03_云南米线辅料蘸水配菜体系.html",n:"YN_V03_云南米线辅料蘸水配菜体系"},
    {f:"catalog/其他/YN_008 小锅米线·昆明风味（子）.html",n:"YN_008 小锅米线·昆明风味（子）"}]},
  {p:"ZHA",n:"中式炸串",e:"🍢",c:[{f:"catalog/ZHA/ZHA_M01_炸串创业母卡.html",n:"ZHA_M01_炸串创业母卡"},{f:"catalog/ZHA/ZHA_T01_炸串总纲.html",n:"ZHA_T01_炸串总纲"},{f:"catalog/ZHA/ZHA_V01_炸串挂糊体系.html",n:"ZHA_V01_炸串挂糊体系"},{f:"catalog/ZHA/ZHA_V02_炸串酱料体系.html",n:"ZHA_V02_炸串酱料体系"},{f:"catalog/ZHA/ZHA_V03_炸串撒料体系.html",n:"ZHA_V03_炸串撒料体系"}]},
  {p:"JL",n:"韩式酱料",e:"🧂",c:[{f:"catalog/JL/JL_020_韩式烤肉蘸酱.html",n:"JL_020_韩式烤肉蘸酱"},{f:"catalog/JL/JL_021_韩式大酱.html",n:"JL_021_韩式大酱"},{f:"catalog/JL/JL_022_韩式辣椒酱.html",n:"JL_022_韩式辣椒酱"}]},
  {p:"KF",n:"韩式汤/主食",e:"🍲",c:[{f:"catalog/KF/KF_001_石锅拌饭.html",n:"KF_001_石锅拌饭"},{f:"catalog/KF/KF_002_冷面.html",n:"KF_002_冷面"},{f:"catalog/KF/KF_003_大酱汤.html",n:"KF_003_大酱汤"},{f:"catalog/KF/KF_004_嫩豆腐汤.html",n:"KF_004_嫩豆腐汤"},{f:"catalog/KF/KF_005_肥牛拌饭.html",n:"KF_005_肥牛拌饭"},{f:"catalog/KF/KF_006_辣白菜炒饭.html",n:"KF_006_辣白菜炒饭"},{f:"catalog/KF/KF_007_海鲜葱饼.html",n:"KF_007_海鲜葱饼"},{f:"catalog/KF/KF_008_辣炒年糕.html",n:"KF_008_辣炒年糕"},{f:"catalog/KF/KF_009_泡菜汤.html",n:"KF_009_泡菜汤"},{f:"catalog/KF/KF_010_部队锅.html",n:"KF_010_部队锅"},{f:"catalog/KF/KF_011_参鸡汤.html",n:"KF_011_参鸡汤"},{f:"catalog/KF/KF_012_排骨汤.html",n:"KF_012_排骨汤"}]},
  {p:"PC",n:"韩式拌菜",e:"🥬",c:[{f:"catalog/PC/PC_K01_韩式辣白菜系列.html",n:"PC_K01_韩式辣白菜系列"},{f:"catalog/PC/PC_K02_韩式牛副拌菜.html",n:"PC_K02_韩式牛副拌菜"},{f:"catalog/PC/PC_K03_韩式明太鱼系列.html",n:"PC_K03_韩式明太鱼系列"},{f:"catalog/PC/PC_K04_韩式豆制品系列.html",n:"PC_K04_韩式豆制品系列"},{f:"catalog/PC/PC_K05_韩式腌菜拌菜系列.html",n:"PC_K05_韩式腌菜拌菜系列"},{f:"catalog/PC/PC_K06_韩式拌豆芽.html",n:"PC_K06_韩式拌豆芽"},{f:"catalog/PC/PC_K07_韩式炒鱼饼.html",n:"PC_K07_韩式炒鱼饼"},{f:"catalog/PC/PC_K08_韩式拌菠菜.html",n:"PC_K08_韩式拌菠菜"}]}];

// 地摊产品卡
const STALL_DATA = [
  {p:"TS",n:"甜品饮品",e:"🍧",c:[{f:"catalog/其他/五指毛桃奶茶（子）TS_067.html",n:"五指毛桃奶茶（子）TS_067"},{f:"catalog/其他/五指毛桃椰乳（母）TS_065.html",n:"五指毛桃椰乳（母）TS_065"},{f:"catalog/其他/五指毛桃薏米水（子）TS_066.html",n:"五指毛桃薏米水（子）TS_066"},{f:"catalog/其他/冰菠萝（母）TS_005.html",n:"冰菠萝（母）TS_005"},{f:"catalog/其他/凤凰单丛果茶（母）TS_087.html",n:"凤凰单丛果茶（母）TS_087"},{f:"catalog/其他/凤梨水果冰（母）TS_006.html",n:"凤梨水果冰（母）TS_006"},{f:"catalog/其他/厚椰冻冻（母）TS_083.html",n:"厚椰冻冻（母）TS_083"},{f:"catalog/其他/厚椰拿铁冻（子）TS_084.html",n:"厚椰拿铁冻（子）TS_084"},{f:"catalog/其他/厚椰斑斓冻（子）TS_085.html",n:"厚椰斑斓冻（子）TS_085"},{f:"catalog/其他/可可麻薯草莓杯（子）TS_077.html",n:"可可麻薯草莓杯（子）TS_077"},{f:"catalog/其他/多彩水果茶（母）TS_007.html",n:"多彩水果茶（母）TS_007"},{f:"catalog/其他/奶茶大满贯（母）TS_008.html",n:"奶茶大满贯（母）TS_008"},{f:"catalog/其他/巴西莓酸奶碗（母）TS_047.html",n:"巴西莓酸奶碗（母）TS_047"},{f:"catalog/其他/抹茶巨无霸珍珠（母）TS_009.html",n:"抹茶巨无霸珍珠（母）TS_009"},{f:"catalog/其他/抹茶麻薯草莓杯（子）TS_076.html",n:"抹茶麻薯草莓杯（子）TS_076"},{f:"catalog/其他/斑斓冻（母）TS_003.html",n:"斑斓冻（母）TS_003"},{f:"catalog/其他/斑斓芒果糯米饭杯（子）TS_051.html",n:"斑斓芒果糯米饭杯（子）TS_051"},{f:"catalog/其他/杏仁豆腐（母）TS_081.html",n:"杏仁豆腐（母）TS_081"},{f:"catalog/其他/杨枝甘露（母）TS_010.html",n:"杨枝甘露（母）TS_010"},{f:"catalog/其他/杨梅冰汤圆（子）TS_060.html",n:"杨梅冰汤圆（子）TS_060"},{f:"catalog/其他/杨梅冰粉（母）TS_059.html",n:"杨梅冰粉（母）TS_059"},{f:"catalog/其他/杨梅荔枝冰粉（子）TS_061.html",n:"杨梅荔枝冰粉（子）TS_061"},{f:"catalog/其他/板栗奶茶（母）TS_011.html",n:"板栗奶茶（母）TS_011"},{f:"catalog/其他/栀子轻乳茶（母）TS_089.html",n:"栀子轻乳茶（母）TS_089"},{f:"catalog/其他/桂花冰粉（母）TS_082.html",n:"桂花冰粉（母）TS_082"},{f:"catalog/其他/桂花酒酿冰奶（子）TS_056.html",n:"桂花酒酿冰奶（子）TS_056"},{f:"catalog/其他/桂花酒酿奶冻（母）TS_055.html",n:"桂花酒酿奶冻（母）TS_055"},{f:"catalog/其他/桂花酒酿小圆子奶冻（子）TS_058.html",n:"桂花酒酿小圆子奶冻（子）TS_058"},{f:"catalog/其他/桂花酒酿拿铁（子）TS_057.html",n:"桂花酒酿拿铁（子）TS_057"},{f:"catalog/其他/桂花马蹄爽（母）TS_012.html",n:"桂花马蹄爽（母）TS_012"},{f:"catalog/其他/椰奶布丁·撞奶（母）TS_013.html",n:"椰奶布丁·撞奶（母）TS_013"},{f:"catalog/其他/椰奶清补凉（母）TS_014.html",n:"椰奶清补凉（母）TS_014"},{f:"catalog/其他/椰奶西米露（母）TS_015.html",n:"椰奶西米露（母）TS_015"},{f:"catalog/其他/椰皇冻水果杯（子）TS_054.html",n:"椰皇冻水果杯（子）TS_054"},{f:"catalog/其他/椰皇冻（母）TS_052.html",n:"椰皇冻（母）TS_052"}]},
  {p:"MP",n:"面点包子",e:"🥟",c:[{f:"catalog/其他/三鲜锅贴（母）MP_030.html",n:"三鲜锅贴（母）MP_030"},{f:"catalog/其他/上海生煎（进阶版）（母）MP_020.html",n:"上海生煎（进阶版）（母）MP_020"},{f:"catalog/其他/上海粢饭团（母）MP_063.html",n:"上海粢饭团（母）MP_063"},{f:"catalog/其他/京东肉饼（母）MP_023.html",n:"京东肉饼（母）MP_023"},{f:"catalog/其他/冰豆浆（母）MP_034.html",n:"冰豆浆（母）MP_034"},{f:"catalog/其他/凉皮凉面（母）MP_042.html",n:"凉皮凉面（母）MP_042"},{f:"catalog/其他/千层葱花饼（母）MP_024.html",n:"千层葱花饼（母）MP_024"},{f:"catalog/其他/叉烧包（广式）（母）MP_058.html",n:"叉烧包（广式）（母）MP_058"},{f:"catalog/其他/叶儿粑（母）MP_047.html",n:"叶儿粑（母）MP_047"},{f:"catalog/其他/土家掉渣饼（母）MP_025.html",n:"土家掉渣饼（母）MP_025"},{f:"catalog/其他/大葱肉包（母）MP_019.html",n:"大葱肉包（母）MP_019"},{f:"catalog/其他/宁波汤圆（母）MP_064.html",n:"宁波汤圆（母）MP_064"},{f:"catalog/其他/小笼包（母）MP_003.html",n:"小笼包（母）MP_003"},{f:"catalog/其他/小馄饨（母）MP_053.html",n:"小馄饨（母）MP_053"},{f:"catalog/其他/山东杂粮煎饼（母）MP_015.html",n:"山东杂粮煎饼（母）MP_015"},{f:"catalog/其他/开封灌汤包（地方强化版）（母）MP_038.html",n:"开封灌汤包（地方强化版）（母）MP_038"},{f:"catalog/其他/手抓饼（母）MP_006.html",n:"手抓饼（母）MP_006"},{f:"catalog/其他/杂粮鸡蛋饼（轻健康）（母）MP_028.html",n:"杂粮鸡蛋饼（轻健康）（母）MP_028"},{f:"catalog/其他/梅菜扣肉包（母）MP_002.html",n:"梅菜扣肉包（母）MP_002"},{f:"catalog/其他/武汉热干面（母）MP_049.html",n:"武汉热干面（母）MP_049"},{f:"catalog/其他/河南水煎包（母）MP_037.html",n:"河南水煎包（母）MP_037"},{f:"catalog/其他/河南胡辣汤（母）MP_036.html",n:"河南胡辣汤（母）MP_036"},{f:"catalog/其他/油条豆腐脑组合（母）MP_039.html",n:"油条豆腐脑组合（母）MP_039"},{f:"catalog/其他/油泼面（母）MP_043.html",n:"油泼面（母）MP_043"},{f:"catalog/其他/油炸糕（母）MP_061.html",n:"油炸糕（母）MP_061"},{f:"catalog/其他/潮汕肠粉（轻早餐版）（母）MP_065.html",n:"潮汕肠粉（轻早餐版）（母）MP_065"},{f:"catalog/其他/灌汤包（母）MP_004.html",n:"灌汤包（母）MP_004"},{f:"catalog/其他/炸酱面（母）MP_033.html",n:"炸酱面（母）MP_033"},{f:"catalog/其他/烤冷面（东北强化版）（母）MP_060.html",n:"烤冷面（东北强化版）（母）MP_060"},{f:"catalog/其他/烤冷面（母）MP_026.html",n:"烤冷面（母）MP_026"},{f:"catalog/其他/烩面（母）MP_040.html",n:"烩面（母）MP_040"},{f:"catalog/其他/热干面（母）MP_031.html",n:"热干面（母）MP_031"},{f:"catalog/其他/煎饼果子（母）MP_008.html",n:"煎饼果子（母）MP_008"},{f:"catalog/其他/牛肉馅饼（母）MP_013.html",n:"牛肉馅饼（母）MP_013"},{f:"catalog/其他/猪肉锅贴（母）MP_029.html",n:"猪肉锅贴（母）MP_029"},{f:"catalog/其他/MP_022 韭菜盒子（母）.html",n:"MP_022 韭菜盒子（母）"}]},
  {p:"HZ",n:"韩式炸鸡",e:"🍗",c:[{f:"catalog/其他/什锦起司棒棒鸡（子）HZ_022.html",n:"什锦起司棒棒鸡（子）HZ_022"},{f:"catalog/其他/全罗道秘酱火辣无骨炸鸡（子）HZ_034.html",n:"全罗道秘酱火辣无骨炸鸡（子）HZ_034"},{f:"catalog/其他/全罗道秘酱火辣炸鸡翅（子）HZ_037.html",n:"全罗道秘酱火辣炸鸡翅（子）HZ_037"},{f:"catalog/其他/初雪雪翼芝士无骨炸鸡（子）HZ_033.html",n:"初雪雪翼芝士无骨炸鸡（子）HZ_033"},{f:"catalog/其他/初雪雪翼芝士炸鸡翅（子）HZ_036.html",n:"初雪雪翼芝士炸鸡翅（子）HZ_036"},{f:"catalog/其他/原味黄金炸鸡（母）HZ_001.html",n:"原味黄金炸鸡（母）HZ_001"},{f:"catalog/其他/原味黄金鸡翅中翅根（子）HZ_014.html",n:"原味黄金鸡翅中翅根（子）HZ_014"},{f:"catalog/其他/咖喱鸡小腿（母）HZ_041.html",n:"咖喱鸡小腿（母）HZ_041"},{f:"catalog/其他/坚果起司棒棒鸡（子）HZ_020.html",n:"坚果起司棒棒鸡（子）HZ_020"},{f:"catalog/其他/培根起司棒棒鸡（子）HZ_018.html",n:"培根起司棒棒鸡（子）HZ_018"},{f:"catalog/其他/奥尔良烤鸡（母）HZ_044.html",n:"奥尔良烤鸡（母）HZ_044"},{f:"catalog/其他/奥尔良黄金鸡翅中翅根（子）HZ_017.html",n:"奥尔良黄金鸡翅中翅根（子）HZ_017"},{f:"catalog/其他/年糕无骨炸鸡（子）HZ_023.html",n:"年糕无骨炸鸡（子）HZ_023"},{f:"catalog/其他/年糕炸鸡系列（母）HZ_005.html",n:"年糕炸鸡系列（母）HZ_005"},{f:"catalog/其他/果味蜜汁鸡块（子）HZ_011.html",n:"果味蜜汁鸡块（子）HZ_011"},{f:"catalog/其他/正宗韩式原味炸整鸡（母）HZ_031.html",n:"正宗韩式原味炸整鸡（母）HZ_031"},{f:"catalog/其他/水果起司棒棒鸡（子）HZ_019.html",n:"水果起司棒棒鸡（子）HZ_019"},{f:"catalog/其他/海鲜年糕无骨炸鸡（子）HZ_027.html",n:"海鲜年糕无骨炸鸡（子）HZ_027"},{f:"catalog/其他/海鲜起司棒棒鸡（子）HZ_021.html",n:"海鲜起司棒棒鸡（子）HZ_021"},{f:"catalog/其他/炸鸡翅系列（母）HZ_003.html",n:"炸鸡翅系列（母）HZ_003"},{f:"catalog/其他/糖醋蜜汁鸡块（子）HZ_013.html",n:"糖醋蜜汁鸡块（子）HZ_013"},{f:"catalog/其他/经典洋酿裹酱整鸡（母）HZ_032.html",n:"经典洋酿裹酱整鸡（母）HZ_032"},{f:"catalog/其他/经典韩风蜜汁鸡块（子）HZ_008.html",n:"经典韩风蜜汁鸡块（子）HZ_008"},{f:"catalog/其他/美式炸鸡（母）HZ_042.html",n:"美式炸鸡（母）HZ_042"},{f:"catalog/其他/脆皮烤鸡（母）HZ_043.html",n:"脆皮烤鸡（母）HZ_043"},{f:"catalog/其他/脆皮芝士雪花炸鸡（母）HZ_039.html",n:"脆皮芝士雪花炸鸡（母）HZ_039"},{f:"catalog/其他/蒜香黄金鸡翅中翅根（子）HZ_015.html",n:"蒜香黄金鸡翅中翅根（子）HZ_015"},{f:"catalog/其他/蜜汁年糕无骨炸鸡（子）HZ_024.html",n:"蜜汁年糕无骨炸鸡（子）HZ_024"},{f:"catalog/其他/蜜汁酱裹鸡块（母）HZ_002.html",n:"蜜汁酱裹鸡块（母）HZ_002"},{f:"catalog/其他/蝴蝶炸虾（子）HZ_029.html",n:"蝴蝶炸虾（子）HZ_029"},{f:"catalog/其他/蝴蝶炸虾（母）HZ_007.html",n:"蝴蝶炸虾（母）HZ_007"},{f:"catalog/其他/香辣黄金鸡翅中翅根（子）HZ_016.html",n:"香辣黄金鸡翅中翅根（子）HZ_016"}]},
  {p:"JP",n:"炸物串烧",e:"🍢",c:[{f:"catalog/其他/什锦天妇罗（母）JP_028.html",n:"什锦天妇罗（母）JP_028"},{f:"catalog/其他/叉烧豚骨拉面（母）JP_015.html",n:"叉烧豚骨拉面（母）JP_015"},{f:"catalog/其他/可乐饼（母）JP_025.html",n:"可乐饼（母）JP_025"},{f:"catalog/其他/味噌拉面（母）JP_013.html",n:"味噌拉面（母）JP_013"},{f:"catalog/其他/咖喱鸡排饭（母）JP_022.html",n:"咖喱鸡排饭（母）JP_022"},{f:"catalog/其他/唐扬鸡块（母）JP_023.html",n:"唐扬鸡块（母）JP_023"},{f:"catalog/其他/地狱辣味噌（母）JP_016.html",n:"地狱辣味噌（母）JP_016"},{f:"catalog/其他/日式炸猪排（母）JP_024.html",n:"日式炸猪排（母）JP_024"},{f:"catalog/其他/月见鸡肉丸（母）JP_009.html",n:"月见鸡肉丸（母）JP_009"},{f:"catalog/其他/柚子盐拉面（母）JP_018.html",n:"柚子盐拉面（母）JP_018"},{f:"catalog/其他/炸虾天妇罗（母）JP_026.html",n:"炸虾天妇罗（母）JP_026"},{f:"catalog/其他/照烧鸡排丼（母）JP_021.html",n:"照烧鸡排丼（母）JP_021"},{f:"catalog/其他/牛丼（母）JP_019.html",n:"牛丼（母）JP_019"},{f:"catalog/其他/盐烧鸡腿串（母）JP_001.html",n:"盐烧鸡腿串（母）JP_001"},{f:"catalog/其他/葱间鸡腿串（母）JP_008.html",n:"葱间鸡腿串（母）JP_008"},{f:"catalog/其他/蔬菜天妇罗（母）JP_027.html",n:"蔬菜天妇罗（母）JP_027"},{f:"catalog/其他/豚骨拉面（母）JP_011.html",n:"豚骨拉面（母）JP_011"},{f:"catalog/其他/酱油拉面（母）JP_012.html",n:"酱油拉面（母）JP_012"},{f:"catalog/其他/酱烧鸡腿串（母）JP_002.html",n:"酱烧鸡腿串（母）JP_002"},{f:"catalog/其他/鸡心串（母）JP_005.html",n:"鸡心串（母）JP_005"},{f:"catalog/其他/鸡白汤拉面（母）JP_017.html",n:"鸡白汤拉面（母）JP_017"},{f:"catalog/其他/鸡皮串（母）JP_003.html",n:"鸡皮串（母）JP_003"},{f:"catalog/其他/鸡翅串（母）JP_010.html",n:"鸡翅串（母）JP_010"},{f:"catalog/其他/鸡肉丸（母）JP_007.html",n:"鸡肉丸（母）JP_007"},{f:"catalog/其他/鸡肉丼（母）JP_020.html",n:"鸡肉丼（母）JP_020"},{f:"catalog/其他/鸡肉天妇罗（母）JP_029.html",n:"鸡肉天妇罗（母）JP_029"},{f:"catalog/其他/鸡胗串（母）JP_006.html",n:"鸡胗串（母）JP_006"},{f:"catalog/其他/鸡脆骨串（母）JP_004.html",n:"鸡脆骨串（母）JP_004"},{f:"catalog/其他/黑蒜油豚骨（母）JP_014.html",n:"黑蒜油豚骨（母）JP_014"}]},
  {p:"DC",n:"傣舂凉菜",e:"🥬",c:[{f:"catalog/其他/傣舂三拼（母）DC_012.html",n:"傣舂三拼（母）DC_012"},{f:"catalog/其他/傣舂全家福（母）DC_013.html",n:"傣舂全家福（母）DC_013"},{f:"catalog/其他/傣舂双拼（母）DC_011.html",n:"傣舂双拼（母）DC_011"},{f:"catalog/其他/傣舂大虾（母）DC_003.html",n:"傣舂大虾（母）DC_003"},{f:"catalog/其他/傣舂木瓜（母）DC_007.html",n:"傣舂木瓜（母）DC_007"},{f:"catalog/其他/傣舂泡面（母）DC_009.html",n:"傣舂泡面（母）DC_009"},{f:"catalog/其他/傣舂海带（母）DC_008.html",n:"傣舂海带（母）DC_008"},{f:"catalog/其他/傣舂米线（母）DC_010.html",n:"傣舂米线（母）DC_010"},{f:"catalog/其他/傣舂菠萝（母）DC_006.html",n:"傣舂菠萝（母）DC_006"},{f:"catalog/其他/傣舂鱿鱼（母）DC_002.html",n:"傣舂鱿鱼（母）DC_002"},{f:"catalog/其他/傣舂鸡脚（母）DC_001.html",n:"傣舂鸡脚（母）DC_001"},{f:"catalog/其他/傣舂鸡腿（母）DC_004.html",n:"傣舂鸡腿（母）DC_004"},{f:"catalog/其他/傣舂黄瓜（母）DC_005.html",n:"傣舂黄瓜（母）DC_005"}]},
  {p:"YL",n:"饮品系列",e:"🍹",c:[{f:"catalog/其他/柳橙冰茶（母）YL_066.html",n:"柳橙冰茶（母）YL_066"},{f:"catalog/其他/水蜜桃冰茶（母）YL_067.html",n:"水蜜桃冰茶（母）YL_067"},{f:"catalog/其他/洛神冰茶（母）YL_064.html",n:"洛神冰茶（母）YL_064"},{f:"catalog/其他/百香冰茶（母）YL_063.html",n:"百香冰茶（母）YL_063"},{f:"catalog/其他/芒果冰茶（母）YL_062.html",n:"芒果冰茶（母）YL_062"},{f:"catalog/其他/菊花雪梨（母）YL_068.html",n:"菊花雪梨（母）YL_068"},{f:"catalog/其他/蜂蜜冰茶（母）YL_061.html",n:"蜂蜜冰茶（母）YL_061"},{f:"catalog/其他/金桔冰茶（母）YL_065.html",n:"金桔冰茶（母）YL_065"},{f:"catalog/其他/金桔蜜柚（母）YL_069.html",n:"金桔蜜柚（母）YL_069"},{f:"catalog/其他/黄金蜜枣冰茶（母）YL_060.html",n:"黄金蜜枣冰茶（母）YL_060"}]},
  {p:"XC",n:"小吃系列",e:"🍿",c:[
    {f:"catalog/其他/甘梅脆皮地瓜条（母）XC_020.html",n:"甘梅脆皮地瓜条（母）XC_020"},
    {f:"catalog/其他/紫菜卷·原味金枪鱼肉松（母）XC_025.html",n:"紫菜卷·原味金枪鱼肉松（母）XC_025"},
    {f:"catalog/其他/美式炸薯条（子）XC_021.html",n:"美式炸薯条（子）XC_021"},
    {f:"catalog/其他/葱香茄子饼（子）XC_024.html",n:"葱香茄子饼（子）XC_024"},
    {f:"catalog/其他/黄金洋葱圈（子）XC_022.html",n:"黄金洋葱圈（子）XC_022"},
    {f:"catalog/其他/黄金香蕉棒（子）XC_023.html",n:"黄金香蕉棒（子）XC_023"},
    {f:"catalog/其他/臭豆腐（母）XC_100.html",n:"臭豆腐（母）XC_100"},
    {f:"catalog/其他/铁板鱿鱼（母）XC_101.html",n:"铁板鱿鱼（母）XC_101"},
    {f:"catalog/其他/铁板豆腐（母）XC_102.html",n:"铁板豆腐（母）XC_102"},
    {f:"catalog/其他/烤面筋（母）XC_103.html",n:"烤面筋（母）XC_103"},
    {f:"catalog/其他/羊肉串（母）XC_104.html",n:"羊肉串（母）XC_104"},
    {f:"catalog/其他/章鱼小丸子（母）XC_105.html",n:"章鱼小丸子（母）XC_105"},
    {f:"catalog/其他/鸡蛋仔（母）XC_106.html",n:"鸡蛋仔（母）XC_106"},
    {f:"catalog/其他/冰糖葫芦（母）XC_107.html",n:"冰糖葫芦（母）XC_107"},
    {f:"catalog/其他/烤红薯（母）XC_108.html",n:"烤红薯（母）XC_108"},
    {f:"catalog/其他/蒜蓉烤生蚝（母）XC_109.html",n:"蒜蓉烤生蚝（母）XC_109"},
    {f:"catalog/其他/酸辣粉（母）XC_110.html",n:"酸辣粉（母）XC_110"},
    {f:"catalog/其他/螺蛳粉（母）XC_111.html",n:"螺蛳粉（母）XC_111"},
    {f:"catalog/其他/干炒牛河（母）XC_112.html",n:"干炒牛河（母）XC_112"},
    {f:"catalog/其他/关东煮（母）XC_113.html",n:"关东煮（母）XC_113"},
    {f:"catalog/其他/麻辣拌（母）XC_114.html",n:"麻辣拌（母）XC_114"},
    {f:"catalog/其他/蛋烘糕（母）XC_115.html",n:"蛋烘糕（母）XC_115"},
    {f:"catalog/其他/钵仔糕（母）XC_116.html",n:"钵仔糕（母）XC_116"},
    {f:"catalog/其他/烤玉米（母）XC_117.html",n:"烤玉米（母）XC_117"},
    {f:"catalog/其他/糖炒栗子（母）XC_118.html",n:"糖炒栗子（母）XC_118"},
    {f:"catalog/其他/脆皮五花肉（母）XC_119.html",n:"脆皮五花肉（母）XC_119"},{f:"catalog/其他/腊汁肉夹馍XC_120.html",n:"腊汁肉夹馍XC_120"},{f:"catalog/其他/红油凉皮XC_121.html",n:"红油凉皮XC_121"},{f:"catalog/其他/信阳热干面XC_122.html",n:"信阳热干面XC_122"},{f:"catalog/其他/登封芝麻烧饼XC_123.html",n:"登封芝麻烧饼XC_123"},{f:"catalog/其他/洛阳涮牛肚XC_124.html",n:"洛阳涮牛肚XC_124"},{f:"catalog/其他/藤椒鸭腿XC_125.html",n:"藤椒鸭腿XC_125"}
  ]},
  {p:"GF",n:"裹粉系列",e:"🌾",c:[{f:"catalog/其他/土豆炸鸡粉（子）GF_003.html",n:"土豆炸鸡粉（子）GF_003"},{f:"catalog/其他/炸鸡面糊·鸡蛋牛奶（子）GF_007.html",n:"炸鸡面糊·鸡蛋牛奶（子）GF_007"},{f:"catalog/其他/米粉炸鸡粉（子）GF_004.html",n:"米粉炸鸡粉（子）GF_004"},{f:"catalog/其他/美式炸鸡裹粉（子）GF_006.html",n:"美式炸鸡裹粉（子）GF_006"},{f:"catalog/其他/脆皮炸鸡粉（子）GF_002.html",n:"脆皮炸鸡粉（子）GF_002"},{f:"catalog/其他/韩式核心炸粉·阿嬷版（子）GF_005.html",n:"韩式核心炸粉·阿嬷版（子）GF_005"},
    {f:"catalog/其他/GF_001 韩式核心炸粉（母）.html",n:"GF_001 韩式核心炸粉（母）"}]},
  {p:"FL",n:"粉料系列",e:"🌶️",c:[{f:"catalog/其他/初雪雪翼芝士粉（子）FL_001.html",n:"初雪雪翼芝士粉（子）FL_001"},{f:"catalog/其他/咖喱芝士粉（子）FL_002.html",n:"咖喱芝士粉（子）FL_002"},{f:"catalog/其他/孜然撒粉（子）FL_004.html",n:"孜然撒粉（子）FL_004"},{f:"catalog/其他/红辣椒撒粉（子）FL_003.html",n:"红辣椒撒粉（子）FL_003"},{f:"catalog/其他/黑胡椒撒粉（子）FL_005.html",n:"黑胡椒撒粉（子）FL_005"}]},
  {p:"KS",n:"韩式小吃",e:"🥟",c:[{f:"catalog/其他/石锅拌饭（母）KS_004.html",n:"石锅拌饭（母）KS_004"},{f:"catalog/其他/韩式炒年糕（母）KS_001.html",n:"韩式炒年糕（母）KS_001"},{f:"catalog/其他/韩式炸蔬菜（母）KS_002.html",n:"韩式炸蔬菜（母）KS_002"},{f:"catalog/其他/韩式炸酱面（母）KS_003.html",n:"韩式炸酱面（母）KS_003"},{f:"catalog/其他/鱿鱼石锅拌饭（子）KS_005.html",n:"鱿鱼石锅拌饭（子）KS_005"}]},
  {p:"LM",n:"柠檬系列",e:"🍋",c:[{f:"catalog/其他/气泡柠檬茶（母）LM_004.html",n:"气泡柠檬茶（母）LM_004"},{f:"catalog/其他/经典手打柠檬茶（母）LM_001.html",n:"经典手打柠檬茶（母）LM_001"},{f:"catalog/其他/蜂蜜柠檬茶（母）LM_003.html",n:"蜂蜜柠檬茶（母）LM_003"},{f:"catalog/其他/香水柠檬茶（母）LM_002.html",n:"香水柠檬茶（母）LM_002"},
    {f:"catalog/其他/LM_005 手打渣男绿（子）.html",n:"LM_005 手打渣男绿（子）"},
    {f:"catalog/其他/LM_007 蜂蜜柠檬茶·浓醇版（子）.html",n:"LM_007 蜂蜜柠檬茶·浓醇版（子）"},
    {f:"catalog/其他/LM_011 百香果柠檬茶（子）.html",n:"LM_011 百香果柠檬茶（子）"}]},
  {p:"GC",n:"果茶系列",e:"🫐",c:[{f:"catalog/其他/白桃乌龙茶（母）GC_002.html",n:"白桃乌龙茶（母）GC_002"},{f:"catalog/其他/百香果冰茶（母）GC_001.html",n:"百香果冰茶（母）GC_001"},{f:"catalog/其他/葡萄冰茶（母）GC_003.html",n:"葡萄冰茶（母）GC_003"}]},
  {p:"JL_",n:"韩式酱料（单品）",e:"🧂",c:[{f:"catalog/其他/伍斯特酱汁（子）JL_011.html",n:"伍斯特酱汁（子）JL_011"},{f:"catalog/其他/全罗道秘酱火辣熟酱（子）JL_002.html",n:"全罗道秘酱火辣熟酱（子）JL_002"},{f:"catalog/其他/忠武路芝士芥末双流酱（子）JL_005.html",n:"忠武路芝士芥末双流酱（子）JL_005"},{f:"catalog/其他/杰克丹尼酱汁（子）JL_012.html",n:"杰克丹尼酱汁（子）JL_012"},{f:"catalog/其他/果酱·苹果酱（子）JL_013.html",n:"果酱·苹果酱（子）JL_013"},{f:"catalog/其他/特甜酱（子）JL_006.html",n:"特甜酱（子）JL_006"},{f:"catalog/其他/猕猴桃酱汁（子）JL_007.html",n:"猕猴桃酱汁（子）JL_007"},{f:"catalog/其他/石锅拌饭酱（子）JL_017.html",n:"石锅拌饭酱（子）JL_017"},{f:"catalog/其他/糖醋蜜汁酱（子）JL_015.html",n:"糖醋蜜汁酱（子）JL_015"},{f:"catalog/其他/经典甜辣炸鸡酱（子）JL_001.html",n:"经典甜辣炸鸡酱（子）JL_001"},{f:"catalog/其他/芝士牛乳酱（子）JL_008.html",n:"芝士牛乳酱（子）JL_008"},{f:"catalog/其他/蒜香酱油酱（子）JL_016.html",n:"蒜香酱油酱（子）JL_016"},{f:"catalog/其他/蜂蜜芥末酱·简易版（子）JL_014.html",n:"蜂蜜芥末酱·简易版（子）JL_014"},{f:"catalog/其他/辣拌海螺酱料（子）JL_019.html",n:"辣拌海螺酱料（子）JL_019"},{f:"catalog/其他/酸奶酱（子）JL_003.html",n:"酸奶酱（子）JL_003"},{f:"catalog/其他/雪花柠檬酱（子）JL_009.html",n:"雪花柠檬酱（子）JL_009"},{f:"catalog/其他/韩式辣白菜酱（子）JL_018.html",n:"韩式辣白菜酱（子）JL_018"},{f:"catalog/其他/首尔蜂蜜黄芥末酱（子）JL_004.html",n:"首尔蜂蜜黄芥末酱（子）JL_004"}]},
  {p:"KF_",n:"韩式汤/主食（单品）",e:"🍲",c:[{f:"catalog/其他/摩卡咖啡（母）KF_003.html",n:"摩卡咖啡（母）KF_003"},{f:"catalog/其他/桂花拿铁（母）KF_009.html",n:"桂花拿铁（母）KF_009"},{f:"catalog/其他/桂花酒酿拿铁（母）KF_013.html",n:"桂花酒酿拿铁（母）KF_013"},{f:"catalog/其他/椰云拿铁（母）KF_006.html",n:"椰云拿铁（母）KF_006"},{f:"catalog/其他/樱花拿铁（母）KF_011.html",n:"樱花拿铁（母）KF_011"},{f:"catalog/其他/油柑美式（母）KF_007.html",n:"油柑美式（母）KF_007"},{f:"catalog/其他/焦糖玛奇朵（母）KF_004.html",n:"焦糖玛奇朵（母）KF_004"},{f:"catalog/其他/生椰拿铁（母）KF_005.html",n:"生椰拿铁（母）KF_005"},{f:"catalog/其他/经典拿铁（母）KF_002.html",n:"经典拿铁（母）KF_002"},{f:"catalog/其他/美式咖啡（母）KF_001.html",n:"美式咖啡（母）KF_001"},{f:"catalog/其他/草莓拿铁（母）KF_012.html",n:"草莓拿铁（母）KF_012"},{f:"catalog/其他/黄皮美式（母）KF_008.html",n:"黄皮美式（母）KF_008"},{f:"catalog/其他/黑糖燕麦拿铁（母）KF_010.html",n:"黑糖燕麦拿铁（母）KF_010"}]},
  {p:"PC_",n:"韩式拌菜（单品）",e:"🥬",c:[{f:"catalog/其他/卷心菜沙拉（子）PC_002.html",n:"卷心菜沙拉（子）PC_002"},{f:"catalog/其他/原味饭团（子）PC_006.html",n:"原味饭团（子）PC_006"},{f:"catalog/其他/圆白菜丝·紫甘蓝丝（子）PC_003.html",n:"圆白菜丝·紫甘蓝丝（子）PC_003"},{f:"catalog/其他/肉松饭团（子）PC_007.html",n:"肉松饭团（子）PC_007"},{f:"catalog/其他/辣拌海螺（子）PC_005.html",n:"辣拌海螺（子）PC_005"},{f:"catalog/其他/酸辣白萝卜（子）PC_004.html",n:"酸辣白萝卜（子）PC_004"},{f:"catalog/其他/金枪鱼饭团（子）PC_008.html",n:"金枪鱼饭团（子）PC_008"},{f:"catalog/其他/韩式酸甜脆白萝卜（子）PC_001.html",n:"韩式酸甜脆白萝卜（子）PC_001"}]}];

// ===== 渲染函数 =====

// 识别卡类型
function getCardTag(name) {
  if (name.indexOf('（母）') > -1 || name.indexOf('(母)') > -1 || name.indexOf('母卡') > -1) return '母';
  if (name.indexOf('（子）') > -1 || name.indexOf('(子)') > -1) return '子';
  return '';
}
function getCardTagColor(tag) {
  if (tag === '母') return '#C0392B';
  if (tag === '子') return '#E8652D';
  return '#999';
}

// 根据卡片名称配不同图标（支持双emoji：主料+口味）
function getCardEmoji(name) {
  var map = [
    ['鸡','🐔'],['鸭','🦆'],['鹅','🦆'],['牛','🐮'],['猪','🐷'],
    ['鱼','🐟'],['虾','🦐'],['蟹','🦀'],['螺','🐚'],['蛙','🐸'],
    ['辣','🌶️'],['麻辣','🌶️'],['藤椒','🌿'],
    ['冰','🧊'],['茶','🍵'],['奶','🥛'],
    ['咖啡','☕'],['拿铁','☕'],['美式','☕'],['可可','🍫'],
    ['包','🥟'],['饺','🥟'],['锅贴','🥟'],['煎','🍳'],
    ['饼','🫓'],['馍','🫓'],['烧饼','🫓'],
    ['面','🍜'],['粉','🍜'],['米线','🍜'],
    ['饭','🍚'],['粥','🥣'],['汤','🥣'],
    ['炸','🍤'],['天妇罗','🍤'],['烤','🔥'],
    ['酱','🫙'],['蘸','🧂'],
    ['串','🍢'],['肠','🌭'],
    ['肉','🥩'],['骨','🦴'],['爪','🐔'],['脚','🐔'],
    ['豆','🫘'],['腐竹','🫘'],['藕','🥔'],['土豆','🥔'],
    ['果','🍎'],['莓','🍓'],['芒','🥭'],['橙','🍊'],
    ['椰','🥥'],['荔','🫐'],['柠','🍋'],['桃','🍑'],
    ['葡','🍇'],['梅','🍒'],['杏','🍑'],
    ['酒','🍶'],['花','🌸'],['桂','🌼'],['茉','🌿'],
    ['菜','🥬'],['蔬','🥦'],['卷','🥗'],
    ['蛋','🥚'],['丸','⚪'],
    ['脆','✨'],['酥','✨'],['蜜','🍯'],['甜','🍯'],
    ['酸','🍋'],['香','🌿'],
    ['糯','🍡'],['麻薯','🍡'],['芋','🟣'],['薯','🍠'],
    ['鲍','🐚'],['参','🌿'],['翅','🪽']
  ];
  var found = [];
  // 优先匹配长关键词（避免"柠"匹配到"柠檬"+前缀重复）
  var priorityKeys = ['麻辣','麻薯','天妇罗','锅贴','米线','烧饼','腐竹','烧鸡','拿铁','美式','烧肉','牛肉','猪肉','鸡肉','鸭肉','鱼饼','柠檬','冰茶','奶茶','蜜汁','酱香','藤椒','蒜香'];
  for (var pi = 0; pi < priorityKeys.length; pi++) {
    if (name.indexOf(priorityKeys[pi]) > -1) {
      // 找到对应emoji
      for (var mj = 0; mj < map.length; mj++) {
        if (map[mj][0] === priorityKeys[pi]) {
          found.push(map[mj][1]);
          break;
        }
      }
    }
  }
  // 再扫普通匹配
  for (var i = 0; i < map.length; i++) {
    if (name.indexOf(map[i][0]) > -1) {
      if (found.indexOf(map[i][1]) === -1) {
        found.push(map[i][1]);
      }
      if (found.length >= 2) break; // 最多两个emoji
    }
  }
  return found.length > 0 ? found.join('') : '';
}

// ===== 门店决策卡：列表模式 =====
function renderStoreCards(id, data, exp) {
  var el = document.getElementById(id);
  if (!el) return;
  var html = '<div class="cat-list">';
  data.forEach(function(d) {
    var h = '<div class="cat-card">';
    h += '<div class="cc-header" onclick="var b=this.nextElementSibling;b.classList.toggle(\'hide\');var a=this.querySelector(\'.cc-arrow\');a.style.transform=a.style.transform===\'rotate(180deg)\'?\'rotate(0deg)\':\'rotate(180deg)\'">';
    h += '<span class="cc-emoji">' + d.e + '</span>';
    h += '<span class="cc-name">' + d.n + '</span>';
    h += '<span class="cc-count">' + d.c.length + '张</span>';
    h += '<span class="cc-arrow">&#9660;</span>';
    h += '</div><div class="cc-body">';
    h += '<div class="list-grid">';
    d.c.forEach(function(c) {
      var tag = getCardTag(c.n);
      var tagColor = getCardTagColor(tag);
      var tagHtml = tag ? '<span class="list-tag" style="background:' + tagColor + '">' + tag + '</span>' : '';
      h += '<a class="list-card" href="' + c.f + '">' + tagHtml + '<span class="list-name">' + c.n + '</span><span class="list-arrow">›</span></a>';
    });
    h += '</div></div></div>';
    html += h;
  });
  html += '</div>';
  el.innerHTML = html;
}

// ===== 地摊产品卡：图标模式（多元化图标） =====
function renderStallCards(id, data) {
  var el = document.getElementById(id);
  if (!el) return;
  var html = '<div class="cat-list">';
  data.forEach(function(d) {
    var h = '<div class="cat-card">';
    h += '<div class="cc-header" onclick="var b=this.nextElementSibling;b.classList.toggle(\'hide\');var a=this.querySelector(\'.cc-arrow\');a.style.transform=a.style.transform===\'rotate(180deg)\'?\'rotate(0deg)\':\'rotate(180deg)\'">';
    h += '<span class="cc-emoji">' + d.e + '</span>';
    h += '<span class="cc-name">' + d.n + '</span>';
    h += '<span class="cc-count">' + d.c.length + '张</span>';
    h += '<span class="cc-arrow">&#9660;</span>';
    h += '</div><div class="cc-body">';
    h += '<div class="icon-grid">';
    d.c.forEach(function(c) {
      var tag = getCardTag(c.n);
      var isFree = c.n.indexOf('免费') > -1 || c.n.indexOf('free') > -1;
      var shortName = c.n.replace(/（[^）]*）/g, '').replace(/\([^)]*\)/g, '').replace(/^[A-Z0-9_]+\\s*/, '').trim();
      if (shortName.length > 8) shortName = shortName.slice(0, 7) + '…';
      var cardEmoji = getCardEmoji(c.n) || d.e;
      var tagColor = getCardTagColor(tag);
      var lockTag = isFree ? '' : '<div class="icon-card-lock" style="position:absolute;top:-4px;left:-4px;font-size:9px;background:#e8a060;color:#fff;width:16px;height:16px;border-radius:50%;display:flex;align-items:center;justify-content:center">🔒</div>';
      h += '<a class="icon-card" href="' + c.f + '">' + lockTag;
      h += '<div class="icon-card-emoji">' + cardEmoji + '</div>';
      h += '<div class="icon-card-name">' + shortName + '</div>';
      if (tag) h += '<div class="icon-card-tag" style="background:' + tagColor + '">' + tag + '</div>';
      h += '</a>';
    });
    h += '</div></div></div>';
    html += h;
  });
  html += '</div>';
  el.innerHTML = html;
}

document.addEventListener('DOMContentLoaded', function() {
  renderStoreCards('storeCards', STORE_DATA);
  renderStallCards('stallCards', STALL_DATA);
});