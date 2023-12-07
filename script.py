# Dependencias
from PyQt6.QtWidgets import QApplication, QDialog, QGridLayout, QLabel, QLineEdit, QSpinBox, QPushButton, QFileDialog, QWidget, QTextEdit
from PyQt6.QtGui import QColor, QTextCharFormat
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
import threading


class SimpleWindow(QDialog):
    def __init__(self, parent=None):
        super(SimpleWindow, self).__init__(parent)

        self.teams_data = {
        "Real Madrid": "https://cdn.gomister.com/file/cdn-common/teams/15.png?version=20231117",
        "Real Sociedad": "https://cdn.gomister.com/file/cdn-common/teams/16.png?version=20231117",
        "Atlético de Madrid": "https://cdn.gomister.com/file/cdn-common/teams/2.png?version=20231117",
        "Girona": "https://cdn.gomister.com/file/cdn-common/teams/222.png?version=20231117",
        "Osasuna": "https://cdn.gomister.com/file/cdn-common/teams/50.png?version=20231117",
        "Athletic Club": "https://cdn.gomister.com/file/cdn-common/teams/1.png?version=20231117",
        "Valencia": "https://cdn.gomister.com/file/cdn-common/teams/19.png?version=20231117",
        "Granada": "https://cdn.gomister.com/file/cdn-common/teams/10.png?version=20231117",
        "Getafe": "https://cdn.gomister.com/file/cdn-common/teams/9.png?version=20231117",
        "Villarreal": "https://cdn.gomister.com/file/cdn-common/teams/20.png?version=20231117",
        "Las Palmas": "https://cdn.gomister.com/file/cdn-common/teams/11.png?version=20231117",
        "Mallorca": "https://cdn.gomister.com/file/cdn-common/teams/408.png?version=20231117",
        "Rayo Vallecano": "https://cdn.gomister.com/file/cdn-common/teams/14.png?version=20231117",
        "Barcelona": "https://cdn.gomister.com/file/cdn-common/teams/3.png?version=20231117",
        "Celta de Vigo": "https://cdn.gomister.com/file/cdn-common/teams/5.png?version=20231117",
        "Cádiz": "https://cdn.gomister.com/file/cdn-common/teams/499.png?version=20231117",
        "Alavés": "https://cdn.gomister.com/file/cdn-common/teams/48.png?version=20231117",
        "Almería": "https://cdn.gomister.com/file/cdn-common/teams/21.png?version=20231117",
        "Sevilla": "https://cdn.gomister.com/file/cdn-common/teams/17.png?version=20231117",
        "Betis": "https://cdn.gomister.com/file/cdn-common/teams/4.png?version=20231117",
        }

        # Crear un diseño de cuadrícula
        layout = QGridLayout(self)
        # Establecer el tamaño máximo de la segunda columna
        layout.setColumnStretch(1, 1)
        layout.setColumnStretch(2, 1)

        # Variables para almacenar la carpeta y la ruta seleccionadas
        self.selected_folder = ""
        self.selected_path = ""
        
        self.driver = None

        ### SELECCIONAR JORNADA INPUT ####################################################
        # INPUT NÚMERO JORNADA 
        label_number = QLabel("Jornada a scrapear:")
        layout.addWidget(label_number, 0, 0)
        # Estilos 
        self.number_input = QSpinBox(self)
        self.number_input.setMinimum(11)  # Establecer el valor mínimo (jornada 1)
        self.number_input.setMaximum(38)  # Establecer el valor máximo (Jornada 36)
        self.number_input.setSingleStep(2)  # Establecer el paso
        self.number_input.setMaximumSize(38, 20)
        self.number_input.setMinimumSize(38, 20)
        # Aliniación
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
        # Alineación
        layout.addWidget(self.text_input, 2, 1)
        # Estilos 
        self.text_input.setMinimumWidth(350)
        

        # BOTÓN PARA SELECCIONAR CARPETA
        select_folder_button = QPushButton("Seleccionar Carpeta")
        select_folder_button.clicked.connect(self.select_folder)
        # Alineación  
        layout.addWidget(select_folder_button, 3, 1, alignment=Qt.AlignmentFlag.AlignRight)
        # Estilos 
        select_folder_button.setMinimumWidth(140)

        #------- GAP vacio -----------------------------------------
        empty_widget = QWidget()
        empty_widget.setFixedHeight(10)  # Tamaño del gap (10 px)
        layout.addWidget(empty_widget, 4, 0)
        #-----------------------------------------------------------


        ###  BOTÓN PARA INICIAR SCRAPER  ################################################
        # Crear un botón llamado "Scrapear"
        scrape_button = QPushButton("Scrapear")

        # Conectar la señal clicked del botón a la función iniciar_scrapear_thread
        scrape_button.clicked.connect(self.iniciar_scrapear_thread)

        # Alineación 
        layout.addWidget(scrape_button, 5, 0)
        # Estilos
        self.number_input.setMaximumSize(38, 20)


        ###  VENTANA OUTPUT SCRAPER  ####################################################
        # Crear un QTextEdit para la salida
        self.output_textedit = QTextEdit(self)
        layout.addWidget(self.output_textedit, 6, 0, 2, 0)  # row, column, rowSpan, columnSpan


        ###  ESTABLECER DISEÑO DE LA VENTANA  ###########################################
        self.setMinimumSize(500, 500) # Configurar el tamaño mínimo de la ventana
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

    def actualizar_version(self,version):
      for equipo, url in self.teams_data.items():
        # Dividir la URL en base al signo de interrogación
        partes = url.split('?')
        
        # Verificar si hay una parte después del signo de interrogación y actualizar la versión
        if len(partes) > 1:
            partes[1] = f"version={version}"
            
            # Volver a unir las partes para formar la URL actualizada
            nueva_url = '?'.join(partes)
            
            # Actualizar la URL en el diccionario
            self.teams_data[equipo] = nueva_url

        #print(version)
        #print("nuevaaaa url-->  ",nueva_url)

    def obtener_valor_por_etiqueta(self,label_deseado):
        # Función para obtener el valor basado en la etiqueta
        elemento = self.driver.find_element(By.XPATH, f"//div[@class='item']//div[@class='label' and text()='{label_deseado}']/following-sibling::div[@class='value']")
        valor = elemento.text
        return valor

    def extraer_info_jugador(self,jornada_absolute,jornada_a_scrapear):
        
        nombre = self.driver.find_element(By.XPATH, "/html/body/div[6]/div[3]/div[2]/div[1]/div/div[1]/div[2]")
        apellido = self.driver.find_element(By.XPATH, " /html/body/div[6]/div[3]/div[2]/div[1]/div/div[1]/div[3]")
        valorS= self.driver.find_element(By.XPATH,'/html/body/div[6]/div[3]/div[2]/div[2]/div/div/div[1]/div[2]')
        valor=valorS.text

        media_puntos_local = self.obtener_valor_por_etiqueta("Media en casa")
        media_puntos_visitante = self.obtener_valor_por_etiqueta("Media fuera")
        try:
            edad = self.obtener_valor_por_etiqueta("Edad")
            altura = self.obtener_valor_por_etiqueta("Altura")
            peso = self.obtener_valor_por_etiqueta("Peso")
        except:
            edad = None
            altura = None
            peso = None
                
        if peso == "kg":
            peso = None

            
        #### OBTENER EQUIPO JUGADOR ####

        # Obtener src del equipo
        team_logo_element = self.driver.find_element(By.XPATH, "/html/body/div[6]/div[3]/div[2]/div[1]/div/div[1]/div[1]/a/img")
        image_url = team_logo_element.get_attribute("src")

        # Comparar la URL de la imagen con las URLs en teams_data
        equipo = None
        proximo_rival=None
        local= False
        for equipo_nombre, equipo_url in self.teams_data.items():
            if image_url == equipo_url:
                equipo = equipo_nombre
                
                #### OBTENER RESULTADO ÚLTIMO PARTIDO ####
                try:
                    divpartido = self.driver.find_element(By.XPATH, "/html/body/div[6]/div[3]/div[3]/div[1]/div[3]/div")
                except:
                    divpartido = self.driver.find_element(By.XPATH, "/html/body/div[6]/div[3]/div[3]/div/div[2]/div")
                
                # Encuentra el div del partido
                item_elements = divpartido.find_elements(By.CLASS_NAME, 'item')
            
                # Encuentra las imágenes dentro del div partido
                img_elements = item_elements[0].find_elements(By.CLASS_NAME, 'team-logo')

                # Guarda las src de las imágenes en variables
                if len(img_elements) >= 2:
                    src_img1 = img_elements[0].get_attribute('src')
                    src_img2 = img_elements[1].get_attribute('src')
                    if src_img1 == image_url:
                        local = True
                        for equipo_nombre, equipo_url in self.teams_data.items():
                            if src_img2 == equipo_url:
                                proximo_rival=equipo_nombre
                    else:
                        local=False
                        for equipo_nombre, equipo_url in self.teams_data.items():
                            if src_img1 == equipo_url:
                                proximo_rival=equipo_nombre
                else:
                    print("No se encontro el próximo partido")
                

        #### OBTENER POSICIÓN DEL JUGADOR ####
        elemento = self.driver.find_element(By.XPATH, '//i[contains(@class, "pos-")]')
        # Obtener el valor del atributo class
        clases = elemento.get_attribute("class").split()

        # Determinar la posición
        posicion = None
        for clase in clases:
            if clase.startswith("pos-") and "pos-big" in clases:
                if clase == "pos-1":
                    posicion = "PT"
                elif clase == "pos-2":
                    posicion = "DF"
                elif clase == "pos-3":
                    posicion = "MC"
                elif clase == "pos-4":
                    posicion = "DL"
                break

            
        #### OBTENER PUNTOS DEL JUGADOR ####
        # Encontrar jornada 
        elementos_principales = self.driver.find_elements(By.CLASS_NAME, 'btn-player-gw')

        # Iterar sobre cada elemento encontrado
        subelemento_gw=None
        jornada_name=None
        for elemento_principal in elementos_principales:
            # Encontrar subelemento con la clase 'gw' dentro de cada elemento principal
            subelemento_gw = elemento_principal.find_element(By.CLASS_NAME, 'gw')

            # Verificar si el texto coincide con el de la jornada
            if subelemento_gw.text == jornada_a_scrapear:
                jornada_name = subelemento_gw.text
                break             
        
        if jornada_name ==jornada_absolute:
            # Encontrar jornada en la web con otro elemennto como referencia
            localizador = self.driver.find_element(By.XPATH, "//h4[text()='Valor']")
            self.driver.execute_script("arguments[0].scrollIntoView(true);", localizador)   
            
            time.sleep(1)
            
            try:
                subelemento_gw.click()
            except:
                elemento_principal.click()
            
            time.sleep(2)
            
            try:
                # PUNTOS MISTER FANTASY
                main_provider = self.driver.find_element(By.CLASS_NAME, 'main-provider')
                points_element = main_provider.find_element(By.CLASS_NAME, 'points')
                final_points = points_element.get_attribute('data-points')

                # PUNTOS AS, MARCA Y MUNDO DEPORTIVO 
                providers_div = self.driver.find_element(By.CLASS_NAME, "providers")
                li_elements = providers_div.find_elements(By.TAG_NAME, "li")

                points_array = []

                for li_element in li_elements:

                    points_div = li_element.find_element(By.CLASS_NAME, "points")
                    points_value = points_div.text
                    points_array.append(points_value)

                as_points=points_array[0]
                marca_points=points_array[1]
                mundo_deportivo_points=points_array[2]
                
                #### OBTENER PARTIDO ANTERIOR ####
                # Encontrar el div principal con la clase "player-match"
                player_match_div = self.driver.find_element(By.CLASS_NAME, "player-match")

                # Encontrar los subelementos dentro del div principal
                team_1 = player_match_div.find_element(By.CLASS_NAME, "left").find_element(By.CLASS_NAME, "team").text
                goals_team_1 = [int(goal.text) for goal in player_match_div.find_elements(By.CLASS_NAME, "goals")][0]  
                goals_team_2 = [int(goal.text) for goal in player_match_div.find_elements(By.CLASS_NAME, "goals")][1]  
                team_2 = player_match_div.find_element(By.CLASS_NAME, "right").find_element(By.CLASS_NAME, "team").text

                if team_1 == equipo:
                    ultimo_rival=team_2

                    if goals_team_1 > goals_team_2:
                        result = "Win"
                    elif goals_team_1 < goals_team_2:  
                        result = "Loss"
                    else:
                        result = "Draw"
                else:
                    ultimo_rival=team_1

                    if goals_team_1 > goals_team_2:
                        result = "Loss"
                    elif goals_team_1 < goals_team_2:  
                        result = "Win"
                    else:
                        result = "Draw"

                self.driver.back()
                
            except:
                final_points=None
                as_points=None
                marca_points=None
                mundo_deportivo_points=None
                ultimo_rival=None
                result=None
                
        else:
            final_points="NA"
            as_points="NA"
            marca_points="NA"
            mundo_deportivo_points="NA"
            ultimo_rival="NA"
            result="NA"
        

        #### IMPRIMIR TODOS LOS DATOS ####
        self.output_textedit.append("_____________________________________________")
        self.output_textedit.append(f"- {nombre.text}, {apellido.text}")
        self.output_textedit.append(f"Valor: {valor}")
        self.output_textedit.append(f"Posición: {posicion}")
        self.output_textedit.append(f"Equipo: {equipo}")
            
        self.output_textedit.append("- - - - - - - - - - - - - - - - - - - - - - - - - -")

        self.output_textedit.append(f"Puntuación Fantasy: {final_points}")
        self.output_textedit.append(f"Puntuación Fantasy: {as_points}")
        self.output_textedit.append(f"Puntuación Marca: {marca_points}")
        self.output_textedit.append(f"Puntuación Mundo Deportivo: {mundo_deportivo_points}")
        
        self.output_textedit.append("- - - - - - - - - - - - - - - - - - - - - - - - - -")
            
        self.output_textedit.append(f"Último rival: {ultimo_rival}")
        self.output_textedit.append(f"Resultado del partido: {result}")

        self.output_textedit.append(f"Próximo rival: {proximo_rival}")
        self.output_textedit.append(f"Próximo partido es local: {local}")
        self.output_textedit.append(f"Media en casa: {media_puntos_local}")
        self.output_textedit.append(f"Media fuera: {media_puntos_visitante}")
        self.output_textedit.append(f"Edad: {edad}")
        self.output_textedit.append(f"Altura: {altura}")
        self.output_textedit.append(f"Peso: {peso}")

        """
        nombre_archivo="output_scraper/"+jornada_absolute+".xlsx"
        jugador = nombre.text + " " + apellido.text

        # Crear un excell o cargar uno existente
        try:
            wb = openpyxl.load_workbook(nombre_archivo)
        except FileNotFoundError:
            wb = openpyxl.Workbook()
            sheet = wb.active
            encabezado = ["Jugador", "Valor", "Posición", "Equipo", "Puntuación Fantasy", "Puntuación AS", "Puntuación Marca", "Puntuación Mundo Deportivo","Último rival","Resultado del partido", "Próximo rival", "Próximo partido es local", "Media en casa", "Media fuera", "Edad", "Altura", "Peso"]
            sheet.append(encabezado)

        # Seleccionar la hoja activa
        sheet = wb.active
            
        # Lista de variables a almacenar
        nueva_fila = [jugador, valor, posicion, equipo, final_points, as_points, marca_points, mundo_deportivo_points,ultimo_rival,result,proximo_rival, local, media_puntos_local, media_puntos_visitante, edad, altura, peso]
        
        # Escribir la nueva fila en la hoja de cálculo
        sheet.append(nueva_fila)

        # Guardar el archivo Excel
        wb.save(nombre_archivo)
        """


    def iniciar_scrapear_thread(self):  
        # Crear un hilo y ejecutar la función en segundo plano
        thread = threading.Thread(target=self.scrapear_funcion)
        thread.start()

    def scrapear_funcion(self):
        self.output_textedit.append("Starting scraper...")

        # GESTIÓN DEL INPUT DEL USUARIO
        # Obtener el valor de la jornada desde el QSpinBox
        numero_jornada = str(self.number_input.value())

        # Concatena 'J' delante del número
        jornada_a_scrapear = 'J' + numero_jornada

        # Mostrar el valor en el QTextEdit
        self.output_textedit.append(f"Jornada seleccionada: {jornada_a_scrapear}")

        ruta_output = self.text_input.text()
        # Hacer lo que necesites con la ruta de salida
        self.output_textedit.append(f"Ruta para la salida del scraper selecionada: {ruta_output}")
        self.output_textedit.append(f"________________________________________________________________________________________")

        if ruta_output=="":
            output_textedit = self.output_textedit
            color_rojo = QColor(255, 0, 0)  # Valores RGB para rojo
            formato_rojo = QTextCharFormat()
            formato_rojo.setForeground(color_rojo)
            output_textedit.mergeCurrentCharFormat(formato_rojo)
            output_textedit.insertPlainText("\n¡La jornada no está inicializada!, Configúrala antes de empezar a scrapear")
            formato_negro = QTextCharFormat()
            formato_negro.setForeground(QColor(0, 0, 0))
            output_textedit.mergeCurrentCharFormat(formato_negro)
            self.output_textedit.append(f"________________________________________________________________________________________")
            return
        
        self.driver = webdriver.Chrome()

        # Navega a la página web que deseas hacer scraping
        self.driver.get("https://mister.mundodeportivo.com/new-onboarding/#market")

        # Espera a que se cargue la página
        self.driver.implicitly_wait(15)

        # Encuentra el botón de "Consentir" 
        button = self.driver.find_element(By.XPATH, '//*[@id="didomi-notice-agree-button"]')
        # Haz clic en el botón de "Consentir" 
        button.click()

        # Encuentra el botón de "Siguinete" 
        button = self.driver.find_element(By.XPATH, '//*[@id="app"]/div/div[2]/div[2]/button')
        # Haz clic en el botón de "Siguiente" 
        button.click()
        button.click()
        button.click()
        button.click()

        # Encuentra el botón de "sing con gmail" 
        button = self.driver.find_element(By.XPATH, '//*[@id="app"]/div/div[2]/div/button[3]')
        button.click()

        # Localiza el elemento del input gmail
        inputgmail = self.driver.find_element(By.XPATH, '//*[@id="email"]')

        # Borra cualquier contenido existente en la caja de texto (opcional)
        inputgmail.clear()

        # Ingresa texto en la caja de texto
        inputgmail.send_keys("m31_grupo6@outlook.com")

        # Localiza el elemento del input gmail
        inputpsw = self.driver.find_element(By.XPATH, '//*[@id="app"]/div/div[2]/div/form/div[2]/input')

        # Borra cualquier contenido existente en la caja de texto (opcional)
        inputpsw.clear()

        # Ingresa texto en la caja de texto
        inputpsw.send_keys("Chocoflakes2")

        # Encuentra el botón de "sing con gmail" 
        button = self.driver.find_element(By.XPATH, '//*[@id="app"]/div/div[2]/div/form/div[3]/button')
        button.click()

        time.sleep(5)

        # Espera a que se cargue la página
        self.driver.implicitly_wait(10)

        #Hacer click en el btn Jugadores con la función click_mas() para manejar errores generados por anuncios intrusiovos
        self.click_mas()

        # Pinchar en el botón "Jugaodres" para acceder al listado de jugadores 
        jugadoresbtn = self.driver.find_element(By.XPATH, '//*[@id="content"]/div[2]/div[1]/button[2]')

        try:
            jugadoresbtn.click()
        except (ElementNotInteractableException, NoSuchElementException):
            # Maneja la excepción y espera antes de intentar nuevamente
            self.output_textedit.append("Anuncio detectado, reiniciando driver...")
            self.driver.refresh()
            time.sleep(3)
            self.click_mas()
            time.sleep(3)
            try:
                jugadoresbtn = self.driver.find_element(By.XPATH, '//*[@id="content"]/div[2]/div[1]/button[2]')
                jugadoresbtn.click()
            except: 
                self.output_textedit.append("Reinicia el script :(")
                sys.exit()

        pag=2
        index=0
        absolute=1
        jornada_absolute=""
        while True:

            # Encontrar todos los elementos li
            elementos_lis = self.driver.find_elements(By.XPATH, "/html/body/div[6]/div[3]/div[3]/ul/li")

            # Longitud de la lista de elementos encontrados
            length=len(elementos_lis)

            while index < length:
                # Encontrar todos los elementos li
                elementos_li = self.driver.find_elements(By.XPATH, "/html/body/div[6]/div[3]/div[3]/ul/li")
                elementos_li[index].click()

                time.sleep(1)
                
                try:
                    team_logo_element = self.driver.find_element(By.XPATH, "/html/body/div[6]/div[3]/div[2]/div[1]/div/div[1]/div[1]/a/img")
                except:
                    try:
                        team_logo_element = self.driver.find_element(By.XPATH, "/html/body/div[6]/div[3]/div[3]/div/div[3]/div/div[1]/div[2]/img[1]")
                    except:
                        team_logo_element = self.driver.find_element(By.XPATH, "/html/body/div[6]/div[3]/div[3]/div/div[3]/div/div[1]/div[2]/img[2]")
                
                image_url = team_logo_element.get_attribute("src")
                # Dividir la URL utilizando el signo de igual como delimitador
                parts = image_url.split('=')
                # El valor de version está en la segunda parte después del =
                version = parts[1]
                self.actualizar_version(version)
                
                if absolute == 1:
                    # Encontrar jornada 
                    elementos_principales = self.driver.find_elements(By.CLASS_NAME, 'btn-player-gw')

                    # Iterar sobre cada elemento encontrado
                    subelemento_gw=None
                    for elemento_principal in elementos_principales:
                        # Encontrar subelemento con la clase 'gw' dentro de cada elemento principal
                        subelemento_gw = elemento_principal.find_element(By.CLASS_NAME, 'gw')
                        
                        # Verificar si el texto coincide con el de la jornada
                        if subelemento_gw.text == jornada_a_scrapear:
                            jornada_absolute = subelemento_gw.text
                            break   
                absolute = 2
                
                self.extraer_info_jugador(jornada_absolute,jornada_a_scrapear)
                
                #Retroceder página
                self.driver.back()
                time.sleep(1)
                elementos_li = self.driver.find_elements(By.XPATH, "/html/body/div[6]/div[3]/div[3]/ul/li")
                if index == 0:
                    self.driver.execute_script("arguments[0].scrollIntoView(true);", elementos_li[index])
                else:
                    self.driver.execute_script("arguments[0].scrollIntoView(true);", elementos_li[index-1])
                time.sleep(1)
                index += 1

            #Pulsar Ver más
            try:
                ver_mas = self.driver.find_element(By.XPATH, '/html/body/div[6]/div[3]/div[3]/div[1]/button')
                ver_mas.click()
                time.sleep(4)
            except:
                break

            #Jugador cambio de pagina
            elementos_li = self.driver.find_elements(By.XPATH, "/html/body/div[6]/div[3]/div[3]/ul/li")
            elementos_li[index].click()
            time.sleep(2)
            self.extraer_info_jugador(jornada_absolute,jornada_a_scrapear)
            self.driver.back()
            
            self.output_textedit.append("____________________________________")
            self.output_textedit.append("------------------------------------")
            self.output_textedit.append(f"Siguiente página... ({pag})")
            self.output_textedit.append("------------------------------------")
            
            index=1
            pag+=1

        self.driver.quit()    
        self.output_textedit.append("Todos los jugadores scrapeados")

if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    window = SimpleWindow()
    window.show()
    sys.exit(app.exec())