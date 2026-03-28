import os
from src.config import BASE_DIR
from src.extract_title import extract_title
from src.frontmatter import parse_frontmatter
from src.markdown_blocks import markdown_to_html_node

def create_dir(path):
    os.makedirs(path, exist_ok=True)

def generate_page(from_path, template_path, dest_path, basepath):
    with open(from_path, "r") as f:
        raw = f.read()

    with open(template_path, "r") as f:
        template_content = f.read()

    meta, markdown_content = parse_frontmatter(raw)
    tags = [t.strip() for t in meta.get('tags', '').split(',') if t.strip()]

    node = markdown_to_html_node(markdown=markdown_content)
    html = node.to_html()
    title = meta.get('title') or extract_title(markdown_content)

    basepath = basepath if basepath.endswith("/") else basepath + "/"
    template_content = template_content.replace('href="/', f'href="{basepath}')
    template_content = template_content.replace('src="/', f'src="{basepath}')

    template_content = template_content.replace("{{ Title }}", title)
    template_content = template_content.replace("{{ Content }}", html)

    if tags:
        tags_html = (
            '<div class="post-tags">'
            + ''.join(f'<span class="tag">{t}</span>' for t in tags)
            + '</div>'
        )
    else:
        tags_html = ''
    template_content = template_content.replace("{{ Tags }}", tags_html)

    create_dir(os.path.dirname(dest_path))
    with open(dest_path, "w", encoding="utf-8") as f:
        f.write(template_content)

    return {'title': title, 'tags': tags}

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    dir_entries = os.listdir(dir_path_content)
    content_root = str(BASE_DIR / 'content')
    posts = []

    for entry in dir_entries:
        actual_dir_path_content = os.path.join(BASE_DIR, f"{dir_path_content}/{entry}")

        if os.path.isfile(actual_dir_path_content) and entry.endswith(".md"):
            dest_dir_ = actual_dir_path_content.replace(".md", ".html").replace(dir_path_content, dest_dir_path)

            meta = generate_page(
                from_path=actual_dir_path_content,
                template_path=template_path,
                dest_path=dest_dir_,
                basepath=basepath
            )

            rel = str(actual_dir_path_content).replace(content_root, '').replace('\\', '/')
            url = rel.replace('/index.md', '/').replace('.md', '/')
            posts.append({'title': meta['title'], 'url': url, 'tags': meta['tags']})

        if os.path.isdir(actual_dir_path_content):
            posts += generate_pages_recursive(
                dir_path_content=actual_dir_path_content,
                template_path=template_path,
                dest_dir_path=os.path.join(dest_dir_path, entry),
                basepath=basepath
            )

    return posts
