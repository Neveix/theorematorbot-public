//-----------------------------------------------------------------------------
// STD
//-----------------------------------------------------------------------------
#include <iostream>
//-----------------------------------------------------------------------------
// BOOST
//-----------------------------------------------------------------------------
#include <boost/asio.hpp>
#include <boost/rational.hpp>
#include <boost/numeric/ublas/exception.hpp>
//-----------------------------------------------------------------------------
#include "les.hpp"
#include "matrix.hpp"
#include "parser.hpp"
#include "linearoperator.hpp"
//-----------------------------------------------------------------------------
#define BUFFER_SIZE 8192
#define PORT_NUM 6789
//-----------------------------------------------------------------------------
// Enums
//-----------------------------------------------------------------------------
enum ProblemID {
  ParseMatrix    = 1,
  ParseQuadratic = 2,
// Matrix
  Sum                 = 101,
  Diff                = 102,
  Mult                = 103,
  Inverse             = 104,
  Transpose           = 105,
  Determinant         = 106,
  Rank                = 107,
  SMD                 = 108,
  PMD                 = 109,
  GaussianElimination = 110,
// LES
  MLIS        = 201, // max linearly independent subsystem
  Basis       = 202,
  IsLIS       = 203, // is linearly independent system
// Linear Operator
  BasisKernel = 401
};
//-----------------------------------------------------------------------------
// Functions
//-----------------------------------------------------------------------------
inline void checkMatrixSize(const matrix_t & a, boost::asio::ip::tcp::socket & socket, nlohmann::json & response)
{
  if(a.size1() > 10 || a.size2() > 10)
  {
    JSON::setErrorCodeAndMsg(response, JSON::Error::LARGE_SIZE, "Переданная матрица слишком большая");
    socket.write_some(boost::asio::buffer(response.dump()));
    return;
  }
}
//-----------------------------------------------------------------------------
void invokeFunction(ProblemID problemID, boost::asio::ip::tcp::socket & socket, nlohmann::json & json, nlohmann::json & response)
{
  matrix_t a, b;
  switch (problemID) 
  {
  case ProblemID::ParseMatrix:
    try {
      a = Parser::parseMatrix(json["Operand1"]);
      JSON::setErrorCode(response, JSON::Error::OK);
      JSON::setErrorMsg(response, "");
      response["Result"] = nlohmann::json::array();
      JSON::setResult(response, JSON::matrixToJson(a));
      JSON::setMatrixSize(response, a.size1(), a.size2());
    } catch (...) {
      JSON::setErrorCode(response, JSON::Error::BAD_INPUT);
      JSON::setErrorMsg(response, "Ошибка ввода");
    }
    break;
  case ProblemID::ParseQuadratic:
    //    pass
    break;
//------------------------Matrix-------------------------//
  case ProblemID::Sum:
    a = JSON::matrixFromJSON(json["Operand1"]);
    checkMatrixSize(a, socket, response);
    b = JSON::matrixFromJSON(json["Operand2"]);
    checkMatrixSize(b, socket, response);
    Matrix::sum(a, b, response);
    break;
  case ProblemID::Diff:
    a = JSON::matrixFromJSON(json["Operand1"]);
    checkMatrixSize(a, socket, response);
    b = JSON::matrixFromJSON(json["Operand2"]);
    checkMatrixSize(b, socket, response);
    Matrix::diff(a, b, response);
    break;
  case ProblemID::Mult:
    a = JSON::matrixFromJSON(json["Operand1"]);
    checkMatrixSize(a, socket, response);
    b = JSON::matrixFromJSON(json["Operand2"]);
    checkMatrixSize(b, socket, response);
    Matrix::mult(a, b, response);
    break;
  case ProblemID::Inverse:
    a = JSON::matrixFromJSON(json["Operand1"]);
    checkMatrixSize(a, socket, response);
    Matrix::inverse(a, response);
    break;
  case ProblemID::Transpose:
    a = JSON::matrixFromJSON(json["Operand1"]);
    checkMatrixSize(a, socket, response);
    Matrix::transpose(a, response);
    break;
  case ProblemID::Determinant:
    a = JSON::matrixFromJSON(json["Operand1"]);
    checkMatrixSize(a, socket, response);
    Matrix::determinant(a, response);
    break;
  case ProblemID::Rank:
    a = JSON::matrixFromJSON(json["Operand1"]);
    checkMatrixSize(a, socket, response);
    Matrix::rank(a, response);
    break;
  case ProblemID::SMD:
    break;
  case ProblemID::PMD:
    break;
  case ProblemID::GaussianElimination:
    a = JSON::matrixFromJSON(json["Operand1"]);
    checkMatrixSize(a, socket, response);
    Matrix::GaussianElimination(a, response);
    break;
//--------------------------LS---------------------------//
  case ProblemID::MLIS:
    a = JSON::matrixFromJSON(json["Operand1"]);
    checkMatrixSize(a, socket, response);
    LES::maxLinearlyIndependentSubsystem(a, response);
    break;
  case ProblemID::IsLIS:
    a = JSON::matrixFromJSON(json["Operand1"]);
    checkMatrixSize(a, socket, response);
    LES::isLinearlyIndependentSubSystem(a, response);
    break;
  case ProblemID::Basis:
    a = JSON::matrixFromJSON(json["Operand1"]);
    checkMatrixSize(a, socket, response);
    LES::findBasis(a, response);
    break;
//-------------------Linear-Operator----------------------//
  case ProblemID::BasisKernel:
    a = JSON::matrixFromJSON(json["Operand1"]);
    checkMatrixSize(a, socket, response);
    LinearOperator::findImageRankKernelAndDefectOfTheLinearOperator(a, response);
    break;

  default:
    std::cout << "default calledd\n";
    break;
  }
}
//-----------------------------------------------------------------------------
void handle_client(boost::asio::ip::tcp::socket socket) 
{
	boost::system::error_code error;
  char buffer [BUFFER_SIZE];
  nlohmann::json json;
  nlohmann::json response;
  // Read data from client
  size_t bytesTransfered = socket.read_some(boost::asio::buffer(buffer), error);
  if (error)
  {
    JSON::setErrorCodeAndMsg(response, JSON::Error::BAD_INPUT, "Ошибка ввода");
    socket.write_some(boost::asio::buffer(response.dump()));
    return;
  }
  // create string buffer
  std::string data (buffer, bytesTransfered);
  try
  {
    json = nlohmann::json::parse(data);
  }
  catch(nlohmann::json::exception & e)
  {
    JSON::setErrorCodeAndMsg(response, JSON::Error::BAD_INPUT, "Ошибка ввода");
    socket.write_some(boost::asio::buffer(response.dump()));
    return;
  }
  int problemID = json["ProblemID"];
  invokeFunction(static_cast<ProblemID>(problemID), socket, json, response);
  socket.write_some(boost::asio::buffer(response.dump()));
}
//-----------------------------------------------------------------------------
int main() 
{
  using namespace boost::asio;
  io_service service;
  ip::tcp::acceptor acceptor(service,ip::tcp::endpoint(ip::tcp::v4(), PORT_NUM));

  std::cout << "Server is listening now...\n";

  while (true) 
  {
    ip::tcp::socket socket(service);
    acceptor.accept(socket);
    std::thread thread (handle_client, std::move(socket));
    thread.detach();
  }
  return 0;
}
//-----------------------------------------------------------------------------