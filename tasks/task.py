from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
import asyncio


class JobStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    SUCCEEDED = "succeeded"
    FAILED = "failed"
    CANCELLED = "cancelled"


@dataclass(frozen=True, slots=True)
class JobResult:
    job_id: str
    status: JobStatus
    message: str
    duration_ms: float


class Job(ABC):
    def __init__(self, job_id: str, name: str, priority: int = 3) -> None:
        self.id = job_id
        self.name = name
        self.priority = priority
        self.status = JobStatus.PENDING

    @property
    def priority(self) -> int:
        return self._priority

    @priority.setter
    def priority(self, value: int) -> None:
        # TODO: validate 1 through 5, then store in self._priority
        if value<1 or value >5 :
            raise ValueError("priority must be between 1 and 5")
            # return
        self._priority = value

    @abstractmethod
    async def execute(self) -> JobResult:
        ...


class HttpJob(Job):
    def __init__(self, job_id: str,name:str,url:str,priority:int =3,delay_in_seconds:float = 0.5)->None:
        super().__init__(job_id,name,priority)
        self._url = url
        self._delay_in_seconds = delay_in_seconds

    @property
    def delay_in_seconds(self) -> float:
        return self._delay_in_seconds

    @delay_in_seconds.setter
    def delay_in_seconds(self, value: float) -> None:
        if value < 0:
            raise ValueError("delay_in_seconds must be greater than 0")
        self._delay_in_seconds = value

    @property
    def url(self)-> str:
        return self._url
    
    @url.setter
    def url(self,value:str)->None:
        if not value.startswith("http"):
            raise ValueError("url must start with http")
        self._url = value

    async def execute(self) -> JobResult:
        self.status = JobStatus.RUNNING
        await asyncio.sleep(self.delay_in_seconds)
        self.status = JobStatus.SUCCEEDED
        return JobResult(job_id=self.id,status=JobStatus.SUCCEEDED,message="Job executed successfully",duration_ms=self.delay_in_seconds*1000)
       
        
