## Utils ##
import AO3
import os
import string
import time
import database as DB

rate_limit = 20

colors = {
    "error": "#800001",
    "status": "#00007F"
}

state = {
    "paused": False
}

def delay_call():
    delay = 60 / rate_limit
    time.sleep(delay)

# A copy of AO3.utils.workid_from_url but for series
def seriesid_from_url(url):
    split_url = url.split("/")
    try:
        index = split_url.index("series")
    except ValueError:
        return
    if len(split_url) >= index+1:
        seriesid = split_url[index+1].split("?")[0]
        if seriesid.isdigit():
            return int(seriesid)
    return

# AO3.session is not throwing AO3.utils.LoginError properly,
# so this is my workaround
def checkAuthentication(session, settings):
    # session.refresh_auth_token()
    html = session.request(f"https://archiveofourown.org/users/{settings['username']}")
    logged_in = html.find("body", {"class": "logged-in"})
    logged_out = html.find("body", {"class": "logged-out"})
    if logged_in == None:
        raise AO3.utils.LoginError("Invalid username or password")
#
def startSession(app, options):
    settings = options[0]
    try:
        session = AO3.Session(settings["username"], settings["password"])
        checkAuthentication(session, settings)
    except Exception as e:
        if not rateLimited(app, e):
            app.updateStatus("Authtentication error.\nCheck that your username and password are correct.", colors["error"])
            print(e)
        return False
    app.updateStatus("Authenticated successfully!", colors["status"])
    #load_bookmarks(app, settings, session)
    # downloading(choose_file_type(), load_bookmarks())
    return True

#
def rateLimited(app, exception):
    # We are being rate-limited. Try again in a while or reduce the number of requests
    #if "rate-limited" in exception:
    if exception == AO3.utils.HTTPError:
        app.updateStatus("Rate-limited :(\nTry again later.", colors["error"])
        print("AAAA RATE LIMIT")
        return True
    else:
        # TODO: make error log?
        return False

#
def addToQueue(app, work, series=False, series_title=""):
    print(f"{work}, {series}, {series_title}")

#
def load_bookmarks(app, settings, session):
    user = AO3.User(settings["username"])
    user.set_session(session)
    user.reload()

    app.updateStatus("Fetching bookmarks...\nThis may take awhile...", colors["status"])

    try:
        for page in range(1, user._bookmarks_pages+1):
            session.refresh_auth_token()
            html = session.request(f"https://archiveofourown.org/users/{settings['username']}/bookmarks?page={page}")
            list = html.find("ol", {"class": "bookmark index group"})

            for li in list.find_all("li", {"role": "article"}):
                if li.h4 is not None:
                    for a in li.h4.find_all("a"):
                        # Distinguish between single works and series
                        if a.attrs["href"].startswith("/works"):
                            #works.append(AO3.common.get_work_from_banner(li))
                            addToQueue(app, AO3.common.get_work_from_banner(li))

                        elif a.attrs["href"].startswith("/series"):
                            seriesid = seriesid_from_url(a['href'])
                            new_s = AO3.Series(seriesid)
                            new_s.set_session(session)
                            new_s.reload()
                            #series.append({"title": new_s.name, "works": new_s.work_list})
                            addToQueue(app, new_s.work_list, series=True, series_title=new_s.name)

        return True
    except Exception as e:
        if not rateLimited(app, e):
            app.updateStatus("Something went wrong.", colors["error"])
            print(e)
        return False

#
def download(work, type, series=None):
    work.set_session(session)
    work.reload()
    #
    if series is not None:
        file_path = "downloads/" + series.translate(str.maketrans('', '', string.punctuation))
    else:
        file_path = "downloads"

    os.makedirs(file_path, exist_ok = True)
    work.download_to_file(f"{file_path}/{work.title.translate(str.maketrans('', '', string.punctuation))}.{type.lower()}", filetype=type)

#
def downloading(file_type, ids):
    print(f"\nWorks: {len(ids["works"])}")
    print(f"Series: {len(ids["series"])}")
    print("File Type: " + file_type + "\n")

    # Works
    print("Downloading works...")
    for work in ids["works"]:
        delay_call()
        download(work, file_type)

    # Series
    print("Downloading series...")
    for series in ids["series"]:
        for work in series["works"]:
            delay_call()
            download(work, file_type, series=series["title"])
