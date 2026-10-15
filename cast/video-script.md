# Script vidéo : démo CAST Imaging sur DomiAffaire (≈ 7 min)

**Présentatrice :** Ines.
**Format :** capture d'écran (Outil Capture, Win + Maj + R) avec voix.
**Règle :** chaque chiffre dit à l'oral vient de l'écran CAST, de la norme ISO/IEC 5055 ou de notre dépôt.
Les `[…]` sont à remplir **après** l'analyse réelle (étape 5).

| # | Durée | À l'écran (clics) | À dire | Source |
|---|---|---|---|---|
| 1 | 0:00–0:40 | Diapo titre, puis la page d'accueil de DomiAffaire (localhost:4200) | « L'ISO/IEC 5055 mesure quatre caractéristiques du code source : sécurité, fiabilité, efficacité de performance et maintenabilité. Le score est le **nombre d'occurrences** de faiblesses CWE (clause 9). Nous appliquons la norme à une vraie application de l'équipe : DomiAffaire, en Spring Boot et Angular. » | ISO/IEC 5055, 1.2 et 9 |
| 2 | 0:40–1:10 | castimaging.io → la liste des applications | « CAST est le seul éditeur qui documente un support natif de l'ISO 5055. L'analyseur tourne **sur notre PC** : seuls les résultats structurels sont envoyés dans le cloud. » | Doc CAST *Improve / Explore* |
| 3 | 1:10–1:40 | Court extrait : profilage puis analyse (barre de progression) | « Nous analysons une copie propre : le backend Java, le service de chat et le front Angular, soit environ 28 500 lignes. Les tests, les bibliothèques tierces et le template acheté sont exclus. » | `cast/guide.md`, partie C |
| 4 | 1:40–2:20 | Page de synthèse puis vue d'architecture (couches, technologies) | « CAST reconstruit l'architecture : Angular appelle l'API, l'API appelle MongoDB. On voit aussi le service de chat, qui accède à la base **sans** passer par l'authentification. » | Écran CAST |
| 5 | 2:20–3:30 | ISO-5055 → **Sécurité** → règle `[…]` → objet → graphe → remédiation | « En sécurité, CAST relève `[X]` violations. Par exemple `[règle]` dans `[fichier]`. Notre revue manuelle avait trouvé la clé JWT codée en dur, CWE-321, une faiblesse de la clause 7.4.17. `[CAST la trouve / ne la trouve pas]`. » | Écran CAST, ISO 7.4.17, nos constats S04 et S14 |
| 6 | 3:30–4:20 | ISO-5055 → **Fiabilité** → une violation | « En fiabilité, `[X]` violations. Par exemple le retour de `findById` utilisé sans vérification, CWE-252, ou un déréférencement nul, CWE-476. » | ISO 7.3.13 et 7.3.27, constats R01 et R02 |
| 7 | 4:20–5:10 | ISO-5055 → **Efficacité de performance** → une violation | « En performance, `[X]` violations : des accès à la base **dans des boucles**, CWE-1050, et des méthodes qui font trop de requêtes, CWE-1073. » | ISO 7.2.18 et 7.2.6, constats P04 et N01 |
| 8 | 5:10–5:40 | **Maintenabilité** si elle est disponible ; sinon le menu qui montre son absence | Si elle est disponible : « `[X]` violations, dont le fichier de 1 585 lignes (seuil ISO : 1 000, CWE-1080). » Sinon : « La version d'essai affiche trois caractéristiques sur quatre ; la maintenabilité sera mesurée avec SonarQube. » | ISO 7.1.26, constat M01 |
| 9 | 5:40–6:30 | Diapo de comparaison (tableau tiré de `reports/05-cast-vs-claude.md`) | « Comparons. La revue manuelle avec la norme estimait `[182 / 86 / 48 / 31]` occurrences ; CAST en compte `[…]`. CAST trouve `[…]` que nous avions manqué. En revanche, **aucun outil ISO 5055** ne signale que n'importe quel client peut supprimer n'importe quel compte : le contrôle d'accès n'est pas dans la liste de la norme. » | `reports/03-review-iso.md`, résultat CAST |
| 10 | 6:30–7:00 | Diapo de conclusion | « L'ISO 5055 rend la qualité **mesurable et comparable**, à condition d'automatiser le comptage (clause 2). Ce n'est pas un audit de sécurité complet : on la combine avec des tests et une revue des autorisations. » | ISO 1.2 et 2 |

## Conseils d'enregistrement
- **Préparer le terrain :** répéter une fois sur l'application de démo de CAST ; ouvrir à l'avance tous les onglets nécessaires.
- **Garder un rythme lent :** parler lentement ; marquer une pause d'une seconde avant chaque clic ; zoomer à 125 %.
- **Découper l'enregistrement :** enregistrer scène par scène (une erreur ne refait qu'une scène), puis assembler dans Clipchamp.
- **Protéger les données :** ne jamais afficher de mot de passe, de jeton ni le fichier `api/config/application.properties`.
