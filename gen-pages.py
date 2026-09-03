# -*- coding: utf-8 -*-
"""根据作品数据生成详情页 work-01~13.html 和 works.html（列表页）"""
import io, os

BASE = os.path.dirname(os.path.abspath(__file__))

# nn, 文件名, 标题, 类别key, 类别标签, 横屏h/竖屏v, 时长秒, 王牌, 背景注, 数据注
WORKS = [
    ("01", "冰箱贴",     "冰箱贴",       "ad",     "信息流广告", "v", 23,  False, "信息流投放素材", ""),
    ("02", "防水包",     "防水包",       "ad",     "信息流广告", "v", 30,  False, "信息流投放素材", ""),
    ("03", "京东外卖",   "京东外卖",     "hot",    "热点视频",   "v", 306, True, "热点跟拍", "播放 8 万+"),
    ("04", "魔术布",     "魔术布",       "ad",     "信息流广告", "v", 14,  False, "信息流投放素材", ""),
    ("05", "千岛湖快闪", "千岛湖快闪",   "brand",  "品牌宣传片", "h", 30,  False, "品牌快闪活动片", ""),
    ("06", "手机防水袋", "手机防水袋",   "ad",     "信息流广告", "v", 32,  False, "信息流投放素材", ""),
    ("07", "铁三角",     "铁三角",       "persona","人设视频",   "h", 550, True, "人设长片", ""),
    ("08", "线下课（终）","线下课",      "brand",  "品牌宣传片", "h", 71,  False, "线下课程宣传", ""),
    ("09", "行李牌",     "行李牌",       "ad",     "信息流广告", "v", 18,  False, "信息流投放素材", ""),
    ("10", "宣传片",     "品牌宣传片",   "brand",  "品牌宣传片", "h", 26,  False, "品牌宣传", ""),
    ("11", "一个人拍vlog","一个人拍VLOG","koubo",  "口播视频",   "v", 170, False, "IP 口播 VLOG", ""),
    ("12", "真人声音4",  "真人声音",     "hot",    "热点视频",   "v", 24,  False, "达人热点素材", ""),
    ("13", "职场故事2.0","职场故事",     "persona","人设视频",   "v", 215, True, "职场人设系列", "播放 2 万+"),
]

def dur_text(sec):
    if sec < 60: return f"{sec} 秒"
    return f"{sec // 60} 分 {sec % 60:02d} 秒"

NAV = """  <header class="navbar">
    <div class="container navbar-inner">
      <a href="index.html" class="logo">薛博<em>.</em></a>
      <nav class="nav-links" id="navLinks">
        <a href="index.html">首页</a>
        <a href="works.html" class="active">作品</a>
        <a href="about.html">关于我</a>
        <a href="index.html#contact">联系</a>
      </nav>
      <button id="menuToggle" class="menu-toggle" aria-label="打开菜单">☰</button>
    </div>
  </header>"""

FOOTER = """  <footer class="footer">
    <div class="container">© 2026 薛博 · 摄像 / 剪辑师 · 求职作品集</div>
  </footer>"""

def detail_page(nn, fname, title, ckey, clabel, orient, sec, star, bg, data):
    idx = int(nn) - 1
    prev = WORKS[idx - 1] if idx > 0 else None
    next_ = WORKS[idx + 1] if idx < len(WORKS) - 1 else None
    wrap_cls = "player-wrap vertical" if orient == "v" else "player-wrap"
    orient_tag = "竖屏" if orient == "v" else "横屏 16:9"
    star_tag = '<span class="tag hl">★ 王牌作品</span>' if star else ""
    prev_link = f'<a href="work-{prev[0]}.html">← 上一个作品：{prev[2]}</a>' if prev else '<a href="works.html">← 返回作品列表</a>'
    next_link = f'<a href="work-{next_[0]}.html">下一个作品：{next_[2]} →</a>' if next_ else '<a href="works.html">返回作品列表 →</a>'
    data_v = data if data else "播放量 / 转化等数据（可后续补充）"
    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{title} · {clabel} | 薛博作品集</title>
  <meta name="description" content="{title}——薛博作品集：{clabel}案例，{bg}，拍摄剪辑全流程，片长{dur_text(sec)}。" />
  <link rel="icon" type="image/png" href="assets/favicon.png" />
  <link rel="stylesheet" href="style.css" />
</head>
<body>

{NAV}

  <main class="work-page">
    <div class="container">
      <a href="works.html" class="back-link">← 返回作品列表</a>

      <div class="work-head">
        <h1>{title}</h1>
        <div class="work-tags">
          <span class="tag hl">{clabel}</span>
          <span class="tag">{orient_tag}</span>
          <span class="tag">片长 {dur_text(sec)}</span>
          {star_tag}
        </div>
      </div>

      <div class="{wrap_cls}">
        <video controls playsinline preload="metadata"
                poster="assets/poster-{nn}.jpg" src="videos/work-{nn}.mp4"></video>
      </div>

      <!-- 四个关键信息卡 -->
      <div class="facts">
        <div class="fact">
          <div class="k">项目背景</div>
          <div class="v">{bg}。</div>
        </div>
        <div class="fact">
          <div class="k">我的角色</div>
          <div class="v">拍摄 + 剪辑全流程，本条由我独立完成。</div>
        </div>
        <div class="fact">
          <div class="k">设备与软件</div>
          <div class="v">索尼 A7M3 / A7M4 / FX3 · Premiere / 达芬奇。</div>
        </div>
        <div class="fact">
          <div class="k">成果数据</div>
          <div class="v">{data_v}。</div>
        </div>
      </div>

      <div class="work-story">
        <h2>这条片子做了什么</h2>
        <p>{bg}——具体项目背景可后续补充。</p>
        <h2>我怎么做</h2>
        <p>从前期拍摄（构图、布光、运镜、收音）到后期剪辑、调色、成片，我一个人完成全流程。</p>
      </div>

      <div class="work-nav">
        {prev_link}
        {next_link}
      </div>
    </div>
  </main>

{FOOTER}

  <script src="main.js"></script>
</body>
</html>
"""

def card(nn, fname, title, ckey, clabel, orient, sec, star, bg, data):
    star_mark = " ★" if star else ""
    data_txt = f" · {data}" if data else ""
    return f"""        <a href="work-{nn}.html" class="work-card fade-in" data-cat="{ckey}">
          <div class="work-thumb">
            <img class="thumb-img" src="assets/thumb-{nn}.jpg" alt="{title}封面" />
            <span class="thumb-cat">{clabel}{star_mark}</span>
          </div>
          <div class="work-body">
            <h3>{title}</h3>
            <p>拍+剪全流程 · {bg}{data_txt} · 片长 {dur_text(sec)}。</p>
            <span class="work-more">查看详情 →</span>
          </div>
        </a>
"""

CHIPS = [
    ("all", "全部"), ("ad", "信息流广告"), ("persona", "人设视频"),
    ("hot", "热点视频"), ("brand", "品牌宣传片"), ("koubo", "口播视频"),
]

def works_page():
    cards = "\n".join(card(*w) for w in WORKS)
    chips = "\n".join(
        f'        <button class="filter-chip{" active" if k == "all" else ""}" data-filter="{k}">{label}</button>'
        for k, label in CHIPS)
    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>作品列表 | 薛博 · 摄像剪辑师</title>
  <meta name="description" content="薛博的作品集：信息流广告、人设视频、热点视频、品牌宣传片、口播，共13条精选作品。" />
  <link rel="icon" type="image/png" href="assets/favicon.png" />
  <link rel="stylesheet" href="style.css" />
</head>
<body>

{NAV}

  <main class="work-page">
    <div class="container">
      <a href="index.html" class="back-link">← 返回首页</a>

      <div class="work-head">
        <h1>作品列表</h1>
        <p class="section-lead">5 年里的 13 条代表作，标 ★ 的是最拿得出手的三条。点开任意一条可看视频和项目介绍。</p>
      </div>

      <div class="filter-bar" id="filterBar">
{chips}
      </div>

      <div class="work-grid" id="workGrid">
{cards}      </div>
    </div>
  </main>

{FOOTER}

  <script src="main.js"></script>
</body>
</html>
"""

os.chdir(BASE)
for w in WORKS:
    with io.open(f"work-{w[0]}.html", "w", encoding="utf-8") as f:
        f.write(detail_page(*w))
    print(f"work-{w[0]}.html 生成")
with io.open("works.html", "w", encoding="utf-8") as f:
    f.write(works_page())
print("works.html 生成（13 张卡片 + 筛选）")
