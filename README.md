# [Jean-Michel Bot](https://twitter.com/jeanmichelbot)

Ce bot n'est pas encore live, mais ça ne serait tarder.

## Conception

Inspiré du fantastique [@BotDuCul](https://twitter.com/botducul) de WhiteFangs dont le code se trouve [sur le GitHub dédié](https://github.com/WhiteFangs/BotDuCul).

- Parent 1 : [Julie Cointy](https://twitter.com/jcointy)
- Parent 2 : [Arthur Derennes](https://twitter.com/isyouawizard)
- Parent 3 : [Benoit Dumenier](https://twitter.com/DumeunierBenoit)

## Architecture
Ce bot tournera intégralement sur un projet Google Cloud Platform. L'application y sera déployée sur Google App Engine Standard avec comme runtime Python 3.7, les tweets seront plannifié grâce à un CRON job App Engine et les données persistantes seront stockées dans Google Cloud Storage en tant que fichiers plat.

"Mais pourquoi une architecture aussi simpliste et pas si optimale ?" me direz-vous. Réponse, la thune mon petit poteau, cette architecture nous permettra de le faire tourner gratis.
