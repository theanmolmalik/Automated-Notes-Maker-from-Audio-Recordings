from distutils.command.config import LANG_EXT
from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
import os
import speech_recognition as sr
# from googletrans import Translator
from translate import Translator
from fpdf import FPDF 
from django.http import FileResponse
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

def index(request):
    return render(request,'index.html')
    
@csrf_exempt
def upload(request):    
	if request.FILES:
		img_path=os.path.join(settings.BASE_DIR,'Hello.wav')
		destination = open(img_path, 'wb+')
		for chunk in request.FILES['image'].chunks():
			destination.write(chunk)
		destination.close()				

		# Downloading File
		
	return HttpResponse('done')


def download(file_path):	
	response = FileResponse(open(file_path, 'rb'))
	return response
	
dic=('afrikaans', 'af', 'albanian', 'sq', 'amharic', 'am', 
     'arabic', 'ar', 'armenian', 'hy', 'azerbaijani', 'az',
 'basque', 'eu', 'belarusian', 'be', 'bengali', 'bn', 'bosnian',
     'bs', 'bulgarian', 'bg', 'catalan', 'ca',
  'cebuano', 'ceb', 'chichewa', 'ny', 'chinese (simplified)',
     'zh-cn', 'chinese (traditional)', 'zh-tw',
  'corsican', 'co', 'croatian', 'hr', 'czech', 'cs', 'danish',
     'da', 'dutch', 'nl', 'english', 'en', 'esperanto',
  'eo', 'estonian', 'et', 'filipino', 'tl', 'finnish', 'fi', 
     'french', 'fr', 'frisian', 'fy', 'galician', 'gl',
  'georgian', 'ka', 'german', 'de', 'greek', 'el', 'gujarati', 
     'gu', 'haitian creole', 'ht', 'hausa', 'ha', 
  'hawaiian', 'haw', 'hebrew', 'he', 'hindi', 'hi', 'hmong', 
     'hmn', 'hungarian', 'hu', 'icelandic', 'is', 'igbo',
  'ig', 'indonesian', 'id', 'irish', 'ga', 'italian', 'it', 
     'japanese', 'ja', 'javanese', 'jw', 'kannada', 'kn',
  'kazakh', 'kk', 'khmer', 'km', 'korean', 'ko', 'kurdish (kurmanji)',
     'ku', 'kyrgyz', 'ky', 'lao', 'lo', 
  'latin', 'la', 'latvian', 'lv', 'lithuanian', 'lt', 'luxembourgish',
     'lb', 'macedonian', 'mk', 'malagasy',
  'mg', 'malay', 'ms', 'malayalam', 'ml', 'maltese', 'mt', 'maori',
     'mi', 'marathi', 'mr', 'mongolian', 'mn',
  'myanmar (burmese)', 'my', 'nepali', 'ne', 'norwegian', 'no',
     'odia', 'or', 'pashto', 'ps', 'persian',
   'fa', 'polish', 'pl', 'portuguese', 'pt', 'punjabi', 'pa',
     'romanian', 'ro', 'russian', 'ru', 'samoan',
   'sm', 'scots gaelic', 'gd', 'serbian', 'sr', 'sesotho', 
     'st', 'shona', 'sn', 'sindhi', 'sd', 'sinhala',
   'si', 'slovak', 'sk', 'slovenian', 'sl', 'somali', 'so', 
     'spanish', 'es', 'sundanese', 'su', 
  'swahili', 'sw', 'swedish', 'sv', 'tajik', 'tg', 'tamil',
     'ta', 'telugu', 'te', 'thai', 'th', 'turkish', 'tr',
  'ukrainian', 'uk', 'urdu', 'ur', 'uyghur', 'ug', 'uzbek', 
     'uz', 'vietnamese', 'vi', 'welsh', 'cy', 'xhosa', 'xh',
  'yiddish', 'yi', 'yoruba', 'yo', 'zulu', 'zu')

def convert_audio_to_pdf_and_download(request):	
	lang=request.GET['lang']
	print (lang,'----')
	# Importing Audio File
	sound=os.path.join(settings.BASE_DIR,'Hello.wav')
	# sound = "/content/Hello.wav"

	r = sr.Recognizer()
	
	text = ""

	with sr.AudioFile(sound) as source:
		r.adjust_for_ambient_noise(source)

		# Listening Audio
		audio = r.listen(source)
		
	try:
		# Converting Audio to Text
		text = r.recognize_google(audio,language=lang)

	except Exception as e:
		print("Error!!!".format(e))
		
	# Invoking the Translator
	#translator = Translator()
	translator= Translator(from_lang=lang,to_lang="en")
	translation = translator.translate(text)
	text=translation
		
	# Translating to the desired Language
	#text = translator.translate(text,dest="en-US",src=lang)
	#text = text_to_translate
	# text=translation

	# ts._google.language_map
	# ts.google(text, from_language=lang, to_language='en')
	
	# Converting Text to PDF
	pdf = FPDF()
	pdf.add_page()
	pdf.set_xy(10, 10)
	pdf.set_font('arial', 'B', 13.0)
	pdf.cell(ln=0, h=5.0, align='L', w=0, txt=text, border=50)
	path=os.path.join(settings.BASE_DIR,'Output.pdf')
	pdf.output(path, 'F')
	output=os.path.join(settings.BASE_DIR,'Output.pdf')	
	return download(output)
