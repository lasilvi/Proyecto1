from io import BytesIO # nos ayuda a convertir un html en pdf
from django.http import HttpResponse, FileResponse
from django.template.loader import get_template
import reportlab 
from weasyprint import HTML



