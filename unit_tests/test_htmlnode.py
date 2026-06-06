import unittest

from src.htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_repr(self):
        answer = HTMLNode(
            tag="h1",
            value="Title of my life",
            children=None,
            props={"href": "www.backrooms.co"},
        )
        self.assertEqual(
            repr(answer),
            "HTMLNode(tag=h1,value=Title of my life,children=None,props={'href': 'www.backrooms.co'})",
        )

    def test_eq(self):
        node = HTMLNode(
            tag=None,
            value=None,
            children=None,
            props={"href": "www.google.com", "target": "_blank"},
        )
        self.assertEqual(node.props_to_html(), ' href="www.google.com" target="_blank"')
        with self.assertRaises(NotImplementedError):
            node.to_html()


if __name__ == "__main__":
    unittest.main()
