import re
from enum import Enum
from unittest import result

from src.htmlnode import HTMLNode, LeafNode, ParentNode
from src.inline_extraction import markdown_to_blocks, text_to_textnodes
from src.textnode import TextNode, TextType, text_node_to_html_node


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def block_to_block_type(markdown_text):
    markdown_lines = markdown_text.split("\n")
    if re.match(r"^#{1,6}\s", markdown_text):
        return BlockType.HEADING
    elif markdown_lines[0].startswith("```") and markdown_lines[-1].strip().startswith(
        "```"
    ):
        return BlockType.CODE
    elif markdown_lines[0].startswith("> ") or markdown_lines[0].startswith(">"):
        for i in range(1, len(markdown_lines)):
            if markdown_lines[i].startswith("> ") or markdown_lines[i].startswith(">"):
                continue
            else:
                return BlockType.PARAGRAPH
        return BlockType.QUOTE
    elif markdown_text.startswith("- "):
        return BlockType.UNORDERED_LIST
    elif re.match(r"^\d+\.\s", markdown_text):
        return BlockType.ORDERED_LIST
    else:
        return BlockType.PARAGRAPH


def text_to_children(block_text):
    text_nodes = text_to_textnodes(block_text)
    leaf_nodes = []
    for text_node in text_nodes:
        result = text_node_to_html_node(text_node)
        leaf_nodes.append(result)
    return leaf_nodes


def markdown_to_html_node(markdown):
    split_markdown = markdown_to_blocks(markdown)
    parentNodes = []

    for block in split_markdown:
        block_type = block_to_block_type(block)
        match block_type:
            case BlockType.PARAGRAPH:
                html_tag = "p"
                removal_newlines = block.strip().split("\n")
                cleaned_block = " ".join(line.strip() for line in removal_newlines)
                leafNodes = text_to_children(cleaned_block)
                parentNodes.append(ParentNode(html_tag, leafNodes))
            case BlockType.HEADING:
                header_length = len(block) - len(block.strip("#"))
                cleaned_block = block.lstrip("#")
                html_tag = f"h{header_length}"
                leafNodes = text_to_children(cleaned_block)
                parentNodes.append(ParentNode(html_tag, leafNodes))
            case BlockType.CODE:
                html_tag = "code"
                cleaned_block = block[4:-3]
                cleaned_block_lines = cleaned_block.split("\n")
                final_block = "\n".join(line.strip() for line in cleaned_block_lines)
                textNode = TextNode(final_block, TextType.TEXT)
                leafNode = text_node_to_html_node(textNode)
                parentNodes.append(
                    ParentNode("pre", [ParentNode(html_tag, [leafNode])])
                )
            case BlockType.QUOTE:
                html_tag = "blockquote"
                split_block = block.split("\n")
                innerNodes = []
                cleaned_lines = []
                for single_line in split_block:
                    cleaned_lines.append(single_line[2:])
                full_quote = " ".join(cleaned_lines)
                leafNodes = text_to_children(full_quote)
                parentNodes.append(ParentNode(html_tag, leafNodes))
            case BlockType.UNORDERED_LIST:
                html_tag = "ul"
                split_block = block.split("\n")
                innerNodes = []
                for single_line in split_block:
                    cleaned_line = single_line[2:]
                    leafNodes = text_to_children(cleaned_line)
                    innerNodes.append(ParentNode("li", leafNodes))
                parentNodes.append(ParentNode(html_tag, innerNodes))
            case BlockType.ORDERED_LIST:
                html_tag = "ol"
                split_block = block.split("\n")
                innerNodes = []
                for single_line in split_block:
                    cleaned_line = re.sub(r"\d+", "", single_line, count=1)
                    leafNodes = text_to_children(cleaned_line)
                    innerNodes.append(ParentNode("li", leafNodes))
                parentNodes.append(ParentNode(html_tag, innerNodes))
    return ParentNode("div", parentNodes)
