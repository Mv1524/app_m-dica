import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3
from tkcalendar import Calendar

class Aplicacion:
    def __init__(self, root):
        self.root = root
        self.root.title("Aplicación Médica")
        self.root.geometry("600x400")

        # Crear base de datos y tablas si no existen
        self.conectar_db()

        # Iniciar la interfaz de usuario
        self.iniciar_interfaz()

    def conectar_db(self):
        conn = sqlite3.connect("citas_medicas.db")
        cursor = conn.cursor()

        # Crear tablas si no existen
        cursor.execute('''CREATE TABLE IF NOT EXISTS usuarios (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            nombre TEXT UNIQUE,
                            tipo TEXT)''')

        cursor.execute('''CREATE TABLE IF NOT EXISTS medicos (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            nombre TEXT,
                            especialidad TEXT)''')

        cursor.execute('''CREATE TABLE IF NOT EXISTS citas (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            usuario TEXT,
                            medico TEXT,
                            fecha TEXT,
                            hora TEXT)''')

        conn.commit()
        conn.close()

        # Actualizar base de datos para agregar columna 'usuario' si no existe
        self.actualizar_base_datos()

    def actualizar_base_datos(self):
        conn = sqlite3.connect("citas_medicas.db")
        cursor = conn.cursor()

        # Verificar si la columna 'usuario' existe en la tabla 'citas'
        cursor.execute("PRAGMA table_info(citas)")
        columnas = [col[1] for col in cursor.fetchall()]
        
        if 'usuario' not in columnas:
            # Si no existe, agregar la columna 'usuario'
            cursor.execute("ALTER TABLE citas ADD COLUMN usuario TEXT")
            print("Columna 'usuario' agregada exitosamente.")
        else:
            print("La columna 'usuario' ya existe.")

        conn.commit()
        conn.close()

    def iniciar_interfaz(self):
        # Panel de inicio
        self.panel_inicio = tk.Frame(self.root)
        self.panel_inicio.pack(pady=20)

        tk.Label(self.panel_inicio, text="Iniciar sesión", font=("Arial", 16)).pack(pady=10)

        tk.Label(self.panel_inicio, text="Usuario:", font=("Arial", 12)).pack(pady=5)
        self.usuario_entry = tk.Entry(self.panel_inicio, font=("Arial", 12))
        self.usuario_entry.pack(pady=5)

        tk.Label(self.panel_inicio, text="Tipo de usuario:", font=("Arial", 12)).pack(pady=5)
        self.tipo_usuario_var = tk.StringVar()
        self.tipo_usuario_var.set("Paciente")
        tipos = ["Paciente", "Administrador"]
        tk.OptionMenu(self.panel_inicio, self.tipo_usuario_var, *tipos).pack(pady=5)

        tk.Button(self.panel_inicio, text="Iniciar sesión", bg="#4682B4", fg="white", font=("Arial", 12), command=self.iniciar_sesion).pack(pady=10)

    def iniciar_sesion(self):
        usuario = self.usuario_entry.get()
        tipo = self.tipo_usuario_var.get()

        if not usuario:
            messagebox.showerror("Error", "Por favor ingrese un nombre de usuario.")
            return

        self.registrar_usuario_si_no_existe(usuario, tipo)

        if tipo == "Administrador":
            self.abrir_panel_administrador()
        else:
            self.abrir_panel_paciente(usuario)

    def registrar_usuario_si_no_existe(self, usuario, tipo):
        conn = sqlite3.connect("citas_medicas.db")
        cursor = conn.cursor()
        cursor.execute("INSERT OR IGNORE INTO usuarios (nombre, tipo) VALUES (?, ?)", (usuario, tipo))
        conn.commit()
        conn.close()

    def regresar(self, panel_actual):
        panel_actual.destroy()  # Destruir el panel actual
        self.iniciar_interfaz()  # Mostrar el panel de inicio nuevamente

    def abrir_panel_administrador(self):
        self.panel_inicio.destroy()

        panel_admin = tk.Frame(self.root)
        panel_admin.pack(pady=20)

        tk.Label(panel_admin, text="Panel Administrador", font=("Arial", 16)).pack(pady=10)

        tk.Button(panel_admin, text="Ver Citas Agendadas", bg="#4682B4", fg="white", font=("Arial", 12), command=self.ver_citas_agendadas).pack(pady=10)
        tk.Button(panel_admin, text="Regresar", bg="gray", fg="white", font=("Arial", 12), command=lambda: self.regresar(panel_admin)).pack(pady=10)

    def abrir_panel_paciente(self, usuario):
        self.panel_inicio.destroy()

        panel_paciente = tk.Frame(self.root)
        panel_paciente.pack(pady=20)

        tk.Label(panel_paciente, text="Panel Paciente", font=("Arial", 16)).pack(pady=10)

        tk.Button(panel_paciente, text="Agendar Cita", bg="#4682B4", fg="white", font=("Arial", 12), command=lambda: self.agendar_cita(usuario)).pack(pady=10)
        tk.Button(panel_paciente, text="Ver Mis Citas", bg="#32CD32", fg="white", font=("Arial", 12), command=lambda: self.ver_mis_citas(usuario)).pack(pady=10)

    def agendar_cita(self, usuario):
        ventana = tk.Toplevel(self.root)
        ventana.title("Agendar Cita")
        ventana.geometry("500x400")

        tk.Label(ventana, text="Seleccionar Médico", font=("Arial", 12)).pack(pady=10)

        # Listado de médicos disponibles
        medicos = ["Dr. Juan Pérez", "Dr. Laura Gómez", "Dr. Carlos Díaz", "Dr. Trino Andrade", "Dr. Manuel Caicedo", "Dr. German Ruiz", "Dr. Fabiana León"]
        medicos_combo = tk.StringVar(value=medicos[0])
        tk.OptionMenu(ventana, medicos_combo, *medicos).pack(pady=10)

        tk.Label(ventana, text="Seleccionar Hora", font=("Arial", 12)).pack(pady=10)

        horas = ["06:00", "07:00", "08:00", "09:00", "10:00", "11:00", "12:00", "13:00", "14:00", "15:00", "16:00", "17:00", "18:00", "19:00"]
        horas_combo = tk.StringVar(value=horas[0])
        tk.OptionMenu(ventana, horas_combo, *horas).pack(pady=10)

        tk.Label(ventana, text="Fecha de la Cita", font=("Arial", 12)).pack(pady=10)

        # Agregar calendario
        cal = Calendar(ventana, selectmode='day', date_pattern='yyyy-mm-dd')
        cal.pack(pady=10)

        tk.Button(ventana, text="Guardar Cita", bg="green", fg="white", command=lambda: self.guardar_cita(usuario, medicos_combo.get(), horas_combo.get(), cal.get_date(), ventana)).pack(pady=10)
        tk.Button(ventana, text="Cancelar", bg="red", fg="white", command=ventana.destroy).pack(pady=10)

    def guardar_cita(self, usuario, medico, hora, fecha, ventana):
        if not medico or not hora or not fecha:
            messagebox.showerror("Error", "Por favor complete todos los campos.")
            return

        conn = sqlite3.connect("citas_medicas.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO citas (usuario, medico, fecha, hora) VALUES (?, ?, ?, ?)", (usuario, medico, fecha, hora))
        conn.commit()
        conn.close()

        messagebox.showinfo("Éxito", "Cita agendada correctamente.")
        ventana.destroy()

    def ver_mis_citas(self, usuario):
        ventana = tk.Toplevel(self.root)
        ventana.title("Mis Citas")
        ventana.geometry("500x400")

        tk.Label(ventana, text=f"Citas de {usuario}", font=("Arial", 14)).pack(pady=10)

        frame = tk.Frame(ventana)
        frame.pack(pady=10)

        tree = ttk.Treeview(frame, columns=("ID", "Médico", "Fecha", "Hora"), show="headings")
        for col in tree["columns"]:
            tree.heading(col, text=col)
        tree.pack()

        conn = sqlite3.connect("citas_medicas.db")
        cursor = conn.cursor()
        cursor.execute("SELECT id, medico, fecha, hora FROM citas WHERE usuario = ?", (usuario,))
        for fila in cursor.fetchall():
            tree.insert("", "end", values=fila)
        conn.close()

        tk.Button(ventana, text="Modificar Cita", bg="orange", fg="white", font=("Arial", 12), command=lambda: self.modificar_cita(tree)).pack(pady=10)
        tk.Button(ventana, text="Cancelar Cita", bg="red", fg="white", font=("Arial", 12), command=lambda: self.eliminar_cita(tree)).pack(pady=10)
        tk.Button(ventana, text="Regresar", bg="gray", fg="white", font=("Arial", 12), command=ventana.destroy).pack(pady=10)

    def modificar_cita(self, tree):
        selected_item = tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Por favor, selecciona una cita para modificar.")
            return

        cita_id = tree.item(selected_item)["values"][0]
        medico_actual = tree.item(selected_item)["values"][1]
        fecha_actual = tree.item(selected_item)["values"][2]
        hora_actual = tree.item(selected_item)["values"][3]

        # Crear ventana para modificar cita
        ventana_modificar = tk.Toplevel(self.root)
        ventana_modificar.title("Modificar Cita")
        ventana_modificar.geometry("500x400")

        tk.Label(ventana_modificar, text="Seleccionar Médico", font=("Arial", 12)).pack(pady=10)

        # Listado de médicos disponibles
        medicos = ["Dr. Juan Pérez", "Dr. Laura Gómez", "Dr. Carlos Díaz", "Dr. Trino Andrade", "Dr. Manuel Caicedo", "Dr. German Ruiz", "Dr. Fabiana León"]
        medicos_combo = tk.StringVar(value=medico_actual)
        tk.OptionMenu(ventana_modificar, medicos_combo, *medicos).pack(pady=10)

        tk.Label(ventana_modificar, text="Seleccionar Hora", font=("Arial", 12)).pack(pady=10)

        horas = ["06:00", "07:00", "08:00", "09:00", "10:00", "11:00", "12:00", "13:00", "14:00", "15:00", "16:00", "17:00", "18:00", "19:00"]
        horas_combo = tk.StringVar(value=hora_actual)
        tk.OptionMenu(ventana_modificar, horas_combo, *horas).pack(pady=10)

        tk.Label(ventana_modificar, text="Fecha de la Cita", font=("Arial", 12)).pack(pady=10)

        # Agregar calendario
        cal = Calendar(ventana_modificar, selectmode='day', date_pattern='yyyy-mm-dd', date=fecha_actual)
        cal.pack(pady=10)

        tk.Button(ventana_modificar, text="Guardar Cambios", bg="green", fg="white", command=lambda: self.guardar_cambios(cita_id, medicos_combo.get(), horas_combo.get(), cal.get_date(), ventana_modificar)).pack(pady=10)
        tk.Button(ventana_modificar, text="Cancelar", bg="red", fg="white", command=ventana_modificar.destroy).pack(pady=10)

    def guardar_cambios(self, cita_id, medico, hora, fecha, ventana):
        if not medico or not hora or not fecha:
            messagebox.showerror("Error", "Por favor complete todos los campos.")
            return

        conn = sqlite3.connect("citas_medicas.db")
        cursor = conn.cursor()
        cursor.execute("UPDATE citas SET medico = ?, fecha = ?, hora = ? WHERE id = ?", (medico, fecha, hora, cita_id))
        conn.commit()
        conn.close()

        messagebox.showinfo("Éxito", "Cita modificada correctamente.")
        ventana.destroy()

    def eliminar_cita(self, tree):
        selected_item = tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Por favor, selecciona una cita para cancelar.")
            return

        cita_id = tree.item(selected_item)["values"][0]
        conn = sqlite3.connect("citas_medicas.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM citas WHERE id = ?", (cita_id,))
        conn.commit()
        conn.close()

        messagebox.showinfo("Éxito", "Cita cancelada correctamente.")
        tree.delete(selected_item)  # Eliminar la cita de la vista

    def ver_citas_agendadas(self):
        ventana = tk.Toplevel(self.root)
        ventana.title("Citas Agendadas")
        ventana.geometry("500x400")

        tk.Label(ventana, text="Citas Agendadas", font=("Arial", 14)).pack(pady=10)

        frame = tk.Frame(ventana)
        frame.pack(pady=10)

        tree = ttk.Treeview(frame, columns=("ID", "Médico", "Fecha", "Hora"), show="headings")
        for col in tree["columns"]:
            tree.heading(col, text=col)
        tree.pack()

        conn = sqlite3.connect("citas_medicas.db")
        cursor = conn.cursor()
        cursor.execute("SELECT id, medico, fecha, hora FROM citas")
        for fila in cursor.fetchall():
            tree.insert("", "end", values=fila)
        conn.close()

        tk.Button(ventana, text="Modificar Cita", bg="orange", fg="white", font=("Arial", 12), command=lambda: self.modificar_cita(tree)).pack(pady=10)
        tk.Button(ventana, text="Cancelar Cita", bg="red", fg="white", font=("Arial", 12), command=lambda: self.eliminar_cita(tree)).pack(pady=10)
        tk.Button(ventana, text="Regresar", bg="gray", fg="white", font=("Arial", 12), command=ventana.destroy).pack(pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    app = Aplicacion(root)
    root.mainloop()
