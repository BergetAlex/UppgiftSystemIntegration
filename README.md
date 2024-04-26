# UppgiftSystemIntegration
Inlämnings uppgift för system integration

All kod ligger i master branchen >> uppgift >> main.py

Jag har fokuserat på att utföra uppgiften för ett hus, men att man kan kolla data från weatherAPI vart man vill.
Jag har hårdkodat data då vi inte har någon sensor att koppla ihopp den med, där jag sätter temperatur som en float och radiator och gardin status som en bool.
Jag har lagt alla sensor i en list beroende på deras funktionalitet så att man på så sett kan komma åt varje unik sensor genom deras id i listan, vilket man gör genom en get.
För att uppdatera sensorernas inställning har jag gjort classer som berättar vad för typ av data som man kan ändra, och sen måste man ange id för vilken gardin eller radiator man vill ändra, medans för temperatur kommer båda sensorerna att få det givna värdet, vilket man gör genom post.


Smart Home API (Lokal tjänst):

Tokenbaserad autentisering: 
Användare autentiseras med hjälp av tokens för att säkerställa auktoriserad åtkomst till API:et.

Överföring av data till molnet: 
En funktion implementeras för att överföra data till molnet genom HTTP-anrop. Detta inkluderar information om temperaturer, gradiner och radiatorer.

Mottagande av instruktioner från molnet:
API:et lyssnar på specifika endpoints för instruktioner som ska utföras i hemmet och tar emot dessa instruktioner från molnet.

Molnbaserad tjänst:

Användarautentisering: 
Anända sig av Oauth2

Användargränssnitt: 
En användarvänlig webbapplikation skapas där användare kan välja hus och ifall den authentikerar sig skickas den vidare till Smart Home API:et.

API för huskontroll: 
Efter authentikarisering kan men via det lokala Smart Home API:et kan göra förfrågningar för att styra husen. Molntjänsten hanterar dessa instruktioner och skickar dem till rätt hus.

Push-meddelanden: 
Molntjänsten implementerar push-meddelanden till Smart Home API:et för att meddela användaren om nya instruktioner eller uppdateringar som behöver göras i husen.

Exempel på Kommunikation Mellan Smart Home API och Cloud Service:

Användareinteraktion: 
Användaren loggar in på den molnbaserade webbappen och väljer det specifika huset de vill justera radiatorerna för.

Begäran om Radiatorändring: 
Efter att loggat in skickas den vidare till Smart Home API:et, der Användareren kan begära ändringar.

Verifikation och Uppdatering: 
Det lokala API:et tar emot och verifierar begäranen, godkänner den och uppdaterar den interna databasen med den nya radiatorstatusen.

Överföring av Data till Molnet: 
Det lokala API:et skickar den uppdaterade radiatorstatusen till molntjänsten genom en HTTP POST-förfrågan.

Lagring och Notifikation: 
Molntjänsten tar emot uppdateringen och lagrar den i sin databas, och skickar sedan en push-notifikation till användarens mobilapp eller webbapplikation för att meddela om radiatorstatusens ändring.

Under är en bild som visar en ritning för g samt vg nivå.



![ritning_systemint](https://github.com/BergetAlex/UppgiftSystemIntegration/assets/149575877/e1205cb0-74e7-4949-9750-20bae97d4b6b)
