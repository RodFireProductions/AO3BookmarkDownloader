## Utils ##
import AO3
import os
import string
import time
import database as DB

rate_limit = {
    "short": 5,
    "medium": 20,
    "long": 30
}

colors = {
    "error": "#800001",
    "status": "#00007F"
}

state = {
    "paused": False
}

def delay_call(length):
    delay = 60 / rate_limit[length]
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

# A workaround for AO3.User's cached_property _bookmarks_pages,
# because the pagination ordered list no longer uses "title".
def bookmarks_pages(session, username):
    session.refresh_auth_token()
    html = session.request(f"https://archiveofourown.org/users/{username}/bookmarks")
    pages = html.find("ol", {"class": "pagination"})
    if pages is None:
        return 1
    n = 1
    for li in pages.findAll("li"):
        text = li.getText()
        if text.isdigit():
            n = int(text)
    return n

# AO3.session is not throwing AO3.utils.LoginError properly,
# so this is my workaround
def checkAuthentication(session, settings):
    # session.refresh_auth_token()
    html = session.request(f"https://archiveofourown.org/users/{settings['username']}")
    logged_in = html.find("body", {"class": "logged-in"})
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
    load_bookmarks(app, settings, session)
    # downloading(choose_file_type(), load_bookmarks())
    return True

#
def rateLimited(app, exception):
    if exception == AO3.utils.HTTPError:
        app.updateStatus("Rate-limited :(\nTry again later.", colors["error"])
        return True
    else:
        # TODO: make error log?
        return False

#
def addToQueue(app, id, work, title, series=False):
    print(f"{work}, {series}, {title}")
    app.addToFicList(id, f"{id} | {title}")

#
def load_bookmarks(app, settings, session):
    app.updateStatus("Fetching bookmarks...\nThis may take awhile...", colors["status"])
    user = AO3.User(settings["username"])
    user.set_session(session)
    user.reload()

    try:
        for page in range(1, bookmarks_pages(session, settings['username'])+1):
            delay_call("short")
            session.refresh_auth_token()
            html = session.request(f"https://archiveofourown.org/users/{settings['username']}/bookmarks?page={page}")
            list = html.find("ol", {"class": "bookmark index group"})

            for li in list.find_all("li", {"role": "article"}):
                if li.h4 is not None:
                    for a in li.h4.find_all("a"):
                        # Distinguish between single works and series
                        if a.attrs["href"].startswith("/works"):
                            workid = AO3.utils.workid_from_url(a['href'])
                            new_w = AO3.Work(workid, session=session)
                            #works.append(AO3.common.get_work_from_banner(li))
                            addToQueue(app, workid, new_w, new_w.title)

                        elif a.attrs["href"].startswith("/series"):
                            seriesid = seriesid_from_url(a['href'])
                            new_s = AO3.Series(seriesid, session=session)
                            new_s.reload()
                            #series.append({"title": new_s.name, "works": new_s.work_list})
                            addToQueue(app, seriesid, new_s, new_s.name, series=True)

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
