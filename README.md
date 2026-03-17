# 💬 Ollama Chat Client - Tkinter GUI

Una aplicación profesional de chat para Ollama con interfaz gráfica Tkinter, diseñada con buenas prácticas de arquitectura: baja dependencia, alta cohesión y módulos separados.

## 📋 Características

✅ **Selección de Modelos**: Dropdown para elegir entre múltiples modelos  
✅ **Historial de Chat**: Visualización con scroll del histórico de mensajes  
✅ **Medición de Tiempos**: Tiempo de respuesta mostrado para cada mensaje  
✅ **Limpieza de Historial**: Botón para borrar toda la conversación  
✅ **Interfaz Intuitiva**: Diseño limpio y moderno con Tkinter  
✅ **Manejo de Errores**: Gestión robusta de conexiones y excepciones  
✅ **Arquitectura Modular**: Código organizado en módulos independientes  

## 📦 Requisitos del Sistema

- **Python 3.8+**
- **Ollama** instalado y ejecutándose en `http://localhost:11434`
- **Tkinter** (incluido por defecto en Python)
- **Windows, macOS o Linux**

## 🔧 Instalación en Windows (CMD)

### 1. Descargar/Clonar el Proyecto

```cmd
cd C:\Users\Tu_Usuario\Desktop
git clone <repository-url>
cd ollama-chat-client
```

O simplemente descarga los archivos y descomprime en una carpeta.

### 2. Crear Entorno Virtual

```cmd
python -m venv venv
```

### 3. Activar Entorno Virtual

```cmd
venv\Scripts\activate
```

Verás `(venv)` al inicio de cada línea en cmd cuando esté activado.

### 4. Instalar Dependencias

```cmd
pip install -r requirements.txt
```

### 5. Verificar Tkinter (Opcional)

```cmd
python -m tkinter
```

Debería abrirse una ventana de prueba.

---

## ⚡ INICIO RÁPIDO (Windows CMD)

### Método 1: Dos Ventanas CMD (Recomendado)

**PASO 1: Primera ventana - Iniciar Ollama**

```cmd
ollama serve
```

Déjala corriendo. Deberías ver mensajes indicando que Ollama está escuchando en `localhost:11434`.

**PASO 2: Segunda ventana - Iniciar Aplicación**

```cmd
cd C:\ruta\a\tu\proyecto

venv\Scripts\activate

python main.py
```

¡La aplicación debe abrirse! 🎉

---

### Método 2: Script Automático (start.bat)

Crea un archivo llamado `start.bat` en la carpeta raíz del proyecto con este contenido:

```batch
@echo off
title Ollama Chat Client
cd /d "%~dp0"

REM Crear entorno virtual si no existe
if not exist "venv" (
    echo Creando entorno virtual...
    python -m venv venv
)

REM Activar entorno
call venv\Scripts\activate

REM Instalar dependencias
echo Instalando dependencias...
pip install -r requirements.txt

REM Ejecutar aplicacion
echo.
echo ===================================
echo ^!^! Ollama Chat Client iniciado ^^!^^!
echo ===================================
echo.
echo IMPORTANTE: Asegúrate de que Ollama esté ejecutándose
echo Ejecuta en otra ventana cmd: ollama serve
echo.
python main.py

pause
```

Luego simplemente haz doble clic en `start.bat` y sigue las instrucciones.

---

### ✅ Checklist antes de iniciar:

```cmd
REM 1. Verificar Python
python --version

REM 2. Verificar Ollama
ollama --version

REM 3. Descargar modelo (si no lo tienes)
ollama pull minyOllama

REM 4. Listar modelos disponibles
ollama list
```

---

## 🚀 Uso

### Paso 1: Inicia Ollama

En una ventana cmd ejecuta:
```cmd
ollama serve
```

Espera a ver: `Listening on 127.0.0.1:11434`

### Paso 2: Inicia la Aplicación

En OTRA ventana cmd ejecuta:
```cmd
cd C:\ruta\a\proyecto
venv\Scripts\activate
python main.py
```

### Paso 3: Usa la Interfaz

1. **Selecciona un modelo** del dropdown
2. **Escribe tu pregunta** en el campo de texto
3. **Presiona "Send"** o `Ctrl + Enter`
4. **Espera la respuesta** (verás el tiempo en segundos)
5. **Limpia el historial** con el botón "Clear History"

---

## 📱 Interfaz de Usuario

### Panel de Control (Arriba)
```
[Select Model: ▼ minyOllama]  ✅ Server: Connected  [🗑️ Clear History]
```

- **Select Model**: Elige entre:
  - minyOllama (rápido, ligero)
  - gemma2:2b (pequeño)
  - llama3.2:3b (mediano)
  - llama3.1:8b (más potente)
- **Server Status**: Verde ✅ = conectado, Rojo ❌ = desconectado
- **Clear History**: Borra toda la conversación

### Área de Chat (Centro)
```
[YOU]: Hola, ¿cómo estás?

[BOT]: (2.34s)
Estoy bien, gracias por preguntar...
```

- Mensajes tuyos en **azul**
- Respuestas del bot en **púrpura** con tiempo en segundos
- Scroll automático al final
- Solo lectura (no puedes editar)

### Área de Entrada (Abajo)
```
Your Message:
[________________________________]
[📤 Send]

Atajo: Ctrl + Enter para enviar
```

---

## 🏗️ Arquitectura del Proyecto

```
ollama-chat-client/
├── main.py                 ← Punto de entrada
├── app/
│   ├── __init__.py         ← Inicialización
│   ├── llm_client.py       ← Cliente API (sin UI)
│   └── ui.py               ← Interfaz Tkinter
├── requirements.txt        ← Dependencias
├── README.md               ← Este archivo
├── start.bat               ← Script automático (opcional)
└── venv/                   ← Entorno virtual (creado automáticamente)
```

### Módulos Explicados

#### `llm_client.py` - Cliente LLM
- Comunica con la API de Ollama
- Valida prompts y modelos
- Mide tiempos de respuesta
- Maneja errores de conexión
- **Sin dependencias de UI**

#### `ui.py` - Interfaz Gráfica
- Widgets Tkinter (texto, botones, dropdown)
- Gestión de chat history
- Threading para no bloquear UI
- Formatea y muestra mensajes

#### `main.py` - Punto de Entrada
- Inicializa la aplicación
- Punto de partida único

---

## 🔌 Configuración de Ollama

### Instalar Ollama

1. Descarga desde https://ollama.ai
2. Ejecuta el instalador
3. Ollama se iniciará automáticamente

### Descargar Modelos

```cmd
REM Descargar modelos disponibles
ollama pull minyOllama
ollama pull gemma2:2b
ollama pull llama3.2:3b
ollama pull llama3.1:8b

REM Listar modelos instalados
ollama list

REM Ver información del servidor
curl http://localhost:11434/api/tags
```

### Verificar Conexión

```cmd
REM Debe responder con información de los modelos
curl http://localhost:11434/api/tags
```

---

## ⚙️ Solución de Problemas

### Error: "Cannot connect to Ollama"
**Solución**: Asegúrate de que `ollama serve` esté ejecutándose en otra ventana cmd

```cmd
REM En otra ventana cmd:
ollama serve
```

### Error: "Model not found: minyOllama"
**Solución**: Descarga el modelo primero

```cmd
ollama pull minyOllama
```

### Error: "No module named 'tkinter'"
**Solución**: Tkinter no está instalado

Windows: Reinstala Python desde python.org y MARCA "tcl/tk and IDLE"

### Error: "venv\Scripts\activate" no funciona
**Solución**: Abre cmd como ADMINISTRADOR o intenta:

```cmd
python -m venv venv
python -m pip install -r requirements.txt
python main.py
```

### La aplicación se abre pero está vacía
**Solución**: Espera a que Ollama cargue. Algunos modelos tardan minutos.

### La respuesta tarda MUCHO tiempo
**Solución**: Modelos grandes (llama3.1:8b) pueden tardar varios minutos. Paciencia 😊

---

## 📊 Ejemplo de Sesión

```
[Usuario abre cmd y navega a la carpeta]

C:\ollama-chat-client> venv\Scripts\activate
(venv) C:\ollama-chat-client> python main.py

[Se abre ventana de aplicación]

[Usuario selecciona "llama3.2:3b" del dropdown]
[Usuario escribe: "¿Cuál es la capital de Colombia?"]
[Usuario presiona Send o Ctrl+Enter]
[Espera 3-5 segundos...]

[BOT]: (4.23s)
La capital de Colombia es Bogotá, ubicada en la región...
```

---

## 🎯 Buenas Prácticas Implementadas

1. **Baja Dependencia** ✅
   - Solo `requests` como dependencia externa
   - Tkinter es stdlib (incluido en Python)
   - Sin frameworks pesados

2. **Alta Cohesión** ✅
   - Cada módulo tiene responsabilidad única
   - LLM Client solo API
   - UI solo interfaz gráfica

3. **Bajo Acoplamiento** ✅
   - Módulos independientes
   - Interfaz clara entre componentes
   - Fácil de mantener y extender

4. **Manejo Robusto de Errores** ✅
   - Try/catch apropiado
   - Mensajes útiles para el usuario
   - Recuperación elegante

5. **Threading** ✅
   - Solicitudes a Ollama en threads separados
   - UI nunca se congela
   - Indicadores de estado

6. **Type Hints** ✅
   - Anotaciones de tipo en métodos
   - Mejor documentación
   - Detección de errores

7. **Documentación** ✅
   - Docstrings en clases y métodos
   - Comentarios explicativos
   - README completo

---

## 🚀 Mejoras Futuras Posibles

- [ ] Guardar/cargar conversaciones (JSON, TXT)
- [ ] Configurar parámetros del modelo (temperatura, top_p)
- [ ] Soporte para streaming (respuestas en tiempo real)
- [ ] Tema oscuro/claro seleccionable
- [ ] Historial persistente entre sesiones
- [ ] Múltiples servidores Ollama
- [ ] Búsqueda en historial
- [ ] Exportar chat a PDF

---

## 📝 Licencia

Código abierto bajo licencia MIT.

---

## 🎨 Notas Técnicas

### Por qué Sin Streaming
El streaming genera tokens en tiempo real pero es más difícil medir tiempos exactos. La versión actual usa requests sin streaming para obtener:
- ✅ Tiempo de respuesta preciso
- ✅ Respuesta completa y consistente
- ✅ Código más simple y confiable

### Por qué Solo Tkinter
Tkinter es:
- ✅ Incluido en Python (sin instalación)
- ✅ Ligero y rápido
- ✅ Suficiente para aplicaciones profesionales
- ✅ Mantiene "baja dependencia"

### Threading para UI
Las solicitudes HTTP pueden tardar segundos/minutos. Por eso usamos threads:
- ✅ La UI no se congela
- ✅ Puedes escribir mientras esperas
- ✅ Respaldo visual con botón deshabilitado

---

## 💡 Tips Útiles

**Copiar conversación**: Haz click derecho en el área de chat → Copiar

**Enviar rápido**: Presiona `Ctrl + Enter` en lugar de clickear Send

**Limpiar rápido**: Usa el botón 🗑️ para borrar historial

**Múltiples modelos**: Cambia el dropdown entre respuestas para comparar

**Ver logs de Ollama**: Mira la ventana de `ollama serve` para logs detallados

---

**¡Disfruta chatear con Ollama! 💬🚀**

Para preguntas o problemas: revisa la sección "Solución de Problemas"
