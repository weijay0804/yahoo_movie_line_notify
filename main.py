from yahoo_movie.helper import RequestHelper
from config import Config
from yahoo_movie import YahooMovie


def send_notify(token: str, message: str):
    """發送 line notify

    Args:
        token (str): line token
    """

    headers = {"Authorization": f"Bearer {token}"}

    data = {"message": message}

    RequestHelper.post(
        "https://notify-api.line.me/api/notify", headers=headers, data=data
    )


def main(*_):

    token = Config.line_token

    # 上映中電影
    playing_url = "https://movies.yahoo.com.tw/movie_intheaters.html"
    # 要爬取的頁面數量
    playing_page = Config.playing_page

    p_ym = YahooMovie(playing_url, playing_page)

    p_movies = p_ym.run()

    for p_m in p_movies:

        message = f"""
        [現正熱映]
        電影名稱 : {p_m.title_ch}
        上映日期 : {p_m.release_date}
        想看 : {p_m.want_watch}
        評分 : {p_m.rate}
        連結 : {p_m.movie_link}
        """

        send_notify(token, message)

    # 即將上映的電影
    comming_url = "https://movies.yahoo.com.tw/movie_comingsoon.html"
    comming_page = Config.comming_page

    c_ym = YahooMovie(comming_url, comming_page)

    c_movies = c_ym.run()

    for c_m in c_movies:

        message = f"""
        [即將上映]
        電影名稱 : {c_m.title_ch}
        上映日期 : {c_m.release_date}
        想看 : {c_m.want_watch}
        評分 : {c_m.rate}
        連結 : {c_m.movie_link}
        """

        send_notify(token, message)
