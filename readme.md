#README
Als je de bot wilt helpen uitbreiden kan je een PR maken

##Requirements:
- Telegram
- Python 2.7

##Setup
Installeer de dependencies van het programmatje door:
``sudo pip install -r requirements.txt``
of
``sudo pip2.7 install -r requirements.txt``
als je ook python 3.x geinstalleerd hebt

Kopieer/hernoem config.json.example naar config.json.

Vul hier jouw student gegevens in, je gewenste interval (minuten), en de tekst die de bot stuurt bij de melding.

Maak een nieuwe telegram bot aan via @BotFather: https://core.telegram.org/bots#6-botfather en vul de token in config.json in

##Start
Start de applicatie met ``python main.py`` of met ``python main.py & disown`` om het programma op de achtergrond te laten draaien
Je kan ook bij het opstarten van je machine het programma laten uitvoeren door een regel in de crontab te zetten

``sudo crontab -e``

En vervolgens bijvoorbeeld voor een standaard raspberry pi installatie:

``@reboot python /home/pi/studievolg_scraper/main.py``

Om de bot automatisch een notificatie naar jou te laten sturen moet je minstens 1x ``/cijfers`` zeggen tegen de bot,
de chat_id zal dan worden opgeslagen, en zolang je die niet weg haalt uit je config.json weet hij jou te vinden.

