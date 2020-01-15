from flask import Flask, render_template, request

LINK_TEMPLATE = "https://www.youtube.com/watch?v={link}"

videos_data = {
    1: {'id': 1,
        'title': "Гарри Поттер и Философский камень",
        'link': '4QljrvtuJ94',
        'description': 'Книга c иллюстрациями Джима Кея. Автор Джоан Роулинг. Часть 1',
        'tags': ['Джоан Роулинг', 'фэнтези', 'Джим Кей'],
        'playlist': 1},
    2: {'id': 2,
        'title': "Гарри Поттер и Тайная комната",
        'link': 'HZiCMJMmYIg',
        'description': 'Книга c иллюстрациями Джима Кея. Автор Джоан Роулинг. Часть 2',
        'tags': ['Джоан Роулинг', 'фэнтези', 'Джим Кей'],
        'playlist': 1},
    3: {'id': 3,
        'title': "Гарри Поттер и узник Азкабана",
        'link': 'BJF6MX-Bn3w',
        'description': 'Книга c иллюстрациями Джима Кея. Автор Джоан Роулинг. Часть 3',
        'tags': ['Джоан Роулинг', 'фэнтези', 'Джим Кей'],
        'playlist': 1},
    4: {'id': 4,
        'title': "Алиса в Зазеркалье",
        'link': 'SyPEAUlveJ4',
        'description': 'В этой книге оживает Викторианская эпоха, всем известная книга Льюиса Кэрролла в новом прдставлении!',
        'tags': ['Люис Кэрол', 'фэнтези'],
        'playlist': 4},
}
playlist_data = {
    1: {'id': 1,
        'title': 'Младшешкольники',
        'description': 'Книги ориентированные на возраст старших дошкольников или учеников 1-2 классовка',
        'videos': [1, 2, 3]},
    2: {'id': 2,
        'title': 'Фэнтези',
        'description': 'Книги написанные в жанре фэнтези',
        'videos': [1, 2, 3, 4]}
}
tags_data = list(set(tag for video in videos_data.values() for tag in video['tags']))
tags_data.sort()

def get_videos_by_text(text):
    video_list = []
    if text == '' or text is None:
        return video_list

    for video in videos_data.values():
        if (text in video['tags']) or (text in video['title']) or (text in video['description']):
            video_list.append(video)
    return video_list


app = Flask(__name__)

@app.route('/')
def main():
    output = render_template("index.html", tags=tags_data, videos=playlist_data)
    return output


@app.route('/about')
def about():
    output = render_template("about.html")
    return output


@app.route('/playlists/<id>/<video_id>')
def video(id, video_id):
    id = int(id)
    current_playlist = playlist_data.get(id)

    if current_playlist is None:
        output = render_template("404.html")
        return output

    video_id = int(video_id)
    if video_id not in current_playlist['videos']:
        video_id = 0

    video_list = []
    for id_video in current_playlist['videos']:
        video_list.append(videos_data.get(id_video))

    output = render_template("playlist.html", playlist=current_playlist, video=videos_data[video_id],
                             list=video_list)
    return output


@app.route('/playlists/<id>/')
def playlist(id):
    id = int(id)
    current_playlist = playlist_data.get(id)

    if current_playlist is None:
        output = render_template("404.html")
        return output

    first_video = current_playlist['videos'][0]

    video_list = []
    for video_id in current_playlist['videos']:
        video_list.append(videos_data.get(video_id))

    output = render_template("playlist.html", playlist=current_playlist, video=videos_data[first_video],
                             list=video_list)
    return output

@app.route('/search')
def search():
    search_text = request.values.get("q")
    result = get_videos_by_text(search_text)
    output = render_template("search.html", tags=tags_data, result=result)
    return output

@app.errorhandler(404)
def page_not_found(error):
    output = render_template("404.html")
    return output

app.run()
