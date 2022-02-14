#!/usr/bin/env python
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter, XMLConverter, HTMLConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from io import BytesIO
from io import StringIO 
import warnings
#Fonction permettant de convertir le pdf en TXT

def convert_pdf(path, format, codec, password):
        rsrcmgr = PDFResourceManager()
        retstr = StringIO()
        laparams = LAParams()
        if format == 'text':
            device = TextConverter(rsrcmgr, retstr, codec, laparams=laparams)
        elif format == 'html':
            retstr = BytesIO()
            device = HTMLConverter(rsrcmgr, retstr, laparams=laparams)
        elif format == 'xml':
            device = XMLConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
        else:
            raise ValueError('provide format, either text, html or xml!')

        fp = open(path, 'rb')
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        maxpages = 0
        caching = True
        pagenos=set()
        for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password,caching=caching, check_extractable=False):
            interpreter.process_page(page)
        text = retstr.getvalue()
        fp.close()
        device.close()
        retstr.close()
        return text
warnings.filterwarnings('ignore') #supprime le warning non bloquant de certains metadata dans le contenu du fichier pdf       


