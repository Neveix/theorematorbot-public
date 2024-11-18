
set(SOURCES
  lib/parser.hpp
  lib/parser.cpp
  lib/matrix.hpp
  lib/tools.hpp
  lib/json.hpp
  lib/les.hpp
)

add_subdirectory(lib/operationTree)

add_library(math_lib STATIC ${SOURCES})

add_executable(server server.cpp)

add_dependencies(server math_lib operationTree)

target_include_directories(math_lib PUBLIC ${Boost_INCLUDE_DIRS})
target_link_libraries(math_lib PUBLIC ${Boost_LIBRARIES})

target_link_libraries(server PRIVATE math_lib operationTree)
target_include_directories(server PRIVATE . lib)
target_link_directories(server PRIVATE lib)

# target_link_libraries(server math_lib)

if (UNIX)
  install(TARGETS math_lib LIBRARY DESTINATION lib)
endif()
