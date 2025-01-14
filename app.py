from flask import Flask, render_template, request, send_from_directory, redirect, url_for
from yt_dlp import YoutubeDL
import os

app = Flask(__name__)

caminho = "downloads/"
os.makedirs(caminho, exist_ok=True)
formato = ""
nomeArq = None

@app.route("/", methods=["GET", "POST"])
def index(): 
    global nomeArq
    if request.method == "POST":
        url = request.form["url"] 
        try: 
            formato = request.form["format"]
            if formato == "mp3":
                nomeArq = downloadMp3Best(url, caminho)
                return redirect(url_for("downloads"))
            elif formato == "mp4":
                nomeArq = downloadMp4Best(url, caminho)
                return redirect(url_for("downloads"))
        except Exception as e:
            print("Erro!") 
            return render_template("index.html", error=str(e))
    return render_template("index.html")


@app.route("/downloads", methods=["GET"])
def downloads():
    global nomeArq
    print("\n" + caminho + nomeArq +"\n")
    if not nomeArq or not os.path.exists(os.path.join(caminho, nomeArq)):
        return "Erro: Arquivo não encontrado.", 404
    return send_from_directory(caminho, nomeArq, as_attachment=True)



#============================================


def downloadMp4Best(url, caminho="downloads/"):
    
    try:
        ydl_opts = {
            'format': 'bestvideo[height<=1080]+bestaudio[ext=m4a]/best', #[ext=mp3]
                'outtmpl': f'{caminho}%(title)s.%(ext)s',
                'merge_output_format': 'mp4',
        }

        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            nome_arquivo = f"{info['title']}.mp4"
            return nome_arquivo
    
    except Exception as e:
        print(f"\nErro ao baixar em qualidade alta: {e}\n")
        ydl_opts_low = {
            'format': 'best',
            'outtmpl': f'{caminho}%(title)s.%(ext)s',
            'merge_output_format': 'mp4',
            }

        with YoutubeDL(ydl_opts_low) as ydl:
            info = ydl.extract_info(url, download=True)
            nome_arquivo = f"{info['title']}.mp4" #.replace(" ", "_")
            return nome_arquivo

# MP3 pelo gepeto

def downloadMp3Best(url, caminho="downloads/"):
    ydl_opts = {
        'format': 'bestaudio', #'bestaudio/best',
        'outtmpl': f'{caminho}%(title)s.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        nome_arquivo = f"{info['title']}.mp3" #.replace(" ", "_")
        return nome_arquivo


#============================================



if __name__ == "__main__":
    app.run(debug=True)

