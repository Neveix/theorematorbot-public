# TheorematorBot

## Установка
### Обновление
`sudo apt-get update && sudo apt-get upgrade -y`

### LaTex инструменты
`sudo apt-get install texlive texlive-latex-extra texlive-fonts-recommended texlive-fonts-extra texlive-lang-cyrillic texlive-extra-utils`
### Python зависимости
`pip install -r requirements.txt`
### GTest
`git clone https://github.com/google/googletest.git`

`mkdir googletest/build && cd googletest/build`

`cmake .. && cmake --build .`

`sudo cmake --install .`

### Остальное
`sudo apt-get install cmake build-essential libboost-dev`


 