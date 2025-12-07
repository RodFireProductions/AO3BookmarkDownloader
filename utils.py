## Utils ##
import AO3
import os
import string
import time

rate_limit = 20

## Utils
def delay_call():
    delay = 60 / 20
    time.sleep(delay)

#
def seriesid_from_url(url):
    # A copy of AO3.utils.workid_from_url but for series
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

## Main Functions
def start_session(username, password):
    global session
    session = AO3.Session(username, password)
    print(AO3.User(username))
    print(f"Bookmarks: {session.bookmarks}")
    # session.refresh_auth_token()

    # Confirming
    correct = input("Is this infromation correct? (yes/no): ")
    if (correct.lower() == "yes"):
        downloading(choose_file_type(), load_bookmarks())
    else:
        print("Double check that you entered the correct username and password.")
        
#
def load_bookmarks():
    user = AO3.User(you.username)
    user.set_session(session)
    user.reload()

    # Parsing bookmark pages
    print("\nLoading bookmarks...")
    works = []
    series = []

    for page in range(1, user._bookmarks_pages+1):
        session.refresh_auth_token()
        html = session.request(f"https://archiveofourown.org/users/{you.username}/bookmarks?page={page}")
        list = html.find("ol", {"class": "bookmark index group"})

        for li in list.find_all("li", {"role": "article"}):
            if li.h4 is not None:
                for a in li.h4.find_all("a"):
                    # Distinguish between single works and series
                    if a.attrs["href"].startswith("/works"):
                        works.append(AO3.common.get_work_from_banner(li))

                    elif a.attrs["href"].startswith("/series"):
                        seriesid = seriesid_from_url(a['href'])
                        new_s = AO3.Series(seriesid)
                        new_s.set_session(session)
                        new_s.reload()
                        series.append({"title": new_s.name, "works": new_s.work_list})

    return {"works": works, "series": series}

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

    # Paste here

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

## Starting Script ##
start_session()
