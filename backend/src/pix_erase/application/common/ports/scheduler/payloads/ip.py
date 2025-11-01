from dataclasses import dataclass

from pix_erase.application.common.ports.scheduler.payloads.base import TaskPayload


@dataclass(frozen=True)
class AnalyzeDomainPayload(TaskPayload):
    domain: str
    timeout: float
