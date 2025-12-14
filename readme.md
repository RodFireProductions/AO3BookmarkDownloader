# AO3 Bookmark Downloader (Outdated)

A script for bulk downloading all of your bookmarks on AO3.

If you're like me and have hundreds of bookmarks, the idea of downloading each
individually is probably daunting.

## How To Use
Prerequisites: Python (Made using 3.12 / Errored in 3.10)

1. Install.
    - Install dependencies: `pip install ao3_api`
    - Clone or download this repo.
2. Configure your install in `you.py`.
    - You'll need to add your username and password to get authentication to
    download restricted works and your private bookmarks.
3. Run `main.py`.
    - Confirm that the information listed is correct.
    - Type in the integer associated with the file type you want.
4. Wait.
    - By default, it only downloads a maximum of 20 fics per minute to avoid
    getting rate limited.
    - It will take quite a few minutes. Go read a fic while you wait or something.

## Issues
- [Downloading stopped](#it-stopped-downloading)
- [Got rate limited](#im-being-rate-limited)
- [Unlisted issue](#other-issues)

### It stopped downloading!
In the case that the script just stops downloading and is frozen, do the following:

1. Stopped the program. If it can't be stopped via keyboard shortcut, just close
the terminal.
2. Edit `main.py`:
    - Search the file for this comment: `# Paste here`
    - If the downloading stopped while individual works were being downloaded:
        - Copy and paste the following underneath:
        ```python
        for i in range(number):
            del ids["works"][0]
        ```
        - Replace `number` with the number of fics that ended up getting
        downloaded. This will remove them from the download queue.
    - If the downloading stopped while series were being downloaded:
        - Copy and paste the following underneath:
        ```python
        for i in range(number):
            del ids["series"][0]
        ```
        - Replace `number` with the number of series that ended up getting
        **FULLY** downloaded. This will remove them from the download queue.
        - Remove the folders and files of the series that were only **partially**
        downloaded.
3. Rerun `main.py`.

### I'm being rate limited!
If the script errored stating that you got rate limited, do one of the following:
1. Wait a little bit before following the [downloading stopped](#it-stopped-downloading)
instructions.

OR

2. Open `main.py`. Find the following line, replace `20` with a smaller number,
and then follow the [downloading stopped](#it-stopped-downloading)
instructions:
    ```python
    rate_limit = 20
    ```

### Other issues
If you're having anything unlisted errors or problems, create an
[issue](https://github.com/RodFireProductions/AO3BookmarkDownloader/issues).
Make sure to include the error message you received.
