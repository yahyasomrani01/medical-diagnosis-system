import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont

def generate_pdf(patient_data):
    """
    Generate a PDF prescription for the given patient data.
    Returns a BytesIO buffer containing the PDF.
    """
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4
    
    # Header
    p.setFont("Helvetica-Bold", 18)
    p.drawCentredString(width/2, height - 20*mm, "Système de Diagnostic Médical")
    
    p.setFont("Helvetica", 14)
    p.drawCentredString(width/2, height - 30*mm, "SERVICE LABORATOIRE")
    
    # Line
    p.setLineWidth(0.5)
    p.line(20*mm, height - 35*mm, width - 20*mm, height - 35*mm)
    
    # Title
    p.setFont("Helvetica-Bold", 16)
    p.drawCentredString(width/2, height - 45*mm, "ORDONNANCE MÉDICALE")
    
    # Patient Info
    p.setFont("Helvetica", 12)
    date_str = datetime.now().strftime("%d/%m/%Y")
    
    # Right aligned date
    p.drawRightString(width - 20*mm, height - 55*mm, f"Date: {date_str}")
    
    # Left aligned patient info
    # Note: Patient name is not stored in DB currently, we only have ID. 
    # But the frontend sends it. However, for this backend generation from DB ID, 
    # we might only have what's in the DB.
    # If we want the name, we should have stored it or pass it in the request.
    # The current model doesn't store name.
    # Let's use "Patient ID: {id}" for now.
    
    p.drawString(20*mm, height - 65*mm, f"Patient ID: {patient_data.id}")
    p.drawString(20*mm, height - 75*mm, f"Age: {patient_data.age} ans")
    p.drawString(20*mm, height - 85*mm, f"Sexe: {'Masculin' if patient_data.gender == 'M' else 'Féminin'}")
    
    # Diagnosis
    p.setFont("Helvetica-Bold", 12)
    p.drawString(20*mm, height - 100*mm, "DIAGNOSTIC:")
    
    p.setFont("Helvetica", 12)
    # Simple mapping for display
    diagnosis_map = {
        'SAIN': 'Patient Sain',
        'DIABETE': 'Diabète',
        'HYPERLIPIDEMIE': 'Hyperlipidémie',
        'RENAL': 'Insuffisance Rénale',
        'HEPATIQUE': 'Insuffisance Hépatique'
    }
    diagnosis_display = diagnosis_map.get(patient_data.diagnosis, patient_data.diagnosis)
    
    if patient_data.diagnosis == 'SAIN':
        p.setFillColorRGB(0, 0.5, 0) # Green
    else:
        p.setFillColorRGB(0.8, 0.2, 0.2) # Red
        
    p.drawString(60*mm, height - 100*mm, diagnosis_display)
    p.setFillColorRGB(0, 0, 0) # Reset to black
    
    # Lab Results Summary
    p.setFont("Helvetica-Bold", 12)
    p.drawString(20*mm, height - 115*mm, "RÉSULTATS D'ANALYSE:")
    p.setFont("Helvetica", 10)
    
    y = height - 125*mm
    results = [
        f"Glucose: {patient_data.glucose} mmol/L",
        f"Cholestérol: {patient_data.cholesterol} mmol/L",
        f"Triglycérides: {patient_data.triglycerides} mmol/L",
        f"Créatinine: {patient_data.creatinine} µmol/L",
        f"Urée: {patient_data.uree} mmol/L",
        f"Acide Urique: {patient_data.uric_acid} µmol/L",
        f"GOT: {patient_data.got} U/L",
        f"GPT: {patient_data.gpt} U/L",
        f"Bilirubine: {patient_data.bilirubin} µmol/L"
    ]
    
    for res in results:
        p.drawString(30*mm, y, f"- {res}")
        y -= 6*mm
        
    # Treatment
    y -= 10*mm
    p.setFont("Helvetica-Bold", 12)
    p.drawString(20*mm, y, "TRAITEMENT PRESCRIT:")
    p.setFont("Helvetica", 12)
    
    y -= 10*mm
    medications = get_medications(patient_data.diagnosis)
    
    for med in medications:
        p.drawString(30*mm, y, f"- {med}")
        y -= 8*mm
        
    # Footer
    p.setFont("Helvetica", 10)
    p.drawCentredString(width/2, 30*mm, "Signature du Médecin:")
    
    p.showPage()
    p.save()
    
    buffer.seek(0)
    return buffer

def get_medications(diagnosis):
    if diagnosis == 'DIABETE':
        return [
            "Metformine 500mg (1 comprimé 2 fois par jour)",
            "Insuline (selon protocole)",
            "Régime alimentaire pauvre en sucre",
            "Activité physique régulière"
        ]
    elif diagnosis == 'HYPERLIPIDEMIE':
        return [
            "Atorvastatine 20mg (1 comprimé le soir)",
            "Régime pauvre en graisses saturées",
            "Oméga-3 (1 capsule par jour)"
        ]
    elif diagnosis == 'RENAL':
        return [
            "Contrôle strict de la tension artérielle",
            "Régime pauvre en sel et en protéines",
            "Suivi néphrologique recommandé",
            "Éviter les AINS"
        ]
    elif diagnosis == 'HEPATIQUE':
        return [
            "Repos strict",
            "Arrêt total de l'alcool",
            "Régime hépatoprotecteur",
            "Vitamines B complexe"
        ]
    elif diagnosis == 'SAIN':
        return [
            "Aucun traitement médicamenteux nécessaire",
            "Maintenir une hygiène de vie saine",
            "Bilan de contrôle dans 1 an"
        ]
    else:
        return ["Consulter un spécialiste pour avis complémentaire"]

def generate_prescription_image(patient_data):
    """
    Generate a PNG prescription image for the given patient data.
    Returns a BytesIO buffer containing the PNG image.
    """
    # Create a white image
    width, height = 800, 1000
    img = Image.new('RGB', (width, height), color='white')
    d = ImageDraw.Draw(img)
    
    # Try to load a font, fallback to default
    try:
        # Try to find a standard font
        font_large = ImageFont.truetype("Arial.ttf", 36)
        font_medium = ImageFont.truetype("Arial.ttf", 24)
        font_small = ImageFont.truetype("Arial.ttf", 18)
        font_bold = ImageFont.truetype("Arial Bold.ttf", 24)
    except IOError:
        # Fallback for Linux/Mac if Arial not found
        try:
            font_large = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 36)
            font_medium = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 24)
            font_small = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 18)
            font_bold = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 24)
        except IOError:
             # Last resort default font
            font_large = ImageFont.load_default()
            font_medium = ImageFont.load_default()
            font_small = ImageFont.load_default()
            font_bold = ImageFont.load_default()

    # Header
    d.text((width/2, 50), "HOPITAL DE CIRCONSCRIPTION DE BOUSALEM", fill="black", anchor="ms", font=font_large)
    d.text((width/2, 90), "SERVICE LABORATOIRE", fill="black", anchor="ms", font=font_medium)
    
    # Line
    d.line((50, 110, width-50, 110), fill="black", width=2)
    
    # Title
    d.text((width/2, 150), "ORDONNANCE MÉDICALE", fill="black", anchor="ms", font=font_bold)
    
    # Patient Info
    date_str = datetime.now().strftime("%d/%m/%Y")
    d.text((width-50, 180), f"Date: {date_str}", fill="black", anchor="rs", font=font_small)
    
    y = 220
    d.text((50, y), f"Patient ID: {patient_data.id}", fill="black", font=font_small)
    y += 30
    d.text((50, y), f"Age: {patient_data.age} ans", fill="black", font=font_small)
    y += 30
    d.text((50, y), f"Sexe: {'Masculin' if patient_data.gender == 'M' else 'Féminin'}", fill="black", font=font_small)
    
    # Diagnosis
    y += 50
    d.text((50, y), "DIAGNOSTIC:", fill="black", font=font_bold)
    
    diagnosis_map = {
        'SAIN': 'Patient Sain',
        'DIABETE': 'Diabète',
        'HYPERLIPIDEMIE': 'Hyperlipidémie',
        'RENAL': 'Insuffisance Rénale',
        'HEPATIQUE': 'Insuffisance Hépatique'
    }
    diagnosis_display = diagnosis_map.get(patient_data.diagnosis, patient_data.diagnosis)
    
    color = (0, 128, 0) if patient_data.diagnosis == 'SAIN' else (204, 51, 51)
    d.text((250, y), diagnosis_display, fill=color, font=font_medium)
    
    # Lab Results
    y += 50
    d.text((50, y), "RÉSULTATS D'ANALYSE:", fill="black", font=font_bold)
    y += 30
    
    results = [
        f"Glucose: {patient_data.glucose} mmol/L",
        f"Cholestérol: {patient_data.cholesterol} mmol/L",
        f"Triglycérides: {patient_data.triglycerides} mmol/L",
        f"Créatinine: {patient_data.creatinine} µmol/L",
        f"Urée: {patient_data.uree} mmol/L",
        f"Acide Urique: {patient_data.uric_acid} µmol/L",
        f"GOT: {patient_data.got} U/L",
        f"GPT: {patient_data.gpt} U/L",
        f"Bilirubine: {patient_data.bilirubin} µmol/L"
    ]
    
    for res in results:
        d.text((80, y), f"- {res}", fill="black", font=font_small)
        y += 25
        
    # Treatment
    y += 30
    d.text((50, y), "TRAITEMENT PRESCRIT:", fill="black", font=font_bold)
    y += 30
    
    medications = get_medications(patient_data.diagnosis)
    
    for med in medications:
        d.text((80, y), f"- {med}", fill="black", font=font_small)
        y += 30
        
    # Footer
    d.text((width/2, height-100), "Signature du Médecin:", fill="black", anchor="ms", font=font_medium)
    
    buffer = io.BytesIO()
    img.save(buffer, format='PNG')
    buffer.seek(0)
    return buffer
