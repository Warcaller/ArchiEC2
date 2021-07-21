import socket
from typing import Union
import ArchieMate.Logger as Logger
import ArchieMate.Poller as Poller

logger = Logger.get_logger(__name__)

class Socket:
  def __init__(self, address: str = None, port: int = None, poller: Poller.Poller = None, *, server: socket.socket = None, server_socket: socket.socket = None):
    logger.debug(f"Socket.__init__(address: '{address}', port: {port}, server: {server}, server_socket={server_socket})")
    self.socket = socket.socket() if server is None and server_socket is None else server if server_socket is None else server_socket
    if server is None and server_socket is None:
      self.socket.connect((address, port))
    self.socket.setblocking(False)
    self.poller = poller
    self.poller.add_socket(self.socket)
  
  def send(self, string: Union[str, bytes]):
    logger.debug(f"Socket.send(string: '{string if len(string) < 1024 else str(len(string)) + ' bytes'}')")
    string = f"{string.strip()}\r\n" if isinstance(string, str) else string
    self.poller.write_to_socket(self.socket, string.encode() if isinstance(string, str) else string)
  
  def recv(self) -> str:
    logger.debug("Socket.recv()")
    recv_bytes: bytes = b""
    try:
      while recv_bytes[-1:] != b"\n":
        received: bytes = self.poller.read_from_socket(self.socket)
        if received == b"":
          return b""
        recv_bytes += received
    except Exception as e:
      logger.exception("Exception when receiving data", exc_info=e, stack_info=True)
    finally:
      if len(recv_bytes) == 0 and self.poller.sockets[self.socket.fileno()].dead:
        raise ConnectionError("Socket is dead")
      ret: str = recv_bytes.decode().strip()
      logger.debug(f"Received: {ret}")
      return ret
  
  def recv_nowait(self) -> str:
    logger.debug("Socket.recv_nowait()")
    received: str = ""
    while len(received) == 0:
      received = self.recv()
    logger.debug(f"NOWAIT received: '{received}'")
    return received
  
  def flush(self):
    logger.debug("Socket.flush()")
    self.poller.flush()
  
  def __del__(self):
    logger.debug(f"Socket.__del__()")
    self.poller.remove_socket(self.socket)
    self.socket.close()
