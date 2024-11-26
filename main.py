## AO3 Bookmark Downloader
import you
import AO3

# Utils
def seriesid_from_url(url):
    # A rewrite of AO3.utils.workid_from_url but for series
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
def start_session():
    global session
    session = AO3.Session(you.username, you.password)
    print(AO3.User(you.username))
    print(f"Bookmarks: {session.bookmarks}")
    # session.refresh_auth_token()

    # Confirming
    correct = input("Is this infromation correct? (yes/no): ")
    if (correct.lower() == "yes"):
        downloading(choose_file_type(), load_bookmarks())
    else:
        print("Double check that you entered the correct username and password.")

def choose_file_type():
    while True:
        type = input("What file type would you like?\nAZW3 [0]\nEPUD [1]\nHTML [2]\nMOBI [3]\nPDF [4]\nEnter a number: ")
        match int(type):
            case 0:
                file_type = "AZW3"
                break
            case 1:
                file_type = "EPUD"
                break
            case 2:
                file_type = "HTML"
                break
            case 3:
                file_type = "MOBI"
                break
            case 4:
                file_type = "PDF"
                break
            case _:
                print("Incorrect input.\n")

    return file_type

def load_bookmarks():
    user = AO3.User(you.username)
    user.set_session(session)

    # Parsing bookmark pages
    print("\nLoading bookmarks...")
    works = []
    series = []

    for page in range(1, you.pages+1):
        session.refresh_auth_token()
        html = user.request(f"https://archiveofourown.org/users/{you.username}/bookmarks?page={page}")
        list = html.find("ol", {"class": "bookmark index group"})

        for li in list.find_all("li", {"role": "article"}):
            if li.h4 is not None:
                # Distinguish between single works and series
                for a in li.h4.find_all("a"):
                    if a.attrs["href"].startswith("/works"):
                        works.append(AO3.common.get_work_from_banner(li))
                        # print(AO3.common.get_work_from_banner(li))

                    elif a.attrs["href"].startswith("/series"):
                        seriesid = seriesid_from_url(a['href'])
                        series.append(AO3.Series(seriesid))
                        # print(AO3.Series(seriesid))

    return {"works": works, "series": series}

    # print(page.text)

def downloading(file_type, ids):
    print(f"\nWorks: {len(ids["works"])}")
    print(f"Series: {len(ids["series"])}")
    print("File Type: " + file_type + "\n")

    # Works
    print("Downloading works...")


    # Series
    print("Downloading series...")

## Starting Script ##
start_session()
