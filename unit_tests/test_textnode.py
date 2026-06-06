import unittest

from src.textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node_2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node_2)

    def test_not_eq(self):
        node = TextNode("This is a text node", TextType.ITALIC)
        node_2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node_2)

    def test_not_eq(self):
        node = TextNode("tHIS IS A TEXT NODE", TextType.BOLD)
        node_2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node_2)

    def test_repr(self):
        answer = TextNode(text="Example test", text_type=TextType.TEXT)
        self.assertEqual(
            repr(answer), "TextNode(text=Example test,text_type=text,url=None)"
        )


if __name__ == "__main__":
    unittest.main()
