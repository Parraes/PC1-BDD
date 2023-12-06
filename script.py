from PyQt6.QtWidgets import QApplication, QDialog, QGridLayout, QLabel, QLineEdit, QSpinBox, QPushButton, QFileDialog, QWidget
from PyQt6.QtCore import Qt
import os

class SimpleWindow(QDialog):
    def __init__(self, parent=None):
        super(SimpleWindow, self).__init__(parent)

        # Crear un diseño de cuadrícula
        layout = QGridLayout(self)

        # Variables para almacenar la carpeta y la ruta seleccionadas
        self.selected_folder = ""
        self.selected_path = ""


        ######## SELECCIONAR JORNADA INPUT #########################################################
        # INPUT NÚMERO JORNADA 
        label_number = QLabel("Jornada a scrapear:")
        layout.addWidget(label_number, 0, 0)

        # Estilos input numero jornada
        number_input = QSpinBox(self)
        number_input.setMinimum(1)  # Establecer el valor mínimo (jornada 1)
        number_input.setMaximum(38)  # Establecer el valor máximo (Jornada 36)
        number_input.setSingleStep(2)  # Establecer el paso
        number_input.setMaximumSize(38, 20)
        number_input.setMinimumSize(38, 20)
        layout.addWidget(number_input, 0, 1)
      

        # Agregar una fila vacía
        empty_widget = QWidget()
        empty_widget.setFixedHeight(10)  # Tamaño del gap (10 px)
        layout.addWidget(empty_widget, 1, 0)


        ######## SELECCIONAR RUTA DONDE GUARDAR EL EXCEL OUTPUT DEL SCRAPER ######################
        # LABEL TEXTO 
        label_text = QLabel("Ruta output scraper:")
        layout.addWidget(label_text, 2, 0)

        # INPUT TEXTO (QLineEdit en lugar de QSpinBox)
        self.text_input = QLineEdit(self)
        # Estilos input del texto
        self.text_input.setFixedHeight(20)  # Establecer una altura fija
        layout.addWidget(self.text_input, 2, 1)

        # BOTÓN PARA SELECCIONAR CARPETA
        select_folder_button = QPushButton("Seleccionar Carpeta")
        select_folder_button.clicked.connect(self.select_folder)
        layout.addWidget(select_folder_button, 3, 0)

        ######## ESTABLECER DISEÑO DE LA VENTANA ###############################################
    
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

if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    window = SimpleWindow()
    window.show()
    sys.exit(app.exec())
