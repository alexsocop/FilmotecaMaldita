FilmotecaMaldita
Un script de Python que automáticamente descarga videos del canal La Filmoteca Maldita. Usa VLC para reproducir los videos porque el tipo de codec que mi script selecciona por defecto usa el que tenga la máxima calidad posible, algunos otros reproductores de video podrían experimentar problemas al momento de reproducir los videos. Además de los videos, el script también descarga las miniaturas y organiza todos los videos por fecha. El script también te permite descargar videos de otros canales, solo debes seleccionar la opción "otros canales" antes de iniciar la descarga. Además crea un archivo llamado "downloaded_archive.txt", donde guarda el registro de los videos ya descargados, así que si la Filmo sube nuevos videos, y tú corres el script de nuevo, sólo bajará los nuevos videos. IMPORTANTE: no borres el archivo "donwload_archive.txt", es el que ayudará al script a mantener el registro. Asegúrate te tener suficiente espacio libre de almacenamiento antes de iniciar con la operación. Yo uso GNU/Linux, pero el scrip puede funcionar en Windows o MacOS.

Importante: primero que nada instala Python en tu computadora.

Aconsejo crear primero un Entorno Virtual (Virtual Environment) para correr este script, debido a que hay que instalar algunas librerías, acá dejo los pasos:

1. Navega a tu carpeta del proyecto
#Abre la terminal de linux (o cualquier terminal de tu sistema operiativo y ubícate en la carpeta de tu proyecto:
cd ~/Documents/"Filmoteca Maldita"


2. Crea un Entorno Virtual
Esto crea un entorno aislado para Python sólo para este proyecto:
Esto creará una carpeta llamada "venv" en tu carpeta de proyecto.
python3 -m venv venv


3. Activa el entorno virtual
Corre este comando:
source venv/bin/activate


Si funciona, verás en tu terminal un cambio en el promp — comenzará con (venv), algo como esto:
(venv) usuario@nombre_pc:~/Documents/Filmoteca Maldita$


4. Ahora instala los paquetes dentro de venv venv
con el entorno activo, puedes instalar de forma segura las dependencias requeridas:
para descargar videos de youtube

python -m pip install -U yt-dlp

python -m pip install -U --pre "yt-dlp[default]"

curl -fsSL https://deno.land/install.sh | sh

correr éste solo si saliste del entorno (virtual environment) 
source ~/.bashrc

Correr todo en un virtual environment (entorno virtual) hará que tu instalación de Python se mantenga limpia

5. corre el script
python download_channel.py


6. (Optional) Desactiva el entorno virtual
Cuando acabes de descargar todos los videos, escribe:
deactivate


Bonus Tip
La próxima vez que quieras regresar a esta carpeta y quieras usar el script, sólo escribe:
cd ~/Documents/"Filmoteca Maldita"
source venv/bin/activate
source ~/.bashrc
python transcriber.py

Extra, un script de bash que puedes usar para bajar un solo vídeo:
python -m yt_dlp \
  --cookies-from-browser firefox \
  --remote-components ejs:github \
  -f "bv*+ba/b" \
  --merge-output-format mkv \
  "https://www.youtube.com/URL-del-video"


Ejecución normal en canal público sin cookies:
python download_channel.py

Con cookies manualmente exportadas para videos restringidos:
python download_channel.py --cookies-file /path/to/cookies.txt
En este repositorio podrás encontrar un archivo de cookies genérico que podrías usar para correr el script, se llama: youtube_cookies.txt


Aquí tienes el flujo limpio en Firefox:

Instala una extensión para exportar cookies que pueda guardar en formato Netscape cookies.txt. Una opción común en Firefox es Get cookies.txt LOCALLY, que indica que exporta en formato Netscape cookies.txt y que no envía información fuera del navegador.

Activa esa extensión en ventanas privadas. Firefox desactiva las extensiones en la navegación privada de forma predeterminada, así que ve a Menú → Complementos y temas → Extensiones → haz clic en la extensión → Ejecutar en ventanas privadas → Permitir. Mozilla documenta exactamente esa ruta de configuración.

Cierra cualquier ventana privada que ya tengas abierta. Después abre una sola ventana privada nueva, y en esa misma ventana y en esa misma pestaña:

inicia sesión en YouTube
ve a youtube.com/robots.txt
exporta las cookies de youtube.com con la extensión
guárdalas con un nombre como youtube_cookies.txt

La documentación de yt-dlp para YouTube indica exactamente este método con ventana privada y dice que la pestaña de robots.txt debe ser la única pestaña privada/incógnito abierta.

Cierra inmediatamente esa ventana privada después de exportar. No sigas usando después esa sesión privada de YouTube en el navegador, porque la idea precisamente es evitar que esas cookies roten.

Ejecuta tu script con el archivo exportado:

python download_channel.py --cookies-file /ruta/a/youtube_cookies.txt

Úsalo sobre todo para los vídeos con restricción de edad o los casos en los que aparezca el mensaje “confirma que no eres un bot”. Para la descarga pública normal en bloque, tu script sin cookies sigue siendo la mejor opción por defecto. yt-dlp dice que las cookies solo son necesarias para contenido que requiere una cuenta, como vídeos con restricción de edad, privados o solo para miembros.

Un par de notas pequeñas de seguridad:

Permite la extensión en ventanas privadas solo si confías en ella. Mozilla advierte que las extensiones en ventanas privadas pueden acceder a los datos de esas sesiones.
Después de exportar, puedes volver a la configuración de la extensión y cambiar Ejecutar en ventanas privadas otra vez a No permitir. Se hace desde la misma ruta de configuración de Firefox indicada arriba.
