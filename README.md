# pjecz-clasificador

Se elaboró en 2020 con el própósito de clasificar los documentos que se entragaban por correo electrónico.

Ahora, desde 2021, se usa el sistema [Plataforma Web](https://github.com/PJECZ/pjecz-plataforma-web) para ese fin.

## Instalar

Requiere un entorno virtual.

```bash
python -m venv venv
. venv/bin/activate
pip install --upgrade pip
pip install wheel
pip install pylint
pip install black
pip install -r requirements.txt
pip install --editable .
```

## Configurar

Debe crear un archivo `settings.ini` tomando como ejemplo `settings-sample.ini`

## Clasificador

Lee, clasifica y envía acuses de recibido

```bash
clasificador --help
```

Listar las direcciones de correo electrónicos de las Listas de Acuerdos

```bash
clasificador --rama Acuerdos informar
```

Órdenes para leer; leer y clasificar; leer, clasificar y responder

```bash
clasificador --rama Acuerdos leer
clasificador --rama Acuerdos leer-clasificar
clasificador --rama Acuerdos leer-clasificar-responder
```

## Contestador

Rastrea el depósito y envía acuses de publicación

```bash
contestador --help
```

Listar las direcciones de correo electrónicos de las Listas de Acuerdos

```bash
contestador --rama Acuerdos informar
```

Órdenes para

```bash
contestador --rama Acuerdos rastrear
contestador --rama Acuerdos rastrear-responder
```

## Cron

Liste crontab

```bash
crontab -l
```

Tareas programadas

```
0 8-20 * * 1-5 /home/consultas/.local/bin/sincronizar-listas-de-acuerdos.sh >> /home/consultas/Logs/sincronizar-listas-de-acuerdos.log 2>&1
15 8-20 * * 1-5 /home/consultas/.local/bin/sincronizar-edictos-juzgados.sh >> /home/consultas/Logs/sincronizar-edictos-juzgados.log 2>&1
30 8-20 * * 1-5 /home/consultas/.local/bin/sincronizar-sentencias.sh >> /home/consultas/Logs/sincronizar-sentencias.log 2>&1
45 8-20 * * 1-5 /home/consultas/.local/bin/sincronizar-edictos.sh >> /home/consultas/Logs/sincronizar-edictos.log 2>&1
```

Bash script sincronizar-listas-de-acuerdos.sh

```bash
#!/bin/bash
date

echo "-- clasificador leer-clasificar-responder"
cd /home/consultas/Documentos/GitHub/PJECZ/pjecz-clasificador
/home/consultas/VirtualEnv/PJECZClasificador/bin/clasificador --rama acuerdos leer-clasificar-responder
echo

echo "-- consultas subir"
cd /home/consultas/Documentos/GitHub/PJECZ/pjecz-consultas
/home/consultas/VirtualEnv/PJECZConsultas/bin/consultas --rama Acuerdos subir
echo

echo "-- rclone copy . archivista"
cd /home/consultas/Nextcloud/Consultas\ Listas\ de\ Acuerdos
rclone --max-age 24h --no-traverse --exclude *.json copy . archivista:/Consultas\ Listas\ de\ Acuerdos
echo

date
echo
```
