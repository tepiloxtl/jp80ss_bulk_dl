# jp80ss_bulk_dl
Bulk resolve and download ouo.io links from jpop80ss blog

Requires requests, patoolib, mediafire_bulk_downloader (from https://github.com/NicKoehler/mediafire_bulk_downloader), ouo_bypass (from https://github.com/tepiloxtl/ouo-bypass)

Clone/download repository, install dependencies using `pip install -r requirements.txt` and create directories `out` and `tmp`

Add link.json file with this format:

    {"artist1": ["link1", "link2"],
     "artist2": ["link3", "link4"]}

The script should automatically resolve links, download files and unpack to directories based on json file
