
import subprocess
import pylatex
import numpy
import json
import fitz
import io

from fractions import Fraction
from uuid import uuid4
from PIL import Image

from numpy._typing import NDArray
from typing import (
  List,
  Dict,
  Any,
  Tuple
)

class ImageLib:
  @staticmethod
  def getImageMessages(input : Dict[str, Any]) -> List[Dict[str, bytes]]:
    messages = []
    name = "pdf/"+str(uuid4())
    doc = pylatex.Document(name, document_options=["a3paper"])

    doc.packages.append(pylatex.Command("usepackage","babel",options="russian"))
    doc.packages.append(pylatex.Command(
      "usepackage","geometry",
      options=["left=0cm","right=0cm","top=0cm","bottom=0cm"]
    ))
    for message in input.get("Solution", []):
      code = message[0]
      match code:
        case 0: # текст
          doc.append(pylatex.Subsection(message[1],numbering=False))
        case 1: # матрица
          doc.append(pylatex.Matrix(ImageLib.__getNumpyMatrix(json.loads(message[1]))))
        case 2: # математический текст
          doc.append(
            pylatex.Subsection(
              pylatex.NoEscape(ImageLib.__generateMathText(message[1])), 
              numbering=False
          ))
    images = ImageLib.__getImagesFromDoc(doc, name)
    for image in images:
      messages.append({"photo" : image})
    return messages

  @staticmethod
  def __getNumpyMatrix(matrix : List[List[Tuple[int,int]]]) -> NDArray[Any]:
    result = []
    for i in range(len(matrix)):
      row = []
      for j in range(len(matrix[0])):
        num, denom = matrix[i][j]
        if denom == 10:
          row.append(num/10)
        else:
          row.append(Fraction(num, denom))
      result.append(row)
    return numpy.array(result)

  @staticmethod
  def __getImagesFromDoc(doc : pylatex.Document, name : str) -> List[bytes]:
    RATIO = 3
    images = []
    
    doc.generate_tex()

    process = subprocess.Popen(["pdflatex","-interaction=nonstopmode","-output-directory=pdf",f"{name}.tex"],stdout=subprocess.PIPE)
    process.wait()

    process = subprocess.Popen(["pdfcrop","--margins","10",f"{name}.pdf"],stdout=subprocess.PIPE)
    process.wait()

    pdfDoc = fitz.open(f"{name}-crop.pdf")
    for pageNum in range(pdfDoc.page_count):
      page = pdfDoc[pageNum]
      pix = page.get_pixmap(dpi=300)
      image = Image.open(io.BytesIO(pix.tobytes("jpeg")))
      newImage : Image.Image
      width, height = image.size
      newImageBytesStream = io.BytesIO()
      if width / height > RATIO:
        ratio = (width / height) / RATIO
        newImage = Image.new("RGB", (width, int(height*ratio)), "white")
      elif height / width > RATIO:
        ratio = (height / width) / RATIO
        newImage = Image.new("RGB", (int(width*ratio), height), "white")
      else:
        image.save(newImageBytesStream,"jpeg",optimize=True)
        images.append(newImageBytesStream.getvalue())
        continue
      newImage.paste(image, (0, 0))
      newImage.save(newImageBytesStream,"jpeg",optimize=True)
      images.append(newImageBytesStream.getvalue())
    return images

  @staticmethod
  def __generateMathText(input : str) -> str:
    return ImageLib.__state0(input, 0)[0]

  @staticmethod
  def __readNumberUntilSymbol(input : str, strID : int, symbol : str) -> Tuple[int, int]:
    result = 0
    while strID < len(input) and input[strID] != symbol:
      result = 10 * result + int(input[strID])
      strID += 1
    return result, strID

  @staticmethod
  def __state0(input : str, strID : int) -> Tuple[str, int]:
    result = ""
    while strID < len(input):
      if input[strID] == '{':
        strID += 1
        mode, strID = ImageLib.__readNumberUntilSymbol(input, strID, '}')
        match mode:
          case 1:
            text, strID = ImageLib.__state1(input, strID)
          case 2:
            text, strID = ImageLib.__state2(input, strID)
            text = '$^{' + text + '}$'
          case 3:
            text, strID = ImageLib.__state3(input, strID)
            text = '$_{' + text + '}$'
          case _:
            text = ""
        result += text
        strID += 1
        continue
      result += input[strID]
      strID += 1
    return result, strID

  @staticmethod
  def __state1(input : str, strID : int) -> Tuple[str, int]:
    # ...{1}...
    # -----^---
    result = "$\\times$"
    # strID += 1
    return result, strID

  @staticmethod
  def __state2(input : str, strID : int) -> Tuple[str, int]:
    # ...2{2}{123}... 
    # ------^--------
    result = ""
    strID += 2 # skip }{
    while strID < len(input):
      if input[strID] == '{':
        strID += 1
        mode, strID = ImageLib.__readNumberUntilSymbol(input, strID, '}')
        match mode:
          case 1:
            text, strID = ImageLib.__state1(input, strID)
          case 2:
            text, strID = ImageLib.__state2(input, strID)
            text = "^{" + text + '}'
          case 3:
            text, strID = ImageLib.__state3(input, strID)
            text = "_{" + text + '}'
          case _:
            text = ""
        result += text
        strID += 1
        continue
      # elif input[strID] == '}':
      #   strID += 1
      #   continue
      result += input[strID]
      strID += 1
    return result, strID
    
  @staticmethod
  def __state3(input : str, strID : int) -> Tuple[str, int]:
    # ...2{3}{123}...
    # ------^--------
    result = ""
    strID += 2
    while strID < len(input):
      if input[strID] == '{':
        strID += 1
        mode, strID = ImageLib.__readNumberUntilSymbol(input, strID, '}')
        match mode:
          case 1:
            text, strID = ImageLib.__state1(input, strID)
          case 2:
            text, strID = ImageLib.__state2(input, strID)
            text = "^{" + text + '}'
          case 3:
            text, strID = ImageLib.__state3(input, strID)
            text = "_{" + text + '}'
          case _:
            text = ""
        result += text
        strID += 1
      # elif input[strID] == '}':
      #   strID += 1
      #   continue
      result += input[strID]
      strID += 1
    return result, strID

