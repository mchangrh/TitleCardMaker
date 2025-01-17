from abc import ABC, abstractmethod
from typing import Optional

from modules.EpisodeInfo import EpisodeInfo
from modules.SeriesInfo import SeriesInfo


class EpisodeDataSource(ABC):
    """
    This class describes an abstract episode data source. Classes of
    this type define sources of Episode data.
    """


    @property
    @abstractmethod
    def SERIES_IDS(self) -> tuple[str]:
        """Valid SeriesInfo ID's that can be set by this data source."""
        raise NotImplementedError


    @abstractmethod
    def set_series_ids(self,
            library_name: Optional[str],
            series_info: SeriesInfo,
        ) -> None:
        """Set the series ID's for the given SeriesInfo object."""

        raise NotImplementedError


    @abstractmethod
    def set_episode_ids(self,
            library_name: Optional[str],
            series_info: SeriesInfo,
            episode_infos: list[EpisodeInfo],
            *,
            inplace: bool = False,
        ) -> None:
        """Set the episode ID's for the given EpisodeInfo objects."""

        raise NotImplementedError


    @abstractmethod
    def get_all_episodes(self,
            library_name: str,
            series_info: SeriesInfo,
            episode_infos: Optional[list[EpisodeInfo]] = None,
        ) -> list[EpisodeInfo]:
        """Get all the EpisodeInfo objects associated with the given series."""

        raise NotImplementedError
