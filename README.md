# osuApiV2
 Небольшая программа для упрощения получения токенов для api v2, а так же информации о комнатах мультиплеера в osu. Ожидаем обновления api.
# Как начать?
1. Зарегистрировать приложение: заходим в [настройки](https://osu.ppy.sh/home/account/edit) аккаунта osu и листаем в самый низ. Жмем кнопку `Новое приложение OAuth`. Заполняем `Имя приложения` и `Callback URL Приложения`. Имя может быть любым (например `test`). В качестве URL используем `https://itsidorkin.github.io/`.

![](readmeSrc/1.gif)

2. В открывшемся окне нужно скопировать `ID клиента`, `Секрет клиента` и `Callback URL Приложения` и заполнить соотвествующие поля в файле `personalData.json` (открыть с помощью блокнота или любого другого текстового редактора). 

![](readmeSrc/2.gif)

3. Открыть main.py. Установить зависимые пакеты, если они отсутствуют. Запустить. 


4. Во время первого запуска будет открыт сайт osu c запросом авторизации. После авторизации вас перенаправит на `https://itsidorkin.github.io/`, где нужно нажать кнопку `Копировать Code`. Данный этап происходит лишь один раз при первом запуске. В дальнейшем ваши токены будут автоматически обнавляться и записываться в `personalData.json` при запуске программы.

