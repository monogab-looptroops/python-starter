
from pubsub import pub
import signal

import threading
import time
from loggerhelper import LoggerHelper, LogLevel

logger = LoggerHelper("sub_module.py")


def listen_to_terminate_signal():
    def emit_terminate_signal(args, kwargs):
        """
        Emit a terminat signal over the pubsub module so running submodules can terminate cleanly
        """
        logger.log("Main module emitting terminate")
        pub.sendMessage("terminate")

    signal.signal(signal.SIGTERM, emit_terminate_signal)
    signal.signal(signal.SIGINT, emit_terminate_signal)


if __name__ == "__main__":

    # Usage:
    # When you create a submodule, you can subscribe at initializiation
    # to the terminate event to allow clean service shutdown
    # Here is an example
    class SubModule():
        def __init__(self) -> None:
            self.run = True  # Used to keep while loops running

            # Subscribe to the terminate event to allow clean service shutdown
            pub.subscribe(self.handle_terminate_signal, 'terminate')

            # Start the main loop
            threading.Thread(target=self.processing_loop).start()

        def handle_terminate_signal(self):
            logger.log(f"Received terminate signal for SubModule.")
            self.run = False  # Set to False to stop all running loops

        def processing_loop(self):
            while self.run:
                logger.log("SubModule is running")
                time.sleep(1)

            logger.log(f"SubModule has stopped running")

    listen_to_terminate_signal()
    SubModule()
    # press control + c to stop
