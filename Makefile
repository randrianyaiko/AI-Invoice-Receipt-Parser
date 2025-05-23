install:
	sudo apt install tesseract-ocr -y
	sudo apt install tesseract-ocr-all -y
	pip install -r requirements.txt

build:
	docker build -t ocr-app .

run:
	docker run -p 8501:8501 ocr-app