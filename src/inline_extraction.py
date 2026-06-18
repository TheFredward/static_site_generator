import re
from readline import append_history_file

from src.textnode import TextNode, TextType, split_nodes_delimiter


def extract_markdown_images(text):
    matches = re.findall(r"\!\[([^\]]*)\]\(([^)]*)\)", text)
    return matches


def extract_markdown_links(text):
    matches = re.findall(r"[^\!]\[([^\]]*)\]\(([^)]*)\)", text)
    return matches


def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:  # pyright: ignore[reportReturnType]
    new_nodes = []
    found_images = []
    for single_old_node in old_nodes:
        found_nodes = []
        found_images = extract_markdown_images(single_old_node.text)
        if single_old_node.text_type != TextType.TEXT:
            new_nodes.append(single_old_node)
            continue
        if len(found_images) == 0:
            found_nodes.append(TextNode(single_old_node.text, TextType.TEXT))
        elif len(found_images) != 0:
            remaining_words = single_old_node.text
            for found_image in found_images:
                filter_word = f"![{found_image[0]}]({found_image[1]})"
                list_of_words = remaining_words.split(filter_word, 1)
                if list_of_words[0] != "":
                    found_nodes.append(TextNode(list_of_words[0], TextType.TEXT))
                found_nodes.append(
                    TextNode(found_image[0], TextType.IMAGE, found_image[1])
                )
                remaining_words = list_of_words[1]
            if remaining_words != "":
                found_nodes.append(TextNode(remaining_words, TextType.TEXT))
        new_nodes.extend(found_nodes)
    return new_nodes


def split_nodes_links(old_nodes: list[TextNode]) -> list[TextNode]:  # pyright: ignore[reportReturnType]
    new_nodes = []
    found_links = []
    for single_old_node in old_nodes:
        found_nodes = []
        found_links = extract_markdown_links(single_old_node.text)
        if single_old_node.text_type != TextType.TEXT:
            new_nodes.append(single_old_node)
            continue
        if len(found_links) == 0:
            found_nodes.append(TextNode(single_old_node.text, TextType.TEXT))
        elif len(found_links) != 0:
            remaining_words = single_old_node.text
            for found_link in found_links:
                filter_word = f"[{found_link[0]}]({found_link[1]})"
                list_of_words = remaining_words.split(filter_word, 1)  # pyright: ignore[reportCallIssue]
                if list_of_words[0] != "":
                    found_nodes.append(TextNode(list_of_words[0], TextType.TEXT))
                found_nodes.append(
                    TextNode(found_link[0], TextType.LINK, found_link[1])
                )
                remaining_words = list_of_words[1]
            if remaining_words != "":
                found_nodes.append(TextNode(remaining_words, TextType.TEXT))
        new_nodes.extend(found_nodes)
    return new_nodes


def text_to_textnodes(text):
    text_node = [TextNode(text, TextType.TEXT)]
    text_node = split_nodes_delimiter(text_node, "**", TextType.BOLD)
    text_node = split_nodes_delimiter(text_node, "_", TextType.ITALIC)
    text_node = split_nodes_delimiter(text_node, "`", TextType.CODE)
    text_node = split_nodes_image(text_node)
    text_node = split_nodes_links(text_node)
    return text_node
