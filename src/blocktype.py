import re
from enum import Enum


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def block_to_block_type(markdown_text):
    if re.match(r"^#{1,6}\s", markdown_text):
        return BlockType.HEADING
    elif markdown_text.startswith("``` "):
        return BlockType.CODE
    elif markdown_text.startswith('> "') or markdown_text.startswith('>"'):
        return BlockType.QUOTE
    elif markdown_text.startswith("- "):
        return BlockType.UNORDERED_LIST
    elif re.match(r"^\d+\.\s", markdown_text):
        return BlockType.ORDERED_LIST
    else:
        return BlockType.PARAGRAPH
