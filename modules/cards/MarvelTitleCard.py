from pathlib import Path
from typing import Literal, Optional

from modules.BaseCardType import BaseCardType, ImageMagickCommands
from modules.ImageMagickInterface import Dimensions


class Coordinate:
    """Class that defines a single Coordinate on an x/y plane."""
    __slots__ = ('x', 'y')

    def __init__(self, x: float, y: float) -> None:
        self.x = x
        self.y = y

    def __str__(self) -> str:
        return f'{self.x:.0f},{self.y:.0f}'


class Rectangle:
    """Class that defines movable SVG rectangle."""
    __slots__ = ('start', 'end')

    def __init__(self, start: Coordinate, end: Coordinate) -> None:
        self.start = start
        self.end = end

    def __str__(self) -> str:
        return f'rectangle {str(self.start)},{str(self.end)}'

    def draw(self) -> str:
        """Draw this Rectangle"""
        return f'-draw "{str(self)}"'


class MarvelTitleCard(BaseCardType):
    """
    This class describes a CardType that produces title cards intended to match
    RedHeadJedi's style of Marvel Cinematic Universe posters. These cards
    feature a white border on the left, top, and right edges, and a black box on
    the bottom. All text is displayed in the bottom box.
    """

    """Directory where all reference files used by this card are stored"""
    REF_DIRECTORY = BaseCardType.BASE_REF_DIRECTORY / 'marvel'

    """Characteristics for title splitting by this class"""
    TITLE_CHARACTERISTICS = {
        'max_line_width': 25,   # Character count to begin splitting titles
        'max_line_count': 1,    # Maximum number of lines a title can take up
        'top_heavy': True,      # This class uses top heavy titling
    }

    """Characteristics of the default title font"""
    TITLE_FONT = str((REF_DIRECTORY / 'Qualion ExtraBold.ttf').resolve())
    TITLE_COLOR = 'white'
    DEFAULT_FONT_CASE = 'upper'
    FONT_REPLACEMENTS = {}

    """Characteristics of the episode text"""
    EPISODE_TEXT_COLOR = '#C9C9C9'
    EPISODE_TEXT_FONT = REF_DIRECTORY / 'Qualion ExtraBold.ttf'

    """Whether this CardType uses season titles for archival purposes"""
    USES_SEASON_TITLE = True

    """Standard class has standard archive name"""
    ARCHIVE_NAME = 'Marvel Style'

    """How thick the border is (in pixels)"""
    DEFAULT_BORDER_SIZE = 55

    """Color of the border"""
    DEFAULT_BORDER_COLOR = 'white'

    """Color of the text box"""
    DEFAULT_TEXT_BOX_COLOR = 'black'

    """Height of the text box (in pixels)"""
    DEFAULT_TEXT_BOX_HEIGHT = 200

    __slots__ = (
        'source_file', 'output_file', 'title_text', 'season_text',
        'episode_text', 'hide_season_text', 'hide_episode_text', 'font_file',
        'font_size', 'font_color', 'font_interline_spacing',
        'font_interword_spacing', 'font_kerning', 'font_vertical_shift',
        'border_color', 'border_size', 'episode_text_color', 'fit_text',
        'episode_text_position', 'hide_border', 'text_box_color',
        'text_box_height', 'font_size_modifier',
    )

    def __init__(self, *,
            source_file: Path,
            card_file: Path,
            title_text: str,
            season_text: str,
            episode_text: str,
            hide_season_text: bool = False,
            hide_episode_text: bool = False,
            font_color: str = TITLE_COLOR,
            font_file: str = TITLE_FONT,
            font_interline_spacing: int = 0,
            font_interword_spacing: int = 0,
            font_kerning: float = 1.0,
            font_size: float = 1.0,
            font_vertical_shift: int = 0,
            blur: bool = False,
            grayscale: bool = False,
            border_color: str = DEFAULT_BORDER_COLOR,
            border_size: int = DEFAULT_BORDER_SIZE,
            episode_text_color: str = EPISODE_TEXT_COLOR,
            episode_text_location: Literal['compact', 'fixed'] = 'fixed',
            fit_text: bool = True,
            hide_border: bool = False,
            text_box_color: str = DEFAULT_TEXT_BOX_COLOR,
            text_box_height: int = DEFAULT_TEXT_BOX_HEIGHT,
            preferences: Optional['Preferences'] = None, # type: ignore
            **unused,
        ) -> None:
        """
        Construct a new instance of this Card.
        """

        # Initialize the parent class - this sets up an ImageMagickInterface
        super().__init__(blur, grayscale, preferences=preferences)

        self.source_file = source_file
        self.output_file = card_file

        # Ensure characters that need to be escaped are
        self.title_text = self.image_magick.escape_chars(title_text)
        self.season_text = self.image_magick.escape_chars(season_text)
        self.episode_text = self.image_magick.escape_chars(episode_text)
        self.hide_season_text = hide_season_text
        self.hide_episode_text = hide_episode_text

        # Font/card customizations
        self.font_color = font_color
        self.font_file = font_file
        self.font_interline_spacing = font_interline_spacing
        self.font_interword_spacing = font_interword_spacing
        self.font_kerning = font_kerning
        self.font_size = font_size
        self.font_size_modifier = 1.0
        self.font_vertical_shift = font_vertical_shift

        # Optional extras
        self.border_color = border_color
        self.border_size = border_size
        self.episode_text_color = episode_text_color
        self.episode_text_position = episode_text_location
        self.fit_text = fit_text
        self.hide_border = hide_border
        self.text_box_color = text_box_color
        self.text_box_height = text_box_height


    @property
    def title_text_commands(self) -> ImageMagickCommands:
        """
        Subcommand for adding title text to the source image.

        Returns:
            List of ImageMagick commands.
        """

        # No title text, or not being shown
        if len(self.title_text) == 0:
            return []

        # Font characteristics
        size = 150 * self.font_size * self.font_size_modifier
        kerning = 1.0 * self.font_kerning
        vertical_shift = 820 + self.font_vertical_shift

        return [
            f'-font "{self.font_file}"',
            f'-fill "{self.font_color}"',
            f'-pointsize {size}',
            f'-kerning {kerning}',
            f'-interline-spacing {self.font_interline_spacing}',
            f'-interword-spacing {self.font_interword_spacing}',
            f'-gravity center',
            f'-annotate +0+{vertical_shift} "{self.title_text}"',
        ]


    def index_text_commands(self,
            title_text_dimensions: Dimensions,
        ) -> ImageMagickCommands:
        """
        Subcommands for adding index text to the source image.

        Args:
            title_text_dimensions: Dimensions of the title text. For
                positioning the index text when the positioning mode
                is `compact`.

        Returns:
            List of ImageMagick commands.
        """

        # If not showing index text, return
        if self.hide_season_text and self.hide_episode_text:
            return []

        # Vertical positioning of all index text
        y_position = 810 + self.font_vertical_shift

        # Commands for season text
        season_text_command = []
        if not self.hide_season_text:
            if self.episode_text_position == 'compact':
                x_position = (self.WIDTH + title_text_dimensions.width) / 2 + 20
                season_text_command = [
                    f'-gravity east',
                    f'-annotate {x_position:+}{y_position:+} "{self.season_text}"',
                ]
            else:
                season_text_command = [
                    f'-gravity west',
                    f'-annotate +{self.border_size}{y_position:+} "{self.season_text}"',
                ]

        # Commands for episode text
        episode_text_command = []
        if not self.hide_episode_text:
            if self.episode_text_position == 'compact':
                x_position = (self.WIDTH + title_text_dimensions.width) / 2 + 20
                episode_text_command = [
                    f'-gravity west',
                    f'-annotate {x_position:+}{y_position:+} "{self.episode_text}"',
                ]
            else:
                episode_text_command = [
                    f'-gravity east',
                    f'-annotate +{self.border_size}{y_position:+} "{self.episode_text}"',
                ]

        font_size = 70 * self.font_size_modifier

        return [
            f'-font "{self.EPISODE_TEXT_FONT.resolve()}"',
            f'-fill "{self.episode_text_color}"',
            f'-pointsize {font_size}',
            f'-kerning 1',
            f'-interword-spacing 15',
            *season_text_command,
            *episode_text_command,
        ]


    @property
    def border_commands(self) -> ImageMagickCommands:
        """
        Subcommands to add the border to the image.

        Returns:
            List of ImageMagick commands.
        """

        # Border is not being shown, skip
        if self.hide_border:
            return []

        # Get each rectangle
        left_rectangle = Rectangle(
            Coordinate(0, 0),
            Coordinate(self.border_size, self.HEIGHT)
        )
        top_rectangle = Rectangle(
            Coordinate(0, 0),
            Coordinate(self.WIDTH, self.border_size)
        )
        right_rectangle = Rectangle(
            Coordinate(self.WIDTH - self.border_size, 0),
            Coordinate(self.WIDTH, self.HEIGHT)
        )

        return [
            f'-fill "{self.border_color}"',
            left_rectangle.draw(),
            top_rectangle.draw(),
            right_rectangle.draw(),
        ]


    @property
    def bottom_border_commands(self) -> ImageMagickCommands:
        """
        Subcommands to add the bottom border to the image.

        Returns:
            List of ImageMagick commands.
        """

        rectangle = Rectangle(
            Coordinate(0, self.HEIGHT - self.text_box_height),
            Coordinate(self.WIDTH, self.HEIGHT)
        )

        return [
            f'-fill "{self.text_box_color}"',
            rectangle.draw(),
        ]


    @staticmethod
    def modify_extras(
            extras: dict,
            custom_font: bool,
            custom_season_titles: bool,
        ) -> None:
        """
        Modify the given extras based on whether font or season titles
        are custom.

        Args:
            extras: Dictionary to modify.
            custom_font: Whether the font are custom.
            custom_season_titles: Whether the season titles are custom.
        """

        # Generic font, reset episode text and box colors
        if not custom_font:
            if 'episode_text_color' in extras:
                extras['episode_text_color'] =MarvelTitleCard.EPISODE_TEXT_COLOR
            if 'border_color' in extras:
                extras['border_color'] = 'white'


    @staticmethod
    def is_custom_font(font: 'Font') -> bool: # type: ignore
        """
        Determine whether the given font characteristics constitute a
        default or custom font.

        Args:
            font: The Font being evaluated.

        Returns:
            True if a custom font is indicated, False otherwise.
        """

        return ((font.color != MarvelTitleCard.TITLE_COLOR)
            or (font.file != MarvelTitleCard.TITLE_FONT)
            or (font.interline_spacing != 0)
            or (font.interword_spacing != 0)
            or (font.kerning != 1.0)
            or (font.size != 1.0)
            or (font.vertical_shift != 0)
        )


    @staticmethod
    def is_custom_season_titles(
            custom_episode_map: bool,
            episode_text_format: str,
        ) -> bool:
        """
        Determine whether the given attributes constitute custom or
        generic season titles.

        Args:
            custom_episode_map: Whether the EpisodeMap was customized.
            episode_text_format: The episode text format in use.

        Returns:
            True if custom season titles are indicated, False otherwise.
        """

        standard_etf = MarvelTitleCard.EPISODE_TEXT_FORMAT.upper()

        return (custom_episode_map
                or episode_text_format.upper() != standard_etf)


    def create(self) -> None:
        """
        Make the necessary ImageMagick and system calls to create this
        object's defined title card.
        """

        # Get the dimensions of the title and index text
        title_text_dimensions = self.get_text_dimensions(
            self.title_text_commands, width='max', height='sum',
        )

        # If fitting text, adjust font size if all text is too wide
        if self.fit_text:
            # Get dimensions of index text
            index_text_dimensions = self.get_text_dimensions(
                self.index_text_commands(title_text_dimensions),
                width='sum', height='sum',
            )

            # If text is too wide, scale font size
            width = title_text_dimensions.width + index_text_dimensions.width
            margin = 20 * (2 - self.hide_season_text - self.hide_episode_text)
            text_width = width + margin
            max_width = self.WIDTH - (2 * self.border_size)

            if text_width > max_width:
                self.font_size_modifier = max_width / text_width

                # Recalculate title text dimensions
                title_text_dimensions = self.get_text_dimensions(
                    self.title_text_commands, width='max', height='sum',
                )

        command = ' '.join([
            f'convert "{self.source_file.resolve()}"',
            # Resize and apply styles to source image
            *self.resize_and_style,
            # Resize to only fit in the bounds of the border
            f'-resize {self.WIDTH - (2 * self.border_size)}x',
            f'-extent {self.TITLE_CARD_SIZE}',
            # Add borders
            *self.border_commands,
            *self.bottom_border_commands,
            # Add text
            *self.title_text_commands,
            *self.index_text_commands(title_text_dimensions),
            # Create card
            *self.resize_output,
            f'"{self.output_file.resolve()}"',
        ])

        self.image_magick.run(command)