import tkinter as tk
from tkinter import ttk, messagebox
import webbrowser
import winreg
import os
import sys
import locale
import ctypes
import platform

# ===== FUNCIONES MULTIARQUITECTURA =====
def get_system_language():
    lang = locale.getdefaultlocale()[0]
    return 'Spanish' if lang and lang.startswith('es') else 'English'

def is_admin():
    try:
        return os.getuid() == 0
    except AttributeError:
        return ctypes.windll.shell32.IsUserAnAdmin()

def detect_real_architecture():
    if platform.machine().endswith('64'):
        return "x64"
    if hasattr(ctypes, 'windll'):
        try:
            class SYSTEM_INFO(ctypes.Structure):
                _fields_ = [("wProcessorArchitecture", ctypes.c_ushort),
                            ("wReserved", ctypes.c_ushort),
                            ("dwPageSize", ctypes.c_uint),
                            ("lpMinimumApplicationAddress", ctypes.c_void_p),
                            ("lpMaximumApplicationAddress", ctypes.c_void_p),
                            ("dwActiveProcessorMask", ctypes.c_void_p),
                            ("dwNumberOfProcessors", ctypes.c_uint),
                            ("dwProcessorType", ctypes.c_uint),
                            ("dwAllocationGranularity", ctypes.c_uint),
                            ("wProcessorLevel", ctypes.c_ushort),
                            ("wProcessorRevision", ctypes.c_ushort)]
            info = SYSTEM_INFO()
            ctypes.windll.kernel32.GetNativeSystemInfo(ctypes.byref(info))
            return "x64" if info.wProcessorArchitecture == 9 else "x86"
        except:
            return "x86"
    return "x86"

def create_registry_entries(lang):
    try:
        # Determinar la ruta correcta del registro según la arquitectura
        if detect_real_architecture() == "x64":
            reg_path = r"SOFTWARE\WOW6432Node\KONAMIPES6\PES6"
            arch_flag = winreg.KEY_WOW64_64KEY
        else:
            reg_path = r"SOFTWARE\KONAMIPES6\PES6"
            arch_flag = winreg.KEY_WOW64_32KEY

        # Crear o abrir la clave con permisos de escritura
        key = winreg.CreateKeyEx(
            winreg.HKEY_LOCAL_MACHINE,
            reg_path,
            0,
            winreg.KEY_SET_VALUE | arch_flag
        )

        values = {
            "installdir": (winreg.REG_SZ, "."),
            "lang_e": (winreg.REG_DWORD, 1 if lang == "English" else 0),
            "lang_s": (winreg.REG_DWORD, 1 if lang == "Spanish" else 0),
            "code": (winreg.REG_SZ, "ESWV4EFNTPK63XVTATEF")
        }

        # Escribir los valores
        for name, (reg_type, value) in values.items():
            winreg.SetValueEx(key, name, 0, reg_type, value)

        winreg.CloseKey(key)
        return True

    except Exception as e:
        error_msg = "Error en registro ({}): {}".format(
            "x64" if detect_real_architecture() == "x64" else "x86",
            str(e)
        )
        print(error_msg)
        with open("registry_error.log", "a") as f:
            f.write(error_msg + "\n")
        return False

# ===== INTERFAZ GRÁFICA COMPLETA =====
class PES6RegistryEditor:
    def __init__(self, root):
        self.root = root
        self.language = get_system_language()
        self.translations = {
            'English': {
                'title': "PES 6 Registry Installer",
                'select_lang': "Select installation language:",
                'buttons': ["English", "Spanish"],
                'detected': "Detected: Windows {0}",
                'admin': ["Administrator required", "Run as Administrator"],
                'success': ["Success", "Registry configured for {0} ({1} system)"],
                'error': "Registry error",
                'credits': "Credits to {0}"
            },
            'Spanish': {
                'title': "Instalador de registro PES 6",
                'select_lang': "Selecciona el idioma de instalación:",
                'buttons': ["Inglés", "Español"],
                'detected': "Detectado: Windows {0}",
                'admin': ["Permisos requeridos", "Ejecutar como Administrador"],
                'success': ["Éxito", "¡Registro configurado para {0} (sistema {1})!"],
                'error': "Error en registro",
                'credits': "Créditos a {0}"
            }
        }
        self.m = self.translations.get(self.language, self.translations['English'])
        self.configure_window()
        self.setup_styles()
        self.create_widgets()
        self.set_icon()

    def set_icon(self):
        """Carga el icono de la aplicación, compatible con Python 3.4"""
        try:
            base_path = sys._MEIPASS
        except AttributeError:
            base_path = os.path.dirname(os.path.abspath(__file__))
        
        icon_path = os.path.normpath(os.path.join(base_path, 'pes6.ico'))
        if os.path.exists(icon_path):
            try:
                self.root.iconbitmap(icon_path)
            except Exception as e:
                with open("error_log.txt", "a") as f:
                    f.write("Error al cargar el icono: {0}\n".format(str(e)))
        else:
            with open("error_log.txt", "a") as f:
                f.write("No se encontró el icono en: {0}\n".format(icon_path))

    def configure_window(self):
        self.root.title(self.m['title'])
        self.root.geometry("380x250")
        self.root.resizable(False, False)
        self.center_window()
        self.root.configure(bg='#f0f0f0')

    def center_window(self):
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        self.root.geometry('+{0}+{1}'.format(x, y))

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('Rounded.TButton',
                      font=('Arial', 10, 'bold'),
                      padding=8,
                      width=12,
                      background='#aaf0ff',
                      relief='solid')
        style.map('Rounded.TButton',
                background=[('active', '#8ae0ff'), ('pressed', '#6ad0ff')])

    def create_widgets(self):
        main_frame = ttk.Frame(self.root, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(main_frame, text=self.m['select_lang'], font=('Arial', 11)).pack(pady=10)

        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(pady=10)

        langs = ['English', 'Spanish']
        for i in range(2):
            btn = ttk.Button(btn_frame, text=self.m['buttons'][i], style='Rounded.TButton',
                            command=lambda l=langs[i]: self.on_install(l))
            btn.pack(side=tk.LEFT, padx=15, ipady=5)

        ttk.Label(main_frame, text=self.m['detected'].format(detect_real_architecture()),
                 font=('Arial', 9)).pack(pady=15)

        credits = tk.Label(self.root, text=self.m['credits'].format("MichaelX17"),
                         fg="blue", cursor="hand2", font=('Arial', 8, 'bold'))
        credits.pack(side=tk.BOTTOM, pady=5)
        credits.bind("<Button-1>", lambda e: webbrowser.open("https://github.com/MichaelX17"))
        credits.bind("<Enter>", lambda e: credits.config(fg="#1a73e8"))
        credits.bind("<Leave>", lambda e: credits.config(fg="blue"))

    def on_install(self, lang):
        if not is_admin():
            messagebox.showwarning(self.m['admin'][0], self.m['admin'][1])
            return

        if create_registry_entries(lang):
            msg = self.m['success'][1].format(lang, detect_real_architecture())
            messagebox.showinfo(self.m['success'][0], msg)
        else:
            messagebox.showerror(self.m['error'], "{0}\n(¿Ejecutado como Admin?)".format(self.m['error']))

if __name__ == "__main__":
    root = tk.Tk()
    app = PES6RegistryEditor(root)
    root.mainloop()