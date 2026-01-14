# 📚 Biblioteca Django

Aplicación web desarrollada con **Python y Django** para la gestión integral de una biblioteca.
Permite administrar libros, autores, categorías, realizar búsquedas avanzadas y visualizar estadísticas básicas.

Este proyecto fue desarrollado como parte de una actividad académica y forma parte de mi **portafolio profesional**.

---

## 🚀 Funcionalidades

- 📖 CRUD completo de libros
- ✍️ Gestión de autores
- 🗂️ Organización por categorías
- 🔎 Búsqueda avanzada de libros
- 📊 Visualización de estadísticas
- 🖼️ Manejo de imágenes (portadas y autores)
- 🎨 Interfaz web responsive

---

## 🛠️ Tecnologías utilizadas

- **Python 3**
- **Django**
- **HTML5**
- **CSS3**
- **JavaScript**
- **SQLite**
- **Git & GitHub**

---

## 📂 Estructura del proyecto

biblioteca-django/
│── biblioteca_project/
│── libros/
│── templates/
│── static/
│── media/
│── manage.py
│── requirements.txt
│── .env.example
│── README.md

yaml
Copiar código

---

## ⚙️ Instalación y configuración

### 1️⃣ Clonar el repositorio
```bash
git clone https://github.com/Pirra1234/biblioteca-django.git
cd biblioteca-django
2️⃣ Crear entorno virtual
bash
Copiar código
python -m venv venv
source venv/bin/activate   # Linux / Mac
venv\Scripts\activate      # Windows
3️⃣ Instalar dependencias
bash
Copiar código
pip install -r requirements.txt
4️⃣ Variables de entorno
Copia el archivo de ejemplo:

bash
Copiar código
cp .env.example .env
Configura tus variables dentro del archivo .env.

⚠️ Nota: El archivo .env no se sube al repositorio por seguridad.

▶️ Ejecutar el proyecto
bash
Copiar código
python manage.py migrate
python manage.py runserver
Accede desde el navegador:

cpp
Copiar código
http://127.0.0.1:8000/
📌 Estado del proyecto
✅ Funcional
🛠️ En constante mejora
📈 Escalable (usuarios, autenticación, API REST)

👨‍💻 Autor
Santiago Castillo Tadeo
Estudiante de Ingeniería en Gestión y Desarrollo de Software
Interés en desarrollo web y ciberseguridad

GitHub: https://github.com/Pirra1234

Portafolio: https://pirra1234.github.io

