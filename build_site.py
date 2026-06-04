#!/usr/bin/env python3
"""Build the Chinese reading guide site for The Book of Elon."""
from __future__ import annotations

import html
from pathlib import Path

ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / "index.html"
FREE_BOOK_URL = "https://www.elonmuskbook.org/free-book-of-elon-musk"
ONLINE_BOOK_URL = "https://www.elonmuskbook.org/the-book-of-elon-free-online-edition"
AUTHOR_URL = "https://www.ejorgenson.com/"

BOOK = [
    ("导读", "Opening", "先理解这本书的读法：它不是传记，而是从访谈、推文、演讲中整理出的行动原则。", [
        ("阅读说明", "Notes on This Book", 15, "把本书当作思想索引，而不是逐字引用来源。正式引用前应回到原文和一手材料核对。"),
        ("序言", "Foreword", 17, "少谈人物崇拜，多看如何把使命、速度、工程能力和组织执行力合在一起。"),
        ("作者欢迎辞", "Eric's Welcome to This Book", 21, "作者解释选材和编排方法，帮助读者从公开表达中抽取可复用的思维模型。"),
    ]),
    ("第一部分：追求使命", "Part I: Pursue Purpose", "使命感不是口号，而是把个人精力压到长期问题上的选择。", [
        ("有使命地生活", "Living a Purposeful Life", 31, "把“有用”放在自我表达之前：持续创造、承受恐惧、在世界还没准备好时提前开始。"),
        ("像物理学家一样思考", "Think Like a Physicist", 53, "回到第一性原理、逼近真实、用极限思维拆解看似不可能的目标，并不断修正自己。"),
        ("工程的价值", "The Value of Engineering", 73, "工程把想法变成世界变化，也决定竞争中的生死速度。"),
    ]),
    ("第二部分：极硬核工作", "Part II: Ultra Hardcore Work", "责任、团队、组织设计、速度和制造，是把使命变成现实的五个杠杆。", [
        ("需要什么", "What It Takes", 85, "真正承担责任意味着深入一线、理解细节、在痛苦和不确定里继续前进。"),
        ("打造卓越团队", "Building Exceptional Teams", 99, "团队不是人群，而是围绕目标组织起来的能力密度。文化要偏向建造者、反馈和高标准。"),
        ("设计组织", "Designing the Organization", 111, "组织复杂度会吞掉速度：先删减、再优化、最后自动化。"),
        ("疯狂紧迫感", "Maniacal Urgency", 139, "速度既是进攻也是防守。用激进时间表暴露约束，再围绕约束快速迭代。"),
        ("我们必须制造东西", "We Must Make Stuff", 151, "制造不是执行尾声，而是护城河本身。工厂、供应链和产能决定愿景能否落地。"),
    ]),
    ("第三部分：创建公司", "Part III: Building Companies", "Zip2、PayPal、Tesla、SpaceX 展示了方法如何落地：连续 all-in，连续纠错。", [
        ("成为创始人", "Becoming a Founder", 163, "看创始人在错误、冲突、融资和失控局面中如何快速修正。"),
        ("建造 Tesla", "Building Tesla", 187, "大型硬科技公司需要同时处理技术、制造、舆论和资本。"),
        ("建造 SpaceX", "Building SpaceX", 219, "预期会失败，但失败必须带来学习；目标是把几乎不可能的事压到刚好可行。"),
    ]),
    ("第四部分：代表人类", "Part IV: On Behalf of Humanity", "把视角拉到文明尺度：公司、丰裕、风险和多行星未来。", [
        ("建造我们的未来", "Building Our Future", 251, "公司可以是推动进步的工具：创造财富、组织人才、扩大问题解决能力。"),
        ("丰裕时代", "The Age of Abundance", 265, "稀缺、指数级智能、人机接口、自动驾驶和可持续能源共同构成未来图景。"),
        ("我们的生存风险", "Our Existential Risks", 283, "把战争、能源、AI 对齐、人口下降和小行星纳入长期行动优先级。"),
        ("成为多行星物种", "Becoming Multiplanetary", 311, "多行星是文明级备份和生命扩展：火星是入口，目标是让生命走出地球脆弱性。"),
    ]),
    ("附录", "Bonus", "附录适合当作速查表：方法、时间线、推荐阅读和来源。", [
        ("69 条 Musk 核心方法", "The 69 Core Musk Methods", 335, "把全书方法浓缩成清单，适合做复盘或团队讨论。"),
        ("Elon Musk 时间线", "Timeline of Elon Musk", 339, "把章节主题重新放回创业和技术发展的历史脉络。"),
        ("Elon 推荐阅读", "Elon's Recommended Reading", 343, "书单揭示了他的知识输入结构：科幻、物理、工程、商业和文明史。"),
        ("来源与致谢", "Sources and Appreciation", 357, "严肃引用仍应回到原访谈、演讲或推文。"),
    ]),
]

KEYWORDS = ["第一性原理", "制造能力", "组织速度"]


def e(value: object) -> str:
    return html.escape(str(value), quote=True)


def render_nav() -> str:
    return "\n".join(
        f'<a href="#part-{i}"><span>{i:02d}</span>{e(part[0])}</a>'
        for i, part in enumerate(BOOK, 1)
    )


def render_card(chapter: tuple[object, ...], i: int) -> str:
    title, title_en, page, summary = chapter
    items = "".join(f"<li>{e(word)}</li>" for word in KEYWORDS)
    return f"""<article class="chapter-card">
      <div class="chapter-meta"><span>{i:02d}</span><span>p. {e(page)}</span></div>
      <h3>{e(title)}</h3><p class="chapter-en">{e(title_en)}</p>
      <p>{e(summary)}</p><ul>{items}</ul>
    </article>"""


def render_part(part: tuple[object, ...], i: int) -> str:
    title, title_en, intro, chapters = part
    cards = "\n".join(render_card(chapter, n) for n, chapter in enumerate(chapters, 1))
    return f"""<section class="part-section" id="part-{i}">
      <div class="part-heading"><p class="eyebrow">{e(title_en)}</p><h2>{e(title)}</h2><p>{e(intro)}</p></div>
      <div class="chapter-grid">{cards}</div>
    </section>"""


def main() -> None:
    parts = "\n".join(render_part(part, i) for i, part in enumerate(BOOK, 1))
    count = sum(len(part[3]) for part in BOOK)
    html_doc = f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>埃隆之书中文导读 | The Book of Elon</title>
  <meta name="description" content="The Book of Elon 中文导读阅读站：按章节整理使命、工程、组织、速度、公司和人类未来等主题。">
  <link rel="canonical" href="https://elon.codex55.lol/">
  <link rel="stylesheet" href="assets/styles.css">
</head>
<body>
  <header class="site-hero">
    <nav class="topbar" aria-label="顶部导航">
      <a class="brand" href="#top">The Book of Elon</a>
      <div><a href="#chapters">章节</a><a href="{FREE_BOOK_URL}" rel="noopener noreferrer">免费 PDF</a><a href="{AUTHOR_URL}" rel="noopener noreferrer">作者</a></div>
    </nav>
    <div class="hero-grid" id="top">
      <div class="hero-copy">
        <p class="eyebrow">中文阅读导读</p>
        <h1>埃隆之书</h1>
        <p class="lead">把 Eric Jorgenson 编纂的 <em>The Book of Elon</em> 整理成中文阅读地图：先抓住章节结构、核心方法和行动线索，再回到官方免费全文深入阅读。</p>
        <div class="hero-actions"><a class="primary-action" href="#chapters">开始阅读</a><a href="{ONLINE_BOOK_URL}" rel="noopener noreferrer">官方在线版</a></div>
      </div>
      <aside class="pattern-panel" aria-label="阅读方法"><p>使命 -> 第一性原理 -> 高密度团队 -> 制造能力 -> 文明尺度</p><span>本页是中文导读和章节索引，不替代原书。完整内容请阅读作者提供的免费在线版或 PDF。</span></aside>
    </div>
  </header>
  <main class="reader-shell" id="chapters">
    <aside class="toc" aria-label="文章目录"><p class="toc-title">目录</p><div class="toc-links">{render_nav()}</div><p class="toc-note">{count} 个阅读节点 · 401 页原书</p></aside>
    <article class="article">
      <section class="source-box"><p class="source-note">来源说明</p><h2>先读地图，再回到原书</h2><p>本页根据用户提供的免费 PDF 目录结构制作中文导读，并链接到作者公开提供的免费在线版与 PDF 入口。原书版权归 Eric Jorgenson 所有；正式引用请回到原文和一手来源核对。</p><div class="source-actions"><a href="{FREE_BOOK_URL}" rel="noopener noreferrer">获取官方免费 PDF/EPUB</a><a href="{ONLINE_BOOK_URL}" rel="noopener noreferrer">阅读官方在线全文</a></div></section>
      {parts}
    </article>
  </main>
  <script src="assets/book.js"></script>
</body>
</html>
"""
    OUTPUT.write_text(html_doc, encoding="utf-8")
    print(f"Wrote {OUTPUT}")


if __name__ == "__main__":
    main()
