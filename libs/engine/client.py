
import socket
import json
import typing

from enum import Enum


HOST="127.0.0.1"
PORT=6789
BUFFER_SIZE=8192

class ProblemID:
  @staticmethod
  def enumToValue (obj : typing.Any):
    if isinstance(obj,Enum):
      return obj.value
    return obj

  class Parser (Enum):
    Matrix    = 1
    Quadratic = 2 # x^2+2xy+xz+zy+z^2+y^2

  class Matrix (Enum):
    Sum         = 101 # sum
    Diff        = 102 # difference
    Mult        = 103 # multiplication
    Inverse     = 104 # 
    Transpose   = 105 #
    Determinant = 106 # determinant
    Rank        = 107 # matrix rank
    SMD         = 108 # singular matrix decomposition
    PMD         = 109 # polar matrix decomposition
  class LS (Enum):
    MLIS                  = 201 # max linearly independent subsystem
    Basis                 = 202 # basis of linear space
    IsLinearlyIndependent = 203 
    FS                    = 204 # fundamental system

  class LES (Enum):
    Trianglize          = 301
    Diagonalize         = 302
    GaussianElimination = 303
    CramerMethod        = 304

  class LinearOperator(Enum):
    Characteristics = 401

  class Basis (Enum):
    GramSchmidt = 501
    GramMatrix  = 502


class Client:
  s : socket.socket

  def __init__ (self):
    self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.s.connect((HOST,PORT))

  def sendJson (self, _json : typing.Dict[str, typing.Any]) -> None:
    jsonStr = json.dumps(_json, default=ProblemID.enumToValue)
    self.s.sendall(jsonStr.encode("utf-8"))

  def receiveJson (self) -> typing.Dict[str, typing.Any]:
    responce = self.s.recv(BUFFER_SIZE)
    return json.loads(responce.decode())

  def __del__(self):
    self.s.close()

# Usage example
# if __name__ == "__main__":
#   cl = Client ()
#   cl.sendJson(
#     {"ProblemID" : ProblemID.Parser.Matrix,
#      "Operand1" : "1 2 3 \n 0 0 0 \n 3 4 5".rstrip()
#     })
#   print(cl.receiveJson())

