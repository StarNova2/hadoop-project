# Machine learning

But : proposer un modèle qui défini notre santé mentale selon nos habitudes (d'après les données recueillies)
proposition : 
- Clustering K-Means pour déduire certains penchants
- MLP pour voir les différences de résultat


# 1. Transformation
Le but ici est de transformer certaines données pour qu'elles puissent correspondre à la logique du clustering (seulement des nombres)
Donc par exemple : 
- rempalcer les genres des nombres (Homme = 1, Autre = 0, Femme = -1)
- remplacer les valeurs "grandissantes" par une suite de nombre (Insomnia = -1, Very Poor = -0.5, Poor = 0, Fair = 0.5, Good = 1)

Après réflexion : 
Le clustering K-Means se base sur la distance entre les données. Il faudra donc trouver une logique entre les différentes données.
Dans un premier temps, je préfère ne pas trop toucher au données déjà en nombre, même si dans l'idée, je voudrais transformer les données pour dire : plus elle est dans le négative, moins c'est bien, plus elle est dans le positif, mieux c'est 

Pour transformer le reste des données string en valeur numérique, il faut d'abord réfléchir sur comment pourrais l'interpréter le modèle. Car en théorie, ce n'est pas parce que un homme = -1 qu'il est plus négative qu'une femme à 1.

Il faut donc séparer la collonne en 3 colonnes : 
- une colonne qui dit 1 si c'est un homme, si ce n'est pas le cas --> 0
- une colonne qui dit 1 si c'est une femme, si ce n'est pas le cas --> 0
- une colonne qui dit 1 si c'est un autre, si ce n'est pas le cas --> 0

Avec ceci, le modèle pourras seulement différencier si c'est un homme ou pas, une femme ou pas un autre ou pas. 
Je vais utiliser la même logique avec les string qui ne peut pas être comparer (comme le genre de jeu)

De plus, toujours dans la logique du clustering k-means, il serais mieux de standariser les valeur vers 0, entre -1 et 1

avant de faire une annalyse, je regroupe les lignes par rapport aux cluster (en faisant une mooynenne) et je les classe des plus risqué au moins risqué sur l'addiction :
[text](../donnee/moyennes_cluster5_seed1.txt)

- les 5 clusters sont tous dans une moyenne de 18 ans --> peut être pas assez de cluster ou de donnéespour montrer des variances
- le rique d'addiction pars bien du moins disqué avec 0,97 pour le cluster 2, a -0,70 pour le cluster 1 --> on remarque qu'on passe à peu de rique (0,97 - 0,9) à d'un coup plus de risque (-0,1 - -0,70) --> les écart semble trop grand, même remaque qu'avant -> peut être pas assez de cluster ou de donnéespour montrer des variances
- le nombre d'heure à un véritable impact sur l'addiction --> pour une recommandation de 7 à 9h pour les 18-25 ans (d'après le centre de Douglas : https://douglas.research.mcgill.ca/fr/sommeil-et-enfant-donnees-scientifiques/), on vois bien une séparation entre les 4h et les 7~6h de someil

Je vu les écarts, je pense qu'il manque qu'il y a pas assez de cluster. Je vais vérifier avec une autre seed : 
[text](../donnee/moyennes_cluster5_seed2.txt)

A première vu il y a une varaiance en plus au niveau de l'âge, le risque d'addiction est un peu plus stable, mais mieux vaut rajouter des cluster pour la suite, les genre de jeu + plateforme

Néanmoins, je m'intérogeais sur la transformation de certaine valeur. Est ce qu'il faudrais mettre les valeur basses comme "négative" et les valeur haute comme "positive" ?
Mon constat est qu'on à pas besoin, car par exemple, pour la perte d'intéressement, vrai = 1, faux = 0
Et ici on voit bien que le cluster le moins impacté par des risque d'addiction aux jeu est à 0,07 comparé au cluster le plus impacté à 0,58

Donc le modèle arrive bien à "comprendre" que la distance entre colonne n'est pas lié de la même manière, et que même si une colonne est à -1, une autre colonne peut être lié à elle en étant à 1