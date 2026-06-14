import re

from src.textnode import TextNode, TextType


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
        found_links = extract_markdown_links(single_old_node.text)
        if len(found_images) == 0 and len(found_links) == 0:
            return TextNode(single_old_node.text, TextType.TEXT)
        elif len(found_images) != 0:
            remaining_words = single_old_node.text
            for found_image in found_images:
                filter_word = f"![{found_image[0]}]({found_image[1]})"
                list_of_words = remaining_words.split(filter_word, 1)
                for i in range(len(list_of_words)):
                    if list_of_words[i] == "":
                        continue
                    if i == 0:
                        found_nodes.append(TextNode(list_of_words[i], TextType.TEXT))
                    remaining_words = list_of_words[1]
                found_nodes.append(
                    TextNode(found_image[0], TextType.IMAGE, found_image[1])
                )
        new_nodes.extend(found_nodes)
    return new_nodes


def split_nodes_links(old_nodes: list[TextNode]) -> list[TextNode]:  # pyright: ignore[reportReturnType]
    new_nodes = []
    found_links = []
    for single_old_node in old_nodes:
        found_nodes = []
        found_links = extract_markdown_links(single_old_node.text)
        if len(found_links) == 0:
            return TextNode(single_old_node.text, TextType.TEXT)
        elif len(found_links) != 0:
            for found_link in found_links:
                word = f"![{found_link[0]}]({found_link[1]})"
                list_of_words = single_old_node.text.split(word, 1)
                found_nodes.append(
                    TextNode(found_link[0], TextType.IMAGE, found_link[1])
                )
    new_nodes.extend(found_nodes)
    print(new_nodes)
    return new_nodes
