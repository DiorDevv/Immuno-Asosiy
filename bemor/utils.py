from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from django.http import HttpResponse
from .models import Bemor

def generate_bemor_pdf(bemor_id):
    try:
        bemor = Bemor.objects.get(id=bemor_id)
    except Bemor.DoesNotExist:
        return HttpResponse("Bunday bemor topilmadi", status=404)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="Bemor_{bemor.bemor.ism}.pdf"'

    p = canvas.Canvas(response, pagesize=A4)

    # PDF sarlavhasi
    p.setFont("Helvetica-Bold", 16)
    p.drawString(200, 800, "Bemor ma'lumotlari")

    # Bemorning shaxsiy ma'lumotlari
    p.setFont("Helvetica", 12)
    p.drawString(100, 770, f"JSHSHIR: {bemor.bemor.JSHSHIR}")
    p.drawString(100, 750, f"Ism: {bemor.bemor.ism}")
    p.drawString(100, 730, f"Familiya: {bemor.bemor.familiya}")
    p.drawString(100, 710, f"Tug'ilgan sana: {bemor.bemor.tugilgan_sana}")
    p.drawString(100, 690, f"Jinsi: {'Erkak' if bemor.bemor.jinsi == 'M' else 'Ayol'}")


    # Bemor manzili
    if bemor.manzil:
        p.setFont("Helvetica-Bold", 14)
        p.drawString(100, 660, "Manzil:")
        p.setFont("Helvetica", 12)
        p.drawString(120, 640, f"Mamlakat: {bemor.manzil.mamlakat}")
        if bemor.manzil.viloyat:
            p.drawString(120, 620, f"Viloyat: {bemor.manzil.viloyat}")
        if bemor.manzil.tuman:
            p.drawString(120, 600, f"Tuman: {bemor.manzil.tuman}")
        p.drawString(120, 580, f"Mahalla: {bemor.manzil.mahalla}")
        p.drawString(120, 560, f"Ko'cha: {bemor.manzil.kocha_nomi}")

    # Bemor holati
    if bemor.bemor_holati:
        p.setFont("Helvetica-Bold", 14)
        p.drawString(100, 530, "Holati:")
        p.setFont("Helvetica", 12)
        p.drawString(120, 510, f"{bemor.bemor_holati.holati}")
        p.drawString(120, 490, f"O'zgarish: {bemor.bemor_holati.ozgarish}")

    # Operatsiya haqida ma'lumot
    if bemor.operatsiya_bolgan_joy:
        p.setFont("Helvetica-Bold", 14)
        p.drawString(100, 460, "Operatsiya ma'lumotlari:")
        p.setFont("Helvetica", 12)
        p.drawString(120, 440, f"Mamlakat: {bemor.operatsiya_bolgan_joy.mamlakat}")
        p.drawString(120, 420, f"Joy: {bemor.operatsiya_bolgan_joy.operatsiya_bolgan_joy}")
        p.drawString(120, 400, f"Transplantatsiya sanasi: {bemor.operatsiya_bolgan_joy.transplantatsiya_sana}")
        p.drawString(120, 380, f"Operatsiya: {bemor.operatsiya_bolgan_joy.transplantatsiya_operatsiyasi}")
        p.drawString(120, 360, f"Ishlatilgan miqdor: {bemor.operatsiya_bolgan_joy.ishlatilgan_miqdor}")

    # Qo'shimcha ma'lumotlar
    if bemor.qoshimcha_malumotlar:
        p.setFont("Helvetica-Bold", 14)
        p.drawString(100, 330, "Qo'shimcha ma'lumotlar:")
        p.setFont("Helvetica", 12)
        p.drawString(120, 310, bemor.qoshimcha_malumotlar)

    # Arxiv ma'lumotlari
    if bemor.arxivga_olingan_sana:
        p.setFont("Helvetica-Bold", 14)
        p.drawString(100, 280, "Arxiv ma'lumotlari:")
        p.setFont("Helvetica", 12)
        p.drawString(120, 260, f"Arxivga olingan sana: {bemor.arxivga_olingan_sana}")
        if bemor.arxiv_sababi:
            p.drawString(120, 240, f"Sababi: {bemor.arxiv_sababi}")
        if bemor.arxiv_izoh:
            p.drawString(120, 220, f"Izoh: {bemor.arxiv_izoh}")

    p.showPage()
    p.save()

    return response
