from enum import Enum

from htmlnode import LeafNode


class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"


class TextNode:
    def __init__(self, text: str, text_type: TextType, url: str | None = None) -> None:
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other) -> bool:
        return (
            self.text == other.text
            and self.text_type == other.text_type
            and self.url == other.url
        )

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(text={self.text},text_type={self.text_type.value},url={self.url})"


def text_node_to_html_node(text_node: TextNode) -> LeafNode:
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text, None).to_html()  # pyright: ignore[reportReturnType]
        case TextType.BOLD:
            return LeafNode("b", text_node.text, None).to_html()  # pyright: ignore[reportReturnType]
        case TextType.ITALIC:
            return LeafNode("i", text_node.text, None).to_html()  # pyright: ignore[reportReturnType]
        case TextType.CODE:
            return LeafNode("code", text_node.text, None).to_html()  # pyright: ignore[reportReturnType]
        case TextType.LINK:
            return LeafNode("a", text_node.text, {"href": text_node.url}).to_html()  # pyright: ignore[reportReturnType, reportArgumentType]
        case TextType.IMAGE:
            return LeafNode(
                "img", "", {"src": text_node.url, "alt": text_node.text}
            ).to_html()  # pyright: ignore[reportReturnType, reportArgumentType]
