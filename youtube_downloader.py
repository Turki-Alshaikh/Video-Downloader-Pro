import customtkinter as ctk
import yt_dlp
import threading
import sys
import os
from tkinter import filedialog # مكتبة اختيار مسار الحفظ

# -----------------------------------------------------------
# دالة صارمة لتحديد مسار FFmpeg الدقيق بجوار ملف البايثون
# -----------------------------------------------------------
def get_ffmpeg_path():
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
    else:
        # هذه الطريقة تجبر البرنامج على النظر في المجلد الذي يحتوي على هذا السكريبت تحديداً
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, "ffmpeg.exe")

# -----------------------------------------------------------
# إعدادات مظهر الواجهة الرسومية
# -----------------------------------------------------------
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class ProYouTubeDownloader(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("⚡ Video Downloader Pro")
        self.geometry("650x580")
        self.resizable(False, False)
        self.configure(fg_color="#181818")

        # 1. قسم العنوان
        self.header_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.header_frame.pack(fill="x", pady=(30, 20))
        
        self.title_label = ctk.CTkLabel(self.header_frame, text=" Downloader", font=("Segoe UI", 32, "bold"), text_color="#FFFFFF")
        self.title_label.pack()
        
        self.subtitle = ctk.CTkLabel(self.header_frame, text="Enterprise-Grade Media Extraction Tool", font=("Segoe UI", 14), text_color="#A0A0A0")
        self.subtitle.pack()

        # 2. قسم إدخال الرابط
        self.input_frame = ctk.CTkFrame(self, fg_color="#242424", corner_radius=15)
        self.input_frame.pack(fill="x", padx=40, pady=10)

        self.url_entry = ctk.CTkEntry(self.input_frame, placeholder_text="🔗 Paste YouTube Video URL here...", 
                                      height=50, font=("Segoe UI", 14), border_width=0, fg_color="#2b2b2b")
        self.url_entry.pack(side="left", fill="x", expand=True, padx=(10, 10), pady=10)

        self.fetch_btn = ctk.CTkButton(self.input_frame, text="🔍 Fetch", command=self.fetch_formats, 
                                       width=110, height=50, font=("Segoe UI", 15, "bold"), corner_radius=10)
        self.fetch_btn.pack(side="right", padx=(0, 10), pady=10)

        # 3. قسم خيارات الجودة
        self.format_var = ctk.StringVar(value="⚙️ Awaiting video URL...")
        self.format_menu = ctk.CTkOptionMenu(self, variable=self.format_var, values=["..."], 
                                             height=45, font=("Segoe UI", 14), corner_radius=10, 
                                             fg_color="#2b2b2b", button_color="#3a3a3a", button_hover_color="#4a4a4a")
        self.format_menu.pack(fill="x", padx=40, pady=15)

        # 4. قسم شريط التقدم
        self.progress_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.progress_frame.pack(fill="x", padx=40, pady=5)
        
        self.progress_bar = ctk.CTkProgressBar(self.progress_frame, height=12, corner_radius=6, progress_color="#00A8E8")
        self.progress_bar.set(0)
        
        self.stats_label = ctk.CTkLabel(self.progress_frame, text="🚀 Speed: -- | ⏱️ ETA: -- | 📊 0%", font=("Consolas", 13), text_color="#A0A0A0")

        # 5. زر التحميل الرئيسي
        self.download_btn = ctk.CTkButton(self, text="⬇️ Download Media", command=self.start_download, state="disabled", 
                                          height=55, fg_color="#00C853", hover_color="#00E676", text_color="#000000",
                                          font=("Segoe UI", 16, "bold"), corner_radius=12)
        self.download_btn.pack(fill="x", padx=40, pady=(20, 10))

        # 6. شريط الحالة السفلي
        self.status_label = ctk.CTkLabel(self, text="System Ready.", font=("Segoe UI", 13), text_color="#757575")
        self.status_label.pack(pady=10)

        self.formats_dict = {}

    def fetch_formats(self):
        url = self.url_entry.get().strip()
        if not url:
            self._update_ui_state("❌ Please enter a valid URL!", "#FF5252", fetch_state="normal", dl_state="disabled")
            return
            
        self._update_ui_state("⏳ Connecting to servers and fetching data...", "#FFD600", fetch_state="disabled", dl_state="disabled", btn_text="⏳...")
        
        self.progress_bar.pack_forget()
        self.stats_label.pack_forget()
        
        threading.Thread(target=self._get_formats_thread, args=(url,), daemon=True).start()

    def _get_formats_thread(self, url):
        ydl_opts = {'quiet': True, 'nocheckcertificate': True}
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                formats = info.get('formats', [])
                
                self.formats_dict.clear()
                options = []
                
                audio_formats = [f for f in formats if f.get('vcodec') == 'none' and f.get('acodec') != 'none']
                best_audio_size = 0
                if audio_formats:
                    best_audio = audio_formats[-1]
                    best_audio_size = best_audio.get('filesize') or best_audio.get('filesize_approx', 0)

                for f in formats:
                    if f.get('vcodec') != 'none':
                        res = f.get('resolution', 'Unknown')
                        if res == 'Unknown' or 'audio' in res.lower(): continue
                            
                        ext = f.get('ext', 'mp4')
                        format_id = f.get('format_id')
                        has_audio = f.get('acodec') != 'none'
                        v_size = f.get('filesize') or f.get('filesize_approx', 0)
                        
                        if not has_audio:
                            total_size = v_size + best_audio_size
                            dl_format = f"{format_id}+bestaudio/best"
                        else:
                            total_size = v_size
                            dl_format = format_id
                            
                        if total_size > 0:
                            size_mb = total_size / (1024 * 1024)
                            size_str = f"{size_mb:.2f} MB"
                        else:
                            size_str = "Unknown Size"
                            
                        label = f"🎬 {res} | 🗂️ {ext} | 💾 {size_str}"
                        
                        if label not in options:
                            options.append(label)
                            self.formats_dict[label] = dl_format

                if not options:
                    self.after(0, lambda: self._update_ui_state("❌ No valid formats found.", "#FF5252", fetch_state="normal"))
                    return

                options.reverse() 
                self.after(0, self._on_fetch_success, options)
                
        except Exception as e:
            self.after(0, lambda: self._update_ui_state("❌ Network Error! Please check the URL.", "#FF5252", fetch_state="normal"))

    def _on_fetch_success(self, options):
        self.format_menu.configure(values=options)
        self.format_var.set(options[0])
        self._update_ui_state("✅ Video data loaded successfully!", "#00E676", fetch_state="normal", dl_state="normal")

    def _update_ui_state(self, msg, color, fetch_state="disabled", dl_state="disabled", btn_text="🔍 Fetch"):
        self.status_label.configure(text=msg, text_color=color)
        self.fetch_btn.configure(state=fetch_state, text=btn_text)
        self.download_btn.configure(state=dl_state)

    def progress_hook(self, d):
        if d['status'] == 'downloading':
            try:
                percent_str = d.get('_percent_str', '0.0%').replace('\x1b[0;94m', '').replace('\x1b[0m', '').strip()
                speed_str = d.get('_speed_str', '--').strip()
                eta_str = d.get('_eta_str', '--').strip()
                
                percent_float = float(percent_str.replace('%', '')) / 100
                self.after(0, self._update_progress, percent_float, speed_str, eta_str, percent_str)
            except:
                pass
        elif d['status'] == 'finished':
            self.after(0, lambda: self.status_label.configure(text="⚙️ Processing & Merging via FFmpeg... Please wait.", text_color="#00A8E8"))

    def _update_progress(self, percent_float, speed_str, eta_str, percent_str):
        self.progress_bar.set(percent_float)
        self.stats_label.configure(text=f"🚀 Speed: {speed_str} | ⏱️ ETA: {eta_str} | 📊 {percent_str}")

    def start_download(self):
        url = self.url_entry.get().strip()
        selected_format = self.format_var.get()
        format_id = self.formats_dict.get(selected_format)
        
        # --- التعديل هنا: فتح نافذة لاختيار مسار الحفظ ---
        save_directory = filedialog.askdirectory(title="📁 Select Save Folder (اختر مجلد الحفظ)")
        
        # إذا ألغى المستخدم النافذة بدون اختيار مسار، نتوقف
        if not save_directory:
            self._update_ui_state("❌ Download cancelled.", "#A0A0A0", fetch_state="normal", dl_state="normal")
            return
        
        self._update_ui_state(f"📥 Downloading to: {save_directory}", "#00A8E8")
        self.url_entry.configure(state="disabled")
        self.format_menu.configure(state="disabled")
        self.download_btn.configure(state="disabled")
        
        self.progress_bar.pack(fill="x", pady=(0, 8))
        self.progress_bar.set(0)
        self.stats_label.pack()
        
        # إرسال مسار الحفظ المحدد إلى ثريد التحميل
        threading.Thread(target=self._download_thread, args=(url, format_id, save_directory), daemon=True).start()

    def _download_thread(self, url, format_id, save_directory):
        # توجيه الملف للمسار الذي اختاره المستخدم
        output_template = os.path.join(save_directory, '%(title)s.%(ext)s')
        
        ydl_opts = {
            'format': format_id,
            'outtmpl': output_template,
            'merge_output_format': 'mp4',
            'ffmpeg_location': get_ffmpeg_path(),
            'progress_hooks': [self.progress_hook],
            'quiet': True,
            'noprogress': True
        }
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            self.after(0, self._on_download_complete, "✅ Complete! File saved in selected folder.", "#00E676")
        except Exception as e:
            self.after(0, self._on_download_complete, "❌ Download Failed! Check network or FFmpeg.", "#FF5252")

    def _on_download_complete(self, msg, color):
        self.status_label.configure(text=msg, text_color=color)
        self.fetch_btn.configure(state="normal")
        self.download_btn.configure(state="normal")
        self.url_entry.configure(state="normal")
        self.format_menu.configure(state="normal")
        
        if "Failed" not in msg:
            self.stats_label.configure(text="Done! 🎉 File is ready.")
            self.progress_bar.set(1)

if __name__ == "__main__":
    app = ProYouTubeDownloader()
    app.mainloop()