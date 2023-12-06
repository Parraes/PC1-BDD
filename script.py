# Dependencias
from PyQt6.QtWidgets import QApplication, QDialog, QGridLayout, QLabel, QLineEdit, QSpinBox, QPushButton, QFileDialog, QWidget, QTextEdit
from PyQt6.QtCore import Qt
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import ElementNotInteractableException, NoSuchElementException
from bs4 import BeautifulSoup
import requests
import openpyxl
import time
import os

class SimpleWindow(QDialog):
    def __init__(self, parent=None):
        super(SimpleWindow, self).__init__(parent)

        # Crear un diseño de cuadrícula
        layout = QGridLayout(self)
        # Establecer el tamaño máximo de la segunda columna
        layout.setColumnStretch(1, 1)
        layout.setColumnStretch(2, 1)

        # Variables para almacenar la carpeta y la ruta seleccionadas
        self.selected_folder = ""
        self.selected_path = ""


        ### SELECCIONAR JORNADA INPUT ####################################################
        # INPUT NÚMERO JORNADA 
        label_number = QLabel("Jornada a scrapear:")
        layout.addWidget(label_number, 0, 0)

        # Estilos input numero jornada
        self.number_input = QSpinBox(self)
        self.number_input.setMinimum(1)  # Establecer el valor mínimo (jornada 1)
        self.number_input.setMaximum(38)  # Establecer el valor máximo (Jornada 36)
        self.number_input.setSingleStep(2)  # Establecer el paso
        self.number_input.setMaximumSize(38, 20)
        self.number_input.setMinimumSize(38, 20)
        layout.addWidget(self.number_input, 0, 1)
        

        #------- GAP vacio -----------------------------------------
        empty_widget = QWidget()
        empty_widget.setFixedHeight(10)  # Tamaño del gap (10 px)
        layout.addWidget(empty_widget, 4, 0)
        #-----------------------------------------------------------


        ###  SELECCIONAR RUTA DONDE GUARDAR EL EXCEL OUTPUT DEL SCRAPER  #################
        # LABEL TEXTO 
        label_text = QLabel("Ruta output scraper:")
        layout.addWidget(label_text, 2, 0)

        # INPUT TEXTO (QLineEdit en lugar de QSpinBox)
        self.text_input = QLineEdit(self)
        # Estilos input del texto
        self.text_input.setFixedHeight(20)  # Establecer una altura fija
        self.text_input.setMaximumWidth(500)
        layout.addWidget(self.text_input, 2, 1)

        # BOTÓN PARA SELECCIONAR CARPETA
        select_folder_button = QPushButton("Seleccionar Carpeta")
        select_folder_button.clicked.connect(self.select_folder)
        layout.addWidget(select_folder_button, 3, 0)

    
        #------- GAP vacio -----------------------------------------
        empty_widget = QWidget()
        empty_widget.setFixedHeight(10)  # Tamaño del gap (10 px)
        layout.addWidget(empty_widget, 4, 0)
        #-----------------------------------------------------------


        ###  BOTÓN PARA INICIAR SCRAPER  ################################################
        # Crear un botón llamado "Scrapear"
        scrape_button = QPushButton("Scrapear")

        # Conectar la señal clicked del botón a la función scrapear_funcion
        scrape_button.clicked.connect(self.scrapear_funcion)

        layout.addWidget(scrape_button, 5, 0)
    

        ###  VENTANA OUTPUT SCRAPER  ####################################################
        # Crear un QTextEdit para la salida
        self.output_textedit = QTextEdit(self)
        layout.addWidget(self.output_textedit, 6, 0, 2, 0)  # row, column, rowSpan, columnSpan


        ###  ESTABLECER DISEÑO DE LA VENTANA  ###########################################
        self.setMinimumSize(400, 100) # Configurar el tamaño mínimo de la ventana
        # Configurar el diseño para la ventana
        self.setLayout(layout)

        # Configurar el título de la ventana
        self.setWindowTitle("Mister Fantasy Mundo Deportivo Scraper")

        # Evento cerrar ventana 
        self.destroyed.connect(self.cleanup)

    def select_folder(self):
        # Obtener el directorio del script de Python
        script_directory = os.path.dirname(__file__)
        
        folder_path = QFileDialog.getExistingDirectory(self, "Seleccionar Carpeta", script_directory)
        if folder_path:
            # Actualizar las variables de clase con la carpeta y la ruta seleccionadas
            self.selected_folder = folder_path
            self.selected_path = folder_path

            # Actualizar el QLineEdit con la ruta seleccionada
            self.text_input.setText(self.selected_path)

    def cleanup(self):
        # Realizar cualquier limpieza necesaria aquí
        QApplication.quit()

    def click_mas(self):
        # Pinchar en el botón del menu "Más"
        masMenu = self.driver.find_element(By.XPATH, '//*[@id="content"]/header/div[2]/ul/li[5]/a')

        try:
            masMenu.click()
        except (ElementNotInteractableException, NoSuchElementException):
            # Maneja la excepción y espera antes de intentar nuevamente
            print("Anuncio detectado, reiniciando driver...")
            self.driver.refresh()
            time.sleep(3) 
            masMenu.click()

    def scrapear_funcion(self):
        self.output_textedit.append("Starting scraper...")

        # Obtener el valor de la jornada desde el QSpinBox
        jornada_a_scrapear = self.number_input.value()
        # Mostrar el valor en el QTextEdit
        self.output_textedit.append(f"Jornada seleccionada: {jornada_a_scrapear}")

        ruta_output = self.text_input.text()
        # Hacer lo que necesites con la ruta de salida
        self.output_textedit.append(f"Ruta para la salida del scraper selecionada: {ruta_output}")
        self.output_textedit.append(f"____________________________________________")


        # Crea una instancia del controlador del navegador
        driver = webdriver.Chrome()

        # Navega a la página web que deseas hacer scraping
        driver.get("https://mister.mundodeportivo.com/new-onboarding/#market")

        # Espera a que se cargue la página
        driver.implicitly_wait(15)

        # Encuentra el botón de "Consentir" 
        button = driver.find_element(By.XPATH, '//*[@id="didomi-notice-agree-button"]')
        # Haz clic en el botón de "Consentir" 
        button.click()

        # Encuentra el botón de "Siguinete" 
        button = driver.find_element(By.XPATH, '//*[@id="app"]/div/div[2]/div[2]/button')
        # Haz clic en el botón de "Siguiente" 
        button.click()
        button.click()
        button.click()
        button.click()

        # Encuentra el botón de "sing con gmail" 
        button = driver.find_element(By.XPATH, '//*[@id="app"]/div/div[2]/div/button[3]')
        button.click()

if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    window = SimpleWindow()
    window.show()
    sys.exit(app.exec())