
```markdown
# ⚡ Video Downloader Pro

A modern, fast, and enterprise-grade YouTube video downloader built with Python. It features a sleek dark-mode UI, multithreading, and automatic high-quality video/audio merging using FFmpeg.

## ✨ Features

* 🎨 **Modern UI:** Built with `customtkinter` for a sleek, responsive, and dark-themed experience.
* 🚀 **High Performance:** Uses the powerful `yt-dlp` library for lightning-fast and reliable media extraction.
* 🎬 **Maximum Quality:** Automatically fetches and merges the highest available video and audio qualities (up to 4K) into a single MP4 file.
* 🧵 **Thread-Safe:** Non-blocking user interface with real-time progress bars, download speed, and ETA calculations.
* 📁 **Smart Save:** Prompts the user to select a download destination before initiating the download.
* 📦 **Standalone Ready:** The code is optimized to be compiled into a single portable `.exe` file with FFmpeg bundled inside.

---

## 🛠️ Prerequisites (For running the source code)

If you want to run the Python script directly, you need to install the required libraries and download FFmpeg.

1. **Install Python Packages:**
   ```bash
   pip install customtkinter yt-dlp

```

2. **Download FFmpeg:**
* Download the `ffmpeg-git-essentials.7z` build from [gyan.dev](https://www.gyan.dev/ffmpeg/builds/).
* Extract the archive, navigate to the `bin` folder, and copy `ffmpeg.exe`.
* Paste `ffmpeg.exe` in the same directory as the Python script.


3. **Run the App:**
```bash
python youtube_downloader.py

```



---

## 📦 Building the Portable Executable (.exe)

This project is configured to easily compile into a single `.exe` file that hides the console and bundles `ffmpeg.exe` internally, so the end-user doesn't need to install anything.

1. Install PyInstaller:
```bash
pip install pyinstaller

```


2. Run the build command:
```bash
pyinstaller --noconsole --onefile --add-binary "ffmpeg.exe;." --collect-all customtkinter youtube_downloader.py

```


3. Find your finished app in the `dist` folder!

---

## 🚀 How to Use

1. Open the application.
2. Paste the YouTube Video URL into the input field.
3. Click **Fetch** to retrieve available video qualities.
4. Select your preferred resolution from the dropdown menu.
5. Click **Download Media** and choose where you want to save the file.
6. Wait for the download and merging process to complete. Enjoy! 🎉

---

## ⚠️ Disclaimer

This tool is for educational purposes and personal use only. Please respect YouTube's Terms of Service and the copyright of the content creators. Do not use this tool to distribute copyrighted material.

```

### نصائح سريعة لـ GitHub:
* **لقطة شاشة (Screenshot):** التقط صورة لواجهة برنامجك الجميلة أثناء عملها، وضعها في نفس المجلد، ثم أضفها إلى الـ README (يمكنك إضافتها تحت العنوان مباشرة برفعها على جيت هب وسحبها داخل الملف). هذا سيرفع من احترافية المشروع بنسبة 100%.
* **تجاهل الملفات الثقيلة:** تأكد من عدم رفع ملف `ffmpeg.exe` أو مجلدات `build` و `dist` إلى GitHub (يفضل إضافة ملف `.gitignore` وتخطيها)، وارفع فقط كود البايثون وصورة الواجهة وملف الـ README. البرنامج النهائي (`.exe`) يمكنك رفعه في قسم **Releases** في GitHub لكي يحمله المستخدمون مباشرة.

```
