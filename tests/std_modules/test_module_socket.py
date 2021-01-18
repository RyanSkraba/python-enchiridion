# -*- mode: python -*-
# -*- coding: utf-8 -*-

##
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
# https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import logging
import socket
import threading
import time
import unittest
from typing import List, Optional

"""Tests for sockets with Python"""

class EchoBytesServer(object):
    """A server that returns the bytes it receives.  Sending a 0 stops the server."""

    def __init__(self, host: str = "", port: int = 0) -> None:
        self.log = logging.getLogger(__name__)
        self.client_count = 0
        self.host = host
        self.port = port

    def run(self) -> None:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            # Bind to the specified port, or find a free port if zero.
            self.log.info("server.bind(%s:%s)", self.host, self.port)
            s.bind((self.host, self.port))
            self.port = s.getsockname()[1]
            self.log.info("       bound: %s", s.getsockname())

            # Mark that the port is available for new clients to listen to.  Only one client can
            # be connected at a time.
            self.log.info("socket.listen()")
            s.listen(0)

            # But serve all clients in order.
            shutdown_requested = False
            while not shutdown_requested:
                try:
                    # Create a new socket (on a different port) to talk to the client.  This
                    # is a blocking call.
                    # addr is a tuple of host, port
                    self.log.info("server.accept()")
                    connection, addr = s.accept()
                    self.log.info("       accepted: %s", addr)

                    self.client_count += 1

                    # Serve all the bytes in order.
                    client_disconnected = False
                    while not shutdown_requested and not client_disconnected:
                        # Echo all bytes
                        self.log.info("server.recv(1)")
                        data = connection.recv(1)
                        self.log.info("       received %s", data)
                        if len(data) == 0:
                            # The client has closed and will no longer send bytes.
                            client_disconnected = True
                        elif data[0] == 0:
                            # At any zero, we'll return the byte but stop receiving.
                            shutdown_requested = True
                        connection.sendall(data)

                finally:
                    # The socket that we accepted should be closed down.
                    connection.close()


class EchoBytesClient(object):
    def __init__(self, host: str, port: int) -> None:
        self.log = logging.getLogger(__name__)
        self.connection = None
        self.host = host
        self.port = port

    def __enter__(self):
        if self.connection is None:
            self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.log.info("client.connect(%s:%s)", self.host, self.port)
            self.connection.connect((self.host, self.port))
            self.log.info("       connected: %s", self.connection.getsockname())
        return self

    def __exit__(self, t, v, tb):
        self.connection.close()

    def send(self, data: Optional[List[int]]) -> bytes:
        if data is not None:
            self.connection.sendall(bytes(data))
        return self.connection.recv(1)


class EchoBytesServerThread(threading.Thread):
    def __init__(self, name, host: str = "", port: int = 0) -> None:
        threading.Thread.__init__(self)
        self.log = logging.getLogger(__name__)
        self.name = name
        self.server = EchoBytesServer(host, port)

    def __enter__(self) -> "EchoBytesServerThread":
        self.log.info("Starting a server.")
        self.start()
        # Block until the server has been launched.
        self.get_port()
        return self

    def __exit__(self, t, v, tb):
        self.log.info("Waiting for server to stop.")
        self.join()
        self.log.info("Server stopped.")

    def run(self) -> None:
        self.log.info("Starting server thread %s.", self.name)
        self.server.run()
        self.log.info("Finished server thread %s.", self.name)

    def get_port(self) -> int:
        while self.server.port == 0:
            time.sleep(1)
        self.log.info("Server discovered on port %s.", self.server.port)
        return self.server.port


class SocketModuleTestSuite(unittest.TestCase):
    def test_basic(self):
        with EchoBytesServerThread(self.test_basic.__name__) as srv:
            port = srv.get_port()
            self.assertNotEqual(port, 0)

            self.assertEqual(0, srv.server.client_count)

            with EchoBytesClient("", port) as c1:
                self.assertEqual(bytes([1]), c1.send([1, 2, 3]))
                self.assertEqual(bytes([2]), c1.send(None))
                self.assertEqual(bytes([3]), c1.send(None))

            self.assertEqual(1, srv.server.client_count)

            with EchoBytesClient("", port) as c2:
                self.assertEqual(bytes([2]), c2.send([2, 3, 4]))
                self.assertEqual(bytes([3]), c2.send(None))
                self.assertEqual(bytes([4]), c2.send(None))

            self.assertEqual(2, srv.server.client_count)

            with EchoBytesClient("", port) as c3:
                self.assertEqual(bytes([3]), c3.send([3, 4, 0]))
                self.assertEqual(bytes([4]), c3.send(None))
                self.assertEqual(bytes([0]), c3.send(None))

            self.assertEqual(3, srv.server.client_count)


if __name__ == "__main__":
    unittest.main()
