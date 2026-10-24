# GitHub — configurar el repositorio del grupo

## Opción rápida: que Cowork lo haga con el conector de GitHub
Abre una tarea de Cowork con la carpeta `AECODE Nexo Sismico` conectada y pega el prompt de abajo (cambia los usuarios de GitHub de los compañeros).

```
Contexto: la carpeta conectada "AECODE Nexo Sismico" es el vault de Obsidian del equipo Nexo Sísmico
(Beca AI Talent, AECODE). Quiero publicarla como repositorio de GitHub. Trabaja SOLO dentro de esa
carpeta: no toques otras carpetas (ni Documents\Claude ni el vault "Oficinas Piedemonte A Bogotá").

1. Revisión previa (no subas nada todavía):
   a. Lee .gitignore y respétalo: fuera 08 Multimedia/* (salvo LEEME.md), *.mp4/*.mov/*.avi,
      .obsidian/workspace*.json, .obsidian/cache, .trash/, __pycache__/, .ipynb_checkpoints/, .env, *.key,
      *token*, *secret*.
   b. Busca en todos los archivos de texto (.md .py .js .json .csv .ipynb) claves de API, tokens de bot
      de Telegram (patrón números:letras), "Bearer", contraseñas, chat IDs numéricos reales, correos
      personales y URLs privadas. En los 3 JSON de n8n de 05 Datos/Piero JSON las credenciales deben
      estar en null y las URLs deben ser marcadores (https://CONFIGURAR-...). Si encuentras algo real,
      detente y muéstramelo.
   c. Confirma que ningún archivo a subir pase de 50 MB.
   d. Muéstrame la lista de archivos que se subirán y la de ignorados, y espera mi OK.

2. Con el conector de GitHub, crea el repositorio PRIVADO "nexo-sismico" en mi cuenta, descripción:
   "Estimación preliminar de derivas sísmicas en edificios aporticados (NSR-10 + Random Forest) —
   equipo Nexo Sísmico, Beca AI Talent AECODE". README.md de la carpeta como portada.

3. Sube todos los archivos aprobados conservando las carpetas y los nombres con tildes y espacios,
   en un commit: "Nexo Sísmico: vault, prototipo NSR-10 y entregables v1". Incluye los binarios
   (.pdf .docx .pptx .xlsx .png .ipynb). Si el conector no puede subir binarios o carpetas
   completas, dime exactamente cuáles quedaron sin subir y dame los pasos con GitHub Desktop
   para terminar (Add local repository → create repository → Commit → Publish).

4. Verifica en GitHub que estén: 00 Inicio.md, REGISTRO_EQUIPO.md, 03 Prototipo/codigo/nexo_nsr10.py,
   04 Entregables/Informe/Informe_tecnico_Nexo_Sismico.pdf,
   04 Entregables/Presentacion/Presentacion_Nexo_Sismico.pptx y que NO esté ningún .mp4.

5. Invita como colaboradores con permiso de escritura a: [usuario_Lucero], [usuario_Alexis],
   [usuario_JeanPiere], [usuario_Joseph]. Si no los tienes, pregúntamelos.

6. Al final dame: enlace del repositorio, número de archivos subidos, lista de ignorados y cualquier
   advertencia. Luego reemplaza en 03 Prototipo/codigo/ficha.py el texto
   "repositorio del equipo (GitHub)" por el enlace real, y en "04 Entregables/Video ejecutivo 5 min.md"
   deja el espacio "(enlace)" listo para el video; sube ese cambio con el commit
   "Enlace del repositorio en la ficha".
```

## Una sola vez (Nicolás, con GitHub Desktop)
1. Instala GitHub Desktop e inicia sesión.
2. File → Add local repository → `C:\Users\nicoi\Documents\AECODE Nexo Sismico`.
3. "This directory does not appear to be a Git repository" → **create a repository** → Create.
4. Revisa la lista de cambios: no debe aparecer nada de `08 Multimedia` ni archivos con claves.
5. Commit to main: `Nexo Sísmico: vault, prototipo NSR-10 y entregables v1`.
6. **Publish repository** → nombre `nexo-sismico` → privado si prefieren.
7. En github.com → Settings → Collaborators → invitar a Lucero, Alexis, Jean Piere y Joseph.

## Cada compañero (una vez)
✅ Repositorio publicado: https://github.com/FrailM7/nexo-sismico. Pasos completos en el `README.md` (sección "Cómo trabajamos en conjunto") y en [[Sincronizacion automatica]]: clonar, abrir como vault y correr `09 Cowork/instalar_sincronizacion.ps1`.

## Día a día
- Antes de trabajar: **Fetch / Pull**.
- Al terminar: Commit con mensaje claro (`Alexis: tabla de la familia 9`) → **Push**.
- Opcional: plugin "Obsidian Git" para hacerlo desde Obsidian.

## Sobre los videos
Los videos generados (`Video_prototipo_NSR10.mp4`, 1.3 MB, y `Video_ejecutivo_Nexo_Sismico.mp4`, 2.9 MB) también quedan en `08 Multimedia/` y se comparten por enlace, igual que el video grabado.

### Video grabado (99 235 KB ≈ 97 MB)
GitHub rechaza archivos de más de 100 MB y advierte desde 50 MB. El video está justo al borde: **no subirlo al repositorio**. Queda en `08 Multimedia/` (ignorado por `.gitignore`) y se comparte por enlace (Drive o YouTube no listado). Si es obligatorio tenerlo en Git, usar Git LFS.

## Qué NO va al repositorio
Videos, credenciales, `.env`, configuración personal de Obsidian (ya está en `.gitignore`).
