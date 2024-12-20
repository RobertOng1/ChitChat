# coding: utf8
import sys
import time
import socket
import tkinter
import winsound
import platform
import threading
from tkinter import *
import tkinter.simpledialog
import tkinter.font as tkFont
from tkinter import messagebox
from random import randint, choices
from tkinter.scrolledtext import ScrolledText
from Modules import ChiffrementRSA, Fonctions, LecteurSauvegarde, Paramètres, Sauvegarde, Serveur, Kripiti


"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

                                          Index

I. Définition de AfficherMenu().......................................................128

    La fonction qui affiche le menu principal de l'application. Elle est appellée au 
    démarrage de l'application et quand l'utilisateur retourne au menu.

II. Hôte et clients...................................................................150

    Les fonctions qui servent à afficher le menus de connexion pour le client et celles 
    qui servent à démarrer le serveur.

    A. Travail spécifique à l'hôte....................................................150

        1. Définition de DevenirHôte()................................................150

            Cette fonction affiche le menu qui permet à l'hôte de configurer le mode de 
            connexion au serveur (Ip, Port et nom d'utilisateur)

        2. Définition de DémarrerServeur()............................................222

            Cette fonction lance le thread du serveur, en récupérant les informations
            données sur l'interface de connexion.

    B. Fonctions spécifiques au client................................................266

        1. Définition de DevenirClient()..............................................266

            Cette fonction affiche l'interface qui permet choisir à quel serveur se 
            connecter 

        2. Définition de SeConnecter()................................................367

            Fonction qui récupere les informations saisies par l'utilisateur dans la 
            fonction DevenirClient() et qui initie une connexion avec le serveur.
    

III. Connexion et envoi de messages...................................................314

    Les fonctions dédiées à l'envoi et à la réception de messages au serveur

    A. Connexion......................................................................314

        1. Définition de Connexion()..................................................314

            Cette fonction sert à se connecter au serveur et à Envoyer le nom 
            d'utilisateur, la clé publique, le module de chiffrement au serveur, et on 
            recoit les informations de chiffrement du serveur, la clé publique et le 
            module de chiffrement. Si le serveur demande un mot de passe,  c'est cette 
            fonction qui le récupére auprès de l'utilisateur, le chiffre et l'envoi au 
            serveur.

    B. Définition de AffichageConversations().........................................381

        Cette fonction sert à générer l'interface de la conversation
   
    C.Envoyer et Recevoir.............................................................481

        1. Définition de Envoyer()....................................................481

            Fonctions qui fonctionne avec deux mode :

                - Le mode "automatique": La fonction récupere la valeur du champ de 
                saisie et l'envoi au serveur
                
                - Le mode "manuel": La fonction est appellée et envoie le message au 
                serveur

        2. Définition de Réception()..................................................607

            Cette fonction est un thread (Suite d'instructions qui s'exécutent arrière 
            plan de l'application). Il permet de recevoir des messages du serveur.

IV. Barre d'application...............................................................687

    A. Définition de RetournerMenu()..................................................687

        Fonction qui efface le contenu de la fenêtre et affiche le menuPrincipal

    B. Définition de InfosServeur()...................................................743

        La fenêtre qui affiche les informations sur le serveur

    C. Définition de Help()...........................................................787

        Fenêtre qui affiche de l'Help

    D. Activer et désactiver le son...................................................828

        Fonctions triviales

        1. Définition de ActiverSon().................................................828

        2. Définition de CouperSon()..................................................837

V. Définition de fermeture()..........................................................900
    
    Fonctions appelée quand l'utilisateur ferme la fenêtre

VI.Lancement du programme.............................................................912

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""


def AfficherMenu():

    """ Fonction qui affiche le menu principal de l'application """

    global MessageBienvenue, CadreBouttons, Logo

    Logo = Label(fen, bg="grey", image=ImageLogo)
    Logo.pack()

    MessageBienvenue = Label(fen, text="Welcome to Chit Chat.\n To get started, tell us if you want to be a host or a client", bg="grey", font=PoliceTitre)
    MessageBienvenue.pack()

    CadreBouttons = Frame(fen, bg="grey")
    CadreBouttons.pack(pady=60)

    BouttonHôte = Button(CadreBouttons, text="Host", font=PoliceBoutton, command=DevenirHôte)
    BouttonHôte.pack(side=LEFT, padx=7)

    BouttonClient = Button(CadreBouttons, text="Client", font=PoliceBoutton, command=DevenirClient)
    BouttonClient.pack(side=LEFT, padx=7)


def DevenirHôte():

    """ Fonction qui affiche l'interface qui permet de définir l'Ip et le port qui seront
    utilisées par le serveur. """

    global InputIp, IP, InputPort, InputNom, CadreParamètres, SousMenuCliqué

    SousMenuCliqué = True
    #Si l"utilisateur veut retourner au menu, on sait qu'il est dans un sous-menu

    MessageBienvenue.pack_forget()
    CadreBouttons.pack_forget()

    Machine = socket.gethostname()
    IP = socket.gethostbyname(Machine)

    CadreParamètres = Frame(fen, bg="grey")
    CadreParamètres.pack()

    # Label de l'adresse Ip
    Label(CadreParamètres, text="Your IP Address:", bg="Grey").pack(anchor=CENTER, pady=7)
    # Pas besoin de stocker les labels dans une variable, on n'aura pas besoin de les 
    # récupérer plus tard

    InputIp = Entry(CadreParamètres)
    InputIp.insert("end", IP) #On insére l'Ip qu'on à récupéré auparavant
    InputIp.pack(anchor=CENTER)

    #Label du port
    Label(CadreParamètres, text="Port:", bg="Grey").pack(anchor=CENTER, pady=7)

    InputPort = Entry(CadreParamètres)
    InputPort.pack(anchor=CENTER)

    if Paramètres.DicoParamètres["PortPréféré"] != "Inconnu":
    # Si l'utilisateur a définit un port par défaut
        Fonctions.placeholder(InputPort, Paramètres.DicoParamètres["PortPréféré"], True)
        #La fonction placeholder reproduit à peu prés le même comportement que l'attribut HTML du
        # même nom : Elle sert à afficher une suggestion qui s'efface de la zone de saisie au clic
        # sur cette dernière.

    else:
        
        PortRecommandé = randint(49152, 65535)
        #On recommande un port dans la plage de ceux les moins utilisés
        Fonctions.placeholder(InputPort, PortRecommandé, True)

    #Label du nom d'utilisateur
    Label(CadreParamètres, text="Your username:", bg="Grey").pack(anchor=CENTER, pady=7)

    InputNom = Entry(CadreParamètres)
    InputNom.pack(anchor=CENTER)

    if Paramètres.DicoParamètres["NomUserDéfaut"] != "Inconnu":
    # Si l'utilisateur a définit un nom d'utilisateur par défaut
        Fonctions.placeholder(InputNom, Paramètres.DicoParamètres["NomUserDéfaut"], True)

    else:

        SuggestionNom = choices(ListeNoms)
        Fonctions.placeholder(InputNom, SuggestionNom[0], True)

    InputNom.bind("<Button-1>", lambda z: Fonctions.placeholder(InputNom, "", False))
    #On utilise une fonction anonyme lambda pour pouvoir exécuter une fonction avec des arguments
    #On associe le clic gauche sur la zone de saisie du nom à la fonction placeholder, qui effacera le contenu
    # de la zone si c'est la suggestion originale

    InputPort.bind("<Button-1>", lambda z: Fonctions.placeholder(InputPort, "", False))

    BouttonStart = Button(CadreParamètres, text="Start", command=DémarrerServeur)
    BouttonStart.pack(pady=20)

def DémarrerServeur():

    """ Cette fonction récupére les coordonées du serveur saisis dans le menu d'hôte, et lance
    le thread du serveur """

    global InputIp, IP, InputPort, Port, Rôle, InputNom, FichierSauvegarde, MotDePasse, NomUser, SauvegardeUtilisée

    if len(InputNom.get()) > 16:

        tkinter.messagebox.showerror(title="Username too long", message="Your username must be less than 16 characters")
        return False
        #On stoppe l'exécution de la fonction

    Rôle = "Hôte"
    IP = InputIp.get()

    try: Port = int(InputPort.get())
    except ValueError:

        tkinter.messagebox.showerror(title="Port problem", message="The port must be an integer between 1 and 65535")
        return False

    Serveur.Démarrer(IP, Port, Paramètres.DicoParamètres["NombreUsersMax"], Paramètres.DicoParamètres["MotDePasse"])

    time.sleep(0.2)
    #On attend que le serveur démarre

    if Connexion() == True:
    #Si la connexion est une réussite, on affiche les conversations

        if Paramètres.DicoParamètres["Sauvegarde"] == "Activée":

            SauvegardeUtilisée = True

            MotDePasse = tkinter.simpledialog.askstring("Password", "Please enter the backup password", show="•")

            if MotDePasse == None or MotDePasse == "":  
                    #Si l'utilisateur annule la connexion, il faut se déconnecter du serveur

                Envoyer(ModeManuel = True, MessageManuel = "/stop")
                ConnexionSocket.close()
                return False

            ConfirmationMotDePasse = tkinter.simpledialog.askstring("Confirmation", "Please confirm the password", show="•")

            if ConfirmationMotDePasse == None or ConfirmationMotDePasse == "":

                Envoyer(ModeManuel = True, MessageManuel = "/stop")
                ConnexionSocket.close()
                return False

            while ConfirmationMotDePasse != MotDePasse:

                ConfirmationMotDePasse = tkinter.simpledialog.askstring("Wrong confirmation", "The two passwords don't match. Please confirm the password", show="•")

            FichierSauvegarde = Sauvegarde.InitialisationSauvegarde(MotDePasse)

        AffichageConversations()


def Connexion():

    """ Cette fonction sert à se connecter au serveur et à Envoyer le nom d'utilisateur, la clé publique, le module de chiffrement au serveur,
    et on recoit les informations de chiffrement du serveur, la clé publique et le module de chiffrement. Si le serveur demande un mot de passe,
    c'est cette fonction qui le récupére auprès de l'utilisateur, le chiffre l'envoi au serveur."
    """

    global IP, Port, NomUser, InputNom, ConnexionSocket, InputIp, Rôle, CléPublique, CléPubliqueServeur, ModuleServeur, NombreConnectés

    IP = InputIp.get()

    try: Port = int(InputPort.get())
    except ValueError:

        tkinter.messagebox.showerror(title="Port problem", message="The port must be an integer between 1 and 65535")
        return False
    NomUser = InputNom.get()

    ConnexionSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #On défini notre connexion socket
    # - AF_INET => Protocole IPV4
    # - SOCK_STREAM => Stream veut dire cours d'eau, comme un flot continu de donnés qui est envoyé

    ConnexionSocket.settimeout(5)
    #Si au bout de 5secondes, il n'y pas de réponse (Délai plus que nécéssaire pour des simples paquets TCP) une exception est générée

    try: ConnexionSocket.connect((IP, Port))

    except (ConnectionRefusedError, socket.timeout):
    #Si on arrive pas à se connecter au serveur

        if Rôle != "Hôte":
        #Si c'est l'hôte, il a déja recu l'erreur de la part du serveur donc affiche rien

            MessageErreur = "It appears that the server coordinates are not valid. Refer to Help to resolve this problem."
            tkinter.messagebox.showerror(title = "Coordinates problem", message = MessageErreur)
    
        return False
    
    else:

        InfosChiffrement = f"{NomUser}\n{CléPublique}\n{Module}"
        InfosChiffrement = InfosChiffrement.encode('utf-8')

        ConnexionSocket.send(bytes(InfosChiffrement))
        #On formate, puis on envoi les informations de chiffrement au serveur

        AutorisationEtDonnées = ConnexionSocket.recv(4096)
        AutorisationEtDonnées = AutorisationEtDonnées.decode("utf-8")
        #On recoit de la part du serveur l'autorisation de se connecter, et les informations de chiffrement du serveur

        if AutorisationEtDonnées != "False":
        #Si le serveur autorise la connexion

            AutorisationEtDonnées = AutorisationEtDonnées.split("|")
            #On récupere les données sous forme de le liste

            CléPubliqueServeur = int(AutorisationEtDonnées[0])
            ModuleServeur = int(AutorisationEtDonnées[1])
            PrésenceMotDePasse = AutorisationEtDonnées[2]
            NombreConnectés = int(AutorisationEtDonnées[3])

            if PrésenceMotDePasse == "True" and Rôle != "Hôte":
            # l'hôte n'a pas besoin de se connecter

                ConnexionEnAttente  = True

                while ConnexionEnAttente:

                    MotDePasseServeur= tkinter.simpledialog.askstring("Server password", "This server requires a password to connect", show="•")

                    if MotDePasseServeur == None or MotDePasseServeur == "":
                    #Si l'utilisateur annule la connexion, il faut se déconnecter du serveur

                        ConnexionSocket.close()
                        return False

                    else:

                        MotDePasseServeurChiffré = ChiffrementRSA.chiffrement(MotDePasseServeur, CléPubliqueServeur, ModuleServeur)

                        ConnexionSocket.send(bytes(MotDePasseServeurChiffré, "utf-8"))

                        Autorisation = ConnexionSocket.recv(4096)
                        Autorisation =  Autorisation.decode("utf-8")

                        if Autorisation == "OK":
                            ConnexionEnAttente = False

                        else:
                            tkinter.messagebox.showwarning(title="Incorrect password", message="Password is incorrect")


            ConnexionSocket.setblocking(0)
            #On définit le mode de connexion sur non bloquant (Voir explications dans la fonction réception)

            return True
            #On retoune que la connexion a été validé

        else:
        #Si le serveur ne donne pas son autorisation

            motif = ConnexionSocket.recv(4096)
            #On recoit du serveur le motif du refus de

            tkinter.messagebox.showerror(title="Connection refused by server", message=motif.decode("utf-8"))
            return False

def DevenirClient():

    """ Cette fonction affiche l'interface qui permet choisir à quel serveur se connecter"""

    global InputIp, InputPort, InputNom, CadreParamètres, SousMenuCliqué

    SousMenuCliqué = True
    #Si l"utilisateur veut retourner au menu, on sait qu'il est dans un sous-menu

    MessageBienvenue.pack_forget()
    CadreBouttons.pack_forget()

    CadreParamètres = Frame(fen, bg="grey")
    CadreParamètres.pack()

    #Label Adresse ip du serveur
    Label(CadreParamètres, text="Server IP address:", bg="Grey").pack(anchor=CENTER, pady=7)

    InputIp = Entry(CadreParamètres)
    InputIp.insert("end", "192.168.1.")
    InputIp.pack(anchor=CENTER)

    PortduServeur = Label(CadreParamètres, text="Server port:", bg="Grey")
    PortduServeur.pack(anchor=CENTER, pady=7)

    InputPort = Entry(CadreParamètres)
    InputPort.pack(anchor=CENTER)

    #Label de nom
    Label(CadreParamètres, text="Your username:", bg="Grey").pack(anchor=CENTER, pady=7)

    InputNom = Entry(CadreParamètres)
    InputNom.pack(anchor=CENTER)

    if Paramètres.DicoParamètres["NomUserDéfaut"] != "Inconnu":
    # Si l'utilisateur a définit un nom d'utilisateur par défaut
        Fonctions.placeholder(InputNom, Paramètres.DicoParamètres["NomUserDéfaut"], True)

    else:
        SuggestionDeNom = choices(ListeNoms)
        Fonctions.placeholder(InputNom, SuggestionDeNom[0], True)

    InputNom.bind("<Button-1>", lambda b: Fonctions.placeholder(InputNom, "", False))
    #On utilise une fonction anonyme lambda pour pouvoir executer une fonction avec des arguments

    Button(CadreParamètres, text="Login",  command=SeConnecter).pack(pady=20)


def SeConnecter():

    """ Fonction qui affiche l'interface de discusion si la connexion au serveur est une réussite"""

    global InputIp, IP, InputPort, Port, Rôle, FichierSauvegarde, MotDePasse, SauvegardeUtilisée

    Rôle = "Client"
    IP = InputIp.get()

    try: Port = int(InputPort.get())
    except ValueError:

        tkinter.messagebox.showerror(title="Port problem", message="The port must be an integer between 1 and 65535")
        return False

    if Connexion() == True:

        if Paramètres.DicoParamètres["Sauvegarde"] == "Activée":

            SauvegardeUtilisée = True

            MotDePasse = tkinter.simpledialog.askstring("Password", "Please enter the backup password", show="•")

            if MotDePasse == None or MotDePasse == "":
            #Si l'utilisateur annule la connexion, il faut se déconnecter du serveur

                ConnexionSocket.close()
                return False

            ConfirmationMotDePasse = tkinter.simpledialog.askstring("Confirmation", "Please confirm the password", show="•")

            if ConfirmationMotDePasse == None or ConfirmationMotDePasse == "":
            #Si l'utilisateur annule la connexion, il faut se déconnecter du serveur

                ConnexionSocket.close()
                return False

            while ConfirmationMotDePasse != MotDePasse:

                ConfirmationMotDePasse = tkinter.simpledialog.askstring("Confirmation", "Wrong confirmation. Please confirm the password", show="•")

            FichierSauvegarde = Sauvegarde.InitialisationSauvegarde(MotDePasse)

        AffichageConversations()

    
def AffichageConversations():

    """ Cette fonction sert à générer l'interface de la conversation"""

    global CadreParamètres, SaisieMessage, NomUser, FilsMessages, BouttonEnvoyer, ConnexionEnCours, ThreadRéception

    Logo.pack_forget()
    CadreParamètres.pack_forget()

    BarreMenu.delete(1)
    BarreMenu.insert_command(1, label="Menu", command= lambda : RetournerMenu(DemandeConfirmation = True, ConversationEnCours = True))
    #On remplace la commande "Menu" pour car la commande associée doit avoir l'argument "ConversationEnCours" à jour

    BarreMenu.insert_command(2, label = "Mute Sound", command = CouperSon)
    BarreMenu.insert_command(4, label = "Server Info", command = InfosServeur)

    FilsMessages = Listbox(fen, width="70", height="20")
    FilsMessages.pack(pady=15)

    SaisieMessage = Entry(fen, width="60")
    SaisieMessage.pack()

    BouttonEnvoyer = Button(fen, text="Send", command=Envoyer)
    BouttonEnvoyer.pack(pady=15)

    SaisieMessage.bind("<Button-1>", lambda a: Fonctions.placeholder(SaisieMessage, "", False))
    #On utilise une lambda pour appeler une fonction avec des arguments

    fen.bind_all('<Return>', lambda c: Envoyer())
    #On associe l'appui a a fonction Envoyer avec une fonction lambda afin de pouvoir Envoyer aucun argument

    ConnexionEnCours = True #Tant que cette variable est égale à True, le thread tournera

    ThreadRéception = threading.Thread(target=Réception)
    ThreadRéception.daemon = True #Cet attribut signifie que quand il ne reste que ce thread, le programme s'arrête.
    ThreadRéception.start()

    Fonctions.placeholder(SaisieMessage, "Enter your message here", True)


def Envoyer(ModeManuel = False, MessageManuel = None):

    #Le mode manuel est un mode qui ne récupére pas l'entrée, mais le message passé en argument

    """Fonction qui chiffre et envoi les message au serveur. Les messages sont chiffrés en fonction du serveur"""

    global SaisieMessage, NomUser, FilsMessages, ConnexionSocket, NombreErreurs, CléPubliqueServeur, ModuleServeur, SonActivé, EnvoiPossible

    if ModeManuel == True: message = MessageManuel
    else: message = SaisieMessage.get()

    if len(message) > 1000: tkinter.messagebox.showerror(title="Beware of spam !", message="To avoid overloading the server, messages of more than 1000 characters are prohibited")

    elif message == "": pass
    elif message[0] == "/":
    #C'est une commande 

        PremierArgument = Fonctions.ParserCommande(message)

        RéponseUser = None
        stop = False
        Permission = True

        if PremierArgument == "/stop" and ModeManuel == False and Rôle == "Hôte":

            RéponseUser = tkinter.messagebox.askokcancel("Chit Chat","Do you really want to stop the server?")
            stop = True

        elif PremierArgument == "/stop" and ModeManuel == False and Rôle != "Hôte":

            tkinter.messagebox.showerror(title = "Permission error", message = "You can't stop the server, you are not the host of the discussion")
            Permission = False

        elif PremierArgument == "/lock" and Rôle == "Client" or message == "/unlock" and Rôle == "Client":

            tkinter.messagebox.showerror(title = "Permission Error", message = "You cannot lock/unlock the server, you are not a discussion admin")
            Permission = False

        elif PremierArgument == "/ban" and Rôle == "Client":

            tkinter.messagebox.showerror(title = "Permission Error", message = "You cannot ban a customer, you are not a discussion admin")
            Permission = False

        elif PremierArgument == "/kick" and Rôle == "Client":

            tkinter.messagebox.showerror(title = "Permission Error", message = "You cannot kick a customer, you are not the discussion admin")
            Permission = False

        elif PremierArgument == "/op" and Rôle != "Hôte":

            tkinter.messagebox.showerror(title = "Permission Error", message = "You cannot use this command, you are not the host of the discussion")
            Permission = False

        if RéponseUser == True and Rôle == "Hôte" or ModeManuel == True or PremierArgument != "/stop" and Permission == True:

            message = Fonctions.formaterPaquet("Commande", message)
            message = ChiffrementRSA.chiffrement(message, CléPubliqueServeur, ModuleServeur)

            messageFinal = f"{len(message)}-{message}"
            messageFinal = messageFinal.encode('utf-8')

            try: ConnexionSocket.send(bytes(messageFinal))
            except (ConnectionResetError, ConnectionAbortedError):
            #Si le serveur ne répond pas

                if NombreErreurs < 3:
                    tkinter.messagebox.showerror(title="Server Error", message="Unable to reach the server. Please try again.")
                    NombreErreurs += 1
                else:
                #Si il y'a plus de trois erreurs, on stoppe le programme, en invitant l'utilisateur à se reconnecter

                    messsageErreur = "The server is unreachable at the moment. Please log in again or refer to Help"
                    tkinter.messagebox.showerror(title="Aïe...", message=messsageErreur)
                    RetournerMenu(DemandeConfirmation = False, ConversationEnCours = True)

            if stop == True: RetournerMenu(DemandeConfirmation = None, ConversationEnCours = True, DemandeArrêt = False)

            SaisieMessage.delete(0, 'end')

    elif len(message) != 0 and EnvoiPossible:

        EnvoiPossible = False

        messageInterface = f"[{time.strftime('%H:%M:%S')}] {NomUser} → {message}"
        #On garde de coté un message avec un formaté spécialement pour l'interface, mais on ne l'utilise que si l'envoi est réussi.

        message = Fonctions.formaterPaquet("Message", message)

        message = ChiffrementRSA.chiffrement(message, CléPubliqueServeur, ModuleServeur)
        messageFinal = f"{len(message)}-{message}"
        #On rajoute un en tête avec la longueur totale du message
        messageFinal = messageFinal.encode('utf-8')

        try: ConnexionSocket.send(bytes(messageFinal))
        except (ConnectionResetError, ConnectionAbortedError):
        #Si le serveur ne répond pas

            if NombreErreurs < 3:
                tkinter.messagebox.showerror(title="Ouch...", message="Unable to reach the server. Please try again.")
                NombreErreurs += 1

            else:
            #Si il y'a plus de trois erreurs, on stoppe le programme, en invitant l'utilisateur à se reconnecter

                messsageErreur = "The server is unreachable at the moment. Please login again or refer to Help"
                #On stocke le message dans un variable pour diminuer la taille de la ligne d'en dessous
                tkinter.messagebox.showerror(title="Aïe...", message=messsageErreur)
                RetournerMenu(DemandeConfirmation = False, ConversationEnCours = True)

        else:
        #Si il n'a pas eu d'execeptions

            if len(messageInterface) > 70:
            #Si le message à afficher fait plus de 70 caratères

                LignesMessages = Fonctions.couperPhrases(messageInterface)
                #On recupere plusieurs lignes de moins de 70 caractères dans une liste

                for ligne in LignesMessages:
                    FilsMessages.insert(END, ligne)

                    if Paramètres.DicoParamètres["Sauvegarde"] == "Activée" and SauvegardeUtilisée:
                        Sauvegarde.NouvelleLigne(FichierSauvegarde, MotDePasse, ligne)
            else:
                FilsMessages.insert(END, messageInterface)

                if Paramètres.DicoParamètres["Sauvegarde"] == "Activée" and SauvegardeUtilisée:
                    Sauvegarde.NouvelleLigne(FichierSauvegarde, MotDePasse, messageInterface)

            FilsMessages.yview(END)
            #On défile tout en bas cette dernière, vers le message le plus récent

            if SonActivé == True:

                if Paramètres.DicoParamètres["SonEnvoi"] != "Inconnu":
                    winsound.PlaySound("Sons/" + Paramètres.DicoParamètres["SonEnvoi"], winsound.SND_ASYNC)

                else:
                    winsound.PlaySound("Sons/Pop.wav", winsound.SND_ASYNC)

            SaisieMessage.delete(0, 'end')

            def RéactivationEnvoi():

                global EnvoiPossible

                EnvoiPossible = True

            fen.after(500, RéactivationEnvoi)
            #Au bout de 500ms en asynchrone, on appelle la fonction qui rendra possible l'envoi de messages

def Réception():

    """Cette fonction est un thread (Suite d'instructions qui s'exécutent arrière plan de l'application). Il permet de recevoir 
    des messages du serveur."""

    global FilsMessages, ConnexionSocket, CléPrivée, Module, SonActivé, ConnexionEnCours, NombreConnectés, Rôle

    while ConnexionEnCours == True:
    #Quand Connexion est égal à False, le Thread s'arrête

        NotifSilencieuse = False
        #Est égal à true si le client recoit un messsage qui ne doit pas s'afficher (connexion/déconnexion par exemple)

        try: MessageReçu = ConnexionSocket.recv(32768)
        #Cette partie du code est dans un bloc "try, except" car "ConnexionSocket.setblocking(0)" a été défini sur False
        #Au lieu d'attendre un message, si rien n'est envoyé cela va générer une exception, ce qui permet un fonctionnement asynchrone.
  
        except BlockingIOError:
        #Si aucun message n'a été envoyé, on ne fait rien et on attend pour préserver les ressources la machine
            time.sleep(0.1)

        except (ConnectionAbortedError, ConnectionResetError):
        #Le serveur a crashé

            tkinter.messagebox.showerror(title="Server Problem", message="The server crashed...")
            RetournerMenu(ConversationEnCours = True)
            #32768 est la limite d'octets recevables

        else:
        #Un message a été reçu

            MessageReçu = MessageReçu.decode("utf-8")

            if MessageReçu != "":

                MessageReçu = MessageReçu.split("-")
                #Le message comporte un petit entête
                #Exemple = 564-6646464/65656/4564564654, 564 est içi la longueur totale du message.

                LongeurMessage = int(MessageReçu[0])

                while len(MessageReçu[1]) < LongeurMessage:
                #Tant que le message recu est plus petit que la longueur totale du message

                    SuiteDuMessage = ConnexionSocket.recv(32768)
                    SuiteDuMessage = SuiteDuMessage.decode("utf-8")

                    MessageReçu[1] += SuiteDuMessage
                    #On ajoute la suite du message reçu

                MessageReçu = ChiffrementRSA.déchiffrement(MessageReçu[1], CléPrivée, Module)
                #On ne déchiffre que l'index 1 du message, qui est le messge en lui même
                #0 étant la longueur de ce message

                if MessageReçu == "ban":

                    tkinter.messagebox.showinfo(title = "You have been banned", message = "You have been banned from the server, you can no longer login again.")
                    ConnexionEnCours = False
                    RetournerMenu(ConversationEnCours = True)
                    NotifSilencieuse = True

                elif MessageReçu == "kick":

                    tkinter.messagebox.showinfo(title = "You have been kicked", message = "You have been kicked from the server.")
                    ConnexionEnCours = False
                    RetournerMenu(ConversationEnCours = True)
                    NotifSilencieuse = True

                if MessageReçu == "connection":

                    NombreConnectés += 1
                    NotifSilencieuse = True

                elif MessageReçu == "disconnection":

                    NombreConnectés -= 1
                    NotifSilencieuse = True

                elif MessageReçu == "promotion":

                    Rôle = "Admin"
                    NotifSilencieuse = True

                elif MessageReçu == "retrogade":

                    Rôle = "Client"
                    NotifSilencieuse = True

                elif len(MessageReçu) > 70:
                #Si le message à afficher fait plus de 70 caratères

                    LignesMessages = Fonctions.couperPhrases(MessageReçu)
                    #On recupére plusieurs lignes de moins de 70 caractères dans une liste

                    for ligne in LignesMessages:

                        FilsMessages.insert(END, ligne)

                        if Paramètres.DicoParamètres["Sauvegarde"] == "Activée":
                            Sauvegarde.NouvelleLigne(FichierSauvegarde, MotDePasse, ligne)

                else:
                    FilsMessages.insert(END, MessageReçu)

                    if Paramètres.DicoParamètres["Sauvegarde"] == "Activée":
                        Sauvegarde.NouvelleLigne(FichierSauvegarde, MotDePasse, MessageReçu)

                FilsMessages.yview(END)
                #On force le défilement tout en bas de cette dernière

                if FenêtreALeFocus == False and NotifSilencieuse == False and Paramètres.DicoParamètres["Notification"] == "Activée":

                    Fonctions.AfficherNotification("Chit Chat", MessageReçu)

                if SonActivé == True and NotifSilencieuse == False:

                    if Paramètres.DicoParamètres["SonRéception"] != "Inconnu":
                        winsound.PlaySound("Sons/" + Paramètres.DicoParamètres["SonRéception"], winsound.SND_ASYNC)
                    else:
                        winsound.PlaySound("Sons/Dong.wav", winsound.SND_ASYNC)


def RetournerMenu(DemandeConfirmation = None, ConversationEnCours = None, DepuisMenu = None, DemandeArrêt = True):

    global FilsMessages, SaisieMessage, BouttonEnvoyer, SousMenuCliqué, ConnexionEnCours

    Confirmation = None

    if DemandeConfirmation == True:
        Confirmation = messagebox.askquestion (f"You are already leaving {NomUser} ?","You really want to return to the menu ?", icon = "warning")

    if Confirmation == "yes" or DemandeConfirmation == None:

        if ConversationEnCours:
        #Si l'utilisateur était dans la fenêtre de conversation

            SousMenuCliqué = False

            if Rôle == "Hôte" and  DemandeArrêt == True:

                Envoyer(True, "/stop") #L'envoi du /stop permet d'éviter au serveur de crasher / tourner dans le vide
                time.sleep(0.3)

            BarreMenu.delete(1)
            BarreMenu.insert_command(1, label="Menu", command= lambda : RetournerMenu(DepuisMenu = True))
            #On remplace la commande "Menu" pour car la commande associée doit avoir l'argument "ConversationEnCours" à jour

            FilsMessages.pack_forget()
            SaisieMessage.pack_forget()
            BouttonEnvoyer.pack_forget()

            fen.unbind_all(ALL)
            fen.bind("<FocusIn>", lambda x: PasserEnTrue())
            fen.bind("<FocusOut>", lambda x: PasserEnFalse())

            BarreMenu.delete(2)
            BarreMenu.delete(3)
            #On efface les commandes "Couper Son" et "Infos Serveur" du menu

            ConnexionEnCours = False #Le thread de réception est arrêté
            ConnexionSocket.close()

        if DepuisMenu:
        #Si l'utilisateur était dans la fenêtre de menu

            if SousMenuCliqué:
            #Si l'utilisateur était dans le sous menu (Démarrage du serveur ou connexion)

                Logo.pack_forget()
                CadreParamètres.pack_forget()

        if SousMenuCliqué or ConversationEnCours:
        #Si l"utilisateur n'est pas dans le menu principal

            if SousMenuCliqué:
                SousMenuCliqué = False

            AfficherMenu()


def InfosServeur():

    """ Cette fonction affiches les informations du serveur dans une fenêtre en top level"""

    global IP, Port, NombreConnectés
      
    fenInfos = Toplevel()
    fenInfos.geometry("300x280")
    fenInfos.configure(bg="grey")
    fenInfos.resizable(width=False, height=False)
    fenInfos.iconbitmap(bitmap="Médias/information.ico")
    fenInfos.title("Server Info")

    TitreAdresseServeur = Label(fenInfos, text="Server address", bg="Grey", font=PoliceTitre)
    TitreAdresseServeur.pack(pady=10)

    AdresseServeur = Label(fenInfos, text=IP, bg="Grey", font=PoliceSousTitre)
    AdresseServeur.pack()

    TitrePortServeur = Label(fenInfos, text="Server port", bg="Grey", font=PoliceTitre)
    TitrePortServeur.pack(pady=10)

    PortServeur = Label(fenInfos, text=Port, bg="Grey", font=PoliceSousTitre)
    PortServeur.pack()

    TitreUtilisateursCo = Label(fenInfos, text="Connected users", bg="Grey", font=PoliceTitre)
    TitreUtilisateursCo.pack(pady=10)

    UtilisateurCo = Label(fenInfos, text = str(NombreConnectés), bg="Grey", font=PoliceSousTitre)
    UtilisateurCo.pack()

    BouttonFermer = Button(fenInfos, text="Close", command = lambda: fenInfos.destroy())
    BouttonFermer.pack(pady=20, side=BOTTOM)

    fenInfos.focus_force()
    #On affiche la fenêtre au premier plan

    fenInfos.mainloop()


def Help():

    """ Cette fonction affiche l'Help dans une fenêtre en top level"""

    def QuitterHelp():
        """Fonction qui détruit la fenêtre d'Help"""
        fenHelp.destroy()

    fenHelp = Toplevel()
    fenHelp.geometry("300x280")
    fenHelp.configure(bg="grey")
    fenHelp.resizable(width=False, height=False)
    fenHelp.iconbitmap(bitmap="Médias/information.ico")
    fenHelp.title("Help")
    #Définition de l'apparence de la fenêtre

    TitreHelpIP = Label(fenHelp, text="If your IP is invalid", bg="Grey", font=PoliceTitre)
    TitreHelpIP.pack(pady=10)

    HelpIP0 = Label(fenHelp, text="Enter the IPv4 address yourself.\nTo find it :", bg="Grey", font=PoliceSousTitre)
    HelpIP0.pack()

    HelpIP1 = Label(fenHelp, text="le-routeur-wifi.com/adresse-ip-mac/", bg="Grey", font=PoliceSousTitre, fg="blue")
    HelpIP1.pack()
    HelpIP1.bind("<Button-1>", lambda e: Fonctions.callback("https://le-routeur-wifi.com/adresse-ip-mac/"))

    TitreHelpPort0 = Label(fenHelp, text="If your port is invalid: ", bg="Grey", font=PoliceTitre)
    TitreHelpPort0.pack(pady=10)

    HelpPort0 = Label(fenHelp, text="Be sure to choose an integer\nbetween 0 and 65535", bg="Grey", font=PoliceSousTitre)
    HelpPort0.pack()

    BouttonClose = Button(fenHelp, text="Close", command=QuitterHelp)
    BouttonClose.pack(pady=20, side=BOTTOM)

    fenHelp.focus_force()
    #On affiche la fenêtre au premier plan

    fenHelp.mainloop()


def ActiverSon():
    global SonActivé

    SonActivé = True

    BarreMenu.delete(2)
    BarreMenu.insert_command(2, label="Mute the sound", command=CouperSon)
    #On supprime la commande à l'index 2 du menu pour y ajouter la commande CouperSon à la même position

def CouperSon():
    global SonActivé

    SonActivé = False

    BarreMenu.delete(2)
    BarreMenu.insert_command(2, label="Turn on sound", command=ActiverSon)
    #On supprime la commande à l'index 2 du menu pour y ajouter la commande ActiverSon à la même position


def fermeture():

    """ Fonction appellée quand l'utilisateur veut fermer la fenêtre """

    RéponseUser  = tkinter.messagebox.askokcancel("Chit Chat","Are you leaving already?")

    if RéponseUser == True:

        sys.exit()
        #On utilise sys.exit() plutôt que exit() car cela éviter au threads de tourner en arrière plan

def PasserEnTrue():

    global FenêtreALeFocus
    FenêtreALeFocus = True

def PasserEnFalse():

    global FenêtreALeFocus
    FenêtreALeFocus = False


#Code exécuté au démarage de l'application

Paramètres.LectureParamètres()

ListeNoms = ["Ozi1", "Ozi2", "Ozi3", "Ozi4", "Ozi5", "Ozi6", "Ozi7", "Ozi8"]
#La liste des noms qui seront suggérés à l'utilisateur.

FichierSauvegarde = None
MotDePasse = None
#Initilisation du mot de passe de la sauvegarde et le fichier de sauvegarde

Module, CléPublique, CléPrivée = ChiffrementRSA.génération(16)
#On génére une clé publique et une clé publique et on garde en mémoire le module de chiffrement

NombreErreurs = 0
NombreConnectés = 1 #On se compte

EnvoiPossible = True
SonActivé = True
SousMenuCliqué = False
SauvegardeUtilisée = None #On ne sait pas à ce stade si la sauvegarde sera utilsée
FenêtreALeFocus = True
#Permet d'envoyer des notifcations uniquement quand la fenêtre est en arrière plan

fen = Tk()
fen.geometry("550x460")
fen.title("Chit Chat")
fen.configure(bg="grey")
fen.resizable(width=False, height=False)
fen.iconbitmap(bitmap="Médias/icone.ico")
fen.bind("<FocusIn>", lambda x: PasserEnTrue())
fen.bind("<FocusOut>", lambda x: PasserEnFalse())
fen.protocol("WM_DELETE_WINDOW", fermeture)

BarreMenu = Menu(fen)
BarreMenu.add_command(label="Menu", command= lambda: RetournerMenu(DepuisMenu = True))
BarreMenu.add_command(label="Help", command=Help)
BarreMenu.add_command(label="Backup", command=LecteurSauvegarde.LecteurSauvegarde)
BarreMenu.add_command(label="Settings", command=Paramètres.InterfaceParamètres)
fen.configure(menu=BarreMenu)

PoliceTitreBienvenue = tkFont.Font(family="Verdanna",size=16,weight="bold")
PoliceBoutton = tkFont.Font(family="Arial",size=12,weight="bold")
PoliceTitre = tkFont.Font(size=14,weight="bold")
PoliceSousTitre = tkFont.Font(size=12)

ImageLogo = PhotoImage(file="Médias/Logo.png")

AfficherMenu()
fen.mainloop()
