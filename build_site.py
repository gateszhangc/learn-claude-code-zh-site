#!/usr/bin/env python3
"""Build the Learn Claude Code Chinese reading site from README-zh.md."""
from __future__ import annotations

import html
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "data" / "readme-zh.md"
OUTPUT = ROOT / "index.html"
SOURCE_URL = "https://github.com/shareAI-lab/learn-claude-code/blob/main/README-zh.md"
RAW_URL = "https://raw.githubusercontent.com/shareAI-lab/learn-claude-code/main/README-zh.md"
SITE_URL = "https://learn-claude-code.codex55.lol/"


def slugify(text: str) -> str:
    slug = re.sub(r"[^0-9a-zA-Z\u4e00-\u9fff]+", "-", text.lower()).strip("-")
    return slug or "section"


def unique_slug(text: str, used: dict[str, int]) -> str:
    base = slugify(text)
    used[base] = used.get(base, 0) + 1
    return base if used[base] == 1 else f"{base}-{used[base]}"


def inline_markdown(text: str) -> str:
    placeholders: list[str] = []

    def keep(value: str) -> str:
        token = f"@@TOKEN{len(placeholders)}@@"
        placeholders.append(value)
        return token

    text = html.escape(text, quote=False)
    text = re.sub(r"`([^`]+)`", lambda match: keep(f"<code>{match.group(1)}</code>"), text)
    text = re.sub(r"\*\*(.+?)\*\*", lambda match: keep(f"<strong>{match.group(1)}</strong>"), text)
    text = re.sub(
        r"\[([^\]]+)\]\(([^)]+)\)",
        lambda match: keep(
            f'<a href="{html.escape(match.group(2), quote=True)}" rel="noopener noreferrer">{match.group(1)}</a>'
        ),
        text,
    )
    text = re.sub(r"(?<!\*)\*([^*\n]+)\*(?!\*)", r"<em>\1</em>", text)
    for index, value in enumerate(placeholders):
        text = text.replace(f"@@TOKEN{index}@@", value)
    return text


def is_table(lines: list[str], index: int) -> bool:
    if index + 1 >= len(lines):
        return False
    return (
        lines[index].lstrip().startswith("|")
        and lines[index + 1].lstrip().startswith("|")
        and bool(re.search(r"\|\s*:?-{3,}:?\s*\|", lines[index + 1]))
    )


def table_block(lines: list[str], index: int) -> tuple[str, int]:
    rows: list[list[str]] = []
    while index < len(lines) and lines[index].lstrip().startswith("|"):
        rows.append([cell.strip() for cell in lines[index].strip().strip("|").split("|")])
        index += 1
    parts = ["<div class=\"table-wrap\"><table>", "<thead><tr>"]
    parts.extend(f"<th>{inline_markdown(cell)}</th>" for cell in rows[0])
    parts.append("</tr></thead><tbody>")
    for row in rows[2:]:
        parts.append("<tr>")
        parts.extend(f"<td>{inline_markdown(cell)}</td>" for cell in row)
        parts.append("</tr>")
    parts.append("</tbody></table></div>")
    return "\n".join(parts), index


def list_block(lines: list[str], index: int) -> tuple[str, int]:
    ordered = bool(re.match(r"\s*\d+\.\s+", lines[index]))
    tag = "ol" if ordered else "ul"
    pattern = r"^\s*\d+\.\s+" if ordered else r"^\s*[-*]\s+"
    items: list[str] = []
    while index < len(lines) and re.match(pattern, lines[index]):
        item = re.sub(pattern, "", lines[index], count=1).strip()
        items.append(f"<li>{inline_markdown(item)}</li>")
        index += 1
    return f"<{tag}>\n" + "\n".join(items) + f"\n</{tag}>", index


def paragraph_block(lines: list[str], index: int) -> tuple[str, int]:
    parts: list[str] = []
    while index < len(lines):
        line = lines[index]
        if not line.strip():
            break
        if line.startswith("#") or line.startswith("```") or line.startswith(">"):
            break
        if is_table(lines, index) or re.match(r"\s*(?:[-*]|\d+\.)\s+", line):
            break
        parts.append(line.strip())
        index += 1
    return f"<p>{inline_markdown(' '.join(parts))}</p>", index


def convert_markdown(markdown: str) -> tuple[str, list[dict[str, str]], dict[str, str]]:
    lines = markdown.splitlines()
    html_parts: list[str] = []
    nav: list[dict[str, str]] = []
    used_slugs: dict[str, int] = {}
    meta = {"title": "Learn Claude Code"}
    index = 0
    while index < len(lines):
        line = lines[index]
        if line.strip() == "[English](./README.md) | [中文](./README-zh.md) | [日本語](./README-ja.md)":
            index += 1
            continue
        if not line.strip():
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
        heading = re.match(r"^(#{1,4})\s+(.+)$", line)
        if heading:
            level = len(heading.group(1))
            title = re.sub(r"\s*\(重要\)\s*$", "", heading.group(2).strip())
            title_plain = re.sub(r"[*_`]", "", title)
            section_id = unique_slug(title_plain, used_slugs)
            if level == 1:
                meta["title"] = re.sub(r"\s+--\s+", "：", title_plain)
            elif level == 2:
                nav.append({"id": section_id, "title": title_plain})
            html_parts.append(f'<h{level} id="{section_id}">{inline_markdown(title)}</h{level}>')
            index += 1
            continue
        if line.startswith(">"):
            quote_lines: list[str] = []
            while index < len(lines) and lines[index].startswith(">"):
                quote_lines.append(lines[index].lstrip("> ").strip())
                index += 1
            html_parts.append(f"<blockquote><p>{inline_markdown(' '.join(quote_lines))}</p></blockquote>")
            continue
        if is_table(lines, index):
            table, index = table_block(lines, index)
            html_parts.append(table)
            continue
        if re.match(r"\s*(?:[-*]|\d+\.)\s+", line):
            listing, index = list_block(lines, index)
            html_parts.append(listing)
            continue
        paragraph, index = paragraph_block(lines, index)
        html_parts.append(paragraph)
    return "\n".join(html_parts), nav, meta


def render_page(article_html: str, nav: list[dict[str, str]], meta: dict[str, str]) -> str:
    nav_items = "\n".join(
        f'<a href="#{item["id"]}"><span>{index:02d}</span>{html.escape(item["title"])}</a>'
        for index, item in enumerate(nav, start=1)
    )
    title = html.escape(meta["title"])
    return f"""<!doctype html>
<html lang="zh-CN">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{title}</title>
    <meta name="description" content="Learn Claude Code 中文长文阅读站：真正的 Agent Harness 工程。">
    <link rel="canonical" href="{SITE_URL}">
    <link rel="stylesheet" href="assets/styles.css">
  </head>
  <body>
    <header class="site-hero">
      <nav class="topbar" aria-label="顶部导航">
        <a class="brand" href="#top">Learn Claude Code</a>
        <div>
          <a href="#全部章节">章节</a>
          <a href="{SOURCE_URL}" rel="noopener noreferrer">GitHub 原文</a>
        </div>
      </nav>
      <div class="hero-grid" id="top">
        <div class="hero-copy">
          <p class="eyebrow">中文阅读站</p>
          <h1>{title}</h1>
          <p class="lead">把 shareAI-lab 的中文 README 整理成适合连续阅读的静态网页：目录常驻、正文窄栏、代码块和表格保持清晰。</p>
          <div class="hero-actions">
            <a class="primary-action" href="#agency-来自模型-agent-产品-模型-harness">开始阅读</a>
            <a href="{RAW_URL}" rel="noopener noreferrer">查看 Markdown</a>
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
        {article_html}
      </article>
    </main>
    <script src="assets/book.js"></script>
  </body>
</html>
"""


def main() -> None:
    markdown = SOURCE.read_text(encoding="utf-8")
    article_html, nav, meta = convert_markdown(markdown)
    OUTPUT.write_text(render_page(article_html, nav, meta), encoding="utf-8")
    print(f"generated {OUTPUT} from {SOURCE}")


if __name__ == "__main__":
    main()
