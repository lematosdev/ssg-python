import os

from block_markdown import extract_title, markdown_to_html_node

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    markdown = open(from_path).read()
    html = open(template_path).read()

    nodes = markdown_to_html_node(markdown)
    content = nodes.to_html()
    title = extract_title(markdown)

    new_html = html.replace(r"{{ Title }}", title)
    new_html = new_html.replace(r"{{ Content }}", content)
    
    dir = os.path.dirname(dest_path)
    if os.path.exists(dir) != "":
        os.makedirs(dir, exist_ok=True)

    file = open(dest_path, "w+")
    file.write(new_html)
    
def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    for filename in os.listdir(dir_path_content):
        src_path = os.path.join(dir_path_content, filename)
        dest_path = os.path.join(dest_dir_path, filename.replace("md", "html"))
        if os.path.isfile(src_path):
            generate_page(src_path, template_path, dest_path)
        else:
            generate_pages_recursive(src_path, template_path, dest_path)