import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import feedparser



#config email
EMAIL_REMETENTE = "fag.almeida2@gmail.com"
SENHA_REMETENTE = "faol vpjn xuoq mebo"
EMAIL_DESTINATARIO = "flalmeida.ag@gmail.com"


#Dicionário mapeando os temas escolhidos para suas respectivas fontes
FEED_NOTICIAS = {
    "Clima & Tempo": "https://g1.globo.com/rss/g1/clima-e-tempo/",
    "Política": "https://www.g1.com.br/rss/g1/politica/",
    "Shows & Música": "https://www.g1.com.br/rss/g1/pop-arte/"
}

def buscar_noticias():
    resumo_noticias = []

    for categoria, url in FEED_NOTICIAS.items():
        print(f"Buscando notícias sobre {categoria}...")
        feed = feedparser.parse(url)

        resumo_noticias.append(f"\n=== {categoria.upper()} ===")

        #pega as 3 noticias mais recentes de cada categoria
        for item in feed.entries[:3]:
            titulo = item.title
            link = item.link
            resumo_noticias.append(f"- {titulo}\n Link: {link}")

    return "\n".join(resumo_noticias)

def enviar_email(conteudo):
     msg = MIMEMultipart()
     msg['From'] = EMAIL_REMETENTE 
     msg['To'] = EMAIL_DESTINATARIO 
     msg['Subject'] = "Seu resumo diário de notícias"

     msg.attach(MIMEText(conteudo, 'plain', 'utf-8'))

     try:
          print("conectando ao servidor SMTP...")
          servidor = smtplib.SMTP('smtp.gmail.com', 587)
          servidor.starttls()
          servidor.login(EMAIL_REMETENTE, SENHA_REMETENTE)

          texto_email = msg.as_string()
          servidor.sendmail(EMAIL_REMETENTE, EMAIL_DESTINATARIO, texto_email)
          servidor.quit()

          print("Email enviado com sucesso!")
     except Exception as e:
        print(f"Erro ao enviar email: {e}")

if __name__ == "__main__":
    print("buscando noticias")
    noticias = buscar_noticias()
    print("enviando email")
    enviar_email(noticias) 
