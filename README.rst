=========
aioserial
=========

Python asynchronous serial module for combining ``asyncio`` and ``pyserial``.

Quick start
===========

Constructor
-----------

.. code:: py

    import aioserial

    aioserial_instance: aioserial.AioSerial = aioserial.AioSerial(
        SAME_WITH_PYSERIAL...,
        loop=None)

Asynchronously Read
-------------------

read_async
``````````

.. code:: py

    bytes_read: bytes = \
        await aioserial_instance.read_async(size: int = 1)

read_until_async
````````````````

.. code:: py

    import serial

    at_most_certain_size_of_bytes_read: bytes = \
        await aioserial_instance.read_until_async(
            expected: bytes = serial.LF, size: Optional[int] = None)

readinto_async
``````````````

.. code:: py

   import array

    number_of_byte_read: int = \
        await aioserial_instance.readinto_async(b: Union[array.array, bytearray])

readline_async
``````````````

.. code:: py

    a_line_of_at_most_certain_size_of_bytes_read: bytes = \
        await aioserial_instance.readline_async(size: int = -1)

readlines_async
```````````````

.. code:: py

    lines_of_at_most_certain_size_of_bytes_read: bytes = \
        await aioserial_instance.readlines_async(hint: int = -1)

Asynchronously Write
--------------------

write_async
```````````

.. code:: py

    number_of_byte_like_data_written: int = \
        await aioserial_instance.write_async(bytes_like_data)

writelines_async
````````````````

.. code:: py

    number_of_byte_like_data_in_the_given_list_written: int = \
        await aioserial_instance.writelines_async(list_of_bytes_like_data)
