import os
import sys
import platform
import json
import logging
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
is_debug=True
#if sys.argv[0]=="--debug":
#	is_debug=True
#else:
#	is_debug=False
if is_debug==False:
	logging.basicConfig(filename="QDE.log",filemode="w",format="%(asctime)s %(levelname)s:%(message)s",datefmt="%Y-%m-%d %H:%M:%S",level=logging.INFO)
else:
	logging.basicConfig(format="%(asctime)s %(levelname)s:%(message)s",datefmt="%Y-%m-%d %H:%M:%S",level=logging.DEBUG)
if os.path.exists("config.json")==False:
	with open(file="config.json",mode="w",encoding="utf-8") as default_conf_witer:
		default_conf_dic={"lang":"zh_CN"}
		json.dump(obj=default_conf_dic,fp=default_conf_witer,indent=4,sort_keys=True)
	logging.warning("No config file found, creating default config file...")
with open(file="config.json",mode="r",encoding="utf-8") as config_reader:
	conf_dic=json.load(config_reader)
class setting:
	lang_=str(conf_dic["lang"])
	font=str(conf_dic["font"])
	font_size=int(conf_dic["font_size"])
	font_weight=int(conf_dic["font_weight"])
	font_italic=bool(conf_dic["font_italic"])
	font_bold=bool(conf_dic["font_bold"])
	font_speed=int(conf_dic["font_speed"])
	damaku_font=QFont(font,pointSize=font_size,weight=font_weight,italic=font_italic)
	damaku_font.setBold(font_bold)
	def update_setting(self,conf_dic:dict):
		new_lang=str(conf_dic["lang"])
		new_font=str(conf_dic["font"])
		new_font_size=str(conf_dic["font_size"])
		new_font_speed=int(conf_dic["font_speed"])
		new_font_weight=int(conf_dic["font_weight"])
		new_font_italic=bool(conf_dic["font_italic"])
		new_font_bold=bool(conf_dic["font_bold"])
		setting.damaku_font=QFont(new_font,pointSize=new_font_size,weight=new_font_weight,italic=new_font_italic)
		setting.damaku_font.setBold(new_font_bold)
		qt_widget_translation="lang/"+setting.lang_+"/widgets_"+setting.lang_+".qm"
		qt_main_translation="lang/"+setting.lang_+"qt_"+setting.lang_+".qm"
		lang.widget_translator=QTranslator()
		lang.widget_translator.load(qt_widget_translation)
		lang.main_translator=QTranslator()
		lang.main_translator.load(qt_main_translation)
		QApplication.processEvents()
with open(file="lang/"+setting.lang_+"/"+setting.lang_+".json",mode="r",encoding="utf-8") as lang_loader:
	langdic=json.load(lang_loader)
# 读入语言数据
class lang:
	qt_widget_translation="lang/"+setting.lang_+"/widgets_"+setting.lang_+".qm"
	qt_main_translation="lang/"+setting.lang_+"qt_"+setting.lang_+".qm"
	widget_translator=QTranslator()
	widget_translator.load(qt_widget_translation)
	main_translator=QTranslator()
	main_translator.load(qt_main_translation)
	class error:
		platform_error=str(langdic["error"]["platform_error"])
	class info:
		loaded_conf=str(langdic["info"]["loaded_conf"])
		current_sys=str(langdic["info"]["current_sys"])
		sended_notification=str(langdic["info"]["sended_notification"])
		shown_tray=str(langdic["info"]["shown_tray"])
		shown_window=str(langdic["info"]["shown_window"])
		closed_tray=str(langdic["info"]["closed_tray"])
	class warning:
		platform_warning=str(langdic["warning"]["platform_warning"])
	class debug:
		created_action=str(langdic["debug"]["created_action"])
		finished_creating_menu=str(langdic["debug"]["created_menu"])
		enabled_toast=str(langdic["debug"]["enabled_toast"])
	class notification:
		title=str(langdic["ui"]["notification_title"])
		msg=str(langdic["ui"]["notification_msg"])
		exit_menu=str(langdic["ui"]["exit_menu"])
		setting_menu=str(langdic["ui"]["setting_menu"])
		tooltip=str(langdic["ui"]["tooltip"])
	class setting_ui:
		yes=str(langdic["ui"]["yes"])
		no=str(langdic["ui"]["no"])
		save=str(langdic["ui"]["save"])
		cancel=str(langdic["ui"]["cancel"])
		title=str(langdic["ui"]["setting_title"])
		lang_label=str(langdic["ui"]["setting_lang_label"])
		font_label=str(langdic["ui"]["setting_font_label"])
		font_size=str(langdic["ui"]["setting_font_size"])
		font_speed=str(langdic["ui"]["setting_font_speed"])
		font_weight=str(langdic["ui"]["setting_font_weight"])
		font_italic=str(langdic["ui"]["setting_font_italic"])
		font_bold=str(langdic["ui"]["setting_font_bold"])
logging.info(lang.info.loaded_conf)

try:
	sys_ver=platform.win32_ver()[0]
except:
	logging.error(lang.error.platform_error)
	exit()
if sys_ver=="10" or sys_ver=="8":
	import win10toast
	is_win10=True
	logging.debug(lang.debug.enabled_toast)
else:
	is_win10=False
	logging.warning(lang.warning.platform_warning)
logging.info(lang.info.current_sys+sys_ver)
class SettingDialog(QDialog):
	def __init__(self):
		super(SettingDialog,self).__init__()
		font=QFont("Microsoft YaHei",15)
		self.setWindowIcon(QIcon("resources/program.ico"))
		self.setWindowTitle("")
		self.setWindowOpacity(0.95)
		self.setAttribute(Qt.WA_TranslucentBackground)
		self.setWindowFlag(Qt.FramelessWindowHint)
		setting_title_label=QLabel(lang.setting_ui.title)
		setting_title_label.setFont(font)
		setting_title_label.setStyleSheet("QLabel{border:1px solid gray;width:15px;border-radius:10px;padding:2px 4px;background:#00CED1;}")
		setting_title_label.setAlignment(Qt.AlignCenter)
		lang_label=QLabel(lang.setting_ui.lang_label)
		lang_label.setFont(font)
		lang_label.setStyleSheet("QLabel{border:1px solid gray;width:15px;border-radius:10px;padding:2px 4px;background:#00CED1;}")
		self.lang_chooser=QComboBox()
		lang_list,lang_files=self.get_lang()
		self.lang_chooser.setFont(font)
		self.lang_chooser.setStyleSheet("QComboBox{border:1px solid gray;width:60px;border-radius:10px;padding:2px 4px;background:#00CED1;}QComboBox:drop-down{subcontrol-origin:padding;subcontrol-position:top right;border-top-right-radius:10px;border-bottom-right-radius:10px;border-top-left-radius:10px;border-bottom-left-radius:10px;}QComboBox:down-arrow{image:url(resources/downarrow.png);width:15px;height:15px;}QComboBox:down-arrow:on{image:url(resources/uparrow.png);}")
		self.lang_chooser.addItems(lang_list)
		self.lang_chooser.setCurrentIndex(lang_list.index(setting.lang_))
		font_label=QLabel(lang.setting_ui.font_label)
		font_label.setFont(font)
		font_label.setStyleSheet("QLabel{border:1px solid gray;width:15px;border-radius:10px;padding:2px 4px;background:#00CED1;}")
		self.font_chooser=QFontComboBox()
		self.font_chooser.setFont(font)
		#self.font_chooser.setStyleSheet("QFontComboBox{border:1px solid gray;width:60px;border-radius:10px;padding:2px 4px;background:#00CED1;}QFontComboBox:drop-down{subcontrol-origin:padding;subcontrol-position:top right;border-top-right-radius:10px;border-bottom-right-radius:10px;border-top-left-radius:10px;border-bottom-left-radius:10px;}QFontCombpBox:down-arrow{image:url(resources/downarrow.png);width:15px;height:15px;}QFontComboBox:down-arrow:on{image:url(resources/uparrow.png);")
		self.font_chooser.setFontFilters(QFontComboBox.AllFonts)
		self.font_chooser.setCurrentFont(setting.damaku_font)
		font_size_label=QLabel(lang.setting_ui.font_size)
		font_size_label.setFont(font)
		font_size_label.setStyleSheet("QLabel{border:1px solid gray;width:15px;border-radius:10px;padding:2px 4px;background:#00CED1;}")
		self.font_size_text=QLineEdit(str(setting.font_size))
		self.font_size_text.setStyleSheet("QLineEdit{border:1px solid gray;width:30px;border-radius:10px;padding:2px 4px;}")
		self.font_size_text.setAlignment(Qt.AlignCenter)
		self.font_size_text.setFont(font)
		font_weight_label=QLabel(lang.setting_ui.font_weight)
		font_weight_label.setFont(font)
		font_weight_label.setStyleSheet("QLabel{border:1px solid gray;width:15px;border-radius:10px;padding:2px 4px;background:#00CED1;}")
		self.font_weight_text=QLineEdit(str(setting.font_weight))
		self.font_weight_text.setStyleSheet("QLineEdit{border:1px solid gray;width:30px;border-radius:10px;padding:2px 4px;}")
		self.font_weight_text.setAlignment(Qt.AlignCenter)
		self.font_weight_text.setFont(font)
		font_speed_label=QLabel(lang.setting_ui.font_speed)
		font_speed_label.setFont(font)
		font_speed_label.setStyleSheet("QLabel{border:1px solid gray;width:15px;border-radius:10px;padding:2px 4px;background:#00CED1;}")
		self.font_speed_text=QLineEdit(str(setting.font_speed))
		self.font_speed_text.setStyleSheet("QLineEdit{border:1px solid gray;width:30px;border-radius:10px;padding:2px 4px;}")
		self.font_speed_text.setAlignment(Qt.AlignCenter)
		self.font_speed_text.setFont(font)
		font_italic_label=QLabel(lang.setting_ui.font_italic)
		font_italic_label.setFont(font)
		font_italic_label.setStyleSheet("QLabel{border:1px solid gray;width:15px;border-radius:10px;padding:2px 4px;background:#00CED1;}")
		self.font_italic_text=QComboBox()
		self.font_italic_text.setStyleSheet("QComboBox{border:1px solid gray;width:60px;border-radius:10px;padding:2px 4px;background:#00CED1;}QComboBox:drop-down{subcontrol-origin:padding;subcontrol-position:top right;border-top-right-radius:10px;border-bottom-right-radius:10px;border-top-left-radius:10px;border-bottom-left-radius:10px;}QComboBox:down-arrow{image:url(resources/downarrow.png);width:15px;height:15px;}QComboBox:down-arrow:on{image:url(resources/uparrow.png);}")
		self.font_italic_text.addItems([lang.setting_ui.yes,lang.setting_ui.no])
		if setting.font_italic==True:
			self.font_italic_text.setCurrentIndex(0)
		else:
			self.font_italic_text.setCurrentIndex(1)
		self.font_italic_text.setFont(font)
		font_bold_label=QLabel(lang.setting_ui.font_bold)
		font_bold_label.setFont(font)
		font_bold_label.setStyleSheet("QLabel{border:1px solid gray;width:15px;border-radius:10px;padding:2px 4px;background:#00CED1;}")
		self.font_bold_text=QComboBox()
		self.font_bold_text.setStyleSheet("QComboBox{border:1px solid gray;width:60px;border-radius:10px;padding:2px 4px;background:#00CED1;}QComboBox:drop-down{subcontrol-origin:padding;subcontrol-position:top right;border-top-right-radius:10px;border-bottom-right-radius:10px;border-top-left-radius:10px;border-bottom-left-radius:10px;}QComboBox:down-arrow{image:url(resources/downarrow.png);width:15px;height:15px;}QComboBox:down-arrow:on{image:url(resources/uparrow.png);}")
		self.font_bold_text.addItems([lang.setting_ui.yes,lang.setting_ui.no])
		if setting.font_bold==True:
			self.font_bold_text.setCurrentIndex(0)
		else:
			self.font_bold_text.setCurrentIndex(1)
		self.font_bold_text.setFont(font)
		save_button=QPushButton(lang.setting_ui.save)
		save_button.setFont(font)
		save_button.setStyleSheet("QPushButton{background:#6DDF6D;border-radius:5px;}QPushButton:hover{background:green;}")
		save_button.clicked.connect(self.save_setting)
		cancel_button=QPushButton(lang.setting_ui.cancel)
		cancel_button.setFont(font)
		cancel_button.setStyleSheet("QPushButton{background:#F76677;border-radius:5px;}QPushButton:hover{background:red;}")
		cancel_button.clicked.connect(self.close)
		lang_layout=QHBoxLayout()
		font_layout=QHBoxLayout()
		font_size_layout=QHBoxLayout()
		font_weight_layout=QHBoxLayout()
		font_speed_layout=QHBoxLayout()
		font_italic_layout=QHBoxLayout()
		font_bold_layout=QHBoxLayout()
		button_layout=QHBoxLayout()
		dialog_layout=QVBoxLayout()
		lang_layout.addWidget(lang_label)
		lang_layout.addWidget(self.lang_chooser)
		font_layout.addWidget(font_label)
		font_layout.addWidget(self.font_chooser)
		font_size_layout.addWidget(font_size_label)
		font_size_layout.addWidget(self.font_size_text)
		font_weight_layout.addWidget(font_weight_label)
		font_weight_layout.addWidget(self.font_weight_text)
		font_speed_layout.addWidget(font_speed_label)
		font_speed_layout.addWidget(self.font_speed_text)
		font_italic_layout.addWidget(font_italic_label)
		font_italic_layout.addWidget(self.font_italic_text)
		font_bold_layout.addWidget(font_bold_label)
		font_bold_layout.addWidget(self.font_bold_text)
		button_layout.addWidget(save_button)
		button_layout.addWidget(cancel_button)
		dialog_layout.addWidget(setting_title_label)
		dialog_layout.addLayout(lang_layout)
		dialog_layout.addLayout(font_layout)
		dialog_layout.addLayout(font_size_layout)
		dialog_layout.addLayout(font_weight_layout)
		dialog_layout.addLayout(font_italic_layout)
		dialog_layout.addLayout(font_bold_layout)
		dialog_layout.addLayout(font_speed_layout)
		dialog_layout.addLayout(button_layout)
		self.setLayout(dialog_layout)
	def get_lang(self):
		lang_list=[]
		lang_files=[]
		self.lang_code_list=[]
		for root,dirs,files in os.walk("lang"):
			for name in files:
				with open(file=os.path.join(root,name),mode="r",encoding="utf-8") as lang_reader:
					if name.endswith(".json"):
						lang_list.append(str(json.load(lang_reader)["code"]))
						lang_files.append(str(os.path.join(root,name)))
						self.lang_code_list.append(name.replace(".json",""))
		return lang_list,lang_files
	def get_fixed_value(self,index:int):
		if index==0:
			return 1
		elif index==1:
			return 0
		else:
			raise ValueError
	def save_setting(self):
		new_conf_dic={"lang":str(self.lang_code_list.index(self.lang_chooser.currentIndex())),"font":str(self.font_chooser.currentFont.family()),"font_size":int(self.font_size_text.text()),"font_speed":int(self.font_speed_text.text()),"font_weight":int(self.font_weight_text.text()),"font_italic":int(self.get_fixed_value(self.font_italic_text.currentIndex())),"font_bold":int(self.get_fixed_value(self.font_bold_text.currentIndex()))}
		with open(file="config.json",mode="w",encoding="utf-8") as new_conf_writer:
			json.dump(obj=new_conf_dic,fp=new_conf_writer,indent=4,sort_keys=True)
class TrayIcon(QSystemTrayIcon):
	def __init__(self):
		super(TrayIcon,self).__init__()
		#QApplication.setQuitOnLastWindowClosed(False)
		self.tray_menu=QMenu()
		action_exit=QAction(QIcon("resources/exit.png"),lang.notification.exit_menu,self)
		action_exit.triggered.connect(self.quit_program)
		logging.debug(lang.debug.created_action)
		action_setting=QAction(QIcon("resources/setting.png"),lang.notification.setting_menu,self)
		action_setting.triggered.connect(self.show_setting_ui)
		logging.debug(lang.debug.created_action)
		self.tray_menu.addAction(action_setting)
		self.tray_menu.addAction(action_exit)
		self.setContextMenu(self.tray_menu)
		self.setToolTip(lang.notification.tooltip)
		self.setIcon(QIcon("resources/program.ico"))
		self.setVisible(True)
		logging.debug(lang.debug.finished_creating_menu)
	def quit_program(self):
		logging.info(lang.info.closed_tray)
		self.deleteLater()
		qApp.quit()
		sys.exit()
	def show_setting_ui(self):
		setting_dialog=SettingDialog()
		setting_dialog.exec_()
class main_window(QMainWindow):
	def __init__(self):
		super(main_window,self).__init__()
		central_widget=QWidget()
		self.setCentralWidget(central_widget)
		self.setWindowOpacity(0.95)
		self.setAttribute(Qt.WA_TranslucentBackground)
		self.setWindowFlag(Qt.FramelessWindowHint)
		screen=QApplication.desktop()
		screen_size=QSize(screen.width(),screen.height())
		self.raise_()



app=QApplication(sys.argv)
app.setQuitOnLastWindowClosed(False)
tray_icon=TrayIcon()
if is_win10==True:
	toaster=win10toast.ToastNotifier()
	# 图标作者:https://github.com/nullice/NViconsLib_Silhouette
	toaster.show_toast(title=lang.notification.title,msg=lang.notification.msg,icon_path="resources/program.ico",duration=5,threaded=True)
else:
	tray_icon.showMessage(lang.notification.title,lang.notification.msg,QIcon("resources/program.ico"),5000)
logging.info(lang.info.sended_notification)
tray_icon.show()
logging.info(lang.info.shown_tray)
w=main_window()
w.show()
logging.info(lang.info.shown_window)
sys.exit(app.exec_())