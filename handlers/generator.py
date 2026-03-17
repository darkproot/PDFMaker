import os
import json
import tornado.web
from concurrent.futures import ThreadPoolExecutor
from tornado.concurrent import run_on_executor

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

FONT_PATH_1 = os.path.join(os.path.dirname(__file__), '../database/fonts/WorkSans.ttf')
FONT_PATH_2 = os.path.join(os.path.dirname(__file__), '../database/fonts/JetBrains.ttf')

class GeneratorHandler(tornado.web.RequestHandler):

    executor = ThreadPoolExecutor(max_workers=4)

    @run_on_executor
    def generate_pdf(self, texte: str, fichier_sortie: str ="sortie.pdf", marge_gauche: float =2*cm, font: str = "Work sans"):
        """Pour generer un texte sous forme de PDF"""
        pdfmetrics.registerFont(TTFont(font, FONT_PATH_1 if font == 'Work sans' else FONT_PATH_2))
        
        output_file = os.path.join(os.path.dirname(__file__), f'../database/pdf/{fichier_sortie}')
        c = canvas.Canvas(output_file, pagesize=A4)
        largeur, hauteur = A4
        
        c.setFont(font, 12)
        hauteur_ligne = 14
        
        # Largeur disponible pour le texte
        largeur_disponible = largeur - marge_gauche - 2*cm  # marge droite fixe
        
        # Traiter les lignes trop longues
        lignes_finales = []
        for ligne in texte.split('\n'):
            if c.stringWidth(ligne, font, 12) > largeur_disponible:
                # Couper les lignes trop longues
                mots = ligne.split()
                ligne_courante = ""
                for mot in mots:
                    test_ligne = ligne_courante + " " + mot if ligne_courante else mot
                    if c.stringWidth(test_ligne, font, 12) <= largeur_disponible:
                        ligne_courante = test_ligne
                    else:
                        if ligne_courante:
                            lignes_finales.append(ligne_courante)
                        ligne_courante = mot
                if ligne_courante:
                    lignes_finales.append(ligne_courante)
            else:
                lignes_finales.append(ligne)
        
        # Calculer la hauteur totale du texte
        hauteur_texte = len(lignes_finales) * hauteur_ligne
        
        # Position Y de départ pour centrage vertical
        # La position est calculée pour que le texte soit centré verticalement
        y_depart = (hauteur + hauteur_texte) / 2
        
        # Dessiner le texte aligné à gauche (pas de centrage horizontal)
        for i, ligne in enumerate(lignes_finales):
            # x fixe pour alignement à gauche (avec marge)
            x = marge_gauche
            # y calculé pour le centrage vertical
            y = y_depart - (i * hauteur_ligne)
            c.drawString(x, y, ligne)
        
        c.save()
        return True

    async def post(self):
        data = json.loads(self.request.body)
        text = data.get("text", None)
        font = data.get("font", None)

        if (not text) or (not font): self.send_error(400)
        else: 
            self.generate_pdf(texte=text, font=font)
            self.write({"name": "sortie.pdf"})