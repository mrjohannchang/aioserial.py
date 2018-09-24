import asyncio
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

    @property
    def loop(self) -> Optional[asyncio.AbstractEventLoop]:
        self.write(b'')
        return self._loop if self._loop else asyncio.get_running_loop()

    @loop.setter
    def loop(self, value: Optional[asyncio.AbstractEventLoop]):
        self.loop = value

    async def read_async(self, size: Optional[int] = None) -> bytes:
        res: bytes = b''

        if size is None:
            size = self.in_waiting

        while size > 0:
            min_size: int = min(size, self.in_waiting)
            res += self.read(min_size)
            size -= min_size
            if size > 0:
                await asyncio.sleep(0.01, loop=self.loop)

        return res

    async def readline_async(self, size: int = -1) -> bytes:
        return await self.read_until_async(expected=serial.LF, size=size)

    async def readlines_async(self, hint: int = -1) -> List[bytes]:
        res: List[bytes] = []

        if hint < 0:
            hint = self.in_waiting

        while hint > 0:
            res.append(await self.readline_async())
            hint -= len(res[-1])

        return res

    async def read_until_async(
            self,
            expected: bytes = serial.LF,
            size: Optional[int] = None) -> bytes:
        res: bytes = b''

        if size is None:
            size = -1

        while size != 0:
            size -= 1
            res += await self.read_async(1)
            if res.endswith(expected):
                size = 0

        return res

    async def write_async(
            self, data: Union[bytearray, bytes, memoryview]) -> int:
        res: int = 0
        data_length: int = len(data)
        step: int = int(self.baudrate * 0.01)

        i: int
        for i in range(0, data_length, step):
            res += self.write(data[i:i+step])

            if i + step < data_length:
                await asyncio.sleep(0.01, loop=self.loop)

        return res

    async def writelines_async(
            self, lines: List[Union[bytearray, bytes, memoryview]]) -> int:
        line: Union[bytearray, bytes, memoryview]
        return sum(await self.write_async(line) for line in lines)
