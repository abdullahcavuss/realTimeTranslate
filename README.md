# What is realTimeTranslate?
It is a simple real-time translation application that transforms the picture taken from the screenshot into text with **tesseract**, then translates it to the language you want and displays it on the screen. Frankly, I wrote this program so as not to constantly go to translation while reading a pdf file.

![Alt Text](http://kozmonott.com/images/rtt.gif)

### How to Install?

##### 1) Install Tesseract
Download from [here](https://digi.bib.uni-mannheim.de/tesseract/tesseract-ocr-w64-setup-v5.0.0-alpha.20200328.exe) and install. I installed to "C:\Tesseract-OCR\tesseract.exe". If you are going to install it somewhere else, you need to change the path in code.

    pytesseract.pytesseract.tesseract_cmd = r"C:\Tesseract-OCR\tesseract.exe"

##### 2) Install Python Modules
You can install the necessary modules by typing the following code in the folder.

	pip install -r requirements.txt

### How to Use?
##### Start Program
You can start the program by typing the code below in the terminal. After that, just take the mouse wherever you want to translate.

	python realTimeTranslate.py
    
##### Change Language
You can change language from here

    result = translate(details, 'tr','en') #translate(text,dest,src)

##### Change Translating Area
You can change translating are from here 

    w=1000 #width
    h=130  #height
    
Also you can increase the height with the "+" key and decrease with the "-" key while the program is running.
