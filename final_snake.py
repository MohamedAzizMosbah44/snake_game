def main():
    import snake
    import snake_Ai
    import tkinter as tk
    from tkinter import simpledialog,messagebox
    def selection_mode_jeu():
        root = tk.Tk()
        root.withdraw()
        mode_jeu = simpledialog.askstring("Mode de Jeu", "Choisissez le mode de jeu (solo/ia):", initialvalue="solo", parent=root)
        return mode_jeu
    def selection_couleur():
        root = tk.Tk()
        root.withdraw()
        couleur = simpledialog.askstring("Couleur", "Choisissez le mode de jeu (vert/rouge):", parent=root)
        if couleur is None:
            main()
        if not (couleur=="vert" or couleur == "rouge"):
            messagebox.showinfo("erreur","Choisi un choix valide")
            couleur = simpledialog.askstring("Couleur", "Choisissez le mode de jeu (vert/rouge):", parent=root)
        return couleur
    def selection_vitesse():
        root = tk.Tk()
        root.withdraw() 
        vitesse = simpledialog.askstring("Vitesse", "Choisissez la vitesse de serpent (entre 1 et 20):", initialvalue="5", parent=root)
        if vitesse is None:
            main()
        if (not vitesse.isdigit()) or (not (0<int(vitesse)<=20)):
            messagebox.showinfo("erreur","Choisi un choix valide")
            vitesse = simpledialog.askstring("Vitesse", "Choisissez la vitesse de serpent (entre 1 et 20):", initialvalue="5", parent=root)
        return int(vitesse)
    while True:
        mode=selection_mode_jeu()
        if mode is None:  # Si l'utilisateur a cliqué sur "Cancel" ou la croix
            print("Fermeture du programme demandée par l'utilisateur.")
            break
        elif mode=='ia':
            vitesse=selection_vitesse()
            couleur=selection_couleur()
            snake_Ai.programme_IA(couleur,vitesse)
        elif mode=='solo':
            vitesse=selection_vitesse()
            couleur=selection_couleur()
            snake.programme_solo(couleur,vitesse)
        else:
            messagebox.showinfo("erreur","Choisi un choix valide")
            mode=selection_mode_jeu()
main()