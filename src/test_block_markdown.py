import unittest

from block_markdown import BlockType, block_to_block_type, extract_title, markdown_to_blocks, markdown_to_html_node

class TestBlockMarkdown(unittest.TestCase):
        def test_markdown_to_blocks(self):
            md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
            blocks = markdown_to_blocks(md)
            self.assertEqual(
                blocks,
                [
                    "This is **bolded** paragraph",
                    "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                    "- This is a list\n- with items",
                ],
            )
        
        def test_heading_block(self):
            md = "###### This is a header"
            block_type = block_to_block_type(md)
            self.assertEqual(BlockType.HEADING, block_type)

        def test_code_block(self):
            md = """```
this a code block
```"""
            block_type = block_to_block_type(md)
            self.assertEqual(BlockType.CODE, block_type)

        def test_quote_block(self):
            md = ">this is a quote\n>this is another quote"
            block_type = block_to_block_type(md)
            self.assertEqual(BlockType.QUOTE, block_type)

        def test_unordered_block(self):
            md = "- esto es un elemento en una lista\n- esto es otro elemento en la lista"
            block_type = block_to_block_type(md)
            self.assertEqual(BlockType.UNORDERED, block_type)

        def test_ordered_block(self):
            md = "1. esto es un elemento en una lista\n2. esto es otro elemento en la lista"
            block_type = block_to_block_type(md)
            self.assertEqual(BlockType.ORDERED, block_type)

        def test_paragraph_block(self):
            md = "esto es un parrafo"
            block_type = block_to_block_type(md)
            self.assertEqual(BlockType.PARAGRAPH, block_type)

        def test_paragraphs(self):
            md = """
### This is a h3 with **bold** text

This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""
            node = markdown_to_html_node(md)
            html = node.to_html()
            self.assertEqual(
                html,
                "<div><h3>This is a h3 with <b>bold</b> text</h3><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
            )
        
        def test_unordered_lists(self):
            md = """
- this is a 
- unordered
- list
"""
            node = markdown_to_html_node(md)
            html = node.to_html()
            self.assertEqual(html, "<div><ul><li>this is a </li><li>unordered</li><li>list</li></ul></div>")

        def test_ordered_lists(self):
            md ="""
1. this is a 
2. ordered
3. list
"""
            node = markdown_to_html_node(md)
            html = node.to_html()
            self.assertEqual(html, "<div><ol><li>this is a </li><li>ordered</li><li>list</li></ol></div>")

        def test_code(self):
            md = """```
 const = "test"
```
"""
            node = markdown_to_html_node(md)
            html = node.to_html()
            self.assertEqual(html, '<div><pre><code> const = "test"</code></pre></div>')

        def test_paragraph(self):
            md = """
This is **bolded** paragraph
text in a p
tag here

"""

            node = markdown_to_html_node(md)
            html = node.to_html()
            self.assertEqual(
                html,
                "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p></div>",
            )

        def test_paragraphs(self):
            md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

            node = markdown_to_html_node(md)
            html = node.to_html()
            self.assertEqual(
                html,
                "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
            )

        def test_lists(self):
            md = """
- This is a list
- with items
- and _more_ items

1. This is an `ordered` list
2. with items
3. and more items

"""

            node = markdown_to_html_node(md)
            html = node.to_html()
            self.assertEqual(
                html,
                "<div><ul><li>This is a list</li><li>with items</li><li>and <i>more</i> items</li></ul><ol><li>This is an <code>ordered</code> list</li><li>with items</li><li>and more items</li></ol></div>",
            )

        def test_headings(self):
            md = """
# this is an h1

this is paragraph text

## this is an h2
"""

            node = markdown_to_html_node(md)
            html = node.to_html()
            self.assertEqual(
                html,
                "<div><h1>this is an h1</h1><p>this is paragraph text</p><h2>this is an h2</h2></div>",
            )

        def test_blockquote(self):
            md = """
> This is a
> blockquote block

this is paragraph text

"""

            node = markdown_to_html_node(md)
            html = node.to_html()
            self.assertEqual(
                html,
                "<div><blockquote>This is a blockquote block</blockquote><p>this is paragraph text</p></div>",
            )

        def test_code(self):
            md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

            node = markdown_to_html_node(md)
            html = node.to_html()
            self.assertEqual(
                html,
                "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
            )

        def test_extract_title(self):
            md = """
# this is a header
"""
            title = extract_title(md)
            self.assertEqual(title, "this is a header")