import re


def remove_html_tags(html_content):
    """
    Removes HTML tags from the given content and returns the plain text.
    """
    clean_text = re.sub(r'<[^>]+>', '', html_content)  # Regular expression to remove HTML tags
    return clean_text
