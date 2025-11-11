import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pandas as pd
import numpy as np
from pandastable import Table
import os

class DataCleanerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Data Cleaner App")
        self.root.geometry("1000x700")
        
        # Variables para almacenar datos
        self.original_df = None
        self.cleaned_df = None
        
        # Crear interfaz
        self.create_widgets()
        
    def create_widgets(self):
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configurar grid
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
        # Botón para cargar archivo
        ttk.Button(main_frame, text="Cargar CSV", command=self.load_csv).grid(row=0, column=0, sticky=tk.W, pady=5)
        
        # Botón para exportar
        ttk.Button(main_frame, text="Exportar CSV Limpio", command=self.export_csv).grid(row=0, column=1, sticky=tk.E, pady=5)
        
        # Notebook (pestañas)
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)
        
        # Pestaña de datos originales
        self.original_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.original_frame, text="Datos Originales")
        
        # Pestaña de datos limpios
        self.cleaned_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.cleaned_frame, text="Datos Limpios")
        
        # Pestaña de opciones de limpieza
        self.options_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.options_frame, text="Opciones de Limpieza")
        
        # Crear opciones de limpieza
        self.create_cleaning_options()
        
        # Inicializar tablas vacías
        self.create_empty_tables()
        
    def create_empty_tables(self):
        # Tabla para datos originales
        self.original_table_frame = ttk.Frame(self.original_frame)
        self.original_table_frame.pack(fill=tk.BOTH, expand=True)
        
        # Tabla para datos limpios
        self.cleaned_table_frame = ttk.Frame(self.cleaned_frame)
        self.cleaned_table_frame.pack(fill=tk.BOTH, expand=True)
        
        # Crear tablas vacías
        self.original_table = Table(self.original_table_frame, showtoolbar=True, showstatusbar=True)
        self.original_table.show()
        
        self.cleaned_table = Table(self.cleaned_table_frame, showtoolbar=True, showstatusbar=True)
        self.cleaned_table.show()
        
    def create_cleaning_options(self):
        # Frame para opciones de limpieza
        options_container = ttk.Frame(self.options_frame)
        options_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Título
        ttk.Label(options_container, text="Selecciona las operaciones de limpieza a aplicar:", 
                 font=('Arial', 12, 'bold')).grid(row=0, column=0, columnspan=2, sticky=tk.W, pady=10)
        
        # Variables para checkboxes
        self.remove_duplicates_var = tk.BooleanVar()
        self.fill_na_var = tk.BooleanVar()
        self.remove_na_var = tk.BooleanVar()
        self.standardize_text_var = tk.BooleanVar()
        self.remove_outliers_var = tk.BooleanVar()
        self.convert_dtypes_var = tk.BooleanVar()
        self.rename_cols_var = tk.BooleanVar()
        
        # Checkboxes para opciones de limpieza
        ttk.Checkbutton(options_container, text="Eliminar filas duplicadas", 
                       variable=self.remove_duplicates_var).grid(row=1, column=0, sticky=tk.W, pady=5)
        
        ttk.Checkbutton(options_container, text="Rellenar valores faltantes", 
                       variable=self.fill_na_var).grid(row=2, column=0, sticky=tk.W, pady=5)
        
        ttk.Separator(options_container, orient='horizontal').grid(row=3, column=0, columnspan=2, sticky=tk.W+tk.E, pady=10)
        
        ttk.Checkbutton(options_container, text="Eliminar filas con valores faltantes", 
                       variable=self.remove_na_var).grid(row=4, column=0, sticky=tk.W, pady=5)
        
        ttk.Checkbutton(options_container, text="Estandarizar texto (minúsculas, quitar espacios)", 
                       variable=self.standardize_text_var).grid(row=5, column=0, sticky=tk.W, pady=5)
        
        ttk.Checkbutton(options_container, text="Eliminar outliers (columna numérica)", 
                       variable=self.remove_outliers_var).grid(row=6, column=0, sticky=tk.W, pady=5)
        
        ttk.Checkbutton(options_container, text="Convertir tipos de datos automáticamente", 
                       variable=self.convert_dtypes_var).grid(row=7, column=0, sticky=tk.W, pady=5)
        
        ttk.Checkbutton(options_container, text="Renombrar columnas (sin espacios, minúsculas)", 
                       variable=self.rename_cols_var).grid(row=8, column=0, sticky=tk.W, pady=5)
        
        # Botón para aplicar limpieza
        ttk.Button(options_container, text="Aplicar Limpieza", 
                  command=self.apply_cleaning).grid(row=9, column=0, pady=20)
        
        # Frame para opciones específicas
        specific_options = ttk.LabelFrame(options_container, text="Opciones Específicas", padding=10)
        specific_options.grid(row=1, column=1, rowspan=8, sticky=(tk.W, tk.E, tk.N, tk.S), padx=20)
        
        # Opciones para rellenar NA
        ttk.Label(specific_options, text="Valor para rellenar NA:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.fill_na_value = ttk.Entry(specific_options, width=15)
        self.fill_na_value.insert(0, "0")
        self.fill_na_value.grid(row=0, column=1, sticky=tk.W, pady=5)
        
        # Opciones para eliminar outliers
        ttk.Label(specific_options, text="Columna para outliers:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.outlier_column = ttk.Combobox(specific_options, width=15, state="readonly")
        self.outlier_column.grid(row=1, column=1, sticky=tk.W, pady=5)
        
        ttk.Label(specific_options, text="Método:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.outlier_method = ttk.Combobox(specific_options, width=15, state="readonly", 
                                          values=["IQR", "Z-score"])
        self.outlier_method.set("IQR")
        self.outlier_method.grid(row=2, column=1, sticky=tk.W, pady=5)
        
        # Opciones para renombrar columnas
        ttk.Label(specific_options, text="Nuevos nombres columnas:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.new_column_names = tk.Text(specific_options, width=20, height=5)
        self.new_column_names.grid(row=3, column=1, sticky=tk.W, pady=5)
        
        ttk.Label(specific_options, text="(Una por línea)").grid(row=4, column=1, sticky=tk.W)
        
    def load_csv(self):
        file_path = filedialog.askopenfilename(
            title="Seleccionar archivo CSV",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        
        if file_path:
            try:
                self.original_df = pd.read_csv(file_path)
                self.cleaned_df = self.original_df.copy()
                
                # Actualizar tablas
                self.update_table(self.original_table, self.original_df)
                self.update_table(self.cleaned_table, self.cleaned_df)
                
                # Actualizar opciones de columnas
                self.update_column_options()
                
                messagebox.showinfo("Éxito", f"Archivo cargado: {os.path.basename(file_path)}")
                
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo cargar el archivo: {str(e)}")
    
    def update_column_options(self):
        if self.original_df is not None:
            # Actualizar combobox de columnas para outliers
            numeric_columns = self.original_df.select_dtypes(include=[np.number]).columns.tolist()
            self.outlier_column['values'] = numeric_columns
            if numeric_columns:
                self.outlier_column.set(numeric_columns[0])
            
            # Prellenar sugerencias para renombrar columnas
            suggested_names = [col.lower().replace(' ', '_').replace('-', '_') for col in self.original_df.columns]
            self.new_column_names.delete(1.0, tk.END)
            self.new_column_names.insert(1.0, '\n'.join(suggested_names))
    
    def update_table(self, table, df):
        # Actualizar la tabla existente con nuevos datos
        table.model.df = df
        table.redraw()
    
    def apply_cleaning(self):
        if self.original_df is None:
            messagebox.showwarning("Advertencia", "Primero carga un archivo CSV")
            return
        
        # Hacer una copia de los datos originales
        self.cleaned_df = self.original_df.copy()
        
        # Aplicar operaciones seleccionadas
        try:
            operations_applied = []
            
            if self.remove_duplicates_var.get():
                before = len(self.cleaned_df)
                self.cleaned_df = self.cleaned_df.drop_duplicates()
                after = len(self.cleaned_df)
                operations_applied.append(f"Eliminadas {before - after} filas duplicadas")
            
            if self.fill_na_var.get():
                fill_value = self.fill_na_value.get()
                # Intentar convertir a número si es posible
                try:
                    fill_value = float(fill_value) if '.' in fill_value else int(fill_value)
                except ValueError:
                    pass  # Mantener como string si no se puede convertir
                
                na_count_before = self.cleaned_df.isna().sum().sum()
                self.cleaned_df = self.cleaned_df.fillna(fill_value)
                na_count_after = self.cleaned_df.isna().sum().sum()
                operations_applied.append(f"Rellenados {na_count_before - na_count_after} valores NA con '{fill_value}'")
            
            if self.remove_na_var.get():
                before = len(self.cleaned_df)
                self.cleaned_df = self.cleaned_df.dropna()
                after = len(self.cleaned_df)
                operations_applied.append(f"Eliminadas {before - after} filas con valores NA")
            
            if self.standardize_text_var.get():
                # Aplicar a columnas de texto
                text_columns = self.cleaned_df.select_dtypes(include=['object']).columns
                for col in text_columns:
                    self.cleaned_df[col] = self.cleaned_df[col].astype(str).str.lower().str.strip()
                operations_applied.append("Texto estandarizado (minúsculas, sin espacios)")
            
            if self.remove_outliers_var.get() and self.outlier_column.get():
                col = self.outlier_column.get()
                if col in self.cleaned_df.columns:
                    before = len(self.cleaned_df)
                    if self.outlier_method.get() == "IQR":
                        Q1 = self.cleaned_df[col].quantile(0.25)
                        Q3 = self.cleaned_df[col].quantile(0.75)
                        IQR = Q3 - Q1
                        lower_bound = Q1 - 1.5 * IQR
                        upper_bound = Q3 + 1.5 * IQR
                        self.cleaned_df = self.cleaned_df[(self.cleaned_df[col] >= lower_bound) & 
                                                         (self.cleaned_df[col] <= upper_bound)]
                    elif self.outlier_method.get() == "Z-score":
                        try:
                            from scipy import stats
                            self.cleaned_df = self.cleaned_df[(np.abs(stats.zscore(self.cleaned_df[col])) < 3)]
                        except ImportError:
                            messagebox.showwarning("Advertencia", "Scipy no está instalado. No se pueden eliminar outliers con Z-score.")
                    after = len(self.cleaned_df)
                    operations_applied.append(f"Eliminados {before - after} outliers de la columna '{col}'")
            
            if self.convert_dtypes_var.get():
                self.cleaned_df = self.cleaned_df.convert_dtypes()
                operations_applied.append("Tipos de datos convertidos automáticamente")
            
            if self.rename_cols_var.get():
                new_names_text = self.new_column_names.get(1.0, tk.END).strip().split('\n')
                if len(new_names_text) == len(self.cleaned_df.columns):
                    new_names = [name.strip() for name in new_names_text if name.strip()]
                    if new_names:
                        self.cleaned_df.columns = new_names
                        operations_applied.append("Columnas renombradas")
            
            # Actualizar tabla de datos limpios
            self.update_table(self.cleaned_table, self.cleaned_df)
            
            # Mostrar resumen de cambios
            original_rows, original_cols = self.original_df.shape
            cleaned_rows, cleaned_cols = self.cleaned_df.shape
            
            summary = f"Operaciones aplicadas exitosamente.\n\n"
            summary += f"Filas originales: {original_rows}\n"
            summary += f"Filas después de limpieza: {cleaned_rows}\n"
            summary += f"Columnas: {cleaned_cols}\n\n"
            summary += "Operaciones aplicadas:\n" + "\n".join([f"• {op}" for op in operations_applied])
            
            messagebox.showinfo("Limpieza Completada", summary)
                               
        except Exception as e:
            messagebox.showerror("Error", f"Error durante la limpieza: {str(e)}")
    
    def export_csv(self):
        if self.cleaned_df is None or self.cleaned_df.empty:
            messagebox.showwarning("Advertencia", "No hay datos para exportar")
            return
        
        file_path = filedialog.asksaveasfilename(
            title="Guardar CSV limpio",
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        
        if file_path:
            try:
                self.cleaned_df.to_csv(file_path, index=False)
                messagebox.showinfo("Éxito", f"Archivo guardado: {os.path.basename(file_path)}")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo guardar el archivo: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = DataCleanerApp(root)
    root.mainloop()
    