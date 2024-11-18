
import json

from fractions import Fraction
from typing import (
  List,
  Dict,
  Any,
  Tuple
)


class TextLib:
  @staticmethod
  def getTextMessages(input : Dict[str, Any]) -> List[Dict[str, str]]:
    messages = []
    for message in input.get("Solution", []):
      messages.append(TextLib.__generateTextMessage(message[0], message[1]))
    return messages

  @staticmethod
  def __generateTextMessage(mode : int, input : str) -> Dict[str, str]:
    message = {}
    match mode:
      case 0:
        message["parse_mode"] = ''
        message["text"] = input
      case 1:
        message["parse_mode"] = "html"
        message["text"] = TextLib.__generateMatrix(input)
      case 2:
        message["parse_mode"] = ''
        message["text"] = TextLib.__generateMathText(input)
      case _:
        print("bruh")
    return message

  @staticmethod
  def __generateMatrix(input : str) -> str:
    result = "<code>"
    matrix = json.loads(input)
    coeffs = [float("-inf")] * len(matrix[0])
    for row in matrix:
      for i,j in enumerate(row):
        coeffs[i] = max(coeffs[i],len(str(Fraction(j[0], j[1]))))
    for rowID, row in enumerate(matrix):
      for numID, num in enumerate(row):
        numStr = str(Fraction(num[0], num[1]))
        result += ''.join([" " for _ in range(int(coeffs[numID])-len(numStr))]) + numStr
        if numID != len(matrix[0]) - 1:
          result += ' '
      if rowID != len(matrix)-1:
        result += '\n'
    return result + "</code>"


  @staticmethod
  def __generateMathText(input : str) -> str:
    return TextLib.__state0(input, 0)[0]

  @staticmethod
  def __getPowerSymbol(key : str) -> str:
    powers = {
      "0" : "\u2070", "1" : "\u00B9", "2" : "\u00B2",
      "3" : "\u00B3", "4" : "\u2074", "5" : "\u2075",
      "6" : "\u2076", "7" : "\u2077", "8" : "\u2078",
      "9" : "\u2079",

      "a" : "ᵃ", "b" : "ᵇ", "c" : "ᶜ", "d" : "ᵈ", 
      "e" : "ᵉ", "f" : "ᶠ", "g" : "ᵍ", "h" : "ʰ", 
      "i" : "ⁱ", "j" : "ʲ", "k" : "ᵏ", "l" : "ˡ", 
      "m" : "ᵐ", "n" : "ⁿ", "o" : "ᵒ", "p" : "ᵖ", 
      "r" : "ʳ", "s" : "ˢ", "t" : "ᵗ", "u" : "ᵘ", 
      "v" : "ᵛ", "w" : "ʷ", "x" : "ˣ", "y" : "ʸ", 
      "z" : "ᶻ",

      "A" : "ᴬ", "B" : "ᴮ", "C" : "ᶜ", 
      "D" : "ᴰ", "E" : "ᴱ", "F" : "ᶠ", 
      "G" : "ᴳ", "H" : "ᴴ", "I" : "ᴵ", 
      "J" : "ᴶ", "K" : "ᴷ", "L" : "ᴸ", 
      "M" : "ᴹ", "N" : "ᴺ", "O" : "ᴼ", 
      "P" : "ᴾ", "Q" : "ᵠ", "R" : "ᴿ", 
      "S" : "ˢ", "T" : "ᵀ", "U" : "ᵁ", 
      "V" : "ⱽ", "W" : "ᵂ", "X" : "ᵡ",
      "Y" : "ᵞ", "Z" : "ᶻ"
    }
    return powers.get(key,"")

  @staticmethod
  def __getIndexSymbol(key : str) -> str:
    indexes = {
      "0" : "₀",
      "1" : "₁", 
      "2" : "₂",
      "3" : "₃",
      "4" : "₄",
      "5" : "₅",
      "6" : "₆", 
      "7" : "₇",
      "8" : "₈",
      "9" : "₉",
      "," : "."
    }
    return indexes.get(key,"")

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
        mode, strID = TextLib.__readNumberUntilSymbol(input, strID, '}')
        match mode:
          case 1:
            text, strID = TextLib.__state1(input, strID)
          case 2:
            text, strID = TextLib.__state2(input, strID)
          case 3:
            text, strID = TextLib.__state3(input, strID)
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
    # умножение
    result = "×"
    return result, strID

  @staticmethod
  def __state2(input : str, strID : int) -> Tuple[str, int]:
    # степень
    result = ""
    strID += 2
    while strID < len(input) and input[strID] != '}':
      if input[strID] == '{':
        strID += 1
        mode, strID = TextLib.__readNumberUntilSymbol(input, strID, '}')
        match mode:
          case 1:
            text, strID = TextLib.__state1(input, strID)
          case 2:
            text, strID = TextLib.__state2(input, strID)
          case 3:
            text, strID = TextLib.__state3(input, strID)
          case _:
            text = ""
        result += text
        strID += 1
        continue
      result += TextLib.__getPowerSymbol(input[strID])
      strID += 1
    return result, strID

  @staticmethod
  def __state3(input : str, strID : int) -> Tuple[str, int]:
    result = ""
    strID += 2
    while strID < len(input) and input[strID] != '}':
      if input[strID] == '{':
        strID += 1
        mode, strID = TextLib.__readNumberUntilSymbol(input, strID, '}')
        match mode:
          case 1:
            text, strID = TextLib.__state1(input, strID)
          case 2:
            text, strID = TextLib.__state2(input, strID)
          case 3:
            text, strID = TextLib.__state3(input, strID)
          case _:
            text = ""
        result += text
        strID += 1
        continue
      result += TextLib.__getIndexSymbol(input[strID])
      strID += 1
    return result, strID
    
    
