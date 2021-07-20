import socket
import queue
from os import environ as env

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
    logger.debug(f"SocketServer.__init__(poller: {poller})")
    self.socket: socket.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.socket.setblocking(False)
    self.socket.bind(('0.0.0.0', int(env.get("ARCHIEMATE_SOCKET_SERVER_PORT"))))
    self.socket.listen()
    self.poller = poller
    self.raw_sockets: queue.Queue = queue.Queue()
    self.sockets: List[SocketServer.SocketInfo] = []
    self.poller.add_socket(self.socket, server=True, server_sockets=self.raw_sockets)
    logger.debug(f"Result: {self.__dict__}")
  
  def check_sockets(self) -> None:
    logger.debug("SocketServer.check_sockets()")
    while self.raw_sockets.qsize() > 0:
      new_socket: socket.socket = self.raw_sockets.get(0)
      logger.debug(f"new socket {new_socket} - something connected!")
      self.sockets.append(SocketServer.SocketInfo(Socket.Socket(poller=self.poller, server_socket=new_socket), SocketType.Unknown, {}))
      dead_sockets = [socket for socket in self.sockets if socket.state.get("dead") == True]
      for dead_socket in dead_sockets:
        logger.debug(f"removing dead socket {dead_socket.__dict__}")
        self.sockets.remove(dead_socket)
    logger.debug(f"Result: {self.__dict__}")
  
  def __del__(self):
    del self.socket
    del self.sockets
