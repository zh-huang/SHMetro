pip install -r requirements.txt

# python3 main.py

pyinstaller --window --onefile --add-data "data:data" main.py
# ./dist/main
