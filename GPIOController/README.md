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

- [OpenJTalk](http://open-jtalk.sp.nitech.ac.jp/)

    ```sh
    $ sudo apt-get install open-jtalk open-jtalk-mecab-naist-jdic htsengine libhtsengine-dev hts-voice-nitech-jp-atr503-m001
    $ wget http://downloads.sourceforge.net/project/mmdagent/MMDAgent_Example/MMDAgent_Example-1.3/MMDAgent_Example-1.3.zip
    $ unzip MMDAgent_Example-1.3.zip
    $ sudo cp -R MMDAgent_Example-1.3/Voice/* /usr/share/hts-voice/
    ```

## License

MIT
