def extract_main_content(soup):
    # Priority order
    selectors = [
        "main",
        "#main",
        "#container",
        ".content",
        ".content-section",
        "body"
    ]

    for sel in selectors:
        node = soup.select_one(sel)
        if node:
            return node.get_text(separator="\n", strip=True)
        
    return soup.get_text(separator="\n", strip=True)