import re
from textnode import TextNode, TextType


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    if len(old_nodes) == 0:
        return new_nodes
    for node in old_nodes:
        if node.text_type != TextType.NORMAL:
            new_nodes.append(node)
            continue  
        splitted = node.text.split(delimiter)
        if len(splitted) % 2 == 0:
            raise ValueError("Missing closing delimiter")   
        for i in range(0, len(splitted)):
            if splitted[i] == "":
                continue
            if i % 2 == 0:
                new_nodes.append(TextNode(splitted[i], TextType.NORMAL))
            else:
                new_nodes.append(TextNode(splitted[i], text_type))
    return new_nodes

def split_nodes_image(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.NORMAL:
            new_nodes.append(old_node)
            continue
        images = extract_markdown_images(old_node.text)
        if len(images) == 0:
            new_nodes.append(old_node)
            continue
        old_text = old_node.text
        for alt, url in images:
            sections = old_text.split(f"![{alt}]({url})", 1)
            if sections[0]:
                new_nodes.append(TextNode(sections[0], TextType.NORMAL))
            new_nodes.append(TextNode(alt, TextType.IMAGE, url))
            old_text = sections[1]

        if old_text:
            new_nodes.append(TextNode(old_text, TextType.NORMAL))

    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.NORMAL:
            new_nodes.append(old_node)
            continue
        links = extract_markdown_links(old_node.text)
        if len(links) == 0:
            new_nodes.append(old_node)
            continue
        text = old_node.text
        for a_text, url in links:
            sections = text.split(f"[{a_text}]({url})", 1)
            if len(sections) != 2:
                raise ValueError("invalid markdown, link section not closed")
            if sections[0]:
                new_nodes.append(TextNode(sections[0], TextType.NORMAL))
            new_nodes.append(TextNode(a_text, TextType.LINK, url))
            text = sections[1]
        if text:
            new_nodes.append(TextNode(text, TextType.NORMAL))
    
    return new_nodes

def text_to_textnodes(text):
    new_nodes = []
    node = TextNode(text, TextType.NORMAL)
    new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
    new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
    new_nodes = split_nodes_delimiter(new_nodes, "`", TextType.CODE)
    new_nodes = split_nodes_image(new_nodes)
    new_nodes = split_nodes_link(new_nodes)
    return new_nodes

def extract_markdown_images(text):
    return re.findall(r"!\[(.*?)\]\((.*?)\)", text)

def extract_markdown_links(text):
    return re.findall(r"\[(.*?)\]\((.*?)\)", text)
