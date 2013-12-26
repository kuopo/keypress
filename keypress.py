import termios, fcntl, sys, os
import json

#sys.path.append("./pubsub")
from pubsub_client import MsgHub


#msghub = MsgHub("pubsub.msghub.io", 443, secure=True)
msghub = MsgHub("https://pubsub.msghub.io", 443)
#msghub = MsgHub("pubsub.msghub.io", 12345)

def cb(ch, msg):
    handle_keypress(msg['ch'])

msghub.subscribe("keypress", cb)


def handle_keypress(ch):
    if ch == '\x7f':
        sys.stdout.write('\033[1D \033[1D')
    elif ch == '\x1b':
        pass
    else:
        sys.stdout.write(ch)

fd = sys.stdin.fileno()
oldterm = termios.tcgetattr(fd)
newattr = termios.tcgetattr(fd)
newattr[3] = newattr[3] & ~termios.ICANON & ~termios.ECHO
termios.tcsetattr(fd, termios.TCSANOW, newattr)

oldflags = fcntl.fcntl(fd, fcntl.F_GETFL)
fcntl.fcntl(fd, fcntl.F_SETFL, oldflags | os.O_NONBLOCK)

try:
    while True:
        try:
            c = sys.stdin.read(1)
            msghub.publish("keypress", {"ch": c, "key": None}, False)
#            msghub.publish("keypress", c, True)
            handle_keypress(c)
#            print "Got character", repr(c)
        except IOError: pass
finally:
    termios.tcsetattr(fd, termios.TCSAFLUSH, oldterm)
    fcntl.fcntl(fd, fcntl.F_SETFL, oldflags)
