def programme_solo(couleur,vitesse):
    import tkinter as tk
    from tkinter import simpledialog
    import pygame
    import time
    import random
    import final_snake
    
    pygame.init()
    
    # Définir les couleurs
    noir = (0, 0, 0)
    rouge = (213, 50, 80)
    rouge_claire=(255, 128, 128)
    vert = (0, 255, 0)
    vert_fonce = (200, 255, 128)
    bleu = (50, 153, 213)
    if couleur=="vert":
        couleur_ns=vert_fonce
        couleur_ns_queue=vert
    else:
        couleur_ns=rouge
        couleur_ns_queue=rouge_claire
    
    # Définir les dimensions de la fenêtre
    largeur = 300
    hauteur = 300
    
    # Initialiser la fenêtre de jeu
    fenetre = pygame.display.set_mode((largeur, hauteur))
    pygame.display.set_caption('Jeu du Serpent Solo')
    
    horloge = pygame.time.Clock()
    vitesse_serpent = vitesse
    
    # Définir la taille du serpent et sa position initiale
    taille_serpent = 10
    serpent_pos = [[largeur // 2, hauteur // 2]]
    
    # Position initiale de la pomme
    pomme_pos = [random.randint(0,(largeur - taille_serpent) // taille_serpent) * taille_serpent,
                 random.randint(0, (hauteur - taille_serpent) // taille_serpent) * taille_serpent]
    
    # Initialiser la direction du serpent
    direction = 'DROITE'
    changer_direction = direction
    
    # Score
    score = 0
    def retour_menu_principale():
        final_snake.main()
    def demander_score_cible():
        root = tk.Tk()
        root.withdraw()  # Cacher la fenêtre principale de Tkinter
        score_cible = simpledialog.askinteger("Score Cible", "Entrez le score à atteindre pour terminer le jeu:", minvalue=1, maxvalue=100)
        return score_cible
    def afficher_score(score):
        police = pygame.font.SysFont('arial', 20)
        texte = police.render(f'Score: {score}', True, bleu)
        fenetre.blit(texte, [10, 10])
    
    def notre_serpent(taille_serpent, serpent_pos):
        # Dessiner la tête du serpent avec une couleur différente
        tete = serpent_pos[0]
        pygame.draw.rect(fenetre, couleur_ns, pygame.Rect(tete[0], tete[1], taille_serpent, taille_serpent))
    
        # Dessiner le reste du corps du serpent
        for pos in serpent_pos[2:]:
            pygame.draw.rect(fenetre, couleur_ns_queue, pygame.Rect(pos[0], pos[1], taille_serpent, taille_serpent))
    
    def game_over():
        police = pygame.font.SysFont('arial', 30)
        texte = police.render('Game Over!', True, rouge)
        fenetre.blit(texte, [largeur // 2 - 80, hauteur // 2 - 20])
        pygame.display.update()
        time.sleep(2)
        pygame.quit()
        retour_menu_principale()
    def gagant():
        police = pygame.font.SysFont('arial', 30)
        texte = police.render('Tu as gagné!', True, rouge)
        fenetre.blit(texte, [largeur // 2 - 80, hauteur // 2 - 20])
        pygame.display.update()
        time.sleep(2)
        pygame.quit()
        retour_menu_principale()
        
    
    # Boucle principale du jeu
    score_cible= demander_score_cible()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT and direction != 'GAUCHE':
                    changer_direction = 'DROITE'
                if event.key == pygame.K_LEFT and direction != 'DROITE':
                    changer_direction = 'GAUCHE'
                if event.key == pygame.K_UP and direction != 'BAS':
                    changer_direction = 'HAUT'
                if event.key == pygame.K_DOWN and direction != 'HAUT':
                    changer_direction = 'BAS'
    
        # Mettre à jour la direction
        direction = changer_direction
    
        # Mettre à jour la position du serpent
        if direction == 'DROITE':
            serpent_pos[0][0] += taille_serpent
        if direction == 'GAUCHE':
            serpent_pos[0][0] -= taille_serpent
        if direction == 'HAUT':
            serpent_pos[0][1] -= taille_serpent
        if direction == 'BAS':
            serpent_pos[0][1] += taille_serpent
    
        # Vérifier les collisions avec les bords
        if serpent_pos[0][0] < 0 or serpent_pos[0][0] >= largeur or serpent_pos[0][1] < 0 or serpent_pos[0][1] >= hauteur:
            game_over()
    
        # Vérifier les collisions avec le corps du serpent
        for bloc in serpent_pos[1:]:
            if serpent_pos[0] == bloc:
                game_over()
        if score==score_cible:
            gagant()
        # Dessiner la pomme
        pygame.draw.rect(fenetre, rouge, pygame.Rect(pomme_pos[0], pomme_pos[1], taille_serpent, taille_serpent))
    
        # Vérifier si le serpent mange la pomme
        if serpent_pos[0] == pomme_pos:
            pomme_pos = [random.randint(0, (largeur - taille_serpent) // taille_serpent) * taille_serpent,
                     random.randint(0, (hauteur - taille_serpent) // taille_serpent) * taille_serpent]
            serpent_pos.append(serpent_pos[-1].copy())  # Ajouter un nouveau bloc au serpent
            score += 1
    
        # Mettre à jour la position du serpent
        for i in range(len(serpent_pos) - 1, 0, -1):
            serpent_pos[i] = serpent_pos[i - 1].copy()
    
    
        # Effacer l'écran
        fenetre.fill(noir)
        
        # Dessiner le serpent
        notre_serpent(taille_serpent, serpent_pos)
        
        # Dessiner la pomme
        pygame.draw.rect(fenetre, rouge, pygame.Rect(pomme_pos[0], pomme_pos[1], taille_serpent, taille_serpent))
        
        # Afficher le score
        afficher_score(score)
        
        # Mettre à jour l'affichage
        pygame.display.update()
        # Contrôler la vitesse du jeu
        horloge.tick(vitesse_serpent)
    
