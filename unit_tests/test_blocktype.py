import unittest

from src.blocktype import BlockType, block_to_block_type, markdown_to_html_node
from src.htmlnode import HTMLNode


class TextBlockType(unittest.TestCase):
    def test_heading_testcase(self):
        markdown_heading_type_1 = block_to_block_type("# this is the level 3 heading!")
        markdown_heading_type_3 = block_to_block_type(
            "### this is the level 3 heading!"
        )
        markdown_heading_type_failure_paragraph = block_to_block_type(
            "###this is the level 3 heading!"
        )
        self.assertEqual(BlockType.HEADING, markdown_heading_type_1)
        self.assertEqual(BlockType.HEADING, markdown_heading_type_3)
        self.assertEqual(BlockType.PARAGRAPH, markdown_heading_type_failure_paragraph)

    def test_code_testcase(self):
        markdown_code_test_1 = block_to_block_type("``` Code is here! ```")
        markdown_code_test_failure_1 = block_to_block_type("` Code is here! ```")
        self.assertEqual(BlockType.CODE, markdown_code_test_1)
        self.assertEqual(BlockType.PARAGRAPH, markdown_code_test_failure_1)

    def test_quote_testcase(self):
        markdown_quote_test_1 = block_to_block_type('> "quote is here!"')
        markdown_quote_test_2 = block_to_block_type('>"quote is here!"')
        markdown_quote_test_failure_1 = block_to_block_type("> quote is here!")
        self.assertEqual(BlockType.QUOTE, markdown_quote_test_1)
        self.assertEqual(BlockType.QUOTE, markdown_quote_test_2)
        self.assertEqual(BlockType.PARAGRAPH, markdown_quote_test_failure_1)

    def test_ordered_list_testcase(self):
        markdown_ordered_list_test_1 = block_to_block_type('1. "ordered_list is here!"')
        markdown_ordered_list_test_2 = block_to_block_type(
            '33. "ordered_list is here!"'
        )
        markdown_ordered_list_test_failure_1 = block_to_block_type(
            "1.ordered_list is here!"
        )
        self.assertEqual(BlockType.ORDERED_LIST, markdown_ordered_list_test_1)
        self.assertEqual(BlockType.ORDERED_LIST, markdown_ordered_list_test_2)
        self.assertEqual(BlockType.PARAGRAPH, markdown_ordered_list_test_failure_1)

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

    def codeblock(self):
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


if __name__ == "__main__":
    unittest.main()
