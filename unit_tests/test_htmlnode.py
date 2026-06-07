import unittest

from src.htmlnode import HTMLNode, LeafNode, ParentNode


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

    def test_values(self):
        node = HTMLNode(
            tag="span",
            value="Used to group elements: for example to",
            children=None,
            props={"style": "color:blue"},
        )
        self.assertEqual(
            node.tag,
            "span",
        )
        self.assertEqual(
            node.value,
            "Used to group elements: for example to",
        )
        self.assertEqual(
            node.props,
            {"style": "color:blue"},
        )


class TestLeafNode(unittest.TestCase):
    def test_repr(self):
        node = LeafNode(
            tag="p",
            value="Finally, a leaf node to test!",
            props={"style": "color:blue"},
        )
        self.assertEqual(
            node.to_html(), '<p style="color:blue">Finally, a leaf node to test!</p>'
        )
        self.assertEqual(
            repr(node),
            "LeafNode(tag=p,value=Finally, a leaf node to test!,props={'style': 'color:blue'})",
        )

    def test_tag(self):
        missing_tag_node = LeafNode(
            tag=None, value="Testing if we can get a raw string", props=None
        )
        self.assertEqual(
            missing_tag_node.to_html(), "Testing if we can get a raw string"
        )

        with_tag_node = LeafNode(
            tag="p", value="Testing if we can get a raw string", props=None
        )
        self.assertEqual(
            with_tag_node.to_html(), "<p>Testing if we can get a raw string</p>"
        )

        with_props_node = LeafNode(
            tag="img",
            value="Grapefruits are in season",
            props={
                "class": "fit-picture",
                "src": "/shared-images/examples/fruits.jpg",
                "alt": "Grapefruit sliced",
            },
        )
        self.assertEqual(
            with_props_node.to_html(),
            '<img class="fit-picture" src="/shared-images/examples/fruits.jpg" alt="Grapefruit sliced">Grapefruits are in season</img>',
        )


class TestParentNode(unittest.TestCase):
    def test_repr(self):
        self.maxDiff = None
        node = ParentNode(
            tag="p",
            children=[
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
            props={"style": "color:blue"},
        )
        self.assertEqual(
            node.to_html(),
            "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>",
        )
        self.assertEqual(
            repr(node),
            "ParentNode(tag=p,children=[LeafNode(tag=b,value=Bold text,props=None), LeafNode(tag=None,value=Normal text,props=None), LeafNode(tag=i,value=italic text,props=None), LeafNode(tag=None,value=Normal text,props=None)],props={'style': 'color:blue'})",
        )

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )


if __name__ == "__main__":
    unittest.main()
