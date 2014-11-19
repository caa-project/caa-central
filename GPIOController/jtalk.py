# -*- coding: utf-8 -*-

import subprocess
import threading


EMOTIONS = ['normal', 'angry', 'bashful', 'happy', 'sad']

def say(message, emotion=EMOTIONS[0]):
    if emotion not in EMOTIONS:
        emotion = EMOTIONS[0] # 'normal'

    env = {"TMP": "/tmp/jsay.wav"}
    commands = """echo '{0:s}' | open_jtalk \
-td tree-dur.inf \
-tf tree-lf0.inf \
-tm tree-mgc.inf \
-tl tree-lpf.inf \
-md dur.pdf \
-mf lf0.pdf \
-mm mgc.pdf \
-ml lpf.pdf \
-dm mgc.win1 \
-dm mgc.win2 \
-dm mgc.win3 \
-df lf0.win1 \
-df lf0.win2 \
-df lf0.win3 \
-dl lpf.win1 \
-ef tree-gv-lf0.inf \
-em tree-gv-mgc.inf \
-cf gv-lf0.pdf \
-cm gv-mgc.pdf \
-k gv-switch.inf \
-s 48000 \
-z 6000 \
-p 240 \
-a 0.55 \
-u 0.0 \
-jm 0.7 \
-jf 0.5 \
-jl 1.0 \
-x /var/lib/mecab/dic/open-jtalk/naist-jdic \
-ow $TMP && \
aplay --quiet $TMP
rm -f $TMP""".format(message)

    proc = subprocess.Popen(commands,
            cwd='/usr/share/hts-voice/mei_{0:s}'.format(emotion),
            env=env, shell=True)

    thread = threading.Thread(target=proc.wait)
    thread.start()


if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        say(''.join(sys.argv[1:]), "normal")
