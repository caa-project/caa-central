GPIOControler
=============

## Usage

### setup

    ```sh
    $ sudo nano /boot/config.txt
    hdmi_drive=2をアンコメント
    ```

### using with websocket

    ```sh
    $ sudo ./main.py [servername=localhost:5000]
    ```

## Dependency

- [websocket-client](https://github.com/liris/websocket-client)

    ```sh
    $ pip install websocket-client
    ```

- [PiBits/ServoBlaster](https://github.com/richardghirst/PiBits)

    ```sh
    $ cd PiBits/ServoBlaster/user
    $ sudo make install
    ```

## License

MIT
