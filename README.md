# Aplicación Médica de Citas

Este proyecto es una aplicación de escritorio que permite a los usuarios agendar, ver, modificar y cancelar citas médicas. La aplicación está desarrollada con Python utilizando la librería Tkinter para la interfaz gráfica de usuario y SQLite para la base de datos.

## Funcionalidades Implementadas

1. **Inicio de sesión:**
   - Los usuarios pueden iniciar sesión como "Paciente" o "Administrador".
   - Si el usuario no está registrado, la aplicación lo agrega automáticamente.

2. **Panel de Administrador:**
   - Ver todas las citas agendadas.
   - Modificar o cancelar citas agendadas.

3. **Panel de Paciente:**
   - Agendar citas médicas.
   - Ver sus citas agendadas.
   - Modificar o cancelar sus propias citas.

4. **Base de Datos:**
   - Se utiliza SQLite para almacenar usuarios, médicos y citas.
   - Las tablas incluyen información sobre los usuarios, médicos y citas médicas.

5. **Interfaz Gráfica:**
   - La interfaz es completamente gráfica, con ventanas emergentes para la visualización de citas y la gestión de ellas.
   - Se utiliza un calendario para seleccionar la fecha de las citas.

## Tecnologías Utilizadas

- **Python 3**: Lenguaje de programación utilizado para el desarrollo.
- **Tkinter**: Librería para la creación de la interfaz gráfica de usuario (GUI).
- **SQLite**: Base de datos utilizada para almacenar usuarios, médicos y citas.
- **tkcalendar**: Librería para integrar un calendario en la interfaz de usuario.

## Cómo Configurar y Ejecutar el Proyecto

1. **Requisitos:**
   - Asegúrate de tener Python 3 instalado en tu sistema.
   - Instala las dependencias necesarias ejecutando el siguiente comando:

   ```bash
   pip install tk tkcalendar sqlite3
