# Europa
Europa is a 2D pixel puzzle horror game set on a submarine outpost on Europa, Jupiter’s moon. It runs using pygame.

# Run Instructions
```bash
pip install -r requirements.txt
```
```bash
python Europa.py
```

# Build Instructions 
```bash
pip install -r requirements.txt
```
```bash
pyinstaller --onefile --add-data "Assets;Assets" --add-data "Audio;Audio" Europa.py
```