from typing import List, Dict, Any, Tuple, Optional
from datetime import datetime, timedelta

# Définition des types
Livre = Dict[str, Any]
Usager = Dict[str, Any]
Emprunt = Dict[str, Any]

# Variables globales
livres: List[Livre] = []
liste_usagers: List[Usager] = []
emprunts: List[Emprunt] = []

# Fonctions pour la gestion des livres
def ajouter_livre(livre: Livre) -> None:
    """Ajoute un nouveau livre à la bibliothèque."""
    livres.append(livre)

def modifier_livre(isbn: str, nouvelles_infos: Dict[str, Any]) -> bool:
    """Modifie les informations d'un livre existant."""
    for livre in livres:
        if livre['isbn'] == isbn:
            livre.update(nouvelles_infos)
            return True
    return False

def supprimer_livre(isbn: str) -> bool:
    """Supprime un livre de la bibliothèque."""
    for i, livre in enumerate(livres):
        if livre['isbn'] == isbn:
            livres.pop(i)
            return True
    return False

def rechercher_livre(critere: str, valeur: str) -> List[Livre]:
    """Recherche des livres selon un critère et une valeur donnés."""
    resultats = []
    for livre in livres:
        if critere in livre and valeur.lower() in str(livre[critere]).lower():
            resultats.append(livre)
    return resultats

# Fonctions pour la gestion des usagers
def valider_usager(usager: Usager) -> Tuple[bool, str]:
    """Valide les données d'un nouvel usager."""
    if not usager.get('nom'):
        return False, "Le nom est obligatoire."
    
    identifiant = usager.get('identifiant')
    if not identifiant:
        return False, "L'identifiant est obligatoire."
    
    for u in liste_usagers:
        if u['identifiant'] == identifiant:
            return False, "L'identifiant est déjà utilisé."
    
    return True, "Usager valide."

def ajouter_usager(usager: Usager) -> Tuple[bool, str]:
    """Ajoute un nouvel usager à la bibliothèque."""
    est_valide, message = valider_usager(usager)
    if est_valide:
        liste_usagers.append(usager)
        return True, "Usager ajouté avec succès."
    return False, message

def modifier_usager(identifiant: str, nouvelles_infos: Dict[str, Any]) -> Tuple[bool, str]:
    """Modifie les informations d'un usager existant."""
    for usager in liste_usagers:
        if usager['identifiant'] == identifiant:
            usager.update(nouvelles_infos)
            return True, "Usager modifié avec succès."
    return False, "Usager non trouvé."

# Fonctions pour la gestion des emprunts
def emprunter_livre(isbn: str, identifiant_usager: str, date_emprunt: datetime = None) -> Tuple[bool, str]:
    """Enregistre l'emprunt d'un livre par un usager."""
    if date_emprunt is None:
        date_emprunt = datetime.now()
    
    # Vérifier si le livre existe et est disponible
    for livre in livres:
        if livre['isbn'] == isbn:
            if livre.get('disponible', True):
                # Vérifier si l'usager existe
                if not any(u['identifiant'] == identifiant_usager for u in liste_usagers):
                    return False, "Usager non trouvé."
                
                # Créer l'emprunt
                emprunt = {
                    'isbn': isbn,
                    'identifiant_usager': identifiant_usager,
                    'date_emprunt': date_emprunt,
                    'date_retour_prevue': date_emprunt + timedelta(days=30),  # 30 jours pour rendre le livre
                    'rendu': False
                }
                emprunts.append(emprunt)
                
                # Marquer le livre comme non disponible
                livre['disponible'] = False
                return True, "Livre emprunté avec succès."
            else:
                return False, "Le livre n'est pas disponible."
    
    return False, "Livre non trouvé."

def retourner_livre(isbn: str, identifiant_usager: str) -> Tuple[bool, str]:
    """Enregistre le retour d'un livre emprunté."""
    for emprunt in emprunts:
        if emprunt['isbn'] == isbn and emprunt['identifiant_usager'] == identifiant_usager and not emprunt['rendu']:
            emprunt['rendu'] = True
            emprunt['date_retour_effectif'] = datetime.now()
            
            # Marquer le livre comme disponible
            for livre in livres:
                if livre['isbn'] == isbn:
                    livre['disponible'] = True
                    break
            
            return True, "Livre retourné avec succès."
    
    return False, "Emprunt non trouvé ou déjà retourné."

def verifier_retards() -> List[Dict[str, Any]]:
    """Vérifie les retours en retard."""
    aujourdhui = datetime.now()
    retards = []
    
    for emprunt in emprunts:
        if not emprunt['rendu'] and emprunt['date_retour_prevue'] < aujourdhui:
            retards.append(emprunt)
    
    return retards

def statistiques_emprunts() -> Dict[str, Any]:
    """Calcule des statistiques sur les emprunts."""
    if not emprunts:
        return {}
    
    # Nombre total d'emprunts
    total = len(emprunts)
    
    # Nombre d'emprunts en cours
    en_cours = sum(1 for e in emprunts if not e['rendu'])
    
    # Nombre de retards
    retards = len(verifier_retards())
    
    # Livre le plus emprunté
    livres_empruntes = [e['isbn'] for e in emprunts]
    if livres_empruntes:
        livre_plus_emprunte = max(set(livres_empruntes), key=livres_empruntes.count)
    else:
        livre_plus_emprunte = "Aucun emprunt"
    
    return {
        'total_emprunts': total,
        'emprunts_en_cours': en_cours,
        'retards': retards,
        'livre_plus_emprunte': livre_plus_emprunte
    }

def categories_populaires() -> List[Tuple[str, int]]:
    """Retourne les catégories les plus populaires."""
    categories = {}
    
    for emprunt in emprunts:
        for livre in livres:
            if livre['isbn'] == emprunt['isbn']:
                categorie = livre.get('categorie', 'Non catégorisé')
                categories[categorie] = categories.get(categorie, 0) + 1
    
    # Trier par nombre d'emprunts décroissant
    return sorted(categories.items(), key=lambda x: x[1], reverse=True)

# Exemple d'utilisation
if __name__ == "__main__":
    # Ajout de quelques livres de test
    livres_test = [
        {
            'titre': 'Python pour les nuls',
            'auteur': 'John Smith',
            'isbn': '1234567890',
            'categorie': 'Informatique',
            'disponible': True
        },
        {
            'titre': 'Le Seigneur des Anneaux',
            'auteur': 'J.R.R. Tolkien',
            'isbn': '2345678901',
            'categorie': 'Fantasy',
            'disponible': True
        },
        {
            'titre': '1984',
            'auteur': 'George Orwell',
            'isbn': '3456789012',
            'categorie': 'Science-Fiction',
            'disponible': True
        }
    ]
    
    # Ajout des livres à la bibliothèque
    for livre in livres_test:
        ajouter_livre(livre)
    
    # Ajout d'un usager
    usager = {
        'identifiant': 'user1',
        'nom': 'Dupont',
        'prenom': 'Jean',
        'email': 'jean.dupont@example.com'
    }
    ajouter_usager(usager)
    
    # Exemple d'emprunt
    emprunter_livre('1234567890', 'user1')
    
    # Affichage des statistiques
    print("=== Statistiques de la bibliothèque ===")
    stats = statistiques_emprunts()
    for k, v in stats.items():
        print(f"{k}: {v}")
    
    # Affichage des catégories populaires
    print("\n=== Catégories populaires ===")
    for categorie, compte in categories_populaires():
        print(f"{categorie}: {compte} emprunt(s)")