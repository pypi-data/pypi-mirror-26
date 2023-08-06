# NooLite MQTT Web Server 

Веб интерфейс для работы с noolite устройсвами через MQTT протокол 

## Установка

Для установки проекта нужен Python 3.5+ и pip

### Из репозитория

В системе должны быть установлены:

- pip для третий версии python

- git

```bash
$ pip3 install git+https://bitbucket.org/AlekseevAV/noolite-mqtt-web-server
```

К примеру установка проекта на ArchLinux будет выглядеть следующим образом:
```bash
# Устанавливаем необходимые пакеты
$ pacman -S python python-pip git
# Устанавливаем noolite_api
$ pip3 install git+https://bitbucket.org/AlekseevAV/noolite-mqtt-web-server
```

### Из исходников

```bash
# Клонируем репозиторий
$ git clone https://bitbucket.org/AlekseevAV/noolite-mqtt-web-server

# Заходим в созданную папку репозитория
$ cd noolite-mqtt-web-server

# Устанавливаем сервер
$ python setup.py install
```

### Настройка MQTT плагина для Homebridge
```bash
# Устанавливаем MQTT плагин для homebridge 
https://www.npmjs.com/package/homebridge-mqtt

# Добавляем в конфиг файл homebridge (config.json) параметры для подключения к MQTT
{
  "platform": "mqtt",
  "name": "mqtt",
  "url": "mqtt://127.0.0.1",
  "topic_type": "multiple",
  "topic_prefix": "homebridge",
  "username": "foo",
  "password": "bar"
}

# Устанавливаем MQTT брокер mosquitto. в дальнейшем запускать не от админа
$ pacman -Sy 
$ pacman -S mosquitto

# Настраиваем конфигурационный файл (mosquitto.conf)
nano /etc/mosquitto/mosquitto.conf

Добавляем строки
pid_file /var/run/mosquitto.pid 
user alarm

# Добавляем кастомные характеристики
$ nano /usr/lib/node_modules/homebridge/node_modules/hap-nodejs/lib/gen/HomeKitTypes.js 
$ cp HomeKitTypes-NooLite.js /usr/lib/node_modules/homebridge/node_modules/
```
## Характеристики NooLite для homebridge


1. Скопировать файл HomeKitTypes-NooLite.js из корня репозитория в /<путь до корня homebridge>/node_modules/hap-nodejs/lib/gen/

Например `cp HomeKitTypes-NooLite.js /usr/lib/node_modules/homebridge/node_modules/hap-nodejs/lib/gen/`

2. Добавить строчку `var HomeKitTypesCustom = require('./HomeKitTypes-NooLite');` в конец файла /<путь до корня homebridge>/node_modules/hap-nodejs/lib/gen/HomeKitTypes.js

Может быть здесь `nano /usr/lib/node_modules/homebridge/node_modules/hap-nodejs/lib/gen/HomeKitTypes.js `

## Запуск

```
$ noolite_web_server
```

## Автозапуск

Создаем `autorun.sh` файл:
```bash
cat <<end > /home/alarm/autorun.sh
#!/bin/sh -
avahi-daemon &
sleep 10
nohup mosquitto -c /etc/mosquitto/mosquitto.conf -d &>> /home/alarm/mosquitto_log&
sleep 15
nohup homebridge &>> /home/alarm/homebridge_log &
sleep 15
nohup noolite_serve &>> /home/alarm/http-api-server_log &
end
```

Добавляем в `autorun.sh` в автозапуск:
```bash
cat <<end > /etc/systemd/system/autorun@root.service
[Unit]
Description=Homebridge
After=network.target
After=avahi-daemon.service

[Service]
Type=forking
User=%i
ExecStart=/home/alarm/autorun.sh

[Install]
WantedBy=multi-user.target
end
```
## Работа

Веб-интерфейс находится по адресу <ip_устройства>:8080

### Структура

Страница   | Описание
---------- | --------
`/`        | Страница для наглядного приема-передачи команд на силовые блоки
`/api.htm` | Параметры GET запроса по этому адресу будут переданы на USB-адаптер


Команды к USB-адаптеру можно выполнять либо самостоятельно формируя GET запросы на `/api.htm` с необходимыми параметрами, передваемыми в URL,
либо используя форму отправки запроса на `/` (_данная форма формирует и выполняет GET запросы на `/api.htm` с указанными в ней параметрами_)
