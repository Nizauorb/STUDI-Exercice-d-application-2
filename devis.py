def saisir_article():
    """
    Fonction pour saisir les détails d'un article
    Retourne un tuple (article, prix, quantité, reduction) ou None si l'utilisateur veut quitter
    """
    article = input("Nom de l'article ? (-1 pour terminer) ")
    if article == "-1":
        return None
    
    try:
        prix = float(input("Quel est le prix de l'article ? "))
        quantite = int(input("Quelle est la quantité ? "))
        reduction = float(input("Quelle est la remise en pourcentage (0-100) ? "))
        
        # Vérification des valeurs saisies
        if prix < 0 or quantite <= 0 or reduction < 0 or reduction > 100:
            print("Erreur : Veuillez saisir des valeurs valides (prix ≥ 0, quantité > 0, réduction entre 0 et 100)")
            return saisir_article()
            
        return (article, prix, quantite, reduction)
    except ValueError:
        print("Erreur : Veuillez saisir des valeurs numériques valides")
        return saisir_article()

def main():
    liste_articles = []
    continuer_achat = True
    
    print("=== Programme de devis ===")
    
    while continuer_achat:
        # Saisie des informations de l'article
        saisie = saisir_article()
        
        # Vérifier si l'utilisateur veut quitter
        if saisie is None:
            continuer_achat = False
            continue
            
        article, prix, quantite, reduction = saisie
        
        # Calcul du prix total avec réduction
        prix_total = prix * quantite * (1 - reduction / 100)
        print(f"Prix total pour {quantite} {article}(s) : {prix_total:.2f} € (dont {reduction}% de réduction)")
        
        # Ajout de l'article à la liste
        liste_articles.append({
            'nom': article,
            'prix_unitaire': prix,
            'quantite': quantite,
            'reduction': reduction,
            'prix_total': prix_total
        })
    
    # Affichage du récapitulatif
    if liste_articles:
        print("\n=== Récapitulatif du devis ===")
        total_a_payer = 0
        
        for i, article in enumerate(liste_articles, 1):
            print(f"{i}. {article['nom']} - "
                  f"{article['quantite']} x {article['prix_unitaire']:.2f} € "
                  f"(-{article['reduction']}%) = {article['prix_total']:.2f} €")
            total_a_payer += article['prix_total']
        
        print(f"\nTotal à payer : {total_a_payer:.2f} €")
    else:
        print("Aucun article n'a été saisi.")

if __name__ == "__main__":
    main()