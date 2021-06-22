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
from typing import Optional

"""Tests for sockets with Python"""


class EchoBytesServer(object):
    """A server that returns the bytes it receives."""

    def __init__(
        self,
        host: str = "",
        port: int = 0,
        stopword=b"Stop",
        timeout: Optional[float] = None,
    ) -> None:
        self.log = logging.getLogger(__name__)
        # The number of connections the server has processed.
        self.client_count = 0
        self.host = host
        self.port = port
        # When this word has been received, shutdown the server.
        self.stopword = stopword
        self.timeout = timeout
        self.__exception = None
        self.__stopword_buffer = bytes(len(self.stopword))
        self.__thread = threading.Thread(target=self.run_catch, name="EchoBytesServer")

    def __enter__(self) -> "EchoBytesServer":
        """Starts itself in a thread, waiting for clients to connect."""
        self.__thread.start()
        return self

    def __exit__(self, t, v, tb) -> None:
        """If started in a thread, wait for the thread to finish."""
        if self.__thread is not None and self.__thread.is_alive():
            self.__thread.join()

    def run_catch(self) -> None:
        try:
            self.run()
        except Exception as e:
            self.__exception = e

    def run(self) -> None:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            # Bind to the specified port, or find a free port if zero.
            self.log.info("server.bind(%s:%s)", self.host, self.port)
            s.bind((self.host, self.port))
            self.port = s.getsockname()[1]
            self.log.info("       bound: %s", s.getsockname())

            if self.timeout is not None:
                s.settimeout(self.timeout)

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
                    if self.timeout is not None:
                        connection.settimeout(self.timeout)
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
                        else:
                            self.__stopword_buffer += data
                            self.__stopword_buffer = self.__stopword_buffer[1:]
                            if self.stopword == self.__stopword_buffer:
                                # At any zero, we'll return the byte but stop receiving.
                                shutdown_requested = True
                        connection.sendall(data)

                finally:
                    # The socket that we accepted should be closed down.
                    connection.close()

    def get_port(self) -> int:
        """Blocks until the port is not zero."""
        while self.port == 0:
            time.sleep(1)
        return self.port


class EchoBytesClient(object):
    """A server for speaking to the EchoBytesServer."""

    def __init__(self, host: str, port: int, timeout: Optional[float] = None) -> None:
        self.log = logging.getLogger(__name__)
        self.connection = None
        self.host = host
        self.port = port
        self.timeout = timeout

    def __enter__(self) -> "EchoBytesClient":
        if self.connection is None:
            self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            if self.timeout is not None:
                self.connection.settimeout(self.timeout)
            self.log.info("client.connect(%s:%s)", self.host, self.port)
            self.connection.connect((self.host, self.port))
            self.log.info("       connected: %s", self.connection.getsockname())
        return self

    def __exit__(self, t, v, tb):
        self.connection.close()

    def send(self, data: Optional[bytes]) -> bytes:
        if data is not None:
            self.connection.sendall(data)
        return self.connection.recv(1)


class SocketModuleTestSuite(unittest.TestCase):
    def test_echo_bytes_server_basic(self) -> None:

        """Simple client/server communication with the server and client."""
        with EchoBytesServer(timeout=10) as srv:
            port = srv.get_port()
            self.assertNotEqual(port, 0)

            self.assertEqual(0, srv.client_count)

            with EchoBytesClient("", port, timeout=10) as c1:
                self.assertEqual(bytes([1]), c1.send(bytes([1, 2, 3])))
                self.assertEqual(bytes([2]), c1.send(None))
                self.assertEqual(bytes([3]), c1.send(None))

            self.assertEqual(1, srv.client_count)

            with EchoBytesClient("", port) as c2:
                self.assertEqual(bytes([2]), c2.send(bytes([2, 3, 4])))
                self.assertEqual(bytes([3]), c2.send(None))
                self.assertEqual(bytes([4]), c2.send(None))

            self.assertEqual(2, srv.client_count)

            with EchoBytesClient("", port) as c3:
                self.assertEqual(bytes([3]), c3.send(b"\x03" + b"Stop"))
                self.assertEqual(b"S", c3.send(None))
                self.assertEqual(b"t", c3.send(None))
                self.assertEqual(b"o", c3.send(None))
                self.assertEqual(b"p", c3.send(None))

            self.assertEqual(3, srv.client_count)

    def test_accept_timeout(self) -> None:
        """A socket.accept call blocks, but can time out."""

        info = {}

        def accept(info: dict) -> None:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                # None of these socket calls are blocking
                s.bind(("", 0))
                info["port"] = s.getsockname()[1]
                s.listen(0)

                s.settimeout(0.5)
                try:
                    # This will block until a client accepts or a timeout occurs.
                    connection, addr = s.accept()
                    info["connection"] = connection
                    info["addr"] = addr
                except socket.timeout:
                    pass

        accept(info)

        self.assertIn("port", info.keys())
        self.assertNotIn("connection", info.keys())
        self.assertNotIn("addr", info.keys())


if __name__ == "__main__":
    unittest.main()
