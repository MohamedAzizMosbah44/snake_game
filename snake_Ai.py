def programme_IA(couleur,vitesse):
    import pygame
    import time
    import random
    import tkinter as tk
    from tkinter import simpledialog
    import final_snake
    pygame.init()
    
    # Définir les couleurs
    noir = (0, 0, 0)
    rouge = (213, 50, 80)
    rouge_claire=(255, 128, 128)
    vert = (0, 255, 0)
    vert_fonce = (200, 255, 128)
    bleu = (50, 153, 213)
    blanc=(255,255,255)
    if couleur=="vert":
        couleur_ns=vert_fonce
        couleur_ns_queue=vert
        couleur_ia=rouge
        couleur_ia_queue=rouge_claire
    else:
        couleur_ia=vert
        couleur_ia_queue=vert_fonce
        couleur_ns=rouge
        couleur_ns_queue=rouge_claire
    # Définir les dimensions de la fenêtre
    largeur = 300
    hauteur = 300
    
    # Initialiser la fenêtre de jeu
    fenetre = pygame.display.set_mode((largeur, hauteur))
    pygame.display.set_caption('Jeu du Serpent contre IA')
    horloge = pygame.time.Clock()
    vitesse_serpent = vitesse
    
    # Définir la taille du serpent et sa position initiale
    taille_serpent = 10
    
    # Positions initiales des serpents
    serpent_pos = [[largeur // 2, hauteur // 2]]
    ia_serpent_pos = [[3 * largeur // 2, hauteur // 2]]
    
    # Position initiale de la pomme
    def retour_menu_principale():
        final_snake.main()
    def placer_pomme(serpent_pos, ia_serpent_pos):
        while True:
            pomme_pos = [random.randint(0, (largeur - taille_serpent) // taille_serpent) * taille_serpent,
                         random.randint(0, (hauteur - taille_serpent) // taille_serpent) * taille_serpent]
            if pomme_pos not in serpent_pos and pomme_pos not in ia_serpent_pos:
                return pomme_pos
    
    pomme_pos = placer_pomme(serpent_pos, ia_serpent_pos)
    
    # Initialiser les directions
    direction = 'DROITE'
    ia_direction = 'GAUCHE'
    
    # Scores
    score = 0
    ia_score = 0
    
    def afficher_score(score, ia_score):
        police = pygame.font.SysFont('arial', 20)
        texte = police.render(f'Votre Score: {score}', True, bleu)
        fenetre.blit(texte, [10, 10])
        texte_ia = police.render(f'Score IA: {ia_score}', True, bleu)
        fenetre.blit(texte_ia, [largeur - 120, 10])
    
    def notre_serpent(taille_serpent, serpent_pos, couleur_tete, couleur_corps):
        if serpent_pos:
            tete = serpent_pos[0]
            pygame.draw.rect(fenetre, couleur_tete, pygame.Rect(tete[0], tete[1], taille_serpent, taille_serpent))
            for pos in serpent_pos[1:]:
                pygame.draw.rect(fenetre, couleur_corps, pygame.Rect(pos[0], pos[1], taille_serpent, taille_serpent))
    
    def reinitialiser_serpent(serpent_pos, x, y):
        serpent_pos.clear()
        serpent_pos.append([x, y])
    
    def changer_direction_ia(ia_tete, ia_direction, pomme_pos):
        directions = []
    
        # Éviter les murs
        if ia_tete[0] > 0 and ia_direction != 'DROITE':
            directions.append('GAUCHE')
        if ia_tete[0] < largeur - taille_serpent and ia_direction != 'GAUCHE':
            directions.append('DROITE')
        if ia_tete[1] > 0 and ia_direction != 'BAS':
            directions.append('HAUT')
        if ia_tete[1] < hauteur - taille_serpent and ia_direction != 'HAUT':
            directions.append('BAS')
    
        # Éviter le corps de l'IA
        if [ia_tete[0] + taille_serpent, ia_tete[1]] in ia_serpent_pos:
            if 'DROITE' in directions:
                directions.remove('DROITE')
        if [ia_tete[0] - taille_serpent, ia_tete[1]] in ia_serpent_pos:
            if 'GAUCHE' in directions:
                directions.remove('GAUCHE')
        if [ia_tete[0], ia_tete[1] - taille_serpent] in ia_serpent_pos:
            if 'HAUT' in directions:
                directions.remove('HAUT')
        if [ia_tete[0], ia_tete[1] + taille_serpent] in ia_serpent_pos:
            if 'BAS' in directions:
                directions.remove('BAS')
    
        # Choisir une direction vers la pomme
        if pomme_pos[0] > ia_tete[0] and 'DROITE' in directions:
            return 'DROITE'
        elif pomme_pos[0] < ia_tete[0] and 'GAUCHE' in directions:
            return 'GAUCHE'
        elif pomme_pos[1] < ia_tete[1] and 'HAUT' in directions:
            return 'HAUT'
        elif pomme_pos[1] > ia_tete[1] and 'BAS' in directions:
            return 'BAS'
    
        # Si aucune direction n'est possible, continuer dans la même direction
        return ia_direction
    def afficher_bouton():
        police = pygame.font.SysFont('arial', 20)
        texte = police.render('Rejouer', True, noir)
        bouton_rect = pygame.Rect(largeur // 2 - 50, hauteur // 2 + 20, 100, 40)
        pygame.draw.rect(fenetre, blanc, bouton_rect)
        pygame.draw.rect(fenetre, noir, bouton_rect, 2)
        fenetre.blit(texte, [largeur // 2 - 35, hauteur // 2 + 30])
        return bouton_rect
    
    def rejouer():
        pygame.quit()
        final_snake.main()
    def game_over():
        police = pygame.font.SysFont('arial', 30)
        texte = police.render('Game Over!', True, rouge)
        fenetre.blit(texte, [largeur // 2 - 100, hauteur // 2 - 20])
        bouton_rect = afficher_bouton()
        pygame.display.update()
        attendre_rejouer = True
        while attendre_rejouer:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    final_snake.main()
                    return False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if bouton_rect.collidepoint(event.pos):
                        attendre_rejouer = False
                        rejouer()
                        return True
            time.sleep(0.1)
    def ia_gagnant():
        police = pygame.font.SysFont('arial', 30)
        texte = police.render('IA a gagné!', True, rouge)
        fenetre.blit(texte, [largeur // 2 - 100, hauteur // 2 - 20])
        bouton_rect = afficher_bouton()
        pygame.display.update()
    
        attendre_rejouer = True
        while attendre_rejouer:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    retour_menu_principale()
                    return False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if bouton_rect.collidepoint(event.pos):
                        attendre_rejouer = False
                        rejouer()
                        return True
            time.sleep(0.1)
    def j_gagnant():
        police = pygame.font.SysFont('arial', 30)
        texte = police.render('Tu as gagné!', True, rouge)
        fenetre.blit(texte, [largeur // 2 - 100, hauteur // 2 - 20])
        bouton_rect = afficher_bouton()
        pygame.display.update()
    
        attendre_rejouer = True
        while attendre_rejouer:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    retour_menu_principale()
                    return False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if bouton_rect.collidepoint(event.pos):
                        attendre_rejouer = False
                        rejouer()
                        return True
            time.sleep(0.1)
    def demander_score_cible():
        root = tk.Tk()
        root.withdraw()  # Cacher la fenêtre principale de Tkinter
        score_cible = simpledialog.askinteger("Score Cible", "Entrez le score à atteindre pour terminer le jeu:", minvalue=1, maxvalue=100)
        return score_cible
    # Boucle principale du jeu
    score_cible = demander_score_cible()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT and direction != 'GAUCHE':
                    direction = 'DROITE'
                if event.key == pygame.K_LEFT and direction != 'DROITE':
                    direction = 'GAUCHE'
                if event.key == pygame.K_UP and direction != 'BAS':
                    direction = 'HAUT'
                if event.key == pygame.K_DOWN and direction != 'HAUT':
                    direction = 'BAS'
    
        if not serpent_pos or not ia_serpent_pos:
            break
    
        # Mettre à jour la position du serpent du joueur
        tete = serpent_pos[0].copy()
        if direction == 'DROITE':
            tete[0] += taille_serpent
        if direction == 'GAUCHE':
            tete[0] -= taille_serpent
        if direction == 'HAUT':
            tete[1] -= taille_serpent
        if direction == 'BAS':
            tete[1] += taille_serpent
    
        # Logique de l'IA
        ia_tete = ia_serpent_pos[0].copy()
        ia_direction = changer_direction_ia(ia_tete, ia_direction, pomme_pos)
    
        if ia_direction == 'DROITE':
            ia_tete[0] += taille_serpent
        if ia_direction == 'GAUCHE':
            ia_tete[0] -= taille_serpent
        if ia_direction == 'HAUT':
            ia_tete[1] -= taille_serpent
        if ia_direction == 'BAS':
            ia_tete[1] += taille_serpent
    
        # Vérifier les collisions avec les bords et les corps pour le joueur
        if (tete[0] < 0 or tete[0] >= largeur or tete[1] < 0 or tete[1] >= hauteur or
            tete in serpent_pos[1:] or tete in ia_serpent_pos[1:]):
            score = 0
            reinitialiser_serpent(serpent_pos, largeur // 4, hauteur // 2)
    
        # Vérifier les collisions avec les bords et les corps pour l'IA
        if (ia_tete[0] < 0 or ia_tete[0] >= largeur or ia_tete[1] < 0 or ia_tete[1] >= hauteur or
            ia_tete in ia_serpent_pos[1:] or ia_tete in serpent_pos[1:]):
            ia_score = 0
            reinitialiser_serpent(ia_serpent_pos, 3 * largeur // 4, hauteur // 2)
    
        # Vérifier si les têtes des serpents se touchent
        if (tete == ia_tete):
            game_over()
        # Vérifier gagnat
        if score==score_cible:
            j_gagnant()
        if ia_score==score_cible:
            ia_gagnant()
        # Vérifier si le serpent du joueur mange la pomme
        if tete == pomme_pos:
            pomme_pos = placer_pomme(serpent_pos, ia_serpent_pos)
            score += 1
        else:
            serpent_pos.pop()
    
        # Vérifier si le serpent de l'IA mange la pomme
        if ia_tete == pomme_pos:
            pomme_pos = placer_pomme(serpent_pos, ia_serpent_pos)
            ia_score += 1
        else:
            ia_serpent_pos.pop()
    
        # Mettre à jour les positions des serpents
        serpent_pos.insert(0, tete)
        ia_serpent_pos.insert(0, ia_tete)
    
        # Effacer l'écran
        fenetre.fill(noir)
    
        # Dessiner les serpents et la pomme
        notre_serpent(taille_serpent, serpent_pos, couleur_ns, couleur_ns_queue)
        notre_serpent(taille_serpent, ia_serpent_pos, couleur_ia, couleur_ia_queue)
        pygame.draw.rect(fenetre, rouge, pygame.Rect(pomme_pos[0], pomme_pos[1], taille_serpent, taille_serpent))
    
        # Afficher les scores
        afficher_score(score, ia_score)
    
        # Mettre à jour l'affichage
        pygame.display.update()
    
        # Contrôler la vitesse du jeu
        horloge.tick(vitesse_serpent)
