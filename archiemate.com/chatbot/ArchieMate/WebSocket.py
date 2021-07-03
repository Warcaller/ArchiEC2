import websocket
import select

import ArchieMate.Logger as Logger
import ArchieMate.Poller as Poller

logger = Logger.get_logger(__name__)

class Socket:
  def __init__(self, address: str, poller: Poller.Poller):
    logger.debug(f"Socket.__init__(address: '{address}', port: {port})")
    self.socket = socket.socket()
    self.socket.connect((address, port))
    self.socket.setblocking(False)
    self.poller = poller
    self.poller.add_socket(self.socket)
  
  def send(self, string: str):
    logger.debug(f"Socket.send(string: '{string}')")
    string = f"{string.strip()}\r\n"
    self.poller.write_to_socket(self.socket, string.encode())
  
  def recv(self) -> str:
    logger.debug("Socket.recv()")
    recv_bytes = b""
    try:
      while recv_bytes[-1:] != b"\n":
        received = self.poller.read_from_socket(self.socket)
        if received == b"":
          return b""
        recv_bytes += received
    except Exception as e:
      logger.exception("Exception when receiving data", exc_info=e, stack_info=True)
    finally:
      if len(recv_bytes) == 0 and self.poller.sockets[self.socket.fileno()].dead:
        raise ConnectionError("Socket is dead")
      ret = recv_bytes.decode().strip()
      logger.debug(f"Received: {ret}")
      return ret
  
  def recv_nowait(self) -> str:
    logger.debug("Socket.recv_nowait()")
    received = ""
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
    del self.socket
