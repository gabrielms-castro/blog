def parse_frontmatter(markdown):
    """
    Parses YAML-like frontmatter delimited by '---'.
    Returns (metadata_dict, content_without_frontmatter).
    If no frontmatter is found, returns ({}, original markdown).
    """
    if not markdown.startswith('---\n'):
        return {}, markdown

    end = markdown.find('\n---', 4)
    if end == -1:
        return {}, markdown

    fm_text = markdown[4:end]
    content = markdown[end + 4:].lstrip('\n')

    meta = {}
    for line in fm_text.split('\n'):
        if ':' in line:
            key, _, value = line.partition(':')
            meta[key.strip()] = value.strip()

    return meta, content
