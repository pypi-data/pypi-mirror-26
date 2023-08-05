#!/usr/bin/env python3
import __future__
import sys
import logging
import platform
import serial
import serial.tools.list_ports
from time import sleep, time
import math
import array
from ctypes import *
try:
    import fcntl
    try:
        from . import bridge
    except Exception:
        import bridge
except ImportError:
    fcntl = None
    bridge = None
if sys.version_info[0] == 2:
    import struct

LOG_FORMAT = '%(asctime)s %(levelname)s: %(message)s'

ACK = b'\x79'
NACK = b'\x1F'


class SerialPort:
    def __init__(self, device):
        self.ser = None
        self.ser = serial.Serial(device,
                                 baudrate=921600,  # 1152000,
                                 bytesize=serial.EIGHTBITS,
                                 parity=serial.PARITY_EVEN,
                                 stopbits=serial.STOPBITS_ONE,
                                 timeout=0.1,
                                 xonxoff=False,
                                 rtscts=False,
                                 dsrdtr=False)
        self._connect = False

        self._lock()
        self._speed_up()

        self.reset_input_buffer = self.ser.reset_input_buffer
        self.reset_output_buffer = self.ser.reset_output_buffer

        self.write = self.ser.write
        self.read = self.ser.read
        self.flush = self.ser.flush

    def __del__(self):
        self._unlock()

    def _lock(self):
        if not fcntl or not self.ser:
            return
        fcntl.flock(self.ser.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
        logging.debug('_lock')

    def _unlock(self):
        if not fcntl or not self.ser:
            return
        fcntl.flock(self.ser.fileno(), fcntl.LOCK_UN)
        logging.debug('_unlock')

    def _speed_up(self):
        if not fcntl:
            return
        if platform.system() != 'Linux':
            return

        logging.debug('_speed_up')

        TIOCGSERIAL = 0x0000541E
        TIOCSSERIAL = 0x0000541F
        ASYNC_LOW_LATENCY = 0x2000

        class serial_struct(Structure):
            _fields_ = [("type", c_int),
                        ("line", c_int),
                        ("port", c_uint),
                        ("irq", c_int),
                        ("flags", c_int),
                        ("xmit_fifo_size", c_int),
                        ("custom_divisor", c_int),
                        ("baud_base", c_int),
                        ("close_delay", c_ushort),
                        ("io_type", c_byte),
                        ("reserved_char", c_byte * 1),
                        ("hub6", c_uint),
                        ("closing_wait", c_ushort),
                        ("closing_wait2", c_ushort),
                        ("iomem_base", POINTER(c_ubyte)),
                        ("iomem_reg_shift", c_ushort),
                        ("port_high", c_int),
                        ("iomap_base", c_ulong)]

        buf = serial_struct()

        try:
            fcntl.ioctl(self.ser.fileno(), TIOCGSERIAL, buf)
            buf.flags |= ASYNC_LOW_LATENCY
            fcntl.ioctl(self.ser.fileno(), TIOCSSERIAL, buf)
        except Exception as e:
            logging.exception(e)

    def reset_sequence(self):
        self.ser.rts = True
        self.ser.dtr = True
        sleep(0.1)

        self.ser.rts = True
        self.ser.dtr = False
        sleep(0.1)

        self.ser.dtr = True
        self.ser.rts = False
        sleep(0.1)

        self.ser.dtr = False


class Flash_Serial(object):
    def __init__(self, device):
        self.ser = None
        if bridge and 'hidraw' in device:
            self.ser = bridge.SerialPort(device)
        else:
            self.ser = SerialPort(device)

    def connect(self):
        if not self._connect:
            logging.debug('connect')
            for i in range(3):
                self._connect = self.start_bootloader()
                if self._connect:
                    return True
                logging.info('repeate reset')
                sleep(0.5)
        return self._connect

    def set_disconnect(self):
        self._connect = False

    def reconnect(self):
        self._connect = False
        return self.connect()

    def start_bootloader(self):
        self.ser.reset_sequence()

        sleep(0.001)

        for i in range(5):
            self.ser.reset_input_buffer()
            self.ser.reset_output_buffer()
            self.ser.write([0x7f])
            self.ser.flush()
            if self._wait_for_ack():
                return True
            sleep(0.01)
        return False

    def _read_data(self, length, start_ack=True, stop_ack=True):
        if start_ack and not self._wait_for_ack():
            return
        data = b''
        i = 10
        while len(data) < length:
            data += self.ser.read(length - len(data))
            i -= 1
            if i == 0:
                return
        if stop_ack and not self._wait_for_ack():
            return
        return data

    def get_command(self):
        if not self.connect():
            return
        self.ser.write([0x00, 0xff])
        self.ser.flush()
        n, bootloader_version = self._read_data(2, start_ack=True, stop_ack=False)
        if sys.version_info[0] == 2:
            n = ord(n)
            bootloader_version = ord(bootloader_version)
        command = self._read_data(n, start_ack=False, stop_ack=True)
        return n, bootloader_version, command

    def get_version(self):
        if not self.connect():
            return
        self.ser.write([0x01, 0xfe])
        self.ser.flush()
        return self._read_data(3)

    def get_ID(self):
        if not self.connect():
            return
        self.ser.write([0x02, 0xfd])
        self.ser.flush()
        return self._read_data(3)

    def read_memory(self, start_address, length):
        logging.debug('_read_memory %x %i' % (start_address, length))
        if length > 256 or length < 0:
            return

        if not self.connect():
            return

        sa = self._int_to_bytes(start_address)
        xor = self._calculate_xor(sa)
        self.ser.write([0x11, 0xee])
        self.ser.flush()

        # if not self._wait_for_ack():
        #     return

        self.ser.write(sa)
        self.ser.write([xor])
        self.ser.flush()

        # if not self._wait_for_ack():
        #     return

        n = length - 1
        self.ser.write([n, 0xff ^ n])
        self.ser.flush()

        if self.ser.read(3) != b'\x79\x79\x79':
            return

        data = self._read_data(length, start_ack=False, stop_ack=False)

        return data

    def extended_erase_memory(self, pages):
        logging.debug('extended_erase_memory pages=%s' % pages)
        if not pages or len(pages) > 80:
            return

        if not self.connect():
            return

        self.ser.write([0x44, 0xbb])
        self.ser.flush()

        if not self._wait_for_ack():
            return

        data = [0x00, len(pages) - 1]

        for page in pages:
            data.append((page >> 8) & 0xff)
            data.append(page & 0xff)

        data.append(self._calculate_xor(data))

        self.ser.write(data)

        return self._wait_for_ack()

    def write_memory(self, start_address, data):
        logging.debug('_write_memory start_address=%x len(data)=%i' % (start_address, len(data)))

        if len(data) > 256:
            return

        if not self.connect():
            return

        mod = len(data) % 4
        if mod != 0:
            data += bytearray([0] * mod)

        sa = self._int_to_bytes(start_address)
        xor = self._calculate_xor(sa)
        data_xor = self._calculate_xor(data)

        self.ser.write([0x31, 0xce])
        self.ser.write(sa)
        self.ser.write([xor])
        self.ser.flush()

        if self.ser.read(2) != b'\x79\x79':
            return

        length = len(data) - 1
        self.ser.write([length])
        self.ser.write(data)
        self.ser.write([length ^ data_xor])
        self.ser.flush()

        return self._wait_for_ack()

    def go(self, start_address):
        logging.debug('go %x' % start_address)
        if not self.connect():
            return

        self.ser.write([0x21, 0xde])
        self.ser.flush()

        if not self._wait_for_ack():
            return

        sa = self._int_to_bytes(start_address)
        xor = self._calculate_xor(sa)

        self.ser.write(sa)
        self.ser.write([xor])
        self.ser.flush()

        return self._wait_for_ack()

    def _calculate_xor(self, data):
        xor = 0
        if isinstance(data, str):
            data = map(ord, data)
        for v in data:
            xor ^= v
        return xor

    def _int_to_bytes(self, value):
        if sys.version_info[0] == 2:
            return struct.pack('>I', value)
        return value.to_bytes(4, 'big', signed=False)

    def _wait_for_ack(self, n=3):
        for i in range(n):
            c = self.ser.read(1)
            if c:
                if c == ACK:
                    return True
                return False
        return False


def _run_connect(api):
    i = 0
    while True:
        try:
            api.set_disconnect()

            if not api.connect():
                raise Exception('Failed to connect')

            if api.get_version() != b'1\x00\x00':
                raise Exception('Bad Verison')

            if api.get_command() != (11, 49, b'\x00\x01\x02\x11!1Dcs\x82\x92'):
                raise Exception('Bad Command')

            if api.get_ID() != b'\x01\x04G':
                raise Exception('Bad ID')

            return True

        except Exception as e:
            if i > 2:
                raise e
            i += 1


def erase(device, length=196608, reporthook=None, api=None):
    if api is None:
        api = Flash_Serial(device)
        _run_connect(api)

    pages = int(math.ceil(length / 128)) + 1
    if pages > 1536:
        pages = 1536

    if reporthook:
        reporthook('Erase ', 0, pages)

    for page_start in range(0, pages, 80):
        page_stop = page_start + 80
        if page_stop > pages:
            page_stop = pages

        if not api.extended_erase_memory(range(page_start, page_stop)):
            raise Exception('Errase error')

        if reporthook:
            reporthook('Erase ', page_stop, pages)


def write(device, firmware, reporthook=None, api=None, start_address=0x08000000):
    if api is None:
        api = Flash_Serial(device)
        _run_connect(api)

    length = len(firmware)

    if reporthook:
        reporthook('Write ', 0, length)

    step = 128
    for offset in range(0, length, step):
        write_len = length - offset
        if write_len > step:
            write_len = step
        for i in range(4):
            if api.write_memory(start_address + offset, firmware[offset:offset + write_len]):
                if reporthook:
                    reporthook('Write ', offset + write_len, length)
                break
            if i == 2:
                _run_connect(api)
        else:
            raise Exception('Write error')

    if reporthook:
        reporthook('Verify', 0, length)


def verify(device, firmware, reporthook=None, api=None, start_address=0x08000000):
    if api is None:
        api = Flash_Serial(device)
        _run_connect(api)

    length = len(firmware)

    step = 128
    for offset in range(0, length, step):
        read_len = length - offset
        if read_len > step:
            read_len = step
        for i in range(4):
            data = api.read_memory(start_address + offset, read_len)
            if data == firmware[offset:offset + read_len]:
                break
            if i == 2:
                _run_connect(api)
        else:
            raise Exception('not match')

        if reporthook:
            reporthook('Verify', offset + read_len, length)


def clone(device, filename, length, reporthook=None, api=None, start_address=0x08000000):
    if api is None:
        api = Flash_Serial(device)
        _run_connect(api)

    f = open(filename, 'wb')
    step = 128
    for offset in range(0, length, step):
        read_len = length - offset
        if read_len > step:
            read_len = step

        for i in range(4):
            data = api.read_memory(start_address + offset, read_len)
            verify = api.read_memory(start_address + offset, read_len)
            if data == verify:
                f.write(data)
                break
            if i == 2:
                _run_connect(api)
        else:
            raise Exception('not match')

        if reporthook:
            reporthook('Clone', offset + read_len, length)

    f.close()


def run(device, filename_bin, reporthook=None):

    firmware = open(filename_bin, 'rb').read()

    api = Flash_Serial(device)

    _run_connect(api)

    length = len(firmware)

    erase(device, length=length, reporthook=reporthook, api=api)

    write(device, firmware, reporthook=reporthook, api=api)

    verify(device, firmware, reporthook=reporthook, api=api)

    api.go(0x08000000)


def get_list_devices():
    table = []
    for p in serial.tools.list_ports.comports():
        if type(p) == tuple:  # for turris
            if 'VID:PID=0483:5740' in p[2]:
                table.append(p[0])
        else:
            if p.vid == 0x0403 and p.pid == 0x6001:
                table.append(p.device)
            if p.vid == 0x0403 and p.pid == 0x6015 and p.serial_number.startswith("bc-usb-dongle"):
                table.append(p.device)
    if bridge:
        for b in bridge.get_list():
            table.append(b[1])

    return table


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, format=LOG_FORMAT)
    run('on.bin', '/dev/ttyUSB0')
