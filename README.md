# UppgiftSystemIntegration
Inlämnings uppgift för system integration

All kod ligger i master branchen >> uppgift >> main.py

Jag har fokuserat på att utföra uppgiften för ett hus, men att man kan kolla data från weatherAPI vart man vill.
Jag har hårdkodat data då vi inte har någon sensor att koppla ihopp den med, där jag sätter temperatur som en float och radiator och gardin status som en bool.
Jag har lagt alla sensor i en list beroende på deras funktionalitet så att man på så sett kan komma åt varje unik sensor genom deras id i listan, vilket man gör genom en get.
För att uppdatera sensorernas inställning har jag gjort classer som berättar vad för typ av data som man kan ändra, och sen måste man ange id för vilken gardin eller radiator man vill ändra, medans för temperatur kommer båda sensorerna att få det givna värdet, vilket man gör genom post.

Man hade kunnat tillämpa flera hus enkelt genom att skapa en class med hus som innehåller allt som redan finns och lägger dessa hus i en lista för att lätta komma åt dem.
Genom att skapa en class för alla hus skulle varje hus kunna ha ett unikt lösenord och användarnamn, jag skulle även använda mig av Oauth istället samt spara API nycklarna i en miljövariabel.
Ifall man vill lägga till mer funktionaliteter kan det lätta tillämpas på samma sätta som tidigare funktionaliteterna.

Under är en bild som visar en ritning för g samt vg nivå.



![ritning_systemint](https://github.com/BergetAlex/UppgiftSystemIntegration/assets/149575877/e1205cb0-74e7-4949-9750-20bae97d4b6b)
