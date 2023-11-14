pip install -r requirements.txt

:: python main.py

pyinstaller --window --onefile --add-data "data;data" main.py
:: dist\main.exe
