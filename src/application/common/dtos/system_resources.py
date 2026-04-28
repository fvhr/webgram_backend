from dataclasses import dataclass

from src.application.common.dto import DTO


@dataclass
class RAMDTO(DTO):
    total_gb: float
    used_gb: float
    free_gb: float


@dataclass
class DiskDTO(DTO):
    total_gb: float
    used_gb: float
    free_gb: float


@dataclass
class CPUDTO(DTO):
    cpu_usage_percent: float
    cpu_free_percent: float
