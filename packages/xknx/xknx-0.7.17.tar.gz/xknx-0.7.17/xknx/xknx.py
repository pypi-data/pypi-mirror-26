"""XKNX is an Asynchronous Python module for reading and writing KNX/IP packets."""
import asyncio
import signal
import logging
from xknx.knx import Address, AddressFormat
from xknx.io import KNXIPInterface, ConnectionConfig
from xknx.core import TelegramQueue, Config
from xknx.devices import Devices


class XKNX:
    """Class for reading and writing KNX/IP packets."""

    # pylint: disable=too-many-instance-attributes

    DEFAULT_ADDRESS = '15.15.250'

    def __init__(self,
                 config=None,
                 loop=None,
                 own_address=Address(DEFAULT_ADDRESS),
                 address_format=AddressFormat.LEVEL3,
                 telegram_received_cb=None,
                 device_updated_cb=None):
        """Initialize XKNX class."""
        # pylint: disable=too-many-arguments
        self.devices = Devices()
        self.telegrams = asyncio.Queue()
        self.loop = loop or asyncio.get_event_loop()
        self.sigint_received = asyncio.Event()
        self.telegram_queue = TelegramQueue(self)
        self.state_updater = None
        self.knxip_interface = None
        self.started = False
        self.address_format = address_format
        self.own_address = own_address
        self.logger = logging.getLogger('xknx.log')
        self.knx_logger = logging.getLogger('xknx.knx')
        self.telegram_logger = logging.getLogger('xknx.telegram')

        if config is not None:
            Config(self).read(config)

        if telegram_received_cb is not None:
            self.telegram_queue.register_telegram_received_cb(telegram_received_cb)

        if device_updated_cb is not None:
            self.devices.register_device_updated_cb(device_updated_cb)

    def __del__(self):
        """Destructor. Cleaning up if this was not done before."""
        if self.started:
            try:
                task = self.loop.create_task(self.stop())
                self.loop.run_until_complete(task)
            except RuntimeError as exp:
                self.logger.warning("Could not close loop, reason: %s", exp)

    @asyncio.coroutine
    def start(self,
              state_updater=False,
              daemon_mode=False,
              connection_config=ConnectionConfig()):
        """Start XKNX module. Connect to KNX/IP devices and start state updater."""
        self.knxip_interface = KNXIPInterface(self, connection_config=connection_config)
        yield from self.knxip_interface.start()
        yield from self.telegram_queue.start()

        if state_updater:
            from xknx.core import StateUpdater
            self.state_updater = StateUpdater(self)
            yield from self.state_updater.start()

        if daemon_mode:
            yield from self.loop_until_sigint()

        self.started = True

    @asyncio.coroutine
    def join(self):
        """Wait until all telegrams were processed."""
        yield from self.telegrams.join()

    def _stop_knxip_interface_if_exists(self):
        """Stop KNXIPInterface if initialized."""
        if self.knxip_interface is not None:
            yield from self.knxip_interface.stop()
            self.knxip_interface = None

    @asyncio.coroutine
    def stop(self):
        """Stop XKNX module."""
        yield from self.join()
        yield from self.telegram_queue.stop()
        yield from self._stop_knxip_interface_if_exists()
        self.started = False

    @asyncio.coroutine
    def loop_until_sigint(self):
        """Loop until Crtl-C was pressed."""
        def sigint_handler():
            """End loop."""
            self.sigint_received.set()
        self.loop.add_signal_handler(signal.SIGINT, sigint_handler)
        self.logger.warning('Press Ctrl+C to stop')
        yield from self.sigint_received.wait()
