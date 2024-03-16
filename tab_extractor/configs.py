import dataclasses
from typing import Any


@dataclasses.dataclass
class Config:
    pass


@dataclasses.dataclass
class ExtractionConfig(Config):

    method: str = "diff_thresholding"


@dataclasses.dataclass
class DiffThresholdingExtractionConfig(ExtractionConfig):

    method: str = "diff_thresholding"

    diff_threshold: float = 10
