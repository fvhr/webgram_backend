import asyncio
from dataclasses import dataclass

import psutil

from src.application.common.dtos.system_resources import DiskDTO, CPUDTO, RAMDTO
from src.application.common.ports.external import GetSystemResourcesProtocol
from src.logger import logger


@dataclass
class GetSystemResources(GetSystemResourcesProtocol):
    async def get_ram(self) -> RAMDTO:
        try:
            mem = psutil.virtual_memory()
            total_gb = round(mem.total / (1024 ** 3), 1)
            used_gb = round(mem.used / (1024 ** 3), 1)
            free_gb = total_gb - used_gb
            return RAMDTO(total_gb=total_gb, used_gb=used_gb, free_gb=free_gb)
        except Exception as ex:
            logger.print_exception(f'не удалось получить данные по ram: {ex}')
            return RAMDTO(total_gb=0.0, used_gb=0.0, free_gb=0.0)

    async def get_cpu(self) -> CPUDTO:
        try:
            cpu_usage_percent = await asyncio.to_thread(psutil.cpu_percent, interval=1)
            cpu_free_percent = 100.0 - cpu_usage_percent
            return CPUDTO(cpu_free_percent=cpu_free_percent, cpu_usage_percent=cpu_usage_percent)
        except Exception as ex:
            logger.print_exception(f'не удалось получить данные по cpu: {ex}')
            return CPUDTO(cpu_free_percent=0.0, cpu_usage_percent=0.0)

    async def get_disk(self) -> DiskDTO:
        try:
            disk = psutil.disk_usage('/')
            total_gb = round(disk.total / (1024 ** 3), 1)
            used_gb = round(disk.used / (1024 ** 3), 1)
            free_gb = round(disk.free / (1024 ** 3), 1)
            return DiskDTO(total_gb=total_gb, used_gb=used_gb, free_gb=free_gb)
        except Exception as ex:
            logger.print_exception(f'не удалось получить данные по disk: {ex}')
            return DiskDTO(total_gb=0.0, used_gb=0.0, free_gb=0.0)
