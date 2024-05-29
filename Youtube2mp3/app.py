import os
from flask import Flask, render_template, request, send_from_directory, redirect, url_for
from pytube import YouTube

app = Flask(__name__)

DOWNLOAD_FOLDER = './downloads'
app.config['DOWNLOAD_FOLDER'] = DOWNLOAD_FOLDER


@app.route('/')
def landing_page():
    return render_template('landing_page.html')


@app.route('/download', methods=['POST'])
def download():
    try:
        video_url = request.form['url']
        download_type = request.form['download_type']

        yt = YouTube(video_url)

        if download_type == 'video':
            stream = yt.streams.filter(file_extension='mp4', progressive=True).first()
        else:
            stream = yt.streams.filter(only_audio=True,file_extension='mp3').first()

        stream.download(app.config['DOWNLOAD_FOLDER'])
        message = f"Downloaded successfully to '{app.config['DOWNLOAD_FOLDER']}'"
    except Exception as e:
        message = f"Error: {str(e)}"

    files = os.listdir(app.config['DOWNLOAD_FOLDER'])
    return render_template('index.html', message=message, files=files)


@app.route('/downloads')
def downloads():
    files = os.listdir(app.config['DOWNLOAD_FOLDER'])
    return render_template('downloads.html', files=files)


@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(app.config['DOWNLOAD_FOLDER'], filename)


@app.route('/delete/<filename>')
def delete_file(filename):
    try:
        file_path = os.path.join(app.config['DOWNLOAD_FOLDER'], filename)
        os.remove(file_path)
        message = f"Deleted file: {filename}"
    except Exception as e:
        message = f"Error deleting file: {str(e)}"

    files = os.listdir(app.config['DOWNLOAD_FOLDER'])
    return render_template('index.html', message=message, files=files)


if __name__ == '__main__':
    app.run(debug=True)
