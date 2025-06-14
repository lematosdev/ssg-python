from generate import generate_page, generate_pages_recursive
from textnode import TextNode, TextType
import os
import shutil


static_dir = "./static"
public_dir = "./public"
content_dir = "./content"
template = "./template.html"

def copy_static(src, dest):
    if not os.path.exists(dest):
        os.mkdir(dest)
    for filename in os.listdir(src):
        src_path = os.path.join(src, filename)
        dest_path = os.path.join(dest, filename)
        if os.path.isfile(src_path):
            shutil.copy(src_path, dest_path)
        else:
            copy_static(src_path, dest_path)
    
def main(): 
    if os.path.exists("public"):
        shutil.rmtree("public")
    copy_static(static_dir, public_dir)
    generate_pages_recursive(content_dir, template, public_dir)

main()