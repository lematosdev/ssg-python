from enum import Enum
import re

from htmlnode import HTMLNode, LeafNode, ParentNode
from inline_markdown import text_to_textnodes
from textnode import TextNode, TextType, text_node_to_html_node

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED = "unordered_list"
    ORDERED = "ordered_list"

def markdown_to_blocks(markdown):
    return [el.strip() for el in markdown.split("\n\n") if el]

def block_to_block_type(block):
    splitted = block.split(" ", 1)[0]
    if splitted in "######":
        return BlockType.HEADING
    
    sections = block.split("\n")

    if sections[0].startswith("```") and sections[-1].startswith("```"):
        return BlockType.CODE

    is_quote = True
    is_unordered_list = True
    is_ordered_list = True
    count = 1

    for section in sections:
        if not section.startswith(">"):
            is_quote = False
        if not section.startswith("- "):
            is_unordered_list = False
        if not section.startswith(f"{count}."):
            is_ordered_list = False
        count += 1

    if is_quote:
        return BlockType.QUOTE
    if is_unordered_list:
        return BlockType.UNORDERED
    if is_ordered_list:
        return BlockType.ORDERED
    
    return BlockType.PARAGRAPH
    
def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        block_type = block_to_block_type(block)
        match block_type:
            case BlockType.PARAGRAPH:
                block_children = text_to_children(block)
                node = ParentNode("p", block_children)
                children.append(node)
            case BlockType.HEADING:
                heading = block.split(" ", 1)
                count = len(heading[0])
                block_children = text_to_children(heading[1])
                node = ParentNode(f"h{count}", block_children)
                children.append(node)
            case BlockType.QUOTE:
                quotes = block.split("\n")
                clean = ""
                for quote in quotes:
                    if quote.startswith(">"):
                        clean += f"{quote[1:].strip()} "
                block_children = text_to_children(clean.strip())
                children.append(ParentNode("blockquote", block_children))
            case BlockType.UNORDERED:
                list = block.split("\n")
                block_children = []
                for el in list:
                    if el.startswith("- "):
                        inline_md = text_to_children(el[2:])
                        block_children.append(ParentNode("li", inline_md))

                node = ParentNode("ul", block_children)
                children.append(node)
            case BlockType.ORDERED:
                list = block.split("\n")
                block_children = []
                count = 1
                for el in list:
                    if el.startswith(f"{count}. "):
                        inline_md = text_to_children(el[3:])
                        block_children.append(ParentNode("li", inline_md))
                    count += 1
                node = ParentNode("ol", block_children)
                children.append(node)
            case BlockType.CODE:
                text_node = TextNode(block[4:-3], TextType.NORMAL)
                html_node = text_node_to_html_node(text_node)
                node = ParentNode("pre", [ParentNode("code", [html_node])])
                children.append(node)

    parent = ParentNode("div", children)
    return parent


def text_to_children(text):
    html_nodes = []
    text_nodes = text_to_textnodes(" ".join(text.split("\n")))
    for node in text_nodes:
        html_nodes.append(text_node_to_html_node(node))
    return html_nodes

def extract_title(markdown):
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        type = block_to_block_type(block)
        if type == BlockType.HEADING:
            return block.split(" ", 1)[1].strip()
    
    raise ValueError("No title provided")