# PyWeb FileShare

<a href="https://t.me/PyWebChan"><img src="https://img.shields.io/badge/follow-@PyWebChan-1DA1F2?logo=telegram&style=%7Bstyle%7D"></a>

Этот проект представляет собой простое средство передачи файлов между устройствами с использованием QR-кода. Вы можете легко отправить файлы с телефона или другого устройства на компьютер и наоборот.

## Установка

1. Установите зависимости, указанные в файле `requirements.txt`, выполнив следующую команду:

```bash
pip install -r requirements.txt
```

## Использование

1. Запустите скрипт `main.py`, который предоставит вам QR-код и ссылку для загрузки файла.

2. Для отправки файла на устройство:
- Введите путь к файлу или перетащите его в консоль.
- Сканируйте сгенерированный QR-код или перейдите по предоставленной ссылке.

3. Для загрузки файла на компьютер:
- Введите "upload" в консоль.
- Сканируйте сгенерированный QR-код или перейдите по предоставленной ссылке.

Примечание: Ссылки на загруженные файлы сбрасываются после каждого завершения работы скрипта.

## Инструкции по использованию

Перед началом использования рекомендуется ознакомиться с инструкциями. Вы можете найти их в файле `iReadReadme`. Не забудьте проверить этот файл перед первым запуском.

## Важно

- Этот проект использует Flask для веб-сервера и Waitress для обслуживания запросов.

- QR-коды генерируются с использованием библиотеки qrcode.

- Пожалуйста, обеспечьте безопасность своей сети при использовании этого инструмента для передачи файлов.