import socket
import queue

from typing import NamedTuple, List, Dict, Any
from enum import Enum

import ArchieMate.Socket as Socket
import ArchieMate.Logger as Logger
import ArchieMate.Poller as Poller

logger = Logger.get_logger(__name__)

class SocketType(Enum):
    Overlay = "ovl"
    Website = "web"
    Unknown = "unk"

class SocketServer:
  class SocketInfo(NamedTuple):
    socket: Socket.Socket
    type: SocketType
    state: Dict[str, Any]
  
  def __init__(self, poller: Poller.Poller):
    self.socket: socket.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.socket.bind(('127.0.0.1', 7627))
    self.socket.listen()
    self.poller = poller
    self.raw_sockets: queue.Queue = queue.Queue()
    self.sockets: List[SocketServer.SocketInfo] = []
    self.poller.add_socket(self.socket, server=True, server_sockets=self.raw_sockets)
  
  def check_sockets(self) -> None:
    while self.raw_sockets.qsize() > 0:
      new_socket: socket.socket = self.raw_sockets.get(0)
      self.sockets.append(SocketServer.SocketInfo(new_socket, SocketType.Unknown, {}))
      dead_sockets = [socket for socket in self.sockets if socket.state.get("dead") == True]
      for dead_socket in dead_sockets:
        self.sockets.remove(dead_socket)
  
  def __del__(self):
    del self.socket
    del self.sockets
