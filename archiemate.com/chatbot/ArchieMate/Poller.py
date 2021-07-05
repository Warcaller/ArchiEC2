import select
import socket
from typing import NamedTuple
import queue
from os import environ as env
import ArchieMate.Logger as Logger

logger = Logger.get_logger(__name__)

READ_ONLY = select.POLLIN | select.POLLPRI | select.POLLHUP | select.POLLERR
READ_WRITE = READ_ONLY | select.POLLOUT

POLLER_TIMEOUT = int(env.get("POLLER_TIMEOUT", "250"))
POLLER_FLUSH_TIMEOUT = POLLER_TIMEOUT * 50

class Poller:
  class SocketInfo(NamedTuple):
    socket: socket.socket
    queue_read: queue.Queue
    queue_write: queue.Queue
    dead: bool
    
  def __init__(self):
    logger.debug("Poller.__init__()")
    self.poller: select.poll = select.poll()
    self.sockets = {}
  
  def add_socket(self, socket: socket.socket):
    logger.debug(f"Poller.add_socket(socket: {socket})")
    self.sockets[socket.fileno()] = Poller.SocketInfo(socket, queue.Queue(), queue.Queue(), False)
    self.poller.register(socket, READ_ONLY)
  
  def remove_socket(self, socket: socket.socket):
    logger.debug(f"Poller.remove_socket(socket: {socket})")
    while not self.sockets[socket.fileno()].queue_write.empty():
      self.poll(POLLER_FLUSH_TIMEOUT)
    self.poller.unregister(socket)
    del self.sockets[socket.fileno()]
  
  def write_to_socket(self, socket: socket.socket, data: bytes):
    logger.debug(f"Poller.write_to_socket(socket: {socket}, data: '{data}')")
    self.sockets[socket.fileno()].queue_write.put(data)
    self.poller.modify(socket, READ_WRITE)
    self.poll(POLLER_TIMEOUT)
  
  def read_from_socket(self, socket: socket.socket) -> bytes:
    logger.debug(f"Poller.read_from_socket(socket: {socket}")
    self.poll(POLLER_TIMEOUT)
    try:
      next_msg = self.sockets[socket.fileno()].queue_read.get_nowait()
    except queue.Empty:
      return b""
    else:
      return next_msg
  
  def poll(self, timeout: float):
    logger.debug(f"Poller.poll(timeout: {timeout})")
    for fd, flag in self.poller.poll(timeout):
      if flag & (select.POLLIN | select.POLLPRI):
        logger.debug(f"socket {self.sockets[fd].socket} is receiving data.")
        for data in self.sockets[fd].socket.recv(8192).split(b"\r\n"):
          if len(data) > 0:
            logger.debug(f"saving data '{data}' to read queue.")
            self.sockets[fd].queue_read.put(data+b"\n")
      elif flag & select.POLLHUP or flag & select.POLLERR:
        logger.debug(f"socket {self.sockets[fd].socket} is dead.")
        self.poller.unregister(self.sockets[fd].socket)
        self.sockets[fd].dead = True
      elif flag & select.POLLOUT:
        logger.debug(f"socket {self.sockets[fd].socket} is ready to send data.")
        try:
          next_msg = self.sockets[fd].queue_write.get_nowait()
        except queue.Empty:
          logger.debug(f"no more data to send to the socket.")
          self.poller.modify(self.sockets[fd].socket, READ_ONLY)
        else:
          logger.debug(f"sending data '{next_msg}'")
          bytes_sent = 0
          while bytes_sent < len(next_msg):
            bytes_sent += self.sockets[fd].socket.send(next_msg[bytes_sent:])
  
  def flush(self):
    logger.debug("Poller.flush()")
    for fd in self.sockets.keys():
      logger.debug(f"Flushing socket fd '{fd}'")
      while not self.sockets[fd].queue_write.empty():
        self.poll(POLLER_FLUSH_TIMEOUT)
  
  def __del__(self):
    logger.debug(f"Poller.__del__()")
    for fd in self.sockets.keys():
      self.poller.remove_socket(self.sockets[fd].socket)
    del self.sockets
    del self.poller