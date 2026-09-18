import sys
import os

# Добавляем директорию src в путь поиска модулей
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

from heat_exchanger.cli import main

if __name__ == "__main__":
    main()