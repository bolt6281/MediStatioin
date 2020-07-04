import pyzbar.pyzbar as pyzbar
from pylibdmtx import pylibdmtx

def scanner(frame):
    # try to detect barcode
    decoded = pyzbar.decode(frame)
    if decoded != []: # scanned barcode
        data = str(decoded[0][0])[2:-1]
        return data

    # try to detect data matrix
    decoded = pylibdmtx.decode(frame)
    if decoded != []: # scanned dtmx
        data = decoded[0][0].decode('utf-8')
        return data
    return "nothing detected"