class HTMLNode:
    def __init__(
        self,
        tag: str | None = None,
        value: str | None = None,
        children: list["HTMLNode"] | None = None,
        props: dict[str, str] | None = None,
    ):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError(
            "The process method must be implemented by subclasses."
        )

    def props_to_html(self):
        formatted_dict = ""
        if self.props:
            for key, value in self.props.items():
                formatted_dict += f' {key}="{value}"'

        return formatted_dict

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(tag={self.tag},value={self.value},children={self.children},props={self.props})"


class LeafNode(HTMLNode):
    def __init__(
        self,
        tag: str | None,
        value: str,
        props: dict[str, str] | None = None,
    ):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value is None:
            raise ValueError("All leaf nodes must have a value")
        if self.tag is None:
            return f"{self.value}"
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(tag={self.tag},value={self.value},props={self.props})"


class ParentNode(HTMLNode):
    def __init__(
        self,
        tag: str,
        children: list["ParentNode"] | None = None,
        props: dict[str, str] | None = None,
    ):
        super().__init__(tag, None, children, props)  # pyright: ignore[reportArgumentType]

    def to_html(self):
        if self.tag is None:
            raise ValueError("All parent tag nodes must have a value")
        if self.children is None:
            raise ValueError("All parent children nodes must have a value")
        final_response = ""
        for child in self.children:
            final_response += f"{child.to_html()}"
        return f"<{self.tag}>{final_response}</{self.tag}>"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(tag={self.tag},children={self.children},props={self.props})"
