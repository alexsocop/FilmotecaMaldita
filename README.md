# FilmotecaMaldita
Un script de Python que automáticamente descarga videos del canal La Filmoteca Maldita. Usa VLC para reproducir los videos porque el tipo de codec que mi script selecciona por defecto usa el que tenga la máxima calidad posible, algunos otros reproductores de video podrían experimentar problemas al momento de reproducir los videos. Además de los videos, el script también descarga las miniaturas y organiza todos los videos por fecha. El script también te permite descargar videos de otros canales, solo debes seleccionar la opción "otros canales" antes de iniciar la descarga. Asegúrate te tener suficiente espacio libre de almacenamiento antes de iniciar con la operación. Yo uso GNU/Linux, pero el scrip puede funcionar en Windows o MacOS.

Aconsejo crear primero un Entorno Virtual (Virtual Environment) para correr este script, debido a que hay que instalar algunas librerías, acá dejo los pasos:

1. Navega a tu carpeta del proyecto
# Abre la terminal de linux (o cualquier terminal de tu sistema operiativo y ubícate en la carpeta de tu proyecto:
cd ~/Documents/"Filmoteca Maldita"


2. Crea un Entorno Virtual
# Esto crea un entorno aislado para Python sólo para este proyecto:
# Esto creará una carpeta llamada "venv" en tu carpeta de proyecto.
python3 -m venv venv


3. Activa el entorno virtual
# Corre este comando:
source venv/bin/activate


# Si funciona, verás en tu terminal un cambio en el promp — comenzará con (venv), algo como esto:
(venv) usuario@nombre_pc:~/Documents/Filmoteca Maldita$


4. Ahora instala los paquetes dentro de venv venv
# con el entorno activo, puedes instalar de forma segura las dependencias requeridas:
# para descargar videos de youtube
python -m pip install -U yt-dlp
python -m pip install -U --pre "yt-dlp[default]"
curl -fsSL https://deno.land/install.sh | sh
# correr éste solo si saliste del entorno (virtual environment) 
source ~/.bashrc

✅ Correr todo en un virtual environment (entorno virtual) hará que tu instalación de Python se mantenga limpia

5. corre el script
python download_channel.py


6. (Optional) Desactiva el entorno virtual
# Cuando acabes de descargar todos los videos, escribe:
deactivate


🧠 Bonus Tip
# La próxima vez que quieras regresar a esta carpeta y quieras usar el script, sólo escribe:
cd ~/Documents/"Filmoteca Maldita"
source venv/bin/activate
source ~/.bashrc
python transcriber.py
