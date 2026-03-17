import sys
import os

# Asegura que Python vea la carpeta del proyecto
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from ui import ChatAppUI # Cambiado de ChatUI a ChatAppUI

def main():
    # ChatAppUI ya crea su propio 'root' internamente según tu código
    app = ChatAppUI() 
    app.run()

if __name__ == "__main__":
    main()
