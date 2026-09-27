import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import feedparser
from http.server import BaseHTTPRequestHandler

# --- CONFIGURAÇÕES VIA VARIÁVEIS DE AMBIENTE ---
EMAIL_REMETENTE = os.environ.get("EMAIL_REMETENTE")
SENHA_REMETENTE = os.environ.get("SENHA_REMETENTE")
EMAIL_DESTINATARIO = os.environ.get("EMAIL_DESTINATARIO")

FEEDS_NOTICIAS = {
    "Clima & Tempo": "https://g1.globo.com/rss/g1/natureza/",
    "Política": "https://g1.globo.com/rss/g1/politica/",
    "Shows & Música": "https://g1.globo.com/rss/g1/pop-arte/"
}

def buscar_noticias():
    resumo_noticias = []
    for categoria, url in FEEDS_NOTICIAS.items():
        feed = feedparser.parse(url)
        resumo_noticias.append(f"=== {categoria.upper()} ===\n")
        for item in feed.entries[:3]:
            resumo_noticias.append(f"• {item.title}\n  {item.link}\n")
    return "\n".join(resumo_noticias)

def enviar_email(conteudo):
    msg = MIMEMultipart()
    msg['From'] = EMAIL_REMETENTE
    msg['To'] = EMAIL_DESTINATARIO
    msg['Subject'] = "📰 Seu Resumo Diário de Notícias"
    msg.attach(MIMEText(conteudo, 'plain', 'utf-8'))

    servidor = smtplib.SMTP('smtp.gmail.com', 587)
    servidor.starttls()
    servidor.login(EMAIL_REMETENTE, SENHA_REMETENTE)
    servidor.sendmail(EMAIL_REMETENTE, EMAIL_DESTINATARIO, msg.as_string())
    servidor.quit()

# Handler exigido pela Vercel
class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            noticias = buscar_noticias()
            enviar_email(noticias)
            self.send_response(200)
            self.send_header('Content-type', 'text/plain; charset=utf-8')
            self.end_headers()
            self.wfile.write('E-mail enviado com sucesso!'.encode('utf-8'))
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'text/plain; charset=utf-8')
            self.end_headers()
            self.wfile.write(f'Erro: {str(e)}'.encode('utf-8'))