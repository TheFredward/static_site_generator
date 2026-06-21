import unittest

from src.inline_extraction import (
    extract_markdown_images,
    extract_markdown_links,
    extract_title,
    markdown_to_blocks,
    split_nodes_image,
    split_nodes_links,
    text_to_textnodes,
)
from src.textnode import TextNode, TextType


class TestInlineExtraction(unittest.TestCase):
    def test_extract_markdown_image(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )

        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_link(self):
        matches = extract_markdown_links(
            "This is text with an [youtube](https://youtube.com)"
        )

        self.assertListEqual([("youtube", "https://youtube.com")], matches)

    def test_extract_markdown_multiple_links(self):
        matches = extract_markdown_links(
            "My best studying is done with [youtube](https://youtube.com), at [parks coffee](https://www.parkscoffee.com/shop) and a Mr.Boots for assistance from [bootdev](https://www.boot.dev/). "
        )

        self.assertListEqual(
            [
                ("youtube", "https://youtube.com"),
                ("parks coffee", "https://www.parkscoffee.com/shop"),
                ("bootdev", "https://www.boot.dev/"),
            ],
            matches,
        )

    def test_extract_markdown_multiple_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )

        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_split_multi_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_multi_images_first_last(self):
        node = TextNode(
            "![image](https://i.imgur.com/zjjcJKZ.png) Starting with an image! Finishing with... ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" Starting with an image! Finishing with... ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_links(self):
        self.maxDiff = None
        node = TextNode(
            "My best studying is done with [youtube](https://youtube.com) and I don't get distracted at all...(no, really I don't). ",
            TextType.TEXT,
        )
        new_nodes = split_nodes_links([node])

        self.assertListEqual(
            [
                TextNode("My best studying is done with ", TextType.TEXT),
                TextNode("youtube", TextType.LINK, "https://youtube.com"),
                TextNode(
                    " and I don't get distracted at all...(no, really I don't). ",
                    TextType.TEXT,
                ),
            ],
            new_nodes,
        )

    def test_split_all(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        new_nodes = text_to_textnodes(text)

        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode(
                    "obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"
                ),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            new_nodes,
        )

    def test_markdown_to_blocks(self):
        md = """
this is **bolded** paragraph

this is another paragraph with _italic_ text and `code` here
this is the same paragraph on a new line

- this is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertListEqual(
            blocks,
            [
                "this is **bolded** paragraph",
                "this is another paragraph with _italic_ text and `code` here\nthis is the same paragraph on a new line",
                "- this is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_extra_spaces(self):
        md = """
this is **bolded** and _italic_ paragraph

this is another paragraph with _italic_ text and `code` here

this is A NEW Paragraph (Two empty lines coming next!)



- this is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertListEqual(
            blocks,
            [
                "this is **bolded** and _italic_ paragraph",
                "this is another paragraph with _italic_ text and `code` here",
                "this is A NEW Paragraph (Two empty lines coming next!)",
                "- this is a list\n- with items",
            ],
        )

    def test_extract_title(self):
        md = """
# this is **bolded** and _italic_ paragraph

## this is another paragraph with _italic_ text and `code` here

this is A NEW Paragraph (Two empty lines coming next!)
"""

        extract_title(md)


if __name__ == "__main__":
    unittest.main()
