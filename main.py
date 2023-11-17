import qrcode, threading, io, secrets, socket, os, string

from flask import Flask, send_file, request, render_template
from waitress import serve

def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    local_ip = s.getsockname()[0]
    s.close()
    return local_ip

class secure:
    key_and_path = {}
    
    def generate_random_string(length: int = 48):
        return "".join([secrets.choice(string.ascii_lowercase + string.ascii_uppercase + string.digits) for _ in range(length)])

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    BLACK = '\033[30m'
    WHITE = '\033[97m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

app = Flask(__name__)

def generate_qr(url):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=1,
        border=2
    )
    qr.add_data(url)
    qr.make(fit=True)

    file = io.StringIO()
    qr.print_ascii(out=file)
    file.seek(0)
    return bcolors.WHITE + file.read().replace("█", "23").replace(" ", "█").replace("▀", "24").replace("▄", "▀").replace("23", " ").replace("24", "▄") + bcolors.ENDC

@app.route("/get_file/<key>")
def send(key: str):
    if key not in secure.key_and_path:
        return "Incorrect key!"
    try:
        print(f"\r{bcolors.OKGREEN}Был загружен файл \"{secure.key_and_path[key]}\"{bcolors.ENDC}\n: ")
        return send_file(secure.key_and_path[key], as_attachment=True)
    except:
        return "File not found!"

@app.route("/upload", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        # Получаем загруженный файл
        uploaded_file = request.files["file"]

        if uploaded_file:
            # Сохраняем файл на сервере (в данном случае, в текущей директории)
            uploaded_file.save(uploaded_file.filename)

            # Выводим сообщение об успешной загрузке
            return render_template("upload.html", suc=True)
    
    # Если это GET-запрос, отображаем форму для загрузки файла
    return render_template("upload.html")

def main():
    if not os.path.exists("iReadReadme"):
        print(f"{bcolors.WARNING}Перед использованием рекомендуется ознакомиться с инструкцией.{bcolors.ENDC}\n\n{bcolors.WHITE}Для того, чтобы создать QR-код с ссылкой на загрузку файла, необходимо ввести в консоль путь к файлу, либо перетацить его в нее. Ссылки на загружаемые файлы сбрасываются после каждого завершения работы скрипта.\nДля того, чтобы загрузить файл на пк, нужно ввести ключевое слово \"upload\".{bcolors.ENDC}")
        input("\nНажмите Enter для продолжения: ")
        with open("iReadReadme", "w"):
            pass
    def _():
        while True:
            try:
                path = input(f"Введите путь к файлу\nВведите \"upload\", если хотите отправить файл и загрузить его на пк\n: {bcolors.OKCYAN}")
            except:
                print(f"{bcolors.WARNING}Выход...{bcolors.ENDC}")
                exit()
            if path == "upload":
                url = f"http://{get_local_ip()}:3454/upload"
                print(generate_qr(url))
                print(f"Отсканируйте QR-код, либо перейдите по ссылке: {bcolors.BOLD}{url}{bcolors.ENDC}")
                continue
            path = path.replace("\"", "", 1) if path.startswith("\"") else path
            path = path.replace("\"", "\\`234") if path.endswith("\"") else path
            path = path.replace("\\`234", "\"", (path.count("\\`234") - 1)) if "\\`234" in path else path
            path = path.replace("\\`234", "") if "\\`234" in path else path
            path = os.path.abspath(path)
            if not os.path.exists(path):
                print(f"{bcolors.FAIL}Такого файла не существует!{bcolors.ENDC}")
                continue
            if os.path.isdir(path):
                print(f"{bcolors.FAIL}Это папка!{bcolors.ENDC}")
                continue
            key = secure.generate_random_string(48)
            secure.key_and_path[key] = path
            url = f"http://{get_local_ip()}:3454/get_file/{key}"
            print(generate_qr(url))
            print(f"Отсканируйте QR-код, либо перейдите по ссылке: {bcolors.BOLD}{url}{bcolors.ENDC}")
    thread = threading.Thread(target=_)
    thread.start()    

main()
serve(app, host="0.0.0.0", port=3454)