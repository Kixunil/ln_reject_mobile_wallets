import sys
import urllib.request

def check_donate():
    if len(sys.argv) > 1 and sys.argv[1] == "--donate":
        amount = 50000
        memo = ""
        if len(sys.argv) > 2:
            amount = int(sys.argv[2])
            if len(sys.argv) > 3:
                memo = sys.argv[3]

        with request.urlopen("https://ln-ask.me/donate/%d/%s" % (amount, memo)) as invoice:
            return invoice.read()

    else:
        return None
