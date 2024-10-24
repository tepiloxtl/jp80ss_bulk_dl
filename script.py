import re, requests, json, time, patoolib, os, shutil, mediafire
from pathlib import Path
from ouo_bypass import ouo_bypass

with open('link.json', 'r', encoding="utf-8") as file:
    data = json.load(file)

print(data)
for artist in data:
    os.mkdir(os.path.join("out", artist))
    lena = len(data[artist])
    for c, link in enumerate(data[artist], start=1):
        print("\033[93mDoing " + str(c) + " of " + str(lena) + "\033[0m")
        mfilename = None
        try:
            shutil.rmtree("tmp/dl")  # Remove the directory and its contents
        except:
            pass
        current_link = link
        while True:
            print(current_link)
            if "google.com/url" in current_link:
                current_link = re.findall("(?<=url=)https:\/\/[a-zA-Z0-9.-]+(?:\/[^\s]*)?", current_link)[0]
            elif "bit.ly" in current_link:
                current_link = requests.get(current_link, allow_redirects=True).url
            elif "ouo.io" in current_link or "ouo.press" in current_link:
                try:
                    current_link = ouo_bypass(current_link)["bypassed_link"]
                except:
                    print("Retrying bypass")
                    time.sleep(10)
            elif "mediafire.com" in current_link:
                try:
                    mfilename = mediafire.get_file(re.findall("(?<=/file/)[a-zA-Z0-9]+(?=/)", current_link)[0], "tmp/")
                except:
                    print("Could not download, file missing: " + str(link))
                    break
                print("DONE: " + mfilename)
                break
            else:
                print("Unsupported link, baka!")
                break
        
        if mfilename == None:
            print("Could not download file, skipping")
            with open("errored/download.txt", 'a') as log:
                log.write(str(artist) + ": " + str(link) + "\n")
            continue
        #shutil.copyfile(mfilename, os.path.normpath("test/" + pathlib.Path(mfilename).name))
        patoolib.extract_archive(mfilename, outdir="tmp/dl/", password="jp80ss")

        dirlisting = list(Path("tmp/dl").iterdir())
        print(dirlisting)
        if len(dirlisting) == 1 and dirlisting[0].is_dir():
            dirlisting2 = list(Path(dirlisting[0]).iterdir())
            if len(dirlisting2) == 1 and dirlisting2[0].is_file() and dirlisting2[0].suffix.lower() == ".rar":
                patoolib.extract_archive(dirlisting2[0], outdir="tmp/dl/", password="jp80ss")
                #os.remove(dirlisting2[0])
                shutil.rmtree(dirlisting[0])
                dirlisting3 = list(Path("tmp/dl").iterdir())
                if len(dirlisting3) == 1 and dirlisting3[0].is_dir():
                    os.rename(dirlisting3[0], os.path.join("out", artist, dirlisting3[0].name))
                    os.remove(mfilename)
                else:
                    print("Unrecognized file structure, moved away 3")
                    os.rename(mfilename, os.path.join("errored", Path(mfilename).name))
            else:
                if any(file.suffix in [".mp3", ".flac"] for file in dirlisting2 if file.is_file()):
                    os.rename(dirlisting[0], os.path.join(artist, dirlisting[0].name))
                else:
                    print("Unrecognized file structure, moved away 2")
                    os.rename(mfilename, os.path.join("errored", Path(mfilename).name))
        else:
            print("Unrecognized file structure, moved away 1")
            os.rename(mfilename, os.path.join("errored", Path(mfilename).name))