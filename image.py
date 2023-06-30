from flask import Flask, render_template, request, send_from_directory
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)

# Конфигурация для загрузки файлов
app.config['UPLOAD_FOLDER'] = 'uploads'  # Папка для сохранения загруженных файлов
app.config['ALLOWED_EXTENSIONS'] = {'txt', 'pdf', 'docx', 'png', 'webp', 'jpg', 'jpeg', ''}  # Разрешенные расширения файлов

# Метод для проверки разрешенных расширений файлов
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def index():
    # Получение списка имен загруженных файлов
    filenames = os.listdir(app.config['UPLOAD_FOLDER'])
    return render_template('hot.html', filenames=filenames)

@app.route('/upload', methods=['POST'])
def upload_file():
    # Получение загруженного файла из запроса
    file = request.files['file']

    # Проверка, что файл был отправлен и имеет допустимое расширение
    if file and allowed_file(file.filename):
        # Безопасное сохранение файла с учетом его имени
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        # Получение списка имен загруженных файлов
        filenames = os.listdir(app.config['UPLOAD_FOLDER'])
        return render_template('hot.html', filenames=filenames)
    else:
        return 'Недопустимый файл. <a href="/">Вернуться</a>'

@app.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    # Путь к папке загруженных файлов
    upload_folder = app.config['UPLOAD_FOLDER']
    # Отправка файла для скачивания
    return send_from_directory(upload_folder, filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
