from collections import namedtuple

import colorama

# colorama.init()

ColorTarget = namedtuple("ColorTarget", "colorama_class replacement reset")
FORE = ColorTarget(colorama.Fore, "~f", colorama.Fore.RESET)
BACK = ColorTarget(colorama.Back, "~b", colorama.Back.RESET)
STYLE = ColorTarget(colorama.Style, "~s", colorama.Style.RESET_ALL)
RESET = ColorTarget(
    colorama.Style.RESET_ALL, "~r", colorama.Style.RESET_ALL
)
ALL_COLOR_TARGETS = [FORE, BACK, STYLE]
ALL_REPLACEMENTS = [_.replacement for _ in ALL_COLOR_TARGETS]


class NonMatchingColorReplacementExpection(Exception):
    """Exception raised when the replacement count does not match the
    color count."""
    def __init__(self, replacement_count, color_count):
        message = (
            "==>"
            f"\n\n~fReplacement count:~r ~f'{replacement_count}'~r "
            "~f~s~bdoes not match~r "
            f"~fColor count:~r ~f'{color_count}'\n"
        )
        pretty_message = PeacockPrint(
            message,
            (
                "blue", "cyan", "red", "BRIGHT", "WHITE", "magenta",
                "LIGHTMAGENTA_EX"
            ),
        )
        super().__init__(pretty_message)


class PeacockPrint:
    """Class for color printing a string using format strings"""
    def __init__(
        self,
        template_string: str,
        color_tuple: tuple[str],
        reset_end: bool = True
    ):
        self.template_string: str = template_string
        self.color_tuple: tuple[str] = color_tuple
        self.reset_end: bool = reset_end

        self.replacement_count: int = self.count_replacements()
        self.validate_args()

        self.text: str = self.perform_replacements()

    def validate_args(self):
        """Validate the 'template_string' and 'color_tuple' length"""
        color_count = len(self.color_tuple)
        if self.replacement_count != color_count:
            raise NonMatchingColorReplacementExpection(
                self.replacement_count, color_count
            )

    def __repr__(self):
        return self.text

    def count_replacements(self) -> int:
        """Count the replacements in the template string"""
        return sum(
            [
                self.template_string.replace(RESET.replacement,
                                             "").count(replacement)
                for replacement in ALL_REPLACEMENTS
            ]
        )

    @staticmethod
    def replace_resets(text) -> str:
        """Replace reset replacements with resets"""
        return text.replace(RESET.replacement, RESET.colorama_class)

    def replace_by_style_type(self, text, color, style_type) -> str:
        """Replace the template string by 'style_type'"""
        color_replacement = self.get_color_replacement(style_type, color)
        return text.replace(style_type.replacement, color_replacement, 1)

    def get_color_replacement(self, style_type: ColorTarget, color: str):
        """Get the equivalent to the given color name"""
        color_replacement = style_type.colorama_class.__dict__.get(
            color.upper(), style_type.reset
        )
        return color_replacement

    @staticmethod
    def get_first_matching_style_type(text: str) -> ColorTarget:
        """Find the lowest index matching style type by it's replacement"""
        lowest_index = len(text)
        style_candidate = None

        for color_target in ALL_COLOR_TARGETS:
            replacement_index = text.find(color_target.replacement)
            if replacement_index < 0:
                continue

            if replacement_index < lowest_index:
                lowest_index = replacement_index
                style_candidate = color_target

        if not style_candidate:
            print("NONE style candidate found")

        return style_candidate

    def perform_replacements(self):
        """Perform replacement operations on the 'template_string'"""
        text = self.template_string
        text = self.replace_resets(text)

        for color in self.color_tuple:
            style_type = self.get_first_matching_style_type(text)
            text = self.replace_by_style_type(text, color, style_type)

        if self.reset_end:
            text += RESET.colorama_class

        return text


def do_demo():
    # Calling it straight away
    pp = PeacockPrint
    print(pp("text~f hello", ("cyan", )))

    # Defining it as a variable
    good_template = "~fgreen~r ~s~bred tem~r~s~fplate"
    good_pretty_text = PeacockPrint(
        good_template, ("green", "BRIGHT", "red", "DIM", "LIGHTBLUE")
    )
    print(good_pretty_text)
    # good_pretty_text.text <-- to get the string

    # Mismatching replacement count and color count
    bad_template = "~fgreen ~fred tem~rplate"
    bad_pretty_text = PeacockPrint(bad_template, ("green", "red", "blue"))
    print(bad_pretty_text)
