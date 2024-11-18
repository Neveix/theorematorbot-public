
if __name__ == "__main__":
  import client
  from text import text
  from image import image
else:
  from libs.engine import client
  from libs.engine.text import text
  from libs.engine.image import image

from PIL import Image
from typing import \
(
  Any,
  Dict,
  List,
  Tuple
)

class Scalar:
  __js : Dict[str, Any]
  def __init__(self, _json : Dict[str, int]):
    self.__js = _json
# getters
  def getJS(self) -> Dict[str, Any]:
    return self.__js

  def getErrorCode(self) -> str:
    return self.__js["ErrorCode"]

  def getErrorMsg(self) -> Dict[str, str]:
    return {"text" : self.__js["ErrorMsg"], "parse_mode" : ""}

  def getTextSolution(self) -> List[Dict[str, str]]:
    return text.TextLib.getTextMessages(self.getJS())

  def getImageSolution(self) -> List[Dict[str, bytes]]:
    return image.ImageLib.getImageMessages(self.getJS())

class Boolean:
  __js : Dict[str, Any]
  def __init__(self, _json : Dict[str, int]):
    self.__js = _json
# getters
  def getJS(self) -> Dict[str, Any]:
    return self.__js
  
  def getErrorCode(self) -> str:
    return self.__js["ErrorCode"]

  def getErrorMsg(self) -> Dict[str, str]:
    return {"text" : self.__js["ErrorMsg"], "parse_mode" : ""}

  def getTextSolution(self) -> List[Dict[str,str]]:
    return text.TextLib.getTextMessages(self.getJS())

  def getImageSolution(self) -> List[Dict[str, bytes]]:
    return image.ImageLib.getImageMessages(self.getJS())

class JsonObject:
  __js : Dict[str, Any]
  def __init__(self, _json : Dict[str, int]):
    self.__js = _json
# getters
  def getJS(self) -> Dict[str, Any]:
    return self.__js
  
  def getErrorCode(self) -> str:
    return self.__js["ErrorCode"]

  def getErrorMsg(self) -> Dict[str, str]:
    return {"text" : self.__js["ErrorMsg"], "parse_mode" : ""}

  def getTextSolution(self) -> List[Dict[str,str]]:
    return text.TextLib.getTextMessages(self.getJS())

  def getImageSolution(self) -> List[Dict[str, bytes]]:
    return image.ImageLib.getImageMessages(self.getJS())

class Matrix:
  __js : Dict[str, Any]
  def __init__(self, matrixJSON : Dict[str, List[List[Tuple[int, int]]]]):
    self.__js = matrixJSON

  @staticmethod
  def createMatrix(matrixStr : str) -> "Matrix":
    cl = client.Client ()
    js : Dict[str, Any] = { 
      "ProblemID" : client.ProblemID.Parser.Matrix, 
      "Operand1"  : matrixStr.rstrip()
    }
    cl.sendJson(js)
    return Matrix(cl.receiveJson())

  def add(self, Other : "Matrix") -> "Matrix":
    cl = client.Client()
    js : Dict[str, Any] = {
      "ProblemID" : client.ProblemID.Matrix.Sum,
      "Operand1"  : self.__js["Result"],
      "Operand2"  : Other.__js["Result"]
    }
    cl.sendJson(js)
    return Matrix(cl.receiveJson())

  def diff(self, Other : "Matrix") -> "Matrix":
    cl = client.Client()
    js : Dict[str, Any] = {
      "ProblemID" : client.ProblemID.Matrix.Diff,
      "Operand1"  : self.__js["Result"],
      "Operand2"  : Other.__js["Result"]
    }
    cl.sendJson(js)
    return Matrix(cl.receiveJson())

  def mult(self, Other : "Matrix") -> "Matrix":
    cl = client.Client()
    js : Dict[str, Any] = {
      "ProblemID" : client.ProblemID.Matrix.Mult,
      "Operand1"  : self.__js["Result"],
      "Operand2"  : Other.__js["Result"]
    }
    cl.sendJson(js)
    return Matrix(cl.receiveJson())

  def inverse(self) -> "Matrix":
    cl = client.Client()
    js : Dict[str, Any] = {
      "ProblemID" : client.ProblemID.Matrix.Inverse,
      "Operand1"  : self.__js["Result"]
    }
    cl.sendJson(js)
    return Matrix(cl.receiveJson())

  def transpose(self) -> "Matrix":
    cl = client.Client()
    js : Dict[str, Any] = {
      "ProblemID" : client.ProblemID.Matrix.Transpose,
      "Operand1"  : self.__js["Result"],
    }
    cl.sendJson(js)
    return Matrix(cl.receiveJson())

  def determinant(self) -> Scalar:
    cl = client.Client()
    js : Dict[str, Any] = {
      "ProblemID" : client.ProblemID.Matrix.Determinant,
      "Operand1"  : self.__js["Result"]
    }
    cl.sendJson(js)
    return Scalar(cl.receiveJson())

  def rank(self) -> Scalar:
    cl = client.Client()
    js : Dict[str, Any] = {
      "ProblemID" : client.ProblemID.Matrix.Rank,
      "Operand1"  : self.__js["Result"]
    }
    cl.sendJson(js)
    return Scalar(cl.receiveJson())

  def SMD(self) -> None:
    pass

  def PMD(self) -> None:
    pass

  def MLIS(self) -> "Matrix":
    cl = client.Client()
    js : Dict[str, Any] = {
      "ProblemID" : client.ProblemID.LS.MLIS,
      "Operand1"  : self.__js["Result"]
    }
    cl.sendJson(js)
    return Matrix(cl.receiveJson())

  def IsLIS(self) -> Boolean:
    cl = client.Client()
    js : Dict[str, Any] = {
      "ProblemID" : client.ProblemID.LS.IsLinearlyIndependent,
      "Operand1"  : self.__js["Result"]
    }
    cl.sendJson(js)
    return Boolean(cl.receiveJson())

  def findBasis(self) -> "Matrix":
    cl = client.Client()
    js : Dict[str, Any] = {
      "ProblemID" : client.ProblemID.LS.Basis,
      "Operand1"  : self.__js["Result"]
    }
    cl.sendJson(js)
    return Matrix(cl.receiveJson())

  def linearOperatorChars(self) -> JsonObject:
    cl = client.Client()
    js : Dict[str, Any] = {
      "ProblemID" : client.ProblemID.LinearOperator.Characteristics,
      "Operand1"  : self.__js["Result"]
    }
    cl.sendJson(js)
    return JsonObject(cl.receiveJson())
# getters
  def getJS (self) -> Dict[str, Any]:
    return self.__js

  def getErrorCode (self) -> int:
    return self.__js["ErrorCode"]

  def getErrorMsg (self) -> Dict[str, str]:
    return {"text" : self.__js["ErrorMsg"], "parse_mode" : ""}

  def getTextSolution (self) -> List[Dict[str, str]]:
    return text.TextLib.getTextMessages(self.getJS())

  def getImageSolution(self) -> List[Dict[str, bytes]]:
    return image.ImageLib.getImageMessages(self.getJS())

if __name__ == "__main__":
  mtrx1 = Matrix.createMatrix("0.1 0 0 \n 0 0 9 \n 0 -5 0")
  if mtrx1.getErrorCode() != 0:
    print(mtrx1.getErrorMsg())
    exit()
  mtrx2 = Matrix.createMatrix("1 \n1 \n1 \n1 \n1 \n1 \n1 \n1 \n1 \n1 \n1 \n")
  if mtrx2.getErrorCode() != 0:
    print(mtrx2.getErrorMsg())
    exit()
  scalar = mtrx2.linearOperatorChars()
  if scalar.getErrorCode() == 0:
    scalar.getImageSolution()
  else:
    print(scalar.getErrorMsg())

