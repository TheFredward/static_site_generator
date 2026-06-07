from htmlnode import HTMLNode, LeafNode, ParentNode
from textnode import TextNode, TextType, text_node_to_html_node


def main():
    new_node = TextNode(
        "This is some anchor text", TextType.LINK, "https://www.boot.dev"
    )
    html_node = HTMLNode(
        "p",
        "Text in the paragraph",
        None,
        {"href": "google.com", "target": "_test_blank"},
    )
    leaf_node = LeafNode(
        None,
        "Text in the paragraph",
        None,
    )
    i_leaf_node = LeafNode(
        "p",
        "Text in the paragraph",
    )
    node = ParentNode(
        "p",
        [
            LeafNode("b", "Bold text"),
            LeafNode(None, "Normal text"),
            LeafNode("i", "italic text"),
            LeafNode(None, "Normal text"),
        ],
    )
    new_text_node = TextNode("This is the raw text", TextType.TEXT)
    italic_text_node = TextNode("This is the italic text", TextType.ITALIC)
    href_text_node = TextNode(
        "Time for some videos!", TextType.LINK, "https://youtube.com"
    )
    image_text_node = TextNode(
        "Time for some videos!", TextType.IMAGE, "https://youtube.com"
    )
    print(new_node)
    print(text_node_to_html_node(new_text_node))
    print(text_node_to_html_node(italic_text_node))
    print(text_node_to_html_node(href_text_node))
    print(text_node_to_html_node(image_text_node))
    print(html_node.props_to_html())
    print(leaf_node.to_html())
    print(i_leaf_node.to_html())
    print(node.to_html())


if __name__ == "__main__":
    main()
