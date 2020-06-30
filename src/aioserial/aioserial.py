# Copyright 2020 Henry Chang
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import array
import asyncio
import concurrent.futures
import sys
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
            timeout: Optional[Union[float, int]] = None,
            xonxoff: bool = False,
            rtscts: bool = False,
            write_timeout: Optional[Union[float, int]] = None,
            dsrdtr: bool = False,
            inter_byte_timeout: Optional[Union[float, int]] = None,
            exclusive: Optional[bool] = None,
            loop: Optional[asyncio.AbstractEventLoop] = None,
            cancel_read_timeout: int = 1,
            cancel_write_timeout: int = 1,
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

        self._cancel_read_executor: concurrent.futures.ThreadPoolExecutor = \
            concurrent.futures.ThreadPoolExecutor(max_workers=1)
        self._cancel_read_timeout: int = cancel_read_timeout
        self._read_executor: concurrent.futures.ThreadPoolExecutor = \
            concurrent.futures.ThreadPoolExecutor(max_workers=1)
        self._read_lock: asyncio.Lock = asyncio.Lock()

        self._cancel_write_executor: concurrent.futures.ThreadPoolExecutor = \
            concurrent.futures.ThreadPoolExecutor(max_workers=1)
        self._cancel_write_timeout: int = cancel_write_timeout
        self._write_executor: concurrent.futures.ThreadPoolExecutor = \
            concurrent.futures.ThreadPoolExecutor(max_workers=1)
        self._write_lock: asyncio.Lock = asyncio.Lock()

    @property
    def loop(self) -> Optional[asyncio.AbstractEventLoop]:
        return self._loop if self._loop else asyncio.get_running_loop() \
                if sys.version_info >= (3, 7) else asyncio.get_event_loop()

    @loop.setter
    def loop(self, value: Optional[asyncio.AbstractEventLoop]):
        self._loop = value

    async def _cancel_read_async(self):
        if not hasattr(self, 'cancel_read'):
            return
        await asyncio.wait_for(
            self.loop.run_in_executor(
                self._cancel_read_executor, self.cancel_read),
            self._cancel_read_timeout)

    async def _cancel_write_async(self):
        if not hasattr(self, 'cancel_write'):
            return
        await asyncio.wait_for(
            self.loop.run_in_executor(
                self._cancel_write_executor, self.cancel_write),
            self._cancel_write_timeout)

    async def read_async(self, size: int = 1) -> bytes:
        async with self._read_lock:
            try:
                return await self.loop.run_in_executor(
                    self._read_executor, self.read, size)
            except asyncio.CancelledError:
                await asyncio.shield(self._cancel_read_async())
                raise

    async def read_until_async(
            self,
            expected: bytes = serial.LF,
            size: Optional[int] = None) -> bytes:
        async with self._read_lock:
            try:
                return await self.loop.run_in_executor(
                    self._read_executor, self.read_until, expected, size)
            except asyncio.CancelledError:
                await asyncio.shield(self._cancel_read_async())
                raise

    async def readinto_async(self, b: Union[array.array, bytearray]):
        async with self._read_lock:
            try:
                return await self.loop.run_in_executor(
                    self._read_executor, self.readinto, b)
            except asyncio.CancelledError:
                await asyncio.shield(self._cancel_read_async())
                raise

    async def readline_async(self, size: int = -1) -> bytes:
        async with self._read_lock:
            try:
                return await self.loop.run_in_executor(
                    self._read_executor, self.readline, size)
            except asyncio.CancelledError:
                await asyncio.shield(self._cancel_read_async())
                raise

    async def readlines_async(self, hint: int = -1) -> List[bytes]:
        async with self._read_lock:
            try:
                return await self.loop.run_in_executor(
                    self._read_executor, self.readlines, hint)
            except asyncio.CancelledError:
                await asyncio.shield(self._cancel_read_async())
                raise

    async def write_async(
            self, data: Union[bytearray, bytes, memoryview]) -> int:
        async with self._write_lock:
            try:
                return await self.loop.run_in_executor(
                    self._write_executor, self.write, data)
            except asyncio.CancelledError:
                await asyncio.shield(self._cancel_write_async())
                raise

    async def writelines_async(
            self, lines: List[Union[bytearray, bytes, memoryview]]):
        async with self._write_lock:
            try:
                return await self.loop.run_in_executor(
                    self._write_executor, self.writelines, lines)
            except asyncio.CancelledError:
                await asyncio.shield(self._cancel_write_async())
                raise
