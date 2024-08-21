from behave import given, when, then
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from PIL import Image
from PIL import ImageGrab
import os
import time

SCREENSHOT_PATH = os.path.join(os.getcwd(), "screenshot.png")
SCREENSHOT_PATH2 = os.path.join(os.getcwd(), "screenshot2.png")

@given('I am on the login page')
def step_impl(context):
    context.driver = webdriver.Chrome()
    context.driver.get("C:/Users/User/Desktop/CUcumberPy/app/report.html")
    context.driver.save_screenshot(SCREENSHOT_PATH2)

@when('I enter a valid username and password')
def step_impl(context):
    context.driver.find_element(By.NAME, "username").send_keys("valid_user")
    context.driver.find_element(By.NAME, "password").send_keys("valid_pass")

@when('I enter an invalid username and password')
def step_impl(context):
    context.driver.find_element(By.NAME, "username").send_keys("invalid_user")
    context.driver.find_element(By.NAME, "password").send_keys("invalid_pass")

@when('I click the login button')
def step_impl(context):
    context.driver.find_element(By.NAME, "login").click()
    context.driver.save_screenshot(SCREENSHOT_PATH)

@then('I should be redirected to the dashboard')
def step_impl(context):
    urlfin=context.driver.current_url
    if( urlfin=="example.com/dashboard"):
        create_pdf(context,"passed")
    else:
        create_pdf(context,"failed")
    print(urlfin)
    assert context.driver.current_url == "example.com/dashboard"  # Cambia esto por la URL real
    context.driver.quit()

@then('I should see an error message')
def step_impl(context):
    error_message = context.driver.find_element(By.ID, "error").text
    
    if(error_message == "Invalid credentials"):
        create_pdf(context,"passed")
    else:
        create_pdf(context,"failed")
    
    assert error_message == "Invalid credentials"  # Cambia esto según el mensaje real
    context.driver.quit()








def create_pdf(context, pas):
    # Obtén la fecha y hora actual en formato de cadena
    timestamp = time.strftime("%Y-%m-%d_%H-%M-%S")

    # Construye la ruta del archivo con la marca de tiempo
    file_path = f"C:/Users/User/Desktop/CUcumberPy/report/results_{timestamp}.pdf"

    c = canvas.Canvas(file_path, pagesize=letter)
    width, height = letter

    # Título
    c.setFont("Helvetica", 14)
    c.drawString(50, height - 50, "Resultados de las Pruebas")

    # Resultado de la prueba con múltiples líneas de texto
    result_text = f"Feature: {context.feature.name}\nScenario: {context.scenario.name}\n"
    result_text += f"Status: {'Passed' if pas == 'passed' else 'Failed'}"
    
    text_object = c.beginText(50, height - 100)
    text_object.setFont("Helvetica", 10)
    for line in result_text.split('\n'):
        text_object.textLine(line)
    c.drawText(text_object)
    
    y_position = text_object.getY() - 20  # Ajusta la posición vertical inicial para el texto y la imagen

    # Añadir captura de pantalla "Antes de la ejecución" al PDF
    c.setFont("Helvetica", 10)
    c.drawString(50, y_position, "Antes de la ejecución")
    y_position -= 15  # Espacio entre el texto y la imagen

    if os.path.exists(SCREENSHOT_PATH2):
        try:
            image = Image.open(SCREENSHOT_PATH2)
            image_width, image_height = image.size
            
            # Ajusta el tamaño de la imagen para que se ajuste a la página
            max_width = width - 200  # Ancho máximo de la imagen en la página
            max_height = height - 250  # Alto máximo de la imagen en la página
            
            # Mantén la proporción de la imagen
            if image_width > max_width or image_height > max_height:
                aspect_ratio = image_width / image_height
                if image_width > max_width:
                    image_width = max_width
                    image_height = image_width / aspect_ratio
                if image_height > max_height:
                    image_height = max_height
                    image_width = image_height * aspect_ratio
            
            # Dibuja la imagen en el PDF
            c.drawImage(SCREENSHOT_PATH2, 50, y_position - image_height, width=image_width, height=image_height)
            y_position -= image_height + 20  # Actualiza la posición vertical después de la imagen
        except Exception as e:
            print(f"Error al abrir la imagen para el PDF: {e}")

    # Añadir captura de pantalla "Después de la ejecución" al PDF
    c.setFont("Helvetica", 10)
    c.drawString(50, y_position, "Después de la ejecución")
    y_position -= 15  # Espacio entre el texto y la imagen

    if os.path.exists(SCREENSHOT_PATH):
        try:
            image = Image.open(SCREENSHOT_PATH)
            image_width, image_height = image.size
            
            # Ajusta el tamaño de la imagen para que se ajuste a la página
            max_width = width - 200  # Ancho máximo de la imagen en la página
            max_height = height - 250  # Alto máximo de la imagen en la página
            
            # Mantén la proporción de la imagen
            if image_width > max_width or image_height > max_height:
                aspect_ratio = image_width / image_height
                if image_width > max_width:
                    image_width = max_width
                    image_height = image_width / aspect_ratio
                if image_height > max_height:
                    image_height = max_height
                    image_width = image_height * aspect_ratio
            
            # Dibuja la imagen en el PDF
            c.drawImage(SCREENSHOT_PATH, 50, y_position - image_height, width=image_width, height=image_height)
        except Exception as e:
            print(f"Error al abrir la imagen para el PDF: {e}")

    c.save()