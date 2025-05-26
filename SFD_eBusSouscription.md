# Spécifications PubSub <!-- omit in toc -->

## Historique <!-- omit in toc -->

| Version | Date       | User Story                                                                                                                      | Fait par | Validé par |
|---------|------------|---------------------------------------------------------------------------------------------------------------------------------|----------|------------|
|         | 21/09/2021 | FB-1061 -- Bouton retour dans le détail d'une publication/souscription                                                          | TMA OSB  |            |
|         | 28/09/2021 | FB-2051 -- [PUB/SUB] Routing key - Publication V1                                                                               | TMA OSB  |            |
|         | 04/10/2021 | FB-2052 -- [PUB/SUB] Routing key - Souscription V1                                                                              | TMA OSB  |            |
|         | 12/10/2021 | FB-1069 -- [PUB/SUB] Créer souscription V2                                                                                      | TMA OSB  |            |
|         | 23/11/2021 | FB-2327 -- [PUB/SUB] Enlever les champs techniques                                                                              | TMA OSB  |            |
| 1.2.0   | 07/01/2021 | FB-1064 -- [PUB/SUB] Catalogue - mise en page + filtre dynamique                                                                | TMA OSB  |            |
| 1.2.0   | 18/01/2022 | FB-2039 -- [PUB/SUB] Détail publication - Ajouter une section "souscriptions validées"                                          | TMA OSB  |            |
| 1.3.0   | 15/02/2022 | FB-2624 -- [PUB/SUB] Versionning                                                                                                | TMA OSB  |            |
| 1.4.0   | 07/03/2022 | FB-2569 -- [PUB/SUB] Ajout des routing pattern dans les souscriptions en attente et validées                                    | TMA OSB  |            |
| 1.4.0   | 07/03/2022 | FB-2444 -- [PUB/SUB] Enlever infos techniques de l'application                                                                  | TMA OSB  |            |
| 1.4.0   | 07/03/2022 | FB-2625 -- [PUB/SUB] Check box par défaut                                                                                       | TMA OSB  |            |
| 1.5.0   | 31/03/2022 | FB-2625 -- [PUB/SUB] Publication à usage interne                                                                                | TMA OSB  |            |
| 1.5.0   | 06/04/2022 | FB-2910 -- [PUB/SUB] Demande de déploiement suite à l'édition d'une souscription                                                | TMA OSB  |            |
| 1.5.0   | 13/04/2022 | FB-1068 -- [PUB/SUB] Mail pour notifier au fournisseur qu'il a une validation en attente                                        | TMA OSB  |            |
| 1.6.0   | 03/05/2022 | FB-2950 -- [Monitoring] Nouveau portail de monitoring eBUS                                                                      | TMA OSB  |            |
| 1.6.0   | 03/05/2022 | FB-2961 -- [Monitoring] Nouveau portail de monitoring eBUS - Détail des logs par message                                        | TMA OSB  |            |
| 1.7.1   | 18/05/2022 | FB-3251 -- [Monitoring] Ajouter le nom de l'application fournisseur dans le formulaire de recherche                             | TMA OSB  |            |
| 1.8.0   | 01/06/2022 | FB-3241 -- [PUB/SUB] Modifier le libellé du statut du déploiement en prod                                                       | TMA OSB  |            |
| 1.9.0   | 29/07/2022 | FB-2954 -- [PUB/SUB] Ajout de critères de recherche des logs (recherche avancée)                                                | TMA OSB  |            |
| 1.9.0   | 22/08/2022 | FB-1059 -- [PUB/SUB] Ajout d'un filtre de recherche par Application dans "Mes Applications"                                     | OBS      |            |
| 1.10.0  | 12/09/2022 | FB-3646 -- [PUB/SUB] double clic ou second clic sur le bouton valider à ne pas prendre en compte                                | OBS      |            |
| 1.11.0  | 19/12/2022 | FB-3268 -- [PUB/SUB] PURGE a subscription stream instance                                                                       | OBS      |            |
| 1.12.0  | 20/12/2022 | FB-3271 -- [eBUS PUB/SUB] DISABLE a subscription stream instance                                                                | OBS      |            |
| 1.13.0  | 22/02/2023 | FB-4199 -- [PUB/SUB] [DTSI] Créer/update application: OBS ou DTSI                                                               | OBS      |            |
| 1.14.0  | 05/04/2023 | FB-4192 -- [PUB/SUB] Vérifier si le Client ID n'existe pas déjà                                                                 | OBS      |            |
| 1.15.0  | 08/05/2023 | FB-4474 -- [PUB/SUB] Bouton Créer Stream INSTANCE                                                                               | OBS      |            |
| 1.16.0  | 04/07/2023 | FB-4694 -- [PUB/SUB] Mode single Ack                                                                                            | OBS      |            |
| 1.17.0  | 01/08/2023 | FB-4836 -- [PUB/SUB] DELETE a stream INSTANCE de PUBLICATION                                                                    | OBS      |            |
| 1.18.0  | 01/08/2023 | FB-4685 -- [PUB/SUB] Page catalogue -> ajout de la description fonctionnelle                                                    | OBS     |          |
| 1.19.0  | 05/09/2023 | FB-4055 -- [PUB/SUB] DELETE a STREAM de SOUSCRIPTION                                                                            | OBS      |            |
| 1.20.0  | 05/09/2023 | FB-3272 -- [PUB/SUB] Ajout du valideur et de la date + env consomateur                                                          | OBS      |            |
| 1.21.0  | 05/09/2023 | FB-2329 -- [PUB/SUB] Mettre à jour une publication : routing key check box si deja des souscriptions                            | OBS      |            |
| 1.22.0  | 13/10/2023 | FB-4908 -- [PUB/SUB] [PUB/SUB] DELETE a STREAM de PUBLICATION                                                                   | OBS      |            |
| 1.25.0  | 05/12/2023 | FB-4193 -- [Monitoring] Ajoutez le champ "Paramètres" associé aux paramètres pour pouvoir effectuer une recherche des messages. | OBS      |            |
| 1.26.0  | 16/01/2024 | FB-5227 -- [PUBLICATION] changer le libellé "publication à usage interne"                                                       | OBS      |            |
| 1.27.0  | 17/01/2024 | FB-4057 -- [PUB/SUB] DELETE an environnement                                                                                    | OBS      |            |
| 1.28.0  | 13/02/2024 | FB-5235 -- [PUB/SUB] [eBUS] Refacto - pas de réplica entre les BDD eBUS et zBus-admin (IMPLEMENTATION)                          | OBS      |            |
| 1.28.0  | 19/02/2024 | FB-5317 -- [PUB/SUB] [PUB/SUB] Maximum number of messages to acknowledge                                                        | OBS      |            |
| 1.32.0  | 05/07/2024 | FB-4056 -- [PUB/SUB] [PUB/SUB] Delete an application                                                                            | OBS      |            |
| 1.33.0  | 06/03/2025 | FB-5889 -- [PUB/SUB] [eBUS] validation de souscription: ajout de l'environnement et de la révocation                                                                             | OBS      |            |

## Table des matières <!-- omit in toc -->

- [1. Introduction](#1-introduction)
  - [1.1. Documents de référence](#11-documents-de-référence)
- [2. Page de démarrage / Accueil](#2-page-de-démarrage--accueil)
  - [2.1. Maquette](#21-maquette)
  - [2.2. Composition](#22-composition)
  - [2.3. Liste des champs du bandeau](#23-liste-des-champs-du-bandeau)
- [3. Menu Catalogue](#3-menu-catalogue)
  - [3.1. Cinématique des écrans](#31-cinématique-des-écrans)
  - [3.2. Maquette](#32-maquette)
  - [3.3. Composition](#33-composition)
- [4. Ecran « Mes Applications »](#4-ecran--mes-applications-)
  - [4.1. Maquette](#41-maquette)
  - [4.2. Composition](#42-composition)
  - [4.3. Diagramme de séquence](#43-diagramme-de-séquence)
- [5. Création d'une application](#5-création-dune-application)
  - [5.1. Cinématique des écrans](#51-cinématique-des-écrans)
  - [5.2. Diagramme de séquence](#52-diagramme-de-séquence)
  - [5.3. Maquette](#53-maquette)
  - [5.4. Composition](#54-composition)
- [6. Edition d'une application](#6-edition-dune-application)
  - [6.1. Cinématique des écrans](#61-cinématique-des-écrans)
  - [6.2. Diagramme de séquence](#62-diagramme-de-séquence)
- [7. Détail d'une application](#7-détail-dune-application)
  - [7.1. Cinématiques des écrans](#71-cinématiques-des-écrans)
  - [7.2. Maquette](#72-maquette)
  - [7.3. Informations générales](#73-informations-générales)
  - [7.4. Orange Developer Inside](#74-orange-developer-inside)
    - [7.4.1. Condition d'affichage](#741-condition-daffichage)
    - [7.4.2. Composition](#742-composition)
  - [7.5. Listes des environnements](#75-listes-des-environnements)
  - [7.5.1 Diagramme de séquence création d'environnement](#751-diagramme-de-séquence-création-denvironnement)
  - [7.5.2 Diagramme de séquence suppression d'environnement](#752-diagramme-de-séquence-suppression-denvironnement)
  - [7.6. Listes des publications](#76-listes-des-publications)
    - [7.6.1. Maquette](#761-maquette)
    - [7.6.2. Composition](#762-composition)
  - [7.7. Liste des souscriptions](#77-liste-des-souscriptions)
    - [7.7.1. Maquette](#771-maquette)
    - [7.7.2. Composition](#772-composition)
  - [7.8. Liste des demandes de souscription à valider](#78-liste-des-demandes-de-souscription-à-valider)
    - [7.8.1. Maquette](#781-maquette)
    - [7.8.2. Condition d'affichage](#782-condition-daffichage)
    - [7.8.3. Composition](#783-composition)
    - [7.8.4. Diagramme de séquence](#784-diagramme-de-séquence)
  - [7.9. Liste des gestionnaires de l'application](#79-liste-des-gestionnaires-de-lapplication)
    - [7.9.1. Maquette](#791-maquette)
    - [7.9.2. Condition d'affichage](#792-condition-daffichage)
  - [7.10. Composition](#710-composition)
    - [7.10.1. Diagramme de séquence de la gestion des gestionnaires d'application](#7101-diagramme-de-séquence-de-la-gestion-des-gestionnaires-dapplication)
  - [7.11. Validation du formulaire](#711-validation-du-formulaire)
  - [7.12. Diagramme de séquence](#712-diagramme-de-séquence)
- [8. Détail d'une publication](#8-détail-dune-publication)
  - [8.1. Cinématique des écrans](#81-cinématique-des-écrans)
    - [8.1.1. Création d'une publication](#811-création-dune-publication)
    - [8.1.2. Consultation d'une publication](#812-consultation-dune-publication)
    - [8.1.3. Suppression d'une publication instance](#813-suppression-dune-publication-instance)
    - [8.1.4. Révocation d'une souscription associée](#814-révocation-dune-souscription-associée)
  - [8.2. Maquettes](#82-maquettes)
    - [8.2.1 Création d'une publication](#821-création-dune-publication)
    - [8.2.2. Consultation d'une publication](#822-consultation-dune-publication)
    - [8.2.3. Suppression d'une publication](#823-suppression-dune-publication)
  - [8.3. Composition](#83-composition)
    - [8.3.1. Diagramme de séquence Création de publication](#831-diagramme-de-séquence-création-de-publication)
  - [8.4. Création d'une instance de publication](#84-création-dune-instance-de-publication)
    - [8.4.1 Diagramme de séquence](#841-diagramme-de-séquence)
  - [8.5. Suppression d'une instance de publication](#85-suppression-dune-instance-de-publication)
    - [8.5.1 Diagramme de séquence](#851-diagramme-de-séquence)
  - [8.6. Révocation d'une souscription associée à la publication](#86-révocation-dune-souscription-associée-à-la-publication)
    - [8.6.1 Diagramme de séquence](#851-diagramme-de-séquence)
- [9. Détail d'une souscription](#9-détail-dune-souscription)
  - [9.1. Cinématique des écrans](#91-cinématique-des-écrans)
    - [9.1.1. Consultation d'une souscription](#911-consultation-dune-souscription)
    - [9.1.2. Création d'une souscription](#912-création-dune-souscription)
  - [9.2. Maquette](#92-maquette)
    - [9.2.1. Consultation d'une souscription](#921-consultation-dune-souscription)
    - [9.2.2. Création d'une souscription](#922-création-dune-souscription)
    - [9.2.3. Suppression d'une souscription](#923-suppression-dune-souscription)
  - [9.3. Composition](#93-composition)
  - [9.5. Création de souscription](#95-création-de-souscription)
    - [9.5.1 Diagramme de séquence](#951-diagramme-de-séquence)
  - [9.6. Création de souscription instance](#96-création-de-souscription-instance)
    - [9.6.1 Diagramme de séquence](#961-diagramme-de-séquence)
    - [9.6.2 Édition souscription](#962-édition-souscription)
  - [9.7 Purge de souscription instance](#97-purge-de-souscription-instance)
    - [9.7.1 Diagramme de séquence](#971-diagramme-de-séquence)
  - [9.8. Activation/Désactivation d'une souscription instance](#98-activationdésactivation-dune-souscription-instance)
    - [9.8.1 Diagramme de séquence pour activation](#981-diagramme-de-séquence-pour-activation)
    - [9.8.2 Diagramme de séquence pour désactivation](#982-diagramme-de-séquence-pour-désactivation)
  - [9.9. Suppression d'une souscription instance](#99-suppression-dune-souscription-instance)
    - [9.9.1 Diagramme de séquence pour suppression](#991-diagramme-de-séquence-pour-suppression)
- [10. Menu Monitoring](#10-menu-monitoring)
  - [10.1. Maquette](#101-maquette)
  - [10.2. Composition](#102-composition)
- [11. Détail des logs d'un message](#11-détail-des-logs-dun-message)
  - [11.1. Maquette](#111-maquette)
  - [11.2. Composition](#112-composition)
- [12. Gestion des erreurs côté portail](#12-gestion-des-erreurs-côté-portail)
  - [12.1. Envoi d'un e-mail à zbus](#121-envoi-dun-e-mail-à-zbus)
  - [12.2. Utilisation de l'API MAIL ENABLER](#122-utilisation-de-lapi-mail-enabler)
- [13. Aide](#13-aide)
  - [13.1. Cinématique d'accès à l'écran d'aide](#131-cinématique-daccès-à-lécran-daide)
  - [13.2. Maquette](#132-maquette)
  - [13.3. Composition](#133-composition)

## 1. Introduction

### 1.1. Documents de référence

| Nom du document      | Référence          | Version | Date       |
|----------------------|--------------------|---------|------------|
| SFG_eBusSouscription | 20200325-160311-NA | 1.0     | 25/03/2020 |

## 2. Page de démarrage / Accueil

### 2.1. Maquette

![](media/myapplis.png)

### 2.2. Composition

La page de démarrage est la page « Mes Applications ». Elle comporte un bandeau de navigation noir qui est présent sur toutes les pages de l'application, à l'identique.

### 2.3. Liste des champs du bandeau

| Type                                        | Description                     | Action                                               |
|---------------------------------------------|---------------------------------|------------------------------------------------------|
| Image                                       | Logo Orange                     | Cliquable. Retour à la page de démarrage.            |
| Texte                                       | Nom de l’application : « eBus » | Cliquable. Retour à la page de démarrage.            |
| Texte/menu                                  | Menu « Catalogue »              | Aller à la page de Catalogue.                        |
| Texte/menu                                  | Menu « Mes Applications »       | Aller à la page « Mes Applications »                 |
| Image « silhouette » + Nom de l’utilisateur | Menu déroulant                  | Accès à 1 fonctionnalité : Déconnexion.              |
| Image : silhouette de helpdesk              | Image cliquable                 | Afficher le lien vers le servicedesk.                |
| Image : symbole de mappemonde               | Image cliquable                 | Change la langue de la page. Recharge la page.       |
| Texte : « aide »                            |                                 | Affichage de l’aide contextuelle de la page courante |

En bas de page se trouve la version de l'application.

## 3. Menu Catalogue

### 3.1. Cinématique des écrans

![](media/cinematique_catalogue.png)

Ce menu est accessible à tous les utilisateurs.

### 3.2. Maquette

![](media/catalogue.png)

### 3.3. Composition

**Formulaire de recherche** :

| Champ                 | Type          | Action                                                                                                                                           |
|-----------------------|---------------|--------------------------------------------------------------------------------------------------------------------------------------------------|
| Nom de la publication | Champ libre   | 3 à 6 caractères numériques                                                                                                                      |
| Nom de l'application  | Champ libre   | Lettres et espaces seulement. 25 caractères max.                                                                                                 |
| Tags                  | Champ libre   | Lettres seulement. Recherche parmi les tags des applications et des publications/souscriptions. 250 caractères max.                              |
| Production            | Bouton à séléctionner | Choix. La recherche s’effectuera uniquement sur les applications ayant des publications et/ou souscriptions en environnement de production.      |
| Hors Production       | Bouton à séléctionner | Choix. La recherche s’effectuera uniquement sur les applications ayant des publications et/ou souscriptions en environnement de hors production. |
| OBS                   | Bouton à séléctionner | Choix. La recherche s’effectuera uniquement sur les applications ayant le périmètre OBS. |
| OFR                  | Bouton à séléctionner | Choix. La recherche s’effectuera uniquement sur les applications ayant le périmètre OFR. |
| INN                  | Bouton à séléctionner | Choix. La recherche s’effectuera uniquement sur les applications ayant le périmètre INN. |
| OWF                  | Bouton à séléctionner | Choix. La recherche s’effectuera uniquement sur les applications ayant le périmètre OWF. |
| OSP                  | Bouton à séléctionner | Choix. La recherche s’effectuera uniquement sur les applications ayant le périmètre OSP. |
| OPL                  | Bouton à séléctionner | Choix. La recherche s’effectuera uniquement sur les applications ayant le périmètre OPL. |
| OCA                  | Bouton à séléctionner | Choix. La recherche s’effectuera uniquement sur les applications ayant le périmètre OCA. |
| MEA                  | Bouton à séléctionner | Choix. La recherche s’effectuera uniquement sur les applications ayant le périmètre MEA. |
| ORM                  | Bouton à séléctionner | Choix. La recherche s’effectuera uniquement sur les applications ayant le périmètre ORM. |
**Tableaux de résultats** :

| Libellée                     | Type                                  | Description                                                                                                                                                                                                                                                                                     |
|------------------------------|---------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Tableau de résultats         | Tableau                               | Le tableau d’affichage des résultats. Les résultats peuvent être triés en sélectionnant la colonne concernée.                                                                                                                                                                                   |
| Pagination                   | Numérotation et flèches de navigation | Apparaît au-dessus du tableau, centrée. 25 applications sont affichées par page                                                                                                                                                                                                                 |
| Nombre de résultats renvoyés | Texte                                 | Apparaît au-dessus, sur la gauche du tableau.  Contient le nombre de publications trouvées suivi du libellé « Publication(s) retournée(s) ».                                                                                                                                                    |
| Bouton d’export Excel        | Bouton (image cliquable)              | Permet d’exporter les données du tableau au format Excel dans un fichier nommé « export.xlsx ».   Toutes les données présentes dans le tableau sont exportées (pas uniquement la page courante). Toutes les données présentes dans le tableau sont exportées (pas uniquement la page courante). |
| Nom de la publication        | Colonne                               | Nom de la publication associée                                                                                                                                                                                                                                                                  |
| Version                      | Colonne                               | Version de la publication                                                                                                                                                                                                                                                                       |
| Environnement                | Colonne                               | Environnement de la publication                                                                                                                                                                                                                                                                 |
| Nom de l’application         | Colonne                               | Nom des applications retournées.                                                                                                                                                                                                                                                                |
| Description fonctionnelle    | Colonne                               | Courte description fonctionnelle des données exploitées par la publication.                                                                                                                                                                                                                                                               |
| Tags                         | Colonne                               | Mots-clés en rapport avec la publication.                                                                                                                                                                                                                                                       |
| Gestionnaire                 | Colonne                               | Le nom du gestionnaire principal pour cette application. Ce contact sera considéré comme le référent de l’application. Ce contact est modifiable par un gestionnaire de l’application, et à choisir parmi les gestionnaires de l’application.                                                   |
| Mail de contact              | Colonne                               | Adresse mail de contact pour cette application. Cette adresse n’est pas liée aux CUID gestionnaires de l’application. Il est préconisé de référencer une adresse mail générique dans ce champ.                                                                                                  |
| S'abonner                    | Colonne                               | Bouton permettant à se souscrire à la publication affichée.                                                                                                  |

Le nom de l'application est cliquable et permet d'accéder à la page de détail de cette application.
Le nom de la publication est cliquable et permet d'accéder à la page de détail de cette publication.

Seront retourné les publications qui correspondront aux champs saisis dans le formulaire. Seules les publications publiques seront retournées

## 4. Ecran « Mes Applications »

### 4.1. Maquette

![](media/myapplis.png)

### 4.2. Composition

| Libellé                         | Description                                                                                |
|---------------------------------|--------------------------------------------------------------------------------------------|
| Champ « Nom de l'application »  | Ce champ permet de filtrer l’affichage des tuiles application par le nom de l'application. |
| Bouton « Création application » | Ce bouton renvoie vers la page création d’une application                                  |
| Tuiles                          | Les tuiles sont cliquables et renvoient vers le détail d’une application.                  |

Chaque tuile contient ces informations :

- Nom de l’application
- Gestionnaire
- Contact
- Entité

Pour un utilisateur au profil ADMIN, toutes les applications sont visibles.
Pour un utilisateur de profil PROJET, seules les applications dont l’utilisateur connecté est gestionnaire, sont visibles.

### 4.3. Diagramme de séquence

![](media/sequence_myapps.png)

## 5. Création d'une application

### 5.1. Cinématique des écrans

![](media/cinematique_new_app.png)

### 5.2. Diagramme de séquence

![](DiagrammeSequence/application_create.seq.png)

### 5.3. Maquette

![](media/create_application.png)

### 5.4. Composition

| Libellé                                                  | Type                     | Description                                                                                                                   | Editable en modification |
|----------------------------------------------------------|--------------------------|-------------------------------------------------------------------------------------------------------------------------------|--------------------------|
| ID Orange Carto                                          | Champ libre, obligatoire | 3 à 6 caractères les chiffres sont les seuls caractères autorisés. Vérification de la validité du formulaire à la validation. | Non                      |
| Nom de l’application                                     | Champ verrouillé         | La valeur est récupérée automatiquement d’Orange Carto                                                                        | Oui                      |
| Description                                              | Champ verrouillé         | La valeur est récupérée automatiquement d’OrangeCarto. Ce champ est limité à 250 caractères.                                  | Oui                      |
| Périmètre de l'application                               | champ verrouillé, obligatoire  |Il a 9 valeurs possibles OBS (OBS	Orange Business) \ OFR	(Orange France) \ INN	(Orange Innovation) \ OWF	(Orange Wholesale France) \ OSP	(Orange Spain) \ OPL	(Orange Poland) \ OCA	(Orange Caraibes) \ MEA	(Orange Middle East Africa) \ ORM	(Orange Réunion Mayotte)                      | Non |
| Nom du contact                                           | Champ libre              |                                                                                                                               | Oui                      |
| Adresse mail de contact                                  | Champ libre, obligatoire | Indiquer ici une adresse mail générique. 60 caractères max.                                                                   | Oui                      |
| Tags (mots clés, mots fonctionnels liés à l’application) | Champ libre              | Chaque tag est à séparer par un point-virgule. Pas de caractères spéciaux. 250 caractères max.                                | Oui                      |
| ID Client ODI Orange France NON-PROD                     | Champ libre, obligatoire et unique | Doit respecter le format /^cli-[a-z0-9_-]+$/. Ce champ est limité à 100 caractères.                                           | Oui                      |
| ID Client ODI Orange France PROD                         | Champ libre, obligatoire et unique | Doit respecter le format /^cli-[a-z0-9_-]+$/. Ce champ est limité à 100 caractères.                                           | Oui                      |

## 6. Edition d'une application

### 6.1. Cinématique des écrans

![](media/cinematique_edit_app.png)

L’écran d’édition est similaire visuellement (maquette) et fonctionnellement (validation) à la création d’application.
Cf. composition de l’écran de la création d’application ci-dessus pour connaitre la liste des champs éditable.

Lors de la mise à jour du mailing "Adresse mail de contact", la liste des contacts de l'application est mise à jour dans zBus via l'API d'admin PUT Application avec la liste exhaustive des contacts.

Lors de la mise à jour de client ID de PROD, un message temporaire dans une pop-up verte s'affiche "Demande soumise -> Mise à jour du client ID de PROD sous 48h", et en cas d'une modification des deux clients ID (PROD, NON PROD) un message temporaire dans une pop-up verte s'affiche "Demande soumise -> Mise à jour du client ID de NON PROD sous 24h. Mise à jour du client ID de PROD sous 48h"

### 6.2. Diagramme de séquence

![](DiagrammeSequence/application_edit.seq.png)

## 7. Détail d'une application

### 7.1. Cinématiques des écrans

![](media/cinematique_myapps.png)

### 7.2. Maquette

![](media/detail_app_0.png)

![](media/detail_app_1.png)

![](media/detail_app_2.png)

### 7.3. Informations générales

| Libellé                                                  | Description                                                                                |
|----------------------------------------------------------|--------------------------------------------------------------------------------------------|
| Nom de l’application                                     | L'information est récupérée automatiquement d'Orange Carto selon l’ID.                     |
| ID Orange Carto                                          | 3 à 6 caractères numériques. La validité est vérifiée lors de la validation du formulaire. |
| Description                                              | L'information est récupérée automatiquement d'Orange Carto selon l’ID.                     |
| Gestionnaire                                             | Prénom et nom du gestionnaire principal de l’application                                   |
| Nom du contact                                           | L'information est récupérée automatiquement d'Orange Carto selon l’ID.                     |
| Adresse mail de contact                                  | Adresse mail générique. Limité à 60 caractères.                                            |
| Tags (mots clés, mots fonctionnels liés à l’application) | Liste des tags séparés par un point-virgule. Limité à 250 caractères.                      |

### 7.4. Orange Developer Inside

#### 7.4.1. Condition d'affichage

Ce bloc est affiché pour les utilisateurs de profil ADMIN et les utilisateurs gestionnaire de cette application.

#### 7.4.2. Composition

L'API ASAP, permettant de créer une souscription à Orange Developer Inside n'est pas encore disponible, eBus
Souscription ne gèrera donc pas dans un premier temps la souscription à Orange Developer Inside. En attendant la mise en
place de cette évolution, un message indique à l'utilisateur qu'il peut suivre les souscriptions aux API attachées aux
applications sur le portail ODI avec un lien hypertexte sur « portail ODI » qui débranche vers le portail
ODI "https://developer-inside.sso.infra.ftgroup".

**Boutons d'action de l'application** :

| Libellé   | Description                        |
|-----------|------------------------------------|
| Editer    | Permet de modifier l'application.  |
| Supprimer | Permet de supprimer l’application. |

### 7.5. Listes des environnements

Deux tableaux seront présents: un pour les environnements de hors production, et un pour les environnements de production.

![](media/detail_app_environments.png)

Ces tableaux comporteront 4 lignes en hors production, 2 lignes pour la production.

La création d'un nouvel environnement s'effectue en renseignant directement dans une ligne vierge du tableau. Pour que
la création d\'un nouvel environnement pour une application soit valide, le nom de l'environnement doit être unique. Chaque ligne est modifiable.

| Libellé     | Description                                                                                                                                                                                                                |
|-------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Nom         | Nom de l’environnement (exemple : pexp). Lettres minuscules et chiffres seulement, 2 à 5 caractères.                                                                                                                       |
| Description | Description brève de l’environnement (exemple : Préproduction). Limité à 50 caractères.                                                                                                                                    |
| Actions     | Pour les utilisateurs de profil ADMIN et les utilisateurs gestionnaire de cette application, un bouton « enregistrer » permet d’envoyer à zBus toute modification d’un environnement déployé ou en attente de déploiement. |

### 7.5.1 Diagramme de séquence création d'environnement

![](DiagrammeSequence/environement_create.seq.png)

### 7.5.2 Diagramme de séquence suppression d'environnement

S'il n'existe pas des publications/souscriptions instances associées à un environnement on peut faire la suppression en cliquant sur l'icône de suppression dans la colonne "Actions", cette opération permet de supprimer la souscription dans eBus et zBus.

![](DiagrammeSequence/environment_delete_seq.png)

### 7.6. Listes des publications

#### 7.6.1. Maquette

![](media/detail_app_publishers.png)

#### 7.6.2. Composition

| Libellé               | Description                             |
|-----------------------|-----------------------------------------|
| Nom de la publication | Nom du flux.                            |
| Numéro de version     | Numéro de version du flux.              |
| Tags                  | Liste des tags séparés par une virgule. |

Pour les utilisateurs de profil ADMIN et les utilisateurs gestionnaire de cette application, un bouton permet de créer une nouvelle publication. Toutes les lignes sont cliquables et permettent d'aller à l'écran de [détail d'une publication](#712-consultation-dune-publication). Le nombre de lignes affichées dans le tableau est ici limité à 10.

### 7.7. Liste des souscriptions

#### 7.7.1. Maquette

![](media/detail_app_consumers.png)

#### 7.7.2. Composition

| Libellé                   | Description                                |
|---------------------------|--------------------------------------------|
| Nom de la souscription    | Nom du flux paramétré côté souscription    |
| Tags                      | Liste des tags séparés par une virgule     |
| Nom publication           | Nom du flux publié auquel ce flux souscrit |
| Version de la publication | Numéro de version de la publication        |

Pour les utilisateurs de profil ADMIN et les utilisateurs gestionnaire de cette application, un bouton permet de créer une nouvelle souscription. Toutes les lignes sont cliquables et permettent d'aller à l'écran de [détail d'une souscription](#811-consultation-dune-souscription). Le nombre de lignes affichées dans le tableau est ici limité à 10.

### 7.8. Liste des demandes de souscription à valider

#### 7.8.1. Maquette

![](media/detail_app_consumers_to_validate.png)

#### 7.8.2. Condition d'affichage

Ce bloc est affiché pour les utilisateurs de profil ADMIN et les utilisateurs gestionnaire de cette application.

#### 7.8.3. Composition

| Libellé                       | Description                                                           |
|-------------------------------|-----------------------------------------------------------------------|
| Nom de la publication         | Nom du flux pour lequel une demande de souscription a été demandée                                                                                                |
| Version                       | Numéro de version du flux pour lequel la demande de souscription a été demandée                                                                                                |
| Environnement du fournisseur  | L'ensemble des environnements du fournisseur sur lesquels les instances de souscription ont été créées                                                                             |
| Environnement du souscripteur | L'ensembles des environnements du souscripteur sur lesquels les instances de  souscriptions ont été créées                                                                            |
| Règles de routage             | Règles de routage associées à la demande de souscription              |
| Nom de l’application          | Nom de l’application demandant la souscription                        |
| Gestionnaire                  | Nom et prénom de contact de l’application demandant la souscription   |
| Actions                       | Les utilisateurs de profil ADMIN et les utilisateurs gestionnaire de cette application, peuvent « Accepter » ou « refuser » la demande de souscription. En cliquant sur l’une des deux actions, un mail est envoyé à l’adresse mail de contact du demandeur, pour le notifier. La demande est globale à la souscription, si une nouvelle demande est émise avant que la précédente n'ai été validée elle ne sera pas prise en compte. C'est la première demande qui, lorsqu'elle sera validée validera les suivantes. Le fournisseur n'a pas à valider chaque demande pour une même souscription. Si la demande est refusée, celle-ci sera supprimée des souscriptions de l’application demandeuse. Une demande de souscription « en attente de validation » n’est pas créée dans zBus. Ce n’est qu’à la validation par un gestionnaire qu’elle sera créée dans zBus.                |

#### 7.8.4. Diagramme de séquence

![](media/sequence_consumers_to_validate.png)

### 7.9. Liste des gestionnaires de l'application

#### 7.9.1. Maquette

![](media/detail_app_managers.png)

#### 7.9.2. Condition d'affichage

Ce bloc est affiché pour les utilisateurs de profil ADMIN et les utilisateurs gestionnaire de cette application.

Lorsqu'un nouveau gestionnaire est ajouté ou supprimé dans zbus, la liste des contacts de l'application dans zbus est mise à jour via l'API PUT Application avec la liste exhaustive des contacts.

### 7.10. Composition

| Libellé      | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |
|--------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Principal    | Case à cocher. Une seule case peut être cochée à la fois. Permet de modifier le Référent de l’application (celui dont le nom est en visibilité au catalogue). La case à cocher est active seulement pour les utilisateurs de profil ADMIN et les utilisateurs gestionnaire de cette application.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |
| CUID         | CUID du gestionnaire                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| Nom          | Nom et prénom du gestionnaire, tels qu’ils sont retournés par Guardian. Si mise à jour il y a, elle se fera automatiquement à la connexion de l’utilisateur, avec les données renvoyées par le Guardian.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
| Adresse mail | Adresse mail de l’utilisateur. La mise à jour de l’adresse mail se fait à partir des données envoyées par Guardian à la connexion de l’utilisateur.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
| Actions      | Un bouton « Suppression » pour supprimer l’utilisateur de la liste. Chaque gestionnaire de l’application et les utilisateurs de profil ADMIN peuvent supprimer n’importe quel gestionnaire de l’application, en dehors de lui-même et du gestionnaire principal. Pour les utilisateurs de profil ADMIN et les utilisateurs gestionnaires de cette application, un bouton « Création » permet d’ajouter une nouvelle ligne. Le CUID ou le Nom sont alors saisissables, avec une auto-complétion (basée sur les CUID et noms présents en BDD). Le choix du nom rempli automatiquement le CUID et inversement. L’adresse mail est renseignée automatiquement. Le CUID ou le nom saisis doivent être déjà enregistrées dans l’application parmi les gestionnaires possibles. La liste des gestionnaires possibles est constituée des utilisateurs qui se sont déjà connectés à l’application. |

#### 7.10.1. Diagramme de séquence de la gestion des gestionnaires d'application

![](media/sequence_managers.png)

### 7.11. Validation du formulaire

La validation des différentes parties de la page s'effectue partie par partie, via des boutons dédiés pour les
utilisateurs de profil ADMIN et les utilisateurs gestionnaire de cette application. Le clic sur les boutons d'action est
bloqué (présence d'un loader) le temps que les actions (appels au back-end, aux APIs) soient effectués.

### 7.12. Diagramme de séquence

![](media/sequence_app.png)

## 8. Détail d'une publication

### 8.1. Cinématique des écrans

#### 8.1.1. Création d'une publication

![](media/cinematique_new_publisher.png)

#### 8.1.2. Consultation d'une publication

![](media/cinematique_publishers.png)

### 8.1.3 Suppression d'une publication instance
Si Pas de souscription instance associée à une publication instance on peut faire la suppression en cliquant sur l'icône suppression dans la colonne des "Actions",afin de supprimer la stream instance dans zbus et de notre BDD.

Avant la suppression, un message de confirmation s'affichera demandant : "Voulez vous confirmer la suppression ?"

### 8.1.4 Révocation d'une souscription associée
Le bouton qui se trouve dans la colonne "Révocation" du tableau des souscriptions associées permet de révoquer une souscription associée à la publication cette action va supprimer la souscription instance dans notre BDD

### 8.2. Maquettes

#### 8.2.1 Création d'une publication

![](media/new_publisher.png)

#### 8.2.2. Consultation d'une publication

![](media/detail_publisher.png)

#### 8.2.3. Suppression d'une publication
Le bouton supprimer en bas de la page au niveau du détail de la publication permet de supprimer la publication ainsi que toutes ses instances. Cependant, si la publication est associée à au moins une souscription, cette publication ne sera pas supprimée. Cette opération entraîne la suppression de la publication tant dans eBus que dans zBus.

![](DiagrammeSequence/publication_deletion.seq.png)

### 8.3. Composition

**Informations générales de création et de détails d'une publication** :

| Libellé                                                          | Description                                                                                                                                                                                                                                                                                                                                                                                                                            | Editable en modification |
|------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------------------------|
| Nom de la publication                                            | Nom de la publication. Accepte uniquement les minuscules, les chiffres et « _ ». Limité à 50 caractères. Non modifiable après déploiement. Le nom d’une publication est unique pour une application, et ne peut pas être utilisé pour une souscription de la même application. Le message « Nom de publication ou souscription déjà utilisé pour cette application » apparait pour un nom qui est déjà utilisé pour cette application. | Non                      |
| Version                                                          | Numéro de version de la publication. Format numérique (ex : "1"). Limité à 5 caractères. Non modifiable après déploiement.                                                                                                                                                                                                                                                                                                             | Non                      |
| Description fonctionnelle des données                            | Courte description fonctionnelle des données exploitées par la publication.                                                                                                                                                                                                                                                                                                                                                            | Oui                      |
| Contient des données personnelles (nom, mail, adresse, ...)      | Menu déroulant permettant de sélectionner si Oui ou Non cette publication contient des données personnelles. Par défaut sur le choix "Oui ou Non".                                                                                                                                                                                                                                                                                     | Oui                      |
| Contient des données sensibles (politique, religion, santé, ...) | Menu déroulant permettant de sélectionner si Oui ou Non cette publication contient des données sensibles. Par défaut sur le choix "Oui ou Non".                                                                                                                                                                                                                                                                                        | Oui                      |
| Format du message                                                | Menu déroulant permettant de sélectionner le format du message entre XML et JSON. Par défaut sur le format JSON. Non modifiable après création de la publication.                                                                                                                                                                                                                                                                      | Non                      |
| Schéma du message                                                | Doit contenir l’url du fichier décrivant la structure du message.                                                                                                                                                                                                                                                                                                                                                                      | Oui                      |
| Accord du fournisseur nécessaire pour souscrire                  | Si cette case est cochée, toute demande de souscription devra être validée par l’application fournisseur. Il est préconisé de cocher la case. La case est cochée par défaut. Dans le cas où les champs "Contient des données personnelles" ou "Contient des données sensibles" sont valorisés à "Oui", cette case est obligatoirement cochée.Lors de la modification d'une publication, On ne peut pas décocher le champ si il ya des demandes de souscription en attente de validation sur ce stream de publication. et/ou - il contient des données sensibles/personnelles. Alors si les deux restrictions s'appliquent, les deux messages seront affichés de manière à maintenir une expérience utilisateur simple et sécurisée. Sinon on peut décocher et sauvegarder.                                                                                          | Oui                      |
| Tags                                                             | Chaque tag est à séparer par un point-virgule. Pas de caractères spéciaux. Limité à 250 caractères.                                                                                                                                                                                                                                                                                                                                    | Oui                      |
| Définir des clés de routage                                      | Indique si des clés de routage sont utilisables, si on a des souscriptions qui sont abonnées à la publication et qui ont défini des clés de routage on ne peut pas décocher cette case à cocher.                                                                                                                                                                                                                                                                                                                                                                                       | Oui                      |
| Publication à usage privé (interne application)               | Ce paramètre permet de réserver cette publication à des usages internes à votre application. Aucune autre application ne pourra y souscrire. Il est impossible de cocher cette case lors d'une édition si une autre application à déjà souscrit à cette publication.                                                                                                                                                                   | Oui                      |
| URL de votre documentation décrivant vos clés de routage         | Lien URL vers la documentation d’utilisation des clés de routage.                                                                                                                                                                                                                                                                                                                                                                      | Oui                      |

**Tableau des streams** :

| Libellé       | Description                                                                                                                                                                                                                                                                                                              |
|---------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| StreamId      | Ce champ est rempli automatiquement lorsqu’une instance est créée. Il est valorisé ainsi : nomDuStream_version_nomEnvironnement le tout en minuscule. Ce stream id est unique par application.                                                                                                                           |
| Environnement | Environnement sur lequel on souhaite envoyer des messages                                                                                                                                                                                                                                                                |
| Statut        | Ce champ est valorisé ainsi : Pour un environnement taggué production "Demande soumise -> Réalisation sous 48h" (pending) ou pour un environnement taggué non-production "Demande soumise -> Réalisation sous 24h" (pending), "En cours de création" (ongoing), "Déployé" (succeeded). |
| Actions       | Sauvegarder. Présent sur une nouvelle ligne d’instance.                                                                                                                                                                                                                                                                  |

**Boutons d'action de la page** :

Le clic sur les boutons d'action est bloqué (présence d'un loader) le temps que les actions (appels au back-end, aux APIs) aient été effectués.

| Libellé        | Description                                                                                                   |
|----------------|---------------------------------------------------------------------------------------------------------------|
| Sauvegarder    | Sauvegarder toutes les modifications effectuées. Présent lors d’une création ou d’une édition de publication. |
| Editer         | Permet de rendre modifiable les champs. Présent lors de la consultation de publication.                       |
| Créer instance | Insère une nouvelle ligne dans le tableau des instances Présent lors de la consultation de publication.       |
| Retour         | Permet de retourner sur la page de l’application.                                                             |

**Tableau des Souscriptions associées** :

| Libellé              | Description                                                       |
|----------------------|-------------------------------------------------------------------|
| Nom de l'application | Nom de l'application consommatrice                                |
| Environnement        | Environnement de la publication                                   |
| Gestionnaire         | Nom du gestionnaire principal de l'application ayant souscris. |
| Mail de contact      | Adresse mail de contact pour cette application.                   |
| Date de souscription | Date de l'envoi de la création de souscription instance à zbus    |
| Valideur             | Si la souscription nécessite une validation manuelle la colonne valideur va contenir le nom et le prénom de celui qui a validé la souscription sinon ça va contenir "Pas de validation requise"                                                                                   |
| Environnement du souscripteur | Nom de l'environnement du fournisseur associé à la publication instance                   |
| Révocation           | Bouton permettant la révocation de la souscription après validation 
et la notification du souscripteur de la suppression de sa souscription instance                                                                                   |

#### 8.3.1. Diagramme de séquence Création de publication

![](DiagrammeSequence/publication_creation.seq.png)

### 8.4. Création d'une instance de publication

#### 8.4.1 Diagramme de séquence

![](DiagrammeSequence/publication_instance_create.seq.png)

### 8.5. Suppression d'une instance de publication

#### 8.5.1 Diagramme de séquence

![](DiagrammeSequence/publication_instance_delete.seq.png)

### 8.6. Révocation d'une souscription associée à la publication

#### 8.6.1 Diagramme de séquence

![](DiagrammeSequence/associated_subscriptions_revocation.seq.png)

## 9. Détail d'une souscription

La page permettant de créer une nouvelle souscription est la même que celle affichant le détail d'une souscription.

### 9.1. Cinématique des écrans

#### 9.1.1. Consultation d'une souscription

![](media/cinematique_consumers.png)

#### 9.1.2. Création d'une souscription

![](media/cinematique_new_consumer.png)

### 9.2. Maquette

#### 9.2.1. Consultation d'une souscription

![](media/detail_consumer.png)

#### 9.2.2. Création d'une souscription

![](media/new_consumer.png)

#### 9.2.3. Suppression d'une souscription

Le bouton supprimer en bas de la page au niveau du détail de la souscription permet de supprimer la souscription en plus de ses instances si il y'en a, cette action permet de supprimer la souscription dans eBus et zBus.

![](DiagrammeSequence/souscription_deletion.seq.png)

### 9.3. Composition

**Informations générales d'une création et de détails d'une souscription** :

| Libellé                                   | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                              | Editable en modification |
|-------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------------------------|
| Nom de la souscription                    | Nom de la souscription. Champ libre. Les caractères autorisés sont les lettres minuscules, les chiffres et le caractère « _ ». Doit faire entre 3 et 50 caractères. Le nom de la souscription est unique pour une application, et ne doit pas être utilisé pour le nom d’une publication de la même application. Le message « Nom de publication ou souscription déjà utilisé pour cette application » apparait pour un nom qui est déjà utilisé pour cette application. | Non                      |
| Nom de l'application fournisseur          | Nom du flux consommé. Liste déroulante parmi les flux de l’application fournisseur.                                                                                                                                                                                                                                                                                                                                                                                      | Non                      |
| Nom de la publication                     | N’apparait qu’une fois l’application fournisseur sélectionnée. Liste déroulante. Choisir une publication parmi les résultats.                                                                                                                                                                                                                                                                                                                                            | Non                      |
| Version                                   | N’apparait qu’une fois l’application fournisseur sélectionnée. Liste déroulante listant les versions de la publication. Choisir une version parmi les résultats.                                                                                                                                                                                                                                                                                                         | Oui                      |
| Acquittement manuel                       | Coché par défaut. Si cette case est cochée, l’acquittement du message ne sera pas effectué automatiquement à réception. Il est déconseillé d’utiliser cette option.                                                                                                                                                                                                                                                                                                      | Oui                      |
| Acquittement individuel pour une requête de plusieurs messages     | Apparait uniquement si l'acquittement manuel est activé. Par défaut la case n'est pas cochée.  Si cette case est cochée, l'acquittement du message sera effectué d'une manière individuelle pour une requête de plusieurs messages.                                                                                                                                                                                                                                                                                                                                                                 | Oui                      |
| Durée limite d’acquittement (en secondes) | Durée au bout de laquelle le message sera renvoyé si l’acquittement n’a pas été reçu. Nécessaire uniquement si acquittement manuel. C’est le délai dont le souscripteur dispose pour envoyer une requête ack à la suite d’une requête GET messages. La valeur zBus par défaut est de 10 secondes, la valeur recommandée est elle aussi de 10 secondes. La valeur maximale est de 3600 secondes.                                                                          | Oui                      |
| Nombre maximale de messages non acquitté | Par défaut sa valeur est positionnée à 50, représentant le nombre maximal des messages en attente d'acquittement.  | Oui                      |
| Tags                                      | Chaque tag est à séparer par un point-virgule. Pas de caractères spéciaux. Limité à 250 caractères.                                                                                                                                                                                                                                                                                                                                                                      | Oui                      |
| Utiliser les règles de routage            | N’apparait pas tant que la publication sélectionnée ne contient pas de routing key déclaré. Décoché par défaut. Si cette case est cochée, alors l’utilisateur devra saisir au moins 1 clé de routage (max : 4). Si aucune clé de routage déclarée, ‘#’ sera envoyé à zbus (= s’abonner à tout)                                                                                                                                                                           | Oui                      |
| Règle de routage (1-4)                    | N’apparait pas tant que la publication sélectionnée ne contient pas de routing key déclaré et que la checkbox ‘utiliser les règles de routage’ n’est pas cochée. Le premier champ est obligatoire. Ces clée(s) seront envoyer à zbus lors de la création (& modification) de la souscription                                                                                                                                                                             | Oui                      |
| ID Orange Carto                           | (Apparait uniquement dans la page de détails) Retourne l'ID Orange Carto de l'application fournisseur                                                                                                                                                                                                                                                                                                                                                                    | N/A                      |

**Tableau des streams** :

| Libellé                   | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
|---------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Stream ID de souscription | Ce champ est rempli automatiquement lorsqu’une instance est créée. Il est valorisé ainsi : nomDuStream_version_nomEnvironnement le tout en minuscule. Ce stream id est unique par application.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
| Env. consommateur         | Environnement sur lequel on souhaite réceptionner les messages. Liste déroulante parmi les environnements de même type que l’environnement fournisseur (c’est-à-dire que seuls les environnements de hors production sont disponibles si l’environnement fournisseur est en hors production, et inversement pour la production).                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| Env. fournisseur          | Environnement fournisseur sur lequel on souhaite se connecter. Liste déroulante parmi les environnements sur lesquels est déployé ce flux. Les Env. fournisseur et Env. consommateur doivent être de même type Hors Prod ou Prod : Lorsqu’une valeur est sélectionnée dans l’un champs Env. fournisseur ou Env. consommateur, la liste déroulante du second champ est filtrée pour ne contenir que les environnements de même type Hors Prod ou Prod. Si les 2 environnements sélectionnés ne sont pas de même type, le message d’erreur suivant : *« L'environnement fournisseur et consommateur doivent être du même type (production ou hors production) »*                                                                                                                                                                                                                                                                                                                                                                   |
| Stream ID de publication  | Ce champ est rempli automatiquement lorsqu’une instance est créée. Il est valorisé ainsi : nomDuStreamPublication_version_nomEnvironnement le tout en minuscule.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| Statut                    | Ce champ est valorisé ainsi : "En attente de l'accord du fournisseur" (pending_validation), pour un environnement taggué production "Demande soumise -> Réalisation sous 48h" (pending) ou pour un environnement taggué non-production "Demande soumise -> Réalisation sous 24h" (pending), "En cours de création" (ongoing), "Déployé" (succeeded).                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| Actions                   | **Sauvegarder** : Si la case « Accord du fournisseur nécessaire pour souscrire » est décochée pour la publication associée, la souscription sera sauvegardée dans eBus au statut « En attente de déploiement » et enregistrée dans zBus. Dans le cas contraire, la souscription sera sauvegardée dans eBus au statut « En attente de l’accord du fournisseur ». Le clic sur les boutons d'action est bloqué (présence d'un loader) le temps que les actions (appels au back-end, aux APIs) soient effectuées. Elle passera au statut « En attente de déploiement » lorsque l’instance de souscription sera validée. Elle sera alors enregistrée dans zBus. L’instance apparaîtra dans la liste des instances et sera automatiquement déployée plus tard. La demande est globale à la souscription, chaque demande d'instance de souscription sera validée lorsque la première le sera. Toutes les autres seront alors automatiquement validées et il ne sera plus nécessaire d'attendre l'accord du fournisseur pour les suivantes.<br/><br/>**Activation/Désactivation d'une instance** : Tout d'abord, l'instance doit être déployée. Pour effectuer l'activation ou la désactivation, quand l'instance est active, le bouton est positionné à "Activer" (au niveau backend, une demande est faite à zBus via un `PUT` à [/api/pull_instances/{pull_instance_id}/messages] pour lier l'instance de flux pull et mettre l'attribut "disabled" à false dans la table `subscription_instance` de la base de données pubsub). Sinon, le bouton est positionné à "Désactiver" (au niveau backend, une demande est faite à zBus via un `DELETE` à [/api/pull_instances/{pull_instance_id}/messages] pour délier l'instance de flux pull et mettre l'attribut "disabled" à true dans la table `subscription_instance` de la base de données pubsub).<br/><br/>**Purge de souscription instance** : Quand l'instance de souscription est créée et déployée, on peut faire la purge en cliquant sur l'icône purge dans la colonne des "Actions". La purge va supprimer tous les messages de l'instance de souscription dans zBus (au niveau backend, une demande est faite à zBus via un `DELETE` à [/api/pull_instances/{pull_instance_id}/messages] afin de supprimer tous les messages liés à cet ID d'instance).<br/><br/>**Historique de purge** : Ce bouton apparaît lorsqu'un historique de purge est disponible pour l'instance. Il affiche la date de la purge ainsi que le nom de l'utilisateur qui a effectué l'opération. Si aucune purge n'a eu lieu, le bouton reste caché. |

**Boutons d'action de la page** :

Le clic sur les boutons d'action est bloqué (présence d'un loader) le temps que les actions (appels au back-end, aux APIs) soient effectués.

| Libellé        | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
|----------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Sauvegarder    | Tous les champs obligatoires n’ont pas besoin d’être remplis pour pouvoir sauvegarder.  Si la publication sélectionnée demande l'accord du fournisseur pour y souscrire, une fenêtre d'envoi de mail s'ouvre afin de permettre la notification au fournisseur de la nouvelle demande de souscription à son flux. La fenêtre d'envoi se mail s'ouvre en cas de création d'une souscription ou de modification des routing keys d'une souscription, à une publication demandant l'accord du fournisseur pour y souscrire.  Le mail est déjà pré-remplis avec l'adresse mail du fournisseur, l'objet du mail et le corps du mail en Français et Anglais. |
| Editer         | Permet de rendre modifiable les champs.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |
| Supprimer      | Permet de supprimer la souscription.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
| Créer instance | Insère une nouvelle ligne dans le tableau des instances.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |
| Retour         | Permet de retourner sur la page de l’application.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |

### 9.5. Création de souscription

#### 9.5.1 Diagramme de séquence

![](DiagrammeSequence/souscription_creation.seq.png)

### 9.6. Création de souscription instance

La souscription instance est dépendante de l'accord du fournisseur. Dans le cas où celle-ci n'est pas obligatoire, la
demande est faite à zBus directement, sinon c'est le fournisseur qui doit valider chaque demande et la demande de
création est effectuée à ce moment-là.
La demande est globale pour toutes les instances de souscription. Si la première est validée, les autres seront
également validées.

Une demande de déploiement est également effectuée pour chaque environnement souscripteur dans les 2 cas.
Une modification des routing keys lance aussi une nouvelle demande de déploiement (si la validation du fournisseur est
nécessaire, cela relance le processus de validation comme à la création de la souscription).

Le clic sur les boutons d'action est bloqué (présence d'un loader) le temps que les actions (appels au back-end, aux
APIs) soient effectués.

#### 9.6.1 Diagramme de séquence

![](DiagrammeSequence/souscription_instance_create.seq.png)

#### 9.6.2 Édition souscription

![](DiagrammeSequence/souscription_edit_after_creating_instance.seq.png)

### 9.7 Purge de souscription instance

Une fois la souscription instance est créée et déployée on peut faire la purge en cliquant sur l'icône purge dans la colonne des "Actions", la purge va supprimer tous les messages de la souscription instance dans Zbus. Un message de confirmation de purge "Purger en supprimant tous les messages" est affiché à l'utilisateur.

#### 9.7.1 Diagramme de séquence

![](media/souscription_instance_purge.png)

### 9.8. Activation/Désactivation d'une souscription instance

Une fois la souscription instance est créée et déployée elle est par défaut activée (bouton vert), l'utilisateur peut désactiver la souscription instance en cliquant sur le bouton dans la colonne "Actions", une fois elle est désactivée le bouton devient rouge.

Si la souscription instance est désactivée, l'utilisateur peut la réactiver à tout moment en cliquant sur le bouton qui redevient par la suite vert.
#### 9.8.1 Diagramme de séquence pour activation

![](media/souscription_instance_activate.png)
#### 9.8.2 Diagramme de séquence pour désactivation

![](media/souscription_instance_deactivate.png)

### 9.9. Suppression d'une souscription instance

Dans la colonne des actions nous pouvons aussi supprimer une instance de souscription en cliquant sur le bouton delete (poubelle), cette action permet de supprimer l'instance de souscription dans zBus et eBus.

#### 9.9.1 Diagramme de séquence pour suppression

![](DiagrammeSequence/souscription_instance_delete.seq.png)

## 10. Menu Monitoring

L'ensemble des utilisateurs a accès à ce menu (administrateurs et non-administrateurs).
L'utilisateur ne peut voir que les applications, publications et souscriptions dont il est manager ou dont ses
applications sont consumer (et dont il est manager).

### 10.1. Maquette

![](media/monitoring.png)

![](media/monitoring_publication_stream_id.png)

### 10.2. Composition

**Recherche de flux** :

| Champ                     | Type                     | Action                                                                                                                                                                                                                                                                                                                                                                         |
|---------------------------|--------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Début - Date              | Champ                    | Date de début de l'intervalle de recherche, au format JJ/MM/AAAA.                                                                                                                                                                                                                                                                                                              |
| Bouton date début         | Bouton (icone cliquable) | Permet de selectionner une date via un calendrier interactif.                                                                                                                                                                                                                                                                                                                  |
| Début - Heure             | Champ                    | Heure de début de l'intervalle de recherche, au format HH:MM.                                                                                                                                                                                                                                                                                                                  |
| Bouton heure début        | Bouton (icone cliquable) | Permet de selectionner une heure via l'icone horloge.                                                                                                                                                                                                                                                                                                                          |
| Fin - Date                | Champ                    | Date de fin de l'intervalle de recherche, au format JJ/MM/AAAA.                                                                                                                                                                                                                                                                                                                |
| Bouton date fin           | Bouton (icone cliquable) | Permet de selectionner une date via un calendrier interactif.                                                                                                                                                                                                                                                                                                                  |
| Fin - Heure               | Champ                    | Heure de fin de l'intervalle de recherche, au format HH:MM.                                                                                                                                                                                                                                                                                                                    |
| Bouton heure fin          | Bouton (icone cliquable) | Permet de selectionner une heure via l'icone horloge.                                                                                                                                                                                                                                                                                                                          |
| Application Fournisseur   | Champ                    | Nom de l'application fournisseur de la publication. Le champ est sélectionnable, et l'utilisateur peut entrer du texte afin de filtrer les resultats affichés dans la liste déroulante. Après avoir sélectionné une application dans la liste, le champ "Publication stream id" est rendu visible.                                                                             |
| Publication stream id     | Champ                    | Id de l'instance de publication. Le champ affiche la liste des streams de l'application sélectionnée précédemment. Le champ est sélectionnable, et l'utilisateur peut entrer du texte afin de filtrer les resultats affichés dans la liste déroulante. Ce champ n'est pas visible tant qu'une application n'a pas été sélectionnée dans le champ "Application Fournisseur".    |
| Bouton Recherche avancée  | Bouton                   | Bouton permettant d'afficher ou non la section dépliante avec les champs de recherche avancée. La section est masquée par défaut à l'arrivée sur l'onglet Monitoring. Le label du bouton est "Afficher/Masquer".                                                                                                                                                               |
| Application Consommatrice | Champ                    | Nom de l'application consommatrice de la publication. Le champ est sélectionnable, et l'utilisateur peut entrer du texte afin de filtrer les resultats affichés dans la liste déroulante. Après avoir sélectionné une application dans la liste, le champ "Souscription stream id" est rendu visible.                                                                          |
| Souscription stream id    | Champ                    | Id de l'instance de souscription. Le champ affiche la liste des streams de l'application sélectionnée précédemment. Le champ est sélectionnable, et l'utilisateur peut entrer du texte afin de filtrer les resultats affichés dans la liste déroulante. Ce champ n'est pas visible tant qu'une application n'a pas été sélectionnée dans le champ "Application Consommatrice". |
| Paramètres    | Champ                    | Le champ est saisissable, l'utilisateur peut entrer du texte. Ce texte contiendra les valeurs des paramètres. L'objectif de ce champ est de retourner les messages correspondants aux valeurs saisies dans le champ des paramètres du message.  |
| Message Id                | Champ                    | Id du message du log. Le champ est sélectionnable, et l'utilisateur peut entrer du texte. Il n'y a pas de liste déroulante à ce champ.                                                                                                                                                                                                                                         |
| Log Code                  | Champ                    | Code du message. Le champ est sélectionnable, et l'utilisateur peut entrer du texte. Il n'y a pas de liste déroulante à ce champ. Ce champ permet de filtrer les résultats de la recherche en fonction du texte en entrée.                                                                                                                                                     |
| Log Type : Info           | Checkbox                 | Coche sélectionnable et déselectionnable, liée au type de log "Info". Permet de filtrer les résultats de la recherche de logs par gravité de type "Info".                                                                                                                                                                                                                      |
| Log Type : Error          | Checkbox                 | Coche sélectionnable et déselectionnable, liée au type de log "Error". Permet de filtrer les résultats de la recherche de logs par gravité de type "Error".                                                                                                                                                                                                                    |
| Log Type : Warning        | Checkbox                 | Coche sélectionnable et déselectionnable, liée au type de log "Warning". Permet de filtrer les résultats la de recherche de logs par gravité de type "Warning".                                                                                                                                                                                                                |
| Log Type : Fatal          | Checkbox                 | Coche sélectionnable et déselectionnable, liée au type de log "Fatal". Permet de filtrer les résultats de la recherche de logs par gravité de type "Fatal".                                                                                                                                                                                                                    |
| Bouton Rechercher         | Bouton                   | Bouton permettant de lancer la recherche de messages de log en fonction des paramètres en entrée.                                                                                                                                                                                                                                                                              |

La recherche ne peut se faire que si au moins l'un des champs "Application Fournisseur" et "Publication Stream Id", "
Application Consommatrice" et "Souscription Stream Id" ou "Message Id" est renseigné.

**Message - \<Id pub stream\>** :

| Libellée                     | Type                                  | Description                                                                                                                                                                            |
|------------------------------|---------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Tableau de résultats         | Tableau                               | Le tableau d’affichage des résultats. Les résultats peuvent être triés en fonction de chaque colonne en cliquant dessus.                                                               |
| Nombre de résultats renvoyés | Texte                                 | Présente le nombre de messages de log retournés suivi du libellé \« messages(s) retourné(s)\».                                                                                         |
| Pagination                   | Numérotation et flèches de navigation | Apparaît au-dessus du tableau, centrée. 25 applications sont affichées au maximum par page.                                                                                            |
| Exportation au format .xlsx  | Bouton                                | Bouton permettant d'exporter les résultats de la recherche au format .xlsx. Le bouton est activé et cliquable uniquement lorsqu'un ou plusieurs résultats sont présents dans la liste. |
| Gravité                      | Colonne                               | Niveau de gravité du log le plus critique dans le flux.                                                                                                                                |
| Date de début                | Colonne                               | Date à laquelle le flux a commencé (date du premier message dans le bus).                                                                                                              |
| Durée                        | Colonne                               | Différence entre la date du premier et du dernier message dans le bus.                                                                                                                 |
| Paramètres                   | Colonne                               | Liste de paramètres envoyés par l'application.                                                                                                                                         |
| Message Id                   | Colonne                               | Id permettant l'identification du flux.                                                                                                                                                |

Seront retournés les messages qui correspondent aux champs saisis dans le formulaire.

\<Id pub stream\> correspond à la valeur de l'Id Stream de publication spécifiée pour la recherche (dans le cas d'une
recherche par Id Stream de souscription ou Message Id, l'Id Stream de publication affichée correspond à celui associé
aux
paramètres de recherche).

L'Id du message est cliquable et permet d'accéder à la page de détails des logs pour le message donné.

## 11. Détail des logs d'un message

L'ensemble des utilisateurs a accès à ce menu (administrateurs et non-administrateurs).

### 11.1. Maquette

![](media/detail_message.png)

### 11.2. Composition

| Libellée                         | Type    | Description                                                                                                                                                                                                                                                                                                      |
|----------------------------------|---------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Tableau des détails du message   | Tableau | Le tableau d’affichage des détails du message. Les informations affichées sont séparées dans des sections de couleur.                                                                                                                                                                                            |
| Message et stream de publication | Ligne   | La ligne est de couleur Orange. Elle affiche l'id du message, la date de début et la durée.                                                                                                                                                                                                                      |
| Publication                      | Ligne   | La ligne est de couleur Grise. Elle peut être dépliée et repliée par le biai d'un bouton disposé à la droite de la ligne. La ligne affiche l'id de la publication, le type de log (Info, Error, Warning ou Fatal), le code du log, la description du log, la date de début, la durée et la liste de paramètres.  |
| Souscription                     | Ligne   | La ligne est de couleur Grise. Elle peut être dépliée et repliée par le biai d'un bouton disposé à la droite de la ligne. La ligne affiche l'id de la souscription, le type de log (Info, Error, Warning ou Fatal), le code du log, la description du log, la date de début, la durée et la liste de paramètres. |
## 12. Gestion des erreurs côté portail

### 12.1. Envoi d'un e-mail à zbus

Afin d'améliorer la gestion des erreurs, nous avons mis en place une solution pour traiter différents cas d'erreurs (404, 500, 503, etc.) qui peuvent survenir lors de l'appel à l'API zbus-admin. L'objectif est d'inclure ces informations dans le corps de l'e-mail de notification qui sera envoyé à l'équipe zbus et à l'équipe support d'ebus.

Lorsqu'un appel à l'API zbus-admin échoue, un e-mail de notification est déclenché, contenant les informations suivantes :

- Nom de l'opération : Le nom de l'opération qui a échoué lors de l'appel à l'API zbus-admin.
- Date : La date et l'heure à laquelle l'erreur s'est produite, au format JJ-MM-AAAA 23:59:59.
- Code erreur : Le code d'erreur correspondant à l'erreur rencontrée lors de l'appel.
- Message d'erreur : Le message d'erreur détaillé expliquant la nature de l'erreur.

Ces informations permettent à l'équipe zbus de prendre connaissance rapidement de l'erreur et de commencer à investiguer pour rétablir le service dans les meilleurs délais.

### 12.2. Utilisation de l'API MAIL ENABLER

Pour l'envoi automatique des e-mails, nous utilisons l'API MAIL ENABLER d'Orange. Cette API fournit les fonctionnalités nécessaires pour envoyer des e-mails entre les projets IT.

les détails de l'API MAIL ENABLER à partir de la documentation disponible à l'adresse suivante : https://emails.obs-tech.com.intraorange.

Une collection Postman fournie dans la documentation de l'API MAIL ENABLER pour tester l'envoi d'e-mails. La collection Postman fournit des exemples de requêtes et de réponses pour vous aider à comprendre comment utiliser l'API.

## 13. Aide

### 13.1. Cinématique d'accès à l'écran d'aide

La page d'aide se consulte en cliquant sur le bouton « aide » présent sur le bandeau en haut de l'écran. Cette page est consultable à n'importe quel moment et spécifique à l'écran consulté au moment du passage sur l'aide.

### 13.2. Maquette

![](media/help.png)

### 13.3. Composition

Elle est composée d\'un sommaire d\'aide qui permet de naviguer entre les aides relatifs aux différents écrans de eBus. Ces pages contiennent des captures d\'écran accompagnés de texte. Elle ne permet pas la navigation vers une autre page. Le texte présent sur cette page donne des indications sur l'écran consulté : la signification des libellés, le format attendu dans les différents champs, etc.
