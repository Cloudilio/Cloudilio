# System packages

*This page is also on the website: [https://cloudilio.com/docs/system-packages](https://cloudilio.com/docs/system-packages)*

## Install programs that pip can't

Some Python libraries need a separate program to work. Examples are ffmpeg for audio and video, Tesseract for reading text in images and Chromium for browser automation. List these programs in a file called `packages.txt`, and Cloudilio installs them every time it builds your app.

## Step 1. Find out which package you need

A missing system package usually shows up as an error in your publish log or your app's logs. Match your error to a row below.

| If you see | You're using | Add these lines |
|---|---|---|
| FileNotFoundError ... 'ffmpeg' | pydub, Whisper, moviepy | `ffmpeg` |
| TesseractNotFoundError | pytesseract | `tesseract-ocr` |
| PDFInfoNotInstalledError | pdf2image | `poppler-utils` |
| cannot find Chrome binary | Selenium | `chromium` `chromium-driver` |
| libGL.so.1: cannot open shared object file | OpenCV | `libgl1` `libglib2.0-0t64` |
| cannot load library 'pango-1.0-0' | WeasyPrint | `libpango-1.0-0` `libpangoft2-1.0-0` `libharfbuzz-subset0` |
| FileNotFoundError ... 'soffice' | LibreOffice conversions | `libreoffice-writer-nogui` |
| ExecutableNotFound ... 'dot' | graphviz, pydot | `graphviz` |
| Can not find valid pkg-config name | mysqlclient | `default-libmysqlclient-dev` `pkg-config` |
| Could not find the GDAL library | GeoDjango | `binutils` `libproj-dev` `gdal-bin` |

For OpenCV, try `opencv-python-headless` in `requirements.txt` first. It needs no system packages. Our post [How to Install System Packages for a Python App](https://cloudilio.com/posts/python-system-packages-packages-txt) explains each package in this table, with code you can test.

**Node.js apps** read `packages.txt` too. They run on Debian 12 (bookworm), the system behind the official Node.js images, so check names on [packages.debian.org/bookworm](https://packages.debian.org/bookworm/). For example, the name there is `libglib2.0-0`, not `libglib2.0-0t64`.

**Apps built from [your own Dockerfile](dockerfile.md)** install what they need in the Dockerfile, so `packages.txt` isn't read. **Static sites** need no system packages.

## Step 2. Find the exact package name

A Python app runs on Debian 13, also called trixie. It is the system behind the official Python images. Package names differ between Linux systems, so a name from an Ubuntu, Alpine or macOS guide may not work.

1. Read the install section of the library's own docs. Copy the names after `apt install` or `apt-get install`.
2. Check each name on [packages.debian.org/trixie](https://packages.debian.org/trixie/).
3. If an error names a missing file, such as `libGL.so.1`, use the "search the contents of packages" form on the same site. It shows which package contains that file.

Names that end in `-dev` are for compiling code. You need them only when pip builds a library from source. A library installed from a ready-made wheel needs only the package without `-dev`.

## Step 3. Create packages.txt

Create a plain text file named `packages.txt` in the same folder as your `requirements.txt`. If your app sits in a subfolder of your project, put the file in that subfolder. Write one package name per line.

**EXAMPLE PACKAGES.TXT**

```
# Convert uploaded audio to MP3, for pydub
ffmpeg
# Read text in scanned receipts, for pytesseract
tesseract-ocr
tesseract-ocr-deu
```

- Lines that start with `#` are comments. Text after a `#` on any line is skipped too.
- Names may contain lowercase letters, numbers, `+`, `-` and `.` only.
- A name listed twice is installed once.
- A file named `apt.txt` works the same way. If you have both files, Cloudilio installs the packages from both.
- Streamlit Community Cloud uses the same `packages.txt` format, so files from there work unchanged.

## Step 4. Try it in a preview, then publish

Publish a new version the way you normally do. To test without touching your live site, start a preview first. A preview builds the app the same way a publish does.

Open the publish log. Near the start of the build, you will see a line that lists your packages.

**PUBLISH LOG**

```
Installing system packages: ffmpeg, tesseract-ocr, tesseract-ocr-deu
```

Cloudilio installs system packages before your Python packages. A library that compiles against a system package while pip installs it, such as `mysqlclient`, finds it ready.

## Step 5. Check that the program works

Add a quick check to your app's startup or a scheduled task you can run with **Run now**. This code prints where each program is installed, or `None` if it is missing.

**CHECK_PACKAGES.PY**

```
import shutil

for program in ["ffmpeg", "tesseract"]:
    print(program, shutil.which(program))
```

## Already installed in every app

You don't need to list these. Every app has them already.

- `build-essential` gives pip a C compiler for packages without a ready-made wheel.
- `libpq-dev` lets `psycopg2` connect to PostgreSQL.
- `curl` downloads files from the command line.
- Python, pip and SQLite.

## Limits

| Limit | Value |
|---|---|
| Packages per app | 50 |
| Time for one build | 15 minutes |
| Size of the built app | 5 GB |
| Package versions | The version in Debian's current release |

Large packages make each build slower. LibreOffice and the `fonts-noto-cjk` fonts are the largest common ones. Chromium and LibreOffice also need more memory than the 256 MB in the Starter plan. Plan for at least 1 GB.

## Fix common problems

"packages.txt, line 3: '...' isn't a valid package name"

That line has a character a Debian package name can't contain, such as a capital letter, a space inside a name, a semicolon or a version number like `ffmpeg=7.1`. Fix the line and publish again. Cloudilio checks every name before the build starts, so nothing else runs.

"E: Unable to locate package ..."

Debian has no package with that name. Check the spelling on [packages.debian.org/trixie](https://packages.debian.org/trixie/). Some older names changed in Debian 13. For example, `libglib2.0-0` is now `libglib2.0-0t64`.

"Your project lists 51 system packages. The most allowed is 50."

Remove packages your code doesn't use. If you copied a long list from another guide, start with the packages from Step 1 and add more only when an error asks for them.

The build stops after 15 minutes

Large packages and large Python libraries together can take too long. Remove packages you don't need, or replace a heavy library with a lighter one. `opencv-python-headless` and `PyMySQL` need no system packages at all.

My app can't run apt-get

That's expected. Your app runs as a normal user without administrator rights, which keeps it safer. Install everything at build time with `packages.txt`.

Everything installed, but the program still isn't found

Check that `packages.txt` sits next to the `requirements.txt` Cloudilio uses, and that the publish log shows the "Installing system packages" line. Some libraries also need the program's path. Selenium, for example, needs `/usr/bin/chromium` and `/usr/bin/chromedriver`.
