# aioserial

* [Quick start](#quick-start)
    + [A simple serial port reader](#a-simple-serial-port-reader)
    + [pyserial-asyncio example replacement](#pyserial-asyncio-example-replacement)
* [API](#api)
    + [AioSerial](#aioserial)
        - [Constructor](#constructor)
        - [Methods](#methods)
            * [read_async](#read-async)
            * [read_until_async](#read-until-async)
            * [readinto_async](#readinto-async)
            * [readline_async](#readline-async)
            * [readlines_async](#readlines-async)
            * [write_async](#write-async)
            * [writelines_async](#writelines-async)
    + [Other APIs](#other-apis)
* [Why aioserial?](#why-aioserial-)

A Python package that combines [asyncio](https://docs.python.org/3/library/asyncio.html) and [pySerial](https://pypi.org/project/pyserial/).

## Quick start

### A simple serial port reader

```py
import asyncio

import aioserial


async def read_and_print(aioserial_instance: aioserial.AioSerial):
    while True:
        print((await aioserial_instance.read_async()).decode(errors='ignore'), end='', flush=True)

asyncio.run(read_and_print(aioserial.AioSerial(port='COM1')))
```

### pyserial-asyncio example replacement

**The example usage from pyserial-asyncio**

https://pyserial-asyncio.readthedocs.io/en/latest/shortintro.html

```py
import asyncio
import serial_asyncio

class Output(asyncio.Protocol):
    def connection_made(self, transport):
        self.transport = transport
        print('port opened', transport)
        transport.serial.rts = False  # You can manipulate Serial object via transport
        transport.write(b'Hello, World!\n')  # Write serial data via transport

    def data_received(self, data):
        print('data received', repr(data))
        if b'\n' in data:
            self.transport.close()

    def connection_lost(self, exc):
        print('port closed')
        self.transport.loop.stop()

    def pause_writing(self):
        print('pause writing')
        print(self.transport.get_write_buffer_size())

    def resume_writing(self):
        print(self.transport.get_write_buffer_size())
        print('resume writing')

loop = asyncio.get_event_loop()
coro = serial_asyncio.create_serial_connection(loop, Output, '/dev/ttyUSB0', baudrate=115200)
loop.run_until_complete(coro)
loop.run_forever()
loop.close()
```

**aioserial equivalence**

```py
import asyncio

import aioserial


async def read_and_print(aioserial_instance: aioserial.AioSerial):
    while True:
        data: bytes = await aioserial_instance.read_async()
        print(data.decode(errors='ignore'), end='', flush=True)
        if b'\n' in data:
            aioserial_instance.close()
            break

aioserial_instance: aioserial.AioSerial = aioserial.AioSerial(port='/dev/ttyUSB0', baudrate=115200)
asyncio.run(asyncio.gather(read_and_print(aioserial_instance), aioserial_instance.write_async(b'Hello, World!\n')))
```

## API

### AioSerial

```py
>>> import aioserial
>>> import serial

>>> isinstance(aioserial.AioSerial(), serial.Serial)
True

>>> issubclass(aioserial.AioSerial, serial.Serial)
True

>>> aioserial.Serial is serial.Serial
True
```

#### Constructor

```py
aioserial_instance: aioserial.AioSerial = aioserial.AioSerial(
    # ... same with what can be passed to serial.Serial ...,
    loop: Optional[asyncio.AbstractEventLoop] = None,
    cancel_read_timeout: int = 1,
    cancel_write_timeout: int = 1)
```

#### Methods


##### read_async

```py
bytes_read: bytes = \
    await aioserial_instance.read_async(size: int = 1)
```

##### read_until_async

```py
at_most_certain_size_of_bytes_read: bytes = \
    await aioserial_instance.read_until_async(
        expected: bytes = aioserial.LF, size: Optional[int] = None)
```

##### readinto_async

```py
number_of_byte_read: int = \
    await aioserial_instance.readinto_async(b: Union[array.array, bytearray])
```

##### readline_async

```py
a_line_of_at_most_certain_size_of_bytes_read: bytes = \
    await aioserial_instance.readline_async(size: int = -1)
```

##### readlines_async

```py
lines_of_at_most_certain_size_of_bytes_read: bytes = \
    await aioserial_instance.readlines_async(hint: int = -1)
```

##### write_async

```py
number_of_byte_like_data_written: int = \
    await aioserial_instance.write_async(bytes_like_data)
```

##### writelines_async

```py
number_of_byte_like_data_in_the_given_list_written: int = \
    await aioserial_instance.writelines_async(list_of_bytes_like_data)
```

### Other APIs

All the other APIs in the mother package [pySerial](https://pypi.org/project/pyserial/) are supported in aioserial as-is.

## Why aioserial?

* Want to use an asyncio-based but not a (self-built) thread-based serial library.
* [pySerial-asyncio](https://pypi.org/project/pyserial-asyncio/) does [not support Windows](https://github.com/pyserial/pyserial-asyncio/issues/3).
* APIs in all the other packages ([pySerial-asyncio](https://pypi.org/project/pyserial-asyncio/),
    [asyncserial](https://pypi.org/project/asyncserial/)) that target the same goal are not designed in high level.
