#!/usr/bin/env python3
"""Build the Learn Claude Code Chinese reading site."""
from __future__ import annotations

import html
import re
import urllib.error
import urllib.request
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
CHAPTER_DATA = DATA / "chapters"
SOURCE = DATA / "readme-zh.md"
OUTPUT = ROOT / "index.html"
SOURCE_URL = "https://github.com/shareAI-lab/learn-claude-code/blob/main/README-zh.md"
RAW_ROOT = "https://raw.githubusercontent.com/shareAI-lab/learn-claude-code/main"
RAW_URL = f"{RAW_ROOT}/README-zh.md"
SITE_URL = "https://learn-claude-code.codex55.lol/"

CHAPTERS = [
    {"slug": "s01_agent_loop", "code": "s01", "title": "Agent Loop", "motto": "一个工具 + 一个循环 = 一个 Agent"},
    {"slug": "s02_tool_use", "code": "s02", "title": "Tool Use", "motto": "新工具注册进 dispatch map"},
    {"slug": "s03_permission", "code": "s03", "title": "Permission", "motto": "先划边界，再给自由"},
    {"slug": "s04_hooks", "code": "s04", "title": "Hooks", "motto": "挂在循环上，不写进循环里"},
    {"slug": "s05_todo_write", "code": "s05", "title": "Todo Write", "motto": "没有计划的 agent 走哪算哪"},
    {"slug": "s06_subagent", "code": "s06", "title": "Subagent", "motto": "大任务拆小，每个小任务干净的上下文"},
    {"slug": "s07_skill_loading", "code": "s07", "title": "Skill Loading", "motto": "用到时再加载"},
    {"slug": "s08_context_compact", "code": "s08", "title": "Context Compact", "motto": "上下文总会满，要有办法腾地方"},
    {"slug": "s09_memory", "code": "s09", "title": "Memory", "motto": "记住该记的，忘掉该忘的"},
    {"slug": "s10_system_prompt", "code": "s10", "title": "System Prompt", "motto": "prompt 是组装出来的"},
    {"slug": "s11_error_recovery", "code": "s11", "title": "Error Recovery", "motto": "错误是重试的起点"},
    {"slug": "s12_task_system", "code": "s12", "title": "Task System", "motto": "任务图持久化"},
    {"slug": "s13_background_tasks", "code": "s13", "title": "Background Tasks", "motto": "慢操作丢后台"},
    {"slug": "s14_cron_scheduler", "code": "s14", "title": "Cron Scheduler", "motto": "定时触发，不需要人推"},
    {"slug": "s15_agent_teams", "code": "s15", "title": "Agent Teams", "motto": "一个搞不定，组队来"},
    {"slug": "s16_team_protocols", "code": "s16", "title": "Team Protocols", "motto": "队友之间要有约定"},
    {"slug": "s17_autonomous_agents", "code": "s17", "title": "Autonomous Agents", "motto": "队友自己看板，有活就认领"},
    {"slug": "s18_worktree_isolation", "code": "s18", "title": "Worktree Isolation", "motto": "各干各的目录，互不干扰"},
    {"slug": "s19_mcp_plugin", "code": "s19", "title": "MCP Plugin", "motto": "能力不够，插上 MCP"},
    {"slug": "s20_comprehensive", "code": "s20", "title": "Comprehensive", "motto": "机制很多，循环一个"},
]


def fetch_text(url: str, cache: Path) -> str:
    cache.parent.mkdir(parents=True, exist_ok=True)
    try:
      with urllib.request.urlopen(url, timeout=20) as response:
          text = response.read().decode("utf-8")
      cache.write_text(text, encoding="utf-8")
      return text
    except (urllib.error.URLError, TimeoutError):
      if cache.exists():
          return cache.read_text(encoding="utf-8")
      raise


def slugify(text: str) -> str:
    slug = re.sub(r"[^0-9a-zA-Z\u4e00-\u9fff]+", "-", text.lower()).strip("-")
    return slug or "section"


def unique_slug(text: str, used: dict[str, int]) -> str:
    base = slugify(text)
    used[base] = used.get(base, 0) + 1
    return base if used[base] == 1 else f"{base}-{used[base]}"


def chapter_for_slug(slug: str) -> dict[str, str] | None:
    return next((chapter for chapter in CHAPTERS if chapter["slug"] == slug), None)


def absolute_href(url: str, page_slug: str | None = None) -> str:
    if not url or url.startswith("#"):
        return url
    parsed = urlparse(url)
    if parsed.scheme or url.startswith("mailto:"):
        return url
    if url.startswith("../"):
        target = url.lstrip("./")
        target = target[3:] if target.startswith("../") else target
        maybe_slug = target.strip("/").split("/")[0]
        if chapter_for_slug(maybe_slug):
            return f"/{maybe_slug}/"
        return f"https://github.com/shareAI-lab/learn-claude-code/tree/main/{target.strip('/')}"
    if url.startswith("./"):
        return f"/{url[2:]}"
    if url.endswith(".md"):
        return f"https://github.com/shareAI-lab/learn-claude-code/blob/main/{page_slug or ''}/{url}".replace("//README", "/README")
    return url


def image_src(url: str, page_slug: str | None = None) -> str:
    if urlparse(url).scheme:
        return url
    prefix = f"{page_slug}/" if page_slug else ""
    return f"{RAW_ROOT}/{prefix}{url.lstrip('./')}"


def inline_markdown(text: str, page_slug: str | None = None) -> str:
    placeholders: list[str] = []

    def keep(value: str) -> str:
        token = f"@@TOKEN{len(placeholders)}@@"
        placeholders.append(value)
        return token

    text = html.escape(text, quote=False)
    text = re.sub(r"`([^`]+)`", lambda match: keep(f"<code>{match.group(1)}</code>"), text)
    text = re.sub(r"\*\*(.+?)\*\*", lambda match: keep(f"<strong>{match.group(1)}</strong>"), text)
    text = re.sub(
        r"!\[([^\]]*)\]\(([^)]+)\)",
        lambda match: keep(
            f'<img src="{html.escape(image_src(match.group(2), page_slug), quote=True)}" '
            f'alt="{html.escape(match.group(1), quote=True)}" loading="lazy">'
        ),
        text,
    )
    text = re.sub(
        r"\[([^\]]+)\]\(([^)]+)\)",
        lambda match: keep(
            f'<a href="{html.escape(absolute_href(match.group(2), page_slug), quote=True)}" rel="noopener noreferrer">{match.group(1)}</a>'
        ),
        text,
    )
    text = re.sub(r"(?<!\*)\*([^*\n]+)\*(?!\*)", r"<em>\1</em>", text)
    changed = True
    while changed:
        changed = False
        for index, value in enumerate(placeholders):
            token = f"@@TOKEN{index}@@"
            if token in text:
                text = text.replace(token, value)
                changed = True
    return text


def is_table(lines: list[str], index: int) -> bool:
    if index + 1 >= len(lines):
        return False
    return (
        lines[index].lstrip().startswith("|")
        and lines[index + 1].lstrip().startswith("|")
        and bool(re.search(r"\|\s*:?-{3,}:?\s*\|", lines[index + 1]))
    )


def table_block(lines: list[str], index: int, page_slug: str | None = None) -> tuple[str, int]:
    rows: list[list[str]] = []
    while index < len(lines) and lines[index].lstrip().startswith("|"):
        rows.append([cell.strip() for cell in lines[index].strip().strip("|").split("|")])
        index += 1
    parts = ['<div class="table-wrap"><table>', "<thead><tr>"]
    parts.extend(f"<th>{inline_markdown(cell, page_slug)}</th>" for cell in rows[0])
    parts.append("</tr></thead><tbody>")
    for row in rows[2:]:
        parts.append("<tr>")
        parts.extend(f"<td>{inline_markdown(cell, page_slug)}</td>" for cell in row)
        parts.append("</tr>")
    parts.append("</tbody></table></div>")
    return "\n".join(parts), index


def list_block(lines: list[str], index: int, page_slug: str | None = None) -> tuple[str, int]:
    ordered = bool(re.match(r"\s*\d+\.\s+", lines[index]))
    tag = "ol" if ordered else "ul"
    pattern = r"^\s*\d+\.\s+" if ordered else r"^\s*[-*]\s+"
    items: list[str] = []
    while index < len(lines) and re.match(pattern, lines[index]):
        item = re.sub(pattern, "", lines[index], count=1).strip()
        items.append(f"<li>{inline_markdown(item, page_slug)}</li>")
        index += 1
    return f"<{tag}>\n" + "\n".join(items) + f"\n</{tag}>", index


def paragraph_block(lines: list[str], index: int, page_slug: str | None = None) -> tuple[str, int]:
    parts: list[str] = []
    while index < len(lines):
        line = lines[index]
        if not line.strip():
            break
        if line.startswith("#") or line.startswith("```") or line.startswith(">") or line.strip() == "---":
            break
        if is_table(lines, index) or re.match(r"\s*(?:[-*]|\d+\.)\s+", line):
            break
        parts.append(line.strip())
        index += 1
    return f"<p>{inline_markdown(' '.join(parts), page_slug)}</p>", index


def convert_markdown(markdown: str, page_slug: str | None = None) -> tuple[str, list[dict[str, str]], dict[str, str]]:
    lines = markdown.splitlines()
    html_parts: list[str] = []
    nav: list[dict[str, str]] = []
    used_slugs: dict[str, int] = {}
    meta = {"title": "Learn Claude Code"}
    index = 0
    while index < len(lines):
        line = lines[index]
        if line.strip() in {
            "[English](./README.md) | [中文](./README-zh.md) | [日本語](./README-ja.md)",
            "[中文](README.md) · [English](README.en.md) · [日本語](README.ja.md)",
        }:
            index += 1
            continue
        if not line.strip():
            index += 1
            continue
        if line.strip() == "---":
            html_parts.append('<hr class="section-rule">')
            index += 1
            continue
        if line.strip().startswith(("<details", "</details", "<summary", "</summary")):
            html_parts.append(line.strip())
            index += 1
            continue
        if line.startswith("```"):
            language = line[3:].strip()
            index += 1
            code_lines: list[str] = []
            while index < len(lines) and not lines[index].startswith("```"):
                code_lines.append(lines[index])
                index += 1
            index += 1
            label = html.escape(language or "code")
            html_parts.append(
                f'<figure class="code-block"><figcaption>{label}</figcaption>'
                f"<pre><code>{html.escape(chr(10).join(code_lines))}</code></pre></figure>"
            )
            continue
        if line.lstrip().startswith("!["):
            html_parts.append(f'<figure class="media-figure">{inline_markdown(line.strip(), page_slug)}</figure>')
            index += 1
            continue
        heading = re.match(r"^(#{1,4})\s+(.+)$", line)
        if heading:
            level = len(heading.group(1))
            title = re.sub(r"\s*\(重要\)\s*$", "", heading.group(2).strip())
            title_plain = re.sub(r"[*_`]", "", title)
            section_id = unique_slug(title_plain, used_slugs)
            if level == 1:
                meta["title"] = re.sub(r"\s+--\s+", "：", title_plain)
            elif level in {2, 3}:
                nav.append({"id": section_id, "title": title_plain, "level": str(level)})
            html_parts.append(f'<h{level} id="{section_id}">{inline_markdown(title, page_slug)}</h{level}>')
            index += 1
            continue
        if line.startswith(">"):
            quote_lines: list[str] = []
            while index < len(lines) and lines[index].startswith(">"):
                quote_lines.append(lines[index].lstrip("> ").strip())
                index += 1
            html_parts.append(f"<blockquote><p>{inline_markdown(' '.join(quote_lines), page_slug)}</p></blockquote>")
            continue
        if is_table(lines, index):
            table, index = table_block(lines, index, page_slug)
            html_parts.append(table)
            continue
        if re.match(r"\s*(?:[-*]|\d+\.)\s+", line):
            listing, index = list_block(lines, index, page_slug)
            html_parts.append(listing)
            continue
        paragraph, index = paragraph_block(lines, index, page_slug)
        html_parts.append(paragraph)
    return "\n".join(html_parts), nav, meta


def render_home(article_html: str, nav: list[dict[str, str]], meta: dict[str, str]) -> str:
    nav_items = "\n".join(
        f'<a href="#{item["id"]}"><span>{index:02d}</span>{html.escape(item["title"])}</a>'
        for index, item in enumerate(nav, start=1)
        if item["level"] == "2"
    )
    title = html.escape(meta["title"])
    chapter_cards = "\n".join(
        f'<a class="chapter-card" href="/{chapter["slug"]}/"><span>{chapter["code"]}</span><strong>{chapter["title"]}</strong><small>{chapter["motto"]}</small></a>'
        for chapter in CHAPTERS
    )
    return f"""<!doctype html>
<html lang="zh-CN">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{title}</title>
    <meta name="description" content="Learn Claude Code 中文长文阅读站：真正的 Agent Harness 工程。">
    <link rel="canonical" href="{SITE_URL}">
    <link rel="stylesheet" href="/assets/styles.css">
  </head>
  <body class="home-page">
    <div class="reading-progress" aria-hidden="true"><span></span></div>
    <header class="site-hero">
      <nav class="topbar" aria-label="顶部导航">
        <a class="brand" href="#top">Learn Claude Code</a>
        <div>
          <a href="#chapters">章节</a>
          <a href="/ebooks/learn-claude-code-zh.epub" download>电子书</a>
          <a href="{SOURCE_URL}" rel="noopener noreferrer">GitHub 原文</a>
        </div>
      </nav>
      <div class="hero-grid" id="top">
        <div class="hero-copy">
          <p class="eyebrow">中文阅读站</p>
          <h1>{title}</h1>
          <p class="lead">把 shareAI-lab 的中文课程整理成适合连续阅读的静态网页：目录常驻、正文窄栏、代码块和表格保持清晰。</p>
          <div class="hero-actions">
            <a class="primary-action" href="/s01_agent_loop/">从 s01 开始</a>
            <a href="/ebooks/learn-claude-code-zh.epub" download>下载 EPUB</a>
            <a href="#chapters">浏览 20 章</a>
          </div>
        </div>
        <aside class="pattern-panel" aria-label="核心公式">
          <p>Harness = Tools + Knowledge + Observation + Action Interfaces + Permissions</p>
          <span>模型做决策，Harness 提供行动空间。</span>
        </aside>
      </div>
    </header>
    <main class="reader-shell">
      <aside class="toc" aria-label="文章目录">
        <p class="toc-title">目录</p>
        <div class="toc-links">{nav_items}</div>
      </aside>
      <article class="article">
        <p class="source-note">来源：<a href="{SOURCE_URL}" rel="noopener noreferrer">shareAI-lab/learn-claude-code README-zh.md</a></p>
        <section class="chapter-index" id="chapters" aria-label="章节索引">
          <h2>全部章节</h2>
          <div class="chapter-grid">{chapter_cards}</div>
        </section>
        {article_html}
      </article>
    </main>
    <script src="/assets/book.js"></script>
  </body>
</html>
"""


def render_chapter(
    chapter: dict[str, str],
    article_html: str,
    nav: list[dict[str, str]],
    meta: dict[str, str],
    previous_chapter: dict[str, str] | None,
    next_chapter: dict[str, str] | None,
) -> str:
    nav_items = "\n".join(
        f'<a class="level-{item["level"]}" href="#{item["id"]}"><span>{index:02d}</span>{html.escape(item["title"])}</a>'
        for index, item in enumerate(nav, start=1)
    )
    chapter_links = "\n".join(
        f'<a class="{"is-current" if item["slug"] == chapter["slug"] else ""}" href="/{item["slug"]}/"><span>{item["code"]}</span>{item["title"]}</a>'
        for item in CHAPTERS
    )
    previous_link = (
        f'<a class="page-link" href="/{previous_chapter["slug"]}/"><span>上一章</span><strong>{previous_chapter["code"]} {previous_chapter["title"]}</strong></a>'
        if previous_chapter
        else '<span class="page-link is-disabled"><span>上一章</span><strong>这是第一章</strong></span>'
    )
    next_link = (
        f'<a class="page-link is-next" href="/{next_chapter["slug"]}/"><span>下一章</span><strong>{next_chapter["code"]} {next_chapter["title"]}</strong></a>'
        if next_chapter
        else '<span class="page-link is-disabled"><span>下一章</span><strong>已经读完</strong></span>'
    )
    title = html.escape(meta["title"])
    return f"""<!doctype html>
<html lang="zh-CN">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{title} · Learn Claude Code</title>
    <meta name="description" content="{html.escape(chapter["motto"])}">
    <link rel="canonical" href="{SITE_URL}{chapter["slug"]}/">
    <link rel="stylesheet" href="/assets/styles.css">
  </head>
  <body class="chapter-page">
    <div class="reading-progress" aria-hidden="true"><span></span></div>
    <header class="chapter-top">
      <nav class="topbar" aria-label="顶部导航">
        <a class="brand" href="/">Learn Claude Code</a>
        <div>
          <a href="/">总览</a>
          <a href="/ebooks/learn-claude-code-zh.epub" download>电子书</a>
          <a href="https://github.com/shareAI-lab/learn-claude-code/tree/main/{chapter["slug"]}" rel="noopener noreferrer">GitHub 原文</a>
        </div>
      </nav>
      <section class="chapter-masthead">
        <p class="eyebrow">{chapter["code"]} / Harness 课程</p>
        <h1>{title}</h1>
        <p class="lead">{html.escape(chapter["motto"])}。这一页按阅读优先重排：窄正文、固定目录、代码块独立呼吸，适合从头读到尾。</p>
        <div class="chapter-pager">{previous_link}{next_link}</div>
      </section>
    </header>
    <main class="chapter-layout">
      <aside class="course-rail" aria-label="课程章节">
        <p class="toc-title">课程</p>
        <div class="course-links">{chapter_links}</div>
      </aside>
      <article class="article chapter-article">
        <p class="source-note">来源：<a href="https://github.com/shareAI-lab/learn-claude-code/tree/main/{chapter["slug"]}" rel="noopener noreferrer">shareAI-lab/learn-claude-code/{chapter["slug"]}</a></p>
        {article_html}
        <nav class="bottom-pager" aria-label="章节翻页">{previous_link}{next_link}</nav>
      </article>
      <aside class="toc chapter-toc" aria-label="本章目录">
        <p class="toc-title">本章目录</p>
        <div class="toc-links">{nav_items}</div>
      </aside>
    </main>
    <script src="/assets/book.js"></script>
  </body>
</html>
"""


def main() -> None:
    markdown = fetch_text(RAW_URL, SOURCE)
    article_html, nav, meta = convert_markdown(markdown)
    OUTPUT.write_text(render_home(article_html, nav, meta), encoding="utf-8")

    for index, chapter in enumerate(CHAPTERS):
        chapter_markdown = fetch_text(f"{RAW_ROOT}/{chapter['slug']}/README.md", CHAPTER_DATA / f"{chapter['slug']}.md")
        chapter_html, chapter_nav, chapter_meta = convert_markdown(chapter_markdown, chapter["slug"])
        target_dir = ROOT / chapter["slug"]
        target_dir.mkdir(exist_ok=True)
        previous_chapter = CHAPTERS[index - 1] if index > 0 else None
        next_chapter = CHAPTERS[index + 1] if index + 1 < len(CHAPTERS) else None
        (target_dir / "index.html").write_text(
            render_chapter(chapter, chapter_html, chapter_nav, chapter_meta, previous_chapter, next_chapter),
            encoding="utf-8",
        )

    print(f"generated {OUTPUT} and {len(CHAPTERS)} chapter pages")


if __name__ == "__main__":
    main()
