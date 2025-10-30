from gui.uis.windows.main_window.functions_main_window import *
import sys
import os
import locale

# IMPORT QT CORE
# ///////////////////////////////////////////////////////////////
from qt_core import *

# IMPORT SETTINGS
# ///////////////////////////////////////////////////////////////
from gui.core.json_settings import Settings

# IMPORT PY ONE DARK WINDOWS
# ///////////////////////////////////////////////////////////////
# MAIN WINDOW
from gui.uis.windows.main_window import *

# IMPORT PY ONE DARK WIDGETS
# ///////////////////////////////////////////////////////////////
from gui.widgets import *
import pandas as pd
from gui.uis.pages.ui_splash_screen import Ui_SplashScreen 
from gui.widgets import PyCircularProgress
# ADJUST QT FONT DPI FOR HIGHT SCALE AN 4K MONITOR
# ///////////////////////////////////////////////////////////////
os.environ["QT_FONT_DPI"] = "96"
# IF IS 4K MONITOR ENABLE 'os.environ["QT_SCALE_FACTOR"] = "2"'

# MAIN WINDOW
# ///////////////////////////////////////////////////////////////
counter = 0
locale.setlocale(locale.LC_ALL, 'Indonesian_indonesia.1252')  # untuk Windows


style_dark = """
            QPushButton {
                background-color: #282A36; /* Warna putih */
                color: white; /* Warna teks hitam */
                border-radius: 10px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #e5a561; /* Warna lebih gelap saat hover */
            }
            QPushButton:pressed {
                background-color: #b2804b; /* Warna lebih gelap saat diklik */
            }
        """
        
style_light = """
            QPushButton {
                background-color: #FFB86C; /* Warna putih */
                color: black; /* Warna teks hitam */
                border-radius: 10px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #e5a561; /* Warna lebih gelap saat hover */
            }
            QPushButton:pressed {
                background-color: #b2804b; /* Warna lebih gelap saat diklik */
            }
        """


class SplashScreen(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = Ui_SplashScreen()
        self.ui.setupUi(self)

        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.progress = PyCircularProgress()
        self.progress_width = 275
        self.progress_height = 275
        self.progress.value = 40
        self.progress.setFixedSize(self.progress_width, self.progress_height)
        self.progress.move(13,13)
        self.progress.font_size = 35
        self.progress.add_shadow(True)
        self.progress.bg_color = QColor(68,71,90,140)
        self.progress.set_progress_gradient([
            (0.0, "#FFB86C"),  # Orange
            (1.0, "#F1FA8C")   # White
        ])
        self.progress.setParent(self.ui.centralwidget)
        self.progress.show()

        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(15)
        self.shadow.setXOffset(0)
        self.shadow.setYOffset(0)
        self.shadow.setColor(QColor(0,0,0,80))
        self.setGraphicsEffect(self.shadow)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(25)
        self.show()

    def update(self):
        global counter
        self.progress.set_value(counter)
        
        if counter>=100:
            self.timer.stop()
            self.main = MainWindow()
            self.main.show()
            self.close()
        else:
            counter += 1

class MainWindow(QMainWindow):
    flag = False
    flag2 = False
    path_temp = ''
    mode = None
    def __init__(self):
        super().__init__()

        # SETUP MAIN WINDOw
        # Load widgets from "gui\uis\main_window\ui_main.py"
        # ///////////////////////////////////////////////////////////////
        self.ui = UI_MainWindow()
        self.ui.setup_ui(self)

        # LOAD SETTINGS
        # ///////////////////////////////////////////////////////////////
        settings = Settings()
        self.settings = settings.items
        self.ui.load_pages.btn_eksternal.setStyleSheet(style_dark)
        self.ui.load_pages.btn_internal.setStyleSheet(style_dark)
        self.ui.load_pages.btn_kembali1.setStyleSheet(style_dark)
        self.ui.load_pages.btn_kembali2.setStyleSheet(style_dark)
        self.ui.load_pages.btn_kembali3.setStyleSheet(style_dark)
        self.apply_dark_input(self.ui.load_pages.input_label)
        self.apply_dark_input(self.ui.load_pages.label_cari_2)

        # SETUP MAIN WINDOW
        # ///////////////////////////////////////////////////////////////
        self.hide_grips = True # Show/Hide resize grips
        SetupMainWindow.setup_gui(self)

        # SHOW MAIN WINDOW
        # ///////////////////////////////////////////////////////////////

        
        # Tampilkan page_menu di awal
        MainFunctions.set_page(self, self.ui.load_pages.page_menu)
        self.ui.left_menu.hide()
        self.ui.load_pages.btn_internal.clicked.connect(self.handle_internal_mode)
        self.ui.load_pages.btn_eksternal.clicked.connect(self.handle_eksternal_mode)
        self.ui.load_pages.btn_kembali1.clicked.connect(self.kembali)
        self.ui.load_pages.btn_kembali2.clicked.connect(self.kembali)
        self.ui.load_pages.btn_kembali3.clicked.connect(self.kembali)

        # Nonaktifkan panel kiri
        self.ui.left_menu.setDisabled(True)
        self.show()

    def apply_dark_input(self, widget):
        widget.setStyleSheet("""
            background-color: #2B2E3B;
            color: #f8f8f2;
            border: 1px solid #44475a;
            border-radius: 5px;
            padding: 6px;
        """)


    def apply_dark_theme_to_table(self, table_view):
        table_view.setStyleSheet("""
            QTableView {
                background-color: #282a36;
                color: #f8f8f2;
                gridline-color: #44475a;
                selection-background-color: #44475a;
                selection-color: #ff79c6;
                border: none;
            }

            QHeaderView::section {
                background-color: #2B2E3B;
                color: #f8f8f2;
                font-weight: bold;
                padding: 6px;
                border: 1px solid #44475a;
            }

            QTableCornerButton::section {
                background-color: #2B2E3B;
                border: 1px solid #44475a;
            }

            QScrollBar:vertical {
                background: #2B2E3B;
                width: 14px;
                margin: 15px 0 15px 0;
                border: none;
            }

            QScrollBar::handle:vertical {
                background: #6272a4;
                min-height: 20px;
                border-radius: 7px;
            }

            QScrollBar::add-line:vertical,
            QScrollBar::sub-line:vertical {
                background: none;
                height: 15px;
            }

            QScrollBar::add-page:vertical,
            QScrollBar::sub-page:vertical {
                background: none;
            }

            QScrollBar:horizontal {
                background: #2B2E3B;
                height: 14px;
                margin: 0 15px 0 15px;
                border: none;
            }

            QScrollBar::handle:horizontal {
                background: #6272a4;
                min-width: 20px;
                border-radius: 7px;
            }

            QScrollBar::add-line:horizontal,
            QScrollBar::sub-line:horizontal {
                background: none;
                width: 15px;
            }

            QScrollBar::add-page:horizontal,
            QScrollBar::sub-page:horizontal {
                background: none;
            }
        """)
        table_view.viewport().setAutoFillBackground(False)

        
    def reset_ui_state(self):
        # Kosongkan semua table view
        self.ui.load_pages.table_view_data.setModel(None)
        self.ui.load_pages.table_view_data_2.setModel(None)
        self.ui.load_pages.table_view_page_3_1.setModel(None)
        self.ui.load_pages.table_view_page_3_2.setModel(None)

        # Bersihkan input path
        self.ui.load_pages.input_label.setText("")
        self.ui.load_pages.label_cari_2.setText("")

        # Reset flag agar dianggap belum ada file dimuat
        self.flag = False
        self.flag2 = False

        # Nonaktifkan tombol filter/export
        self.ui.load_pages.btn_filter_data.setEnabled(False)
        self.ui.load_pages.btn_export_data_3.setEnabled(False)
        self.ui.load_pages.btn_filter_data_3.setEnabled(False)

        # Terapkan style gelap untuk tombol-tombol tersebut
        self.ui.load_pages.btn_filter_data.setStyleSheet(style_dark)
        self.ui.load_pages.btn_filter_data_3.setStyleSheet(style_dark)
        self.ui.load_pages.btn_export_data_3.setStyleSheet(style_dark)

        # Optional: nonaktifkan cari file page 3 sampai input utama dimasukkan lagi
        self.ui.load_pages.btn_cari_2.setEnabled(False)
        self.ui.load_pages.btn_cari_2.setStyleSheet(style_dark)

    def kembali(self):
        self.ui.left_menu.hide()  # atau .setVisible(False)

        # Kembali ke halaman menu utama
        MainFunctions.set_page(self, self.ui.load_pages.page_menu)

        # Reset semua input dan tabel
        self.ui.load_pages.input_label.clear()
        self.ui.load_pages.label_cari_2.clear()

        self.ui.left_menu.setDisabled(True)

        self.ui.load_pages.table_view_data.setModel(None)
        self.ui.load_pages.table_view_data_2.setModel(None)
        self.ui.load_pages.table_view_page_3_1.setModel(None)
        self.ui.load_pages.table_view_page_3_2.setModel(None)

        # Reset flag dan mode
        self.flag = False
        self.flag2 = False
        self.mode = None



    def handle_internal_mode(self):
        self.reset_ui_state()
        self.ui.left_menu.select_only_one("btn_page_1")
        self.ui.left_menu.show()  # atau .setVisible(False)
        self.ui.left_menu.setDisabled(False)
        # Ubah status mode
        self.mode = "internal"
        
        # Debug info
        print("Mode saat ini:", self.mode)
        


        # Pindah ke halaman Page 1
        MainFunctions.set_page(self, self.ui.load_pages.page_1)

        # Ubah tampilan tombol, status, dll sesuai kebutuhan
        self.ui.load_pages.btn_cari_file.setStyleSheet(style_light)
        self.ui.load_pages.btn_load_file.setStyleSheet(style_dark)

    def handle_eksternal_mode(self):
        self.reset_ui_state()
        self.ui.left_menu.select_only_one("btn_page_1")
        
        # Aktifkan left menu kembali
        self.ui.left_menu.show()
        self.ui.left_menu.setDisabled(False)

        # Ubah status mode
        self.mode = "eksternal"
        
        # Debug info
        print("Mode saat ini:", self.mode)

        
        

        # Pindah ke halaman Page 1
        MainFunctions.set_page(self, self.ui.load_pages.page_1)
        

        # Ubah tampilan tombol, status, dll sesuai kebutuhan
        self.ui.load_pages.btn_cari_file.setStyleSheet(style_light)
        self.ui.load_pages.btn_load_file.setStyleSheet(style_dark)

    def get_current_mode(self):
        return self.mode
    
    def get_selected_columns(self):
        if self.get_current_mode().lower() == "eksternal":
            return [
                'Spbu No.', 'Ship To Code', 'OrderNumber', 'Delivery Number', 'Product', 
                'Volume', 'Delivery Date', 'Order Expired', 'Rit', 'MS2', 'Order Status'
            ]
        else:
            return [
                'Spbu No.', 'Ship To Code', 'OrderNumber', 'Delivery Number', 'Product', 
                'Volume', 'Delivery Date', 'Order Expired', 'Rit', 'MS2', 'Order Status',
                'City', 'Max Tanker'
            ]

    ### FUNGSI PAGE 1 DAN 2 ###
    def browsefiles(self):
        global style_dark
        global style_light

        # self.ui.load_pages.input_label.setReadOnly(True)
        fname = QFileDialog.getOpenFileName(self, 'Open File', 'D:', 'Excel Files (*.xlsx);;CSV Files (*.csv)')
        self.ui.load_pages.input_label.setText(fname[0])
        table = self.ui.load_pages.table_view_data  # QTableView
        path = self.ui.load_pages.input_label.text()
        
        # Tampilkan pop-up loading
        progress = QProgressDialog("Memuat data...", "Batal", 0, 100, self)
        progress.setWindowModality(Qt.WindowModal)
        progress.setWindowTitle("Loading")
        progress.setMinimumDuration(100)  # Minimal waktu tampilan agar tidak hilang terlalu cepat
        progress.setValue(20)  # Awal progress

        if not os.path.exists(path):
            print("File tidak ditemukan!")
            self.flag = False
            self.ui.load_pages.btn_load_file.setStyleSheet(style_dark)
            return
        
        try:
            df = pd.read_excel(path)  # Baca Excel
            progress.setValue(50)
            # Buat model untuk QTableView
            model = QStandardItemModel(df.shape[0], df.shape[1])
            model.setHorizontalHeaderLabels(df.columns)  # Set header kolom

            # Masukkan data ke dalam model
            for row in range(df.shape[0]):
                for col in range(df.shape[1]):
                    item = QStandardItem(str(df.iat[row, col]))
                    model.setItem(row, col, item)
                progress.setValue(50 + (row / df.shape[0]) * 50)

            if progress.wasCanceled():
                self.flag = False
                self.ui.load_pages.btn_load_file.setStyleSheet(style_dark)
                QMessageBox.warning(self, "Dibatalkan", "Proses loading dibatalkan.")
                return
            
            # Set model ke QTableView
            table.setModel(model)
            self.apply_dark_theme_to_table(table)
            progress.setValue(100)
            self.ui.load_pages.btn_load_file.setStyleSheet(style_light)

        except Exception as e:
            self.flag = False
            self.ui.load_pages.btn_load_file.setStyleSheet(style_dark)
            print(f"Error saat membaca file: {e}")
    
    def load_data(self):
        path = self.ui.load_pages.input_label.text()
        self.path_temp = path

        if not os.path.exists(path):
            self.flag = False
            QMessageBox.critical(self, "Error", "File tidak ditemukan!")
            return

        try:
            df = pd.read_excel(path)  # Membaca file Excel

            # Buat model untuk QTableView
            model = QStandardItemModel(df.shape[0], df.shape[1])
            model.setHorizontalHeaderLabels(df.columns)

            # Masukkan data ke dalam model
            for row in range(df.shape[0]):
                for col in range(df.shape[1]):
                    item = QStandardItem(str(df.iat[row, col]))
                    model.setItem(row, col, item)
            
            
            self.flag = True

            # Set model ke QTableView
            self.ui.load_pages.table_view_data.setModel(model)
            self.apply_dark_theme_to_table(self.ui.load_pages.table_view_data_2)

            # Tampilkan pop-up sukses
            QMessageBox.information(self, "Sukses", "Data Berhasil Dimuat!")

        except Exception as e:
            self.flag = False
            QMessageBox.critical(self, "Error", f"Terjadi kesalahan: {e}")
        
    
    def filter_data(self):
        path = self.ui.load_pages.input_label.text()
        
        if not os.path.exists(path):
            QMessageBox.critical(self, "Error", "File tidak ditemukan!")
            return

        try:
            df = pd.read_excel(path)

            # Ambil kolom berdasarkan mode
            selected_columns = self.get_selected_columns()

            # Tambahkan kolom kosong jika tidak ada
            for col in selected_columns:
                if col not in df.columns:
                    df[col] = ""

            index_def = df[(df['Product'] == "PERTAMAX") & (df['Volume'] == 2000)].index
            not_filtered_data = df.drop(index_def)
            filtered_data_value = df.loc[index_def]

            # Ambil hanya kolom yang dipilih
            filtered_data_value = filtered_data_value[selected_columns]
            not_filtered_data = not_filtered_data[selected_columns]

            # Buat model berdasarkan kolom yang dipilih
            filtered_data = filtered_data_value.values.tolist()
            model = QStandardItemModel(len(filtered_data), len(selected_columns))
            model.setHorizontalHeaderLabels(selected_columns)
            table = self.ui.load_pages.table_view_data_2
            header = table.horizontalHeader()
            header.setStretchLastSection(True)
            header.setSectionResizeMode(QHeaderView.Stretch)

            for row_idx, row_data in enumerate(filtered_data):
                for col_idx, value in enumerate(row_data):
                    item = QStandardItem(str(value))
                    model.setItem(row_idx, col_idx, item)

            self.ui.load_pages.table_view_data_2.setModel(model)
            self.apply_dark_theme_to_table(self.ui.load_pages.table_view_data_2)

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Terjadi kesalahan: {e}")
            return pd.DataFrame(), pd.DataFrame()
        print("Selected columns:", selected_columns)
        print("Data columns in model:", len(filtered_data[0]) if filtered_data else 0)

        return pd.DataFrame(not_filtered_data), pd.DataFrame(filtered_data_value)
    


    
    def show_data_2(self):
        path = self.ui.load_pages.input_label.text()

        # Tampilkan pop-up loading
        progress = QProgressDialog("Memuat data...", "Batal", 0, 100, self)
        progress.setWindowModality(Qt.WindowModal)
        progress.setWindowTitle("Loading")
        progress.setMinimumDuration(100)  # Minimal waktu tampilan agar tidak hilang terlalu cepat
        progress.setValue(20)  # Awal progress

        if not os.path.exists(path):
            QMessageBox.critical(self, "Error", "File tidak ditemukan!")
            return

        try:
            df = pd.read_excel(path)  # Membaca file Excel
            progress.setValue(50)
            # Buat model untuk QTableView
            model = QStandardItemModel(df.shape[0], df.shape[1])
            model.setHorizontalHeaderLabels(df.columns)
            

            # Masukkan data ke dalam model
            for row in range(df.shape[0]):
                for col in range(df.shape[1]):
                    item = QStandardItem(str(df.iat[row, col]))
                    model.setItem(row, col, item)
                progress.setValue(50 + (row / df.shape[0]) * 50)
            

            if progress.wasCanceled():
                QMessageBox.warning(self, "Dibatalkan", "Proses loading dibatalkan.")
                return
            # Set model ke QTableView
            self.ui.load_pages.table_view_data_2.setModel(model)
            progress.setValue(100)

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Terjadi kesalahan: {e}")

    ### FUNGSI PAGE 3 ###

    def browse_data_3(self):
        global style_light
        global style_dark

        print("ditekann tombol cari")
        fname = QFileDialog.getOpenFileName(self, 'Open File', 'D:', 'Excel Files (*.xlsx);;CSV Files (*.csv)')
        self.ui.load_pages.label_cari_2.setText(fname[0])
        table = self.ui.load_pages.table_view_page_3_1  # QTableView
        path = self.ui.load_pages.label_cari_2.text()
    
        # Tampilkan pop-up loading
        progress = QProgressDialog("Memuat data...", "Batal", 0, 100, self)
        progress.setWindowModality(Qt.WindowModal)
        progress.setWindowTitle("Loading")
        progress.setMinimumDuration(100)  # Minimal waktu tampilan agar tidak hilang terlalu cepat
        progress.setValue(20)  # Awal progress

        if not os.path.exists(path):
            print("File tidak ditemukan!")
            self.flag2 = False
            return
        
        try:
            df = pd.read_excel(path)  # Baca Excel
            df = df.loc[:, ~df.columns.isna()]  # Buang kolom tanpa nama
            progress.setValue(50)
            # Buat model untuk QTableView
            model = QStandardItemModel()
            model.setColumnCount(len(df.columns))
            model.setRowCount(len(df.index))
            model.setHorizontalHeaderLabels([str(col) for col in df.columns])


            # Masukkan data ke dalam model
            for row in range(df.shape[0]):
                for col in range(df.shape[1]):
                    item = QStandardItem(str(df.iat[row, col]))
                    model.setItem(row, col, item)
                progress.setValue(50 + (row / df.shape[0]) * 50)
            self.flag2 = True

            if progress.wasCanceled():
                QMessageBox.warning(self, "Dibatalkan", "Proses loading dibatalkan.")
                self.flag2 = False
                return
            
            # Set model ke QTableView
            self.flag2 =True
            self.ui.load_pages.btn_filter_data_3.setEnabled(True)
            self.ui.load_pages.btn_export_data_3.setEnabled(False)

            self.ui.load_pages.btn_filter_data_3.setStyleSheet(style_light)
            self.ui.load_pages.btn_export_data_3.setStyleSheet(style_dark)
            table.setModel(model)
            header = table.horizontalHeader()
            header.setStretchLastSection(True)
            header.setSectionResizeMode(QHeaderView.Stretch)

            self.apply_dark_theme_to_table(table)
            progress.setValue(100)
            

        except Exception as e:
            print(f"Error saat membaca file: {e}")
            self.flag2 = False


    def filter_data_3(self):
        global style_light
        global style_dark
        print("Ditekan tombol filter")
        
        # Ambil path dari file
        path_mentah = self.path_temp
        path_filter = self.ui.load_pages.label_cari_2.text()
        not_filtered_data = self.filter_data() 

        # Load data dari Excel
        df_mentah = pd.read_excel(path_mentah)
        df_filter = pd.read_excel(path_filter)


        # Filter data
        if "Delivery Number" in df_mentah.columns and "Loading Order" in df_filter.columns:
            filtered_data = df_mentah[df_mentah["Delivery Number"].isin(df_filter["Loading Order"])]
        else:
            print("ERROR: Kolom tidak ditemukan!")
            self.flag2 = False
            return  # Hentikan eksekusi jika kolom tidak ada
        
        selected_columns = self.get_selected_columns()

        # Pastikan semua kolom tersedia dalam filtered_data
        available_columns = [col for col in selected_columns if col in filtered_data.columns]
        filtered_data_value = filtered_data[available_columns]

        # Set QTableView
        table = self.ui.load_pages.table_view_page_3_2
        model = QStandardItemModel(filtered_data_value.shape[0], filtered_data_value.shape[1])
        model.setHorizontalHeaderLabels(filtered_data_value.columns)

        # Isi model dengan data
        for row in range(filtered_data_value.shape[0]):
            for col in range(filtered_data_value.shape[1]):
                item = QStandardItem(str(filtered_data_value.iat[row, col]))
                model.setItem(row, col, item)

        # Set model ke tabel
        table.setModel(model)
        header = table.horizontalHeader()
        header.setStretchLastSection(True)
        header.setSectionResizeMode(QHeaderView.Stretch)

        self.apply_dark_theme_to_table(table)
        self.flag2 = True
        self.ui.load_pages.btn_filter_data_3.setEnabled(True)
        self.ui.load_pages.btn_export_data_3.setEnabled(True)

        self.ui.load_pages.btn_filter_data_3.setStyleSheet(style_light)
        self.ui.load_pages.btn_export_data_3.setStyleSheet(style_light)  
        return pd.DataFrame(filtered_data_value)




    def export_data_3(self):
        df = pd.read_excel(self.path_temp)
        settings = QSettings("MyApp", "ExportSettings")
        last_saved_path = settings.value("last_export_path", "", type=str)

        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getSaveFileName(self, "Simpan File", last_saved_path, "Excel Files (*.xlsx);;All Files (*)", options=options)
        if not file_path:
            return

        try:
            with pd.ExcelWriter(file_path, engine='xlsxwriter') as writer:
                # Data awal dan filter
                not_filtered_data_3 = self.filter_data_3()
                not_filtered_data, filtered_data_value = self.filter_data()
                filtered_out_data = not_filtered_data[~not_filtered_data['Delivery Number'].isin(not_filtered_data_3['Delivery Number'])]

                product_values = filtered_out_data["Product"].unique()
                rekap_data = []

                for product in product_values:
                    a = filtered_out_data.loc[(filtered_out_data['Product'] == product) & (filtered_out_data['Volume'])]
                    print(a)
                    rit1 = filtered_out_data[(filtered_out_data["Product"] == product) & (filtered_out_data["Rit"] == 1) ]
                    rit2 = filtered_out_data[(filtered_out_data["Product"] == product) & (filtered_out_data["Rit"] == 2) ]
                    rit3 = filtered_out_data[(filtered_out_data["Product"] == product) & (filtered_out_data["Rit"] == 3) ]

                    rit1_vol = rit1["Volume"].sum()
                    rit2_vol = rit2["Volume"].sum()
                    rit3_vol = rit3["Volume"].sum()
                    total_volume = rit1_vol + rit2_vol + rit3_vol

                    rekap_data.append({
                        "Product": product,
                        "Rit 1": rit1_vol,
                        "Rit 2": rit2_vol,
                        "Rit 3": rit3_vol,
                        "Total": total_volume
                    })

                rekap_df = pd.DataFrame(rekap_data)

                total_row = {
                    "Product": "Grand Total",
                    "Rit 1": rekap_df["Rit 1"].sum(),
                    "Rit 2": rekap_df["Rit 2"].sum(),
                    "Rit 3": rekap_df["Rit 3"].sum(),
                    "Total": rekap_df["Total"].sum()
                }
                rekap_df = pd.concat([rekap_df, pd.DataFrame([total_row])], ignore_index=True)

                # Simpan data ke sheet
                filtered_out_data.to_excel(writer, sheet_name="Sheet1", index=False)
                not_filtered_data_3.to_excel(writer, sheet_name="SPBUN", index=False)
                filtered_data_value.to_excel(writer, sheet_name="PERTASHOP", index=False)

                # Hitung summary pivot
                count_delivery_number = filtered_out_data.groupby("Product")["Delivery Number"].count().reset_index()
                sum_of_volume = filtered_out_data.groupby("Product")["Volume"].sum().reset_index()
                count_delivery_number.columns = ["Product", "Count_of_Delivery_Number"]
                sum_of_volume.columns = ["Product", "Sum_of_Volume"]
                pivot_df = pd.merge(count_delivery_number, sum_of_volume, on="Product", how="outer")

                grand_total = pd.DataFrame({
                    "Product": ["Grand Total"],
                    "Count_of_Delivery_Number": [pivot_df["Count_of_Delivery_Number"].sum()],
                    "Sum_of_Volume": [pivot_df["Sum_of_Volume"].sum()]
                })
                pivot_df = pd.concat([pivot_df, grand_total], ignore_index=True)

                # Setup posisi tulis pivot dan rekap
                pivot_startcol = len(filtered_out_data.columns) + 1
                rekap_startrow = 10
                rekap_startcol = 14

                workbook = writer.book
                worksheet = writer.sheets["Sheet1"]

                # Format angka ribuan sesuai Indonesia (default Excel locale harus Indonesia)
                number_format = workbook.add_format({'num_format': '#,##0', 'align': 'right'})
                header_format = workbook.add_format({
                    "bold": True,
                    "bg_color": "#C5D9F1",
                    "border": 1,
                    "align": "center",
                    "valign": "vcenter"
                })
                body_format = workbook.add_format({
                    "font_color": "black",
                    "bg_color": "white",
                    "border": 1,
                    "align": "left",
                    "valign": "vcenter"
                })
                body_number_format = workbook.add_format({
                    "num_format": '#,##0',
                    "border": 1,
                    "align": "right",
                    "valign": "vcenter"
                })
                grand_total_format = workbook.add_format({
                    "bold": True,
                    "bg_color": "#B7DEE8",
                    "border": 1,
                    "align": "left",
                    "valign": "vcenter"
                })
                grand_total_number_format = workbook.add_format({
                    "bold": True,
                    "bg_color": "#B7DEE8",
                    "border": 1,
                    "align": "right",
                    "valign": "vcenter",
                    "num_format": '#,##0'
                })

                # Tulis header pivot manual (supaya styling header)
                for col_num, value in enumerate(pivot_df.columns.values):
                    worksheet.write(0, pivot_startcol + col_num, value, header_format)

                # Tulis body pivot manual dengan format angka
                for row_num in range(len(pivot_df) - 1):
                    for col_num in range(len(pivot_df.columns)):
                        cell_value = pivot_df.iloc[row_num, col_num]
                        if col_num == 0:
                            worksheet.write(row_num + 1, pivot_startcol + col_num, cell_value, body_format)
                        else:
                            worksheet.write(row_num + 1, pivot_startcol + col_num, cell_value, body_number_format)

                # Tulis grand total pivot terakhir dengan format khusus
                last_row_pivot = len(pivot_df) - 1
                for col_num in range(len(pivot_df.columns)):
                    cell_value = pivot_df.iloc[last_row_pivot, col_num]
                    if col_num == 0:
                        worksheet.write(last_row_pivot + 1, pivot_startcol + col_num, cell_value, grand_total_format)
                    else:
                        worksheet.write(last_row_pivot + 1, pivot_startcol + col_num, cell_value, grand_total_number_format)

                # Tulis rekap_df ke Sheet1 dengan posisi dan styling
                rekap_df.to_excel(writer, sheet_name="Sheet1", startrow=rekap_startrow, startcol=rekap_startcol, index=False)

                # Autofit manual kolom pivot dan rekap
                self.autofit_columns(worksheet, pivot_df, pivot_startcol)
                self.autofit_columns(worksheet, rekap_df, rekap_startcol, rekap_startrow)

                # Format header rekap manual (baris header di rekap_startrow)
                for col_num, value in enumerate(rekap_df.columns.values):
                    worksheet.write(rekap_startrow, rekap_startcol + col_num, value, header_format)

                # Format isi rekap manual
                for row_num in range(len(rekap_df) - 1):
                    for col_num in range(len(rekap_df.columns)):
                        value = rekap_df.iloc[row_num, col_num]
                        if col_num == 0:  # Kolom "Product"
                            worksheet.write(rekap_startrow + 1 + row_num, rekap_startcol + col_num, value, body_format)
                        else:
                            worksheet.write(rekap_startrow + 1 + row_num, rekap_startcol + col_num, value, body_number_format)

                # Format total grand total rekap
                last_row_rekap = len(rekap_df) - 1
                for col_num in range(len(rekap_df.columns)):
                    value = rekap_df.iloc[last_row_rekap, col_num]
                    if col_num == 0:  # Kolom "Product"
                        worksheet.write(rekap_startrow + 1 + last_row_rekap, rekap_startcol + col_num, value, grand_total_format)
                    else:
                        worksheet.write(rekap_startrow + 1 + last_row_rekap, rekap_startcol + col_num, value, grand_total_number_format)


                # Simpan lokasi terakhir
                settings.setValue("last_export_path", file_path)
                QMessageBox.information(self, "Sukses", f"Data berhasil diekspor ke:\n{file_path}")

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Gagal mengekspor file: {e}")



    def autofit_columns(self, worksheet, dataframe, startcol=0, startrow=0):
        for idx, col in enumerate(dataframe.columns):
            col_values = dataframe[col].tolist()

            if pd.api.types.is_numeric_dtype(dataframe[col]):
                # Format angka ribuan Indonesia (1.000)
                str_values = [f"{int(v):,}".replace(",", ".") if pd.notnull(v) else "" for v in col_values]
                max_len = max([len(str(col))] + [len(s) for s in str_values]) + 5  # margin lebih besar untuk angka
            else:
                str_values = [str(v) if pd.notnull(v) else "" for v in col_values]
                max_len = max(len(str(col)), max(len(s) for s in str_values)) + 5  # margin standar untuk teks

            worksheet.set_column(startcol + idx, startcol + idx, max_len)





    def btn_clicked(self):
        global style_light
        global style_dark
        # GET BT CLICKED
        btn = SetupMainWindow.setup_btns(self)

        #LEFT MENUUU
        # Open Page 1
        if btn.objectName() == "btn_page_1":
            #select page
            self.ui.left_menu.select_only_one(btn.objectName())

            #Load Page
            MainFunctions.set_page(self, self.ui.load_pages.page_1)
            self.ui.load_pages.btn_cari_file.setStyleSheet(style_light)
            self.ui.load_pages.btn_load_file.setStyleSheet(style_dark)

            
        # Open Page 2
        if btn.objectName() == "btn_page_2":
            #select page
            self.ui.left_menu.select_only_one(btn.objectName())
            

            #Load Page
            MainFunctions.set_page(self, self.ui.load_pages.page_2)
            path = self.ui.load_pages.input_label.text()
            if self.flag == False:
                QMessageBox.warning(self, "Peringatan", "File Belum Di Input!")
                self.ui.load_pages.btn_filter_data.setEnabled(False)
                self.ui.load_pages.btn_filter_data.setStyleSheet(style_dark)
            else:
                self.ui.load_pages.btn_filter_data.setEnabled(True)
                self.ui.load_pages.btn_filter_data.setStyleSheet(style_light)
                # self.ui.load_pages.btn_export_data.setEnabled(True)
                self.show_data_2()
            
        # Open Page 3
        if btn.objectName() == "btn_page_3":
            #select page
            self.ui.left_menu.select_only_one(btn.objectName())        
            #Load Page
            MainFunctions.set_page(self, self.ui.load_pages.page_3)
            if self.flag == False:
                print("Input File")
                self.ui.load_pages.btn_cari_2.setEnabled(False)
                self.ui.load_pages.btn_filter_data_3.setEnabled(False)
                self.ui.load_pages.btn_export_data_3.setEnabled(False)

                self.ui.load_pages.btn_cari_2.setStyleSheet(style_dark)
                self.ui.load_pages.btn_filter_data_3.setStyleSheet(style_dark)
                self.ui.load_pages.btn_export_data_3.setStyleSheet(style_dark)
            else:
                self.ui.load_pages.btn_cari_2.setEnabled(True)
                self.ui.load_pages.btn_filter_data_3.setEnabled(False)
                self.ui.load_pages.btn_export_data_3.setEnabled(False)

                self.ui.load_pages.btn_cari_2.setStyleSheet(style_light)
                self.ui.load_pages.btn_filter_data_3.setStyleSheet(style_dark)
                self.ui.load_pages.btn_export_data_3.setStyleSheet(style_dark)


                
        

    # LEFT MENU BTN IS RELEASED
    # Run function when btn is released
    # Check funtion by object name / btn_id
    # ///////////////////////////////////////////////////////////////
    def btn_released(self):
        # GET BT CLICKED
        btn = SetupMainWindow.setup_btns(self)

        # DEBUG
        print(f"Button {btn.objectName()}, released!")

    # RESIZE EVENT
    # ///////////////////////////////////////////////////////////////
    def resizeEvent(self, event):
        SetupMainWindow.resize_grips(self)

    # MOUSE CLICK EVENTS
    # ///////////////////////////////////////////////////////////////
    def mousePressEvent(self, event):
        # SET DRAG POS WINDOW
        self.dragPos = event.globalPos()

    

# SETTINGS WHEN TO START
# Set the initial class and also additional parameters of the "QApplication" class
# ///////////////////////////////////////////////////////////////

if __name__ == "__main__":
    # APPLICATION
    # ///////////////////////////////////////////////////////////////
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("icon.ico"))
    window = SplashScreen()

    # EXEC APP
    # ///////////////////////////////////////////////////////////////
    sys.exit(app.exec_())