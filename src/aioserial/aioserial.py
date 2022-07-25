import array
import asyncio
import concurrent.futures
from typing import List, Optional, Union

import serial


class AioSerial(serial.Serial):

    def __init__(
            self,
            port: Optional[str] = None,
            baudrate: int = 9600,
            bytesize: int = serial.EIGHTBITS,
            parity: str = serial.PARITY_NONE,
            stopbits: Union[float, int] = serial.STOPBITS_ONE,
            timeout: Optional[float] = None,
            xonxoff: bool = False,
            rtscts: bool = False,
            write_timeout: Optional[float] = None,
            dsrdtr: bool = False,
            inter_byte_timeout: Optional[float] = None,
            exclusive: Optional[bool] = None,
            loop: Optional[asyncio.AbstractEventLoop] = None,
            **kwargs):
        super().__init__(
            port=port,
            baudrate=baudrate,
            bytesize=bytesize,
            parity=parity,
            stopbits=stopbits,
            timeout=timeout,
            xonxoff=xonxoff,
            rtscts=rtscts,
            write_timeout=write_timeout,
            dsrdtr=dsrdtr,
            inter_byte_timeout=inter_byte_timeout,
            exclusive=exclusive,
            **kwargs)
        self._loop: Optional[asyncio.AbstractEventLoop] = loop
        self._read_executor = \
            concurrent.futures.ThreadPoolExecutor(max_workers=1)
        self._write_executor = \
            concurrent.futures.ThreadPoolExecutor(max_workers=1)

    @property
    def loop(self) -> Optional[asyncio.AbstractEventLoop]:
        self.write(b'')
        return self._loop if self._loop else asyncio.get_running_loop()

    @loop.setter
    def loop(self, value: Optional[asyncio.AbstractEventLoop]):
        self.loop = value

    async def read_async(self, size: int = 1) -> bytes:
        return await self.loop.run_in_executor(
            self._read_executor, self.read, size)

    async def read_until_async(
            self,
            expected: bytes = serial.LF,
            size: Optional[int] = None) -> bytes:
        return await self.loop.run_in_executor(
            self._read_executor, self.read_until, expected, size)

    async def readinto_async(self, b: Union[array.array, bytearray]):
        return await self.loop.run_in_executor(
            self._read_executor, self.readinto, b)

    async def readline_async(self, size: int = -1) -> bytes:
        return await self.loop.run_in_executor(
            self._read_executor, self.readline, size)

    async def readlines_async(self, hint: int = -1) -> List[bytes]:
        return await self.loop.run_in_executor(
            self._read_executor, self.readlines, hint)

    async def write_async(
            self, data: Union[bytearray, bytes, memoryview]) -> int:
        return await self.loop.run_in_executor(
            self._write_executor, self.write, data)

    async def writelines_async(
            self, lines: List[Union[bytearray, bytes, memoryview]]) -> int:
        return await self.loop.run_in_executor(
            self._write_executor, self.writelines, lines)
