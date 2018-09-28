=========
aioserial
=========

Python asynchronous serial module for combining ``asyncio`` and ``pyserial``.

Quick start
===========

AioSerial
---------

.. code:: py

    import aioserial
    import serial

    isinstance(aioserial.AioSerial(), serial.Serial)
    True

    issubclass(aioserial.AioSerial, serial.Serial)
    True

Constructor
```````````

.. code:: py

    aioserial_instance: aioserial.AioSerial = aioserial.AioSerial(
        # ... same with what can be passed to serial.Serial ...,
        loop: Optional[asyncio.AbstractEventLoop] = None)

Methods
```````

read_async
::::::::::

.. code:: py

    bytes_read: bytes = \
        await aioserial_instance.read_async(size: int = 1)

read_until_async
::::::::::::::::

.. code:: py

    at_most_certain_size_of_bytes_read: bytes = \
        await aioserial_instance.read_until_async(
            expected: bytes = serial.LF, size: Optional[int] = None)

readinto_async
::::::::::::::

.. code:: py

    number_of_byte_read: int = \
        await aioserial_instance.readinto_async(b: Union[array.array, bytearray])

readline_async
::::::::::::::

.. code:: py

    a_line_of_at_most_certain_size_of_bytes_read: bytes = \
        await aioserial_instance.readline_async(size: int = -1)

readlines_async
:::::::::::::::

.. code:: py

    lines_of_at_most_certain_size_of_bytes_read: bytes = \
        await aioserial_instance.readlines_async(hint: int = -1)

write_async
:::::::::::

.. code:: py

    number_of_byte_like_data_written: int = \
        await aioserial_instance.write_async(bytes_like_data)

writelines_async
::::::::::::::::

.. code:: py

    number_of_byte_like_data_in_the_given_list_written: int = \
        await aioserial_instance.writelines_async(list_of_bytes_like_data)

Other APIs
``````````

All the other APIs in ``serial.Serial`` are supported in aioserial.AioSerial as original.
