def Démarrer(IP, Port, NombreClientsMax, MotDePasse):

    def Déconnexion(Client, Silencieux = False):
        if Rôle[Client] == "Hôte": HôteVientDePartir = True
        else: HôteVientDePartir = False

        if Rôle[Client] == "Client" and Silencieux == False:
            annonce = f"[{time.strftime('%H:%M:%S', time.localtime())}] {Nom[Client]} has disconnected"
            print(annonce)

        elif Silencieux == False:
            annonce = f"[{time.strftime('%H:%M:%S', time.localtime())}] {Nom[Client]} has stopped the server."

        ListeDesClientsConnectés.remove(Client)
        ListeDesPseudos.remove(Nom[Client])
        del Nom[Client]
        del CléPublique[Client]
        del ModuleDeChiffrement[Client]
        del Rôle[Client]
        del Statut[Client]
        del AdresseIp[Client]
        #On supprime les informations du client déconnecté
        #On utilise le mot clé del plutot que d'affecter une valeur vide car sinon la clé resterait conservée en mémoire

        if Silencieux == False: 
            Envoi("disconnected", "Annonce")
            time.sleep(0.3)
            Envoi(annonce, "Annonce")
        #On envoi l'annonce aprés avoir supprimé les infos du client car sinon il serait sur la liste d'envoi

        if HôteVientDePartir: ArrêtServeur()

    def EasterEgg():

        Fact = Kripiti.ChuckNorrisFacts()
        Fact = f"[{time.strftime('%H:%M:%S', time.localtime())}] {Fact}"
        print(Fact)
        Envoi(Fact, "Annonce")


    def Envoi(message, type, Envoyeur = None):
        #On rend l'argument Envoyeur facultatif pour que les annonces soit envoyées à tout le monde

        """ Cette fonction sert à envoyer des messages au clients connectés"""

        global ListeDesClientsConnectés
        #On récupere la liste de toute les clients connectés

        for destinataire in ListeDesClientsConnectés:
        #On désigne les destinaires du message, à savoir tout les clients connectés

            if destinataire != Envoyeur:
            #Si le destinaire n'est pas l'expéditeur

                messageEnvoi = ChiffrementRSA.chiffrement(message, CléPublique[destinataire], ModuleDeChiffrement[destinataire])
                #On transforme les caractéres du message en chiffre selon leur ID Unicode, puis ensuite on chiffre le message
                #Avec la clé publiq ue et le module de chaque client

                ChaineMessage = f"{len(messageEnvoi)}-{messageEnvoi}"
                messageEnvoi = ChaineMessage.encode('utf-8')
                destinataire.send(bytes(messageEnvoi))
                #On encode le tout en UTF8 et on l'envoi au client

    #Début du code de la fonction démarrer serveur
    global Module, CléPubliqueServeur, CléPrivée, ClientsMax, ListeDesClientsConnectés, ListeDesPseudos, HôteConnecté, Nom, Rôle
    global CléPublique, ModuleDeChiffrement, MDP, PrésenceMDP, Statut, ConnexionSocket, ServeurVerrouilé

    fen = Tk()
    fen.withdraw()
    #On crée une fenêtre qu'on affiche pas pour éviter qu'une fenêtre se génère lors de message d'erreurs

    Module, CléPubliqueServeur, CléPrivée = ChiffrementRSA.génération(16)
    #On génère notre jeu de clés Privée et Publique, ainsi que notre module de chiffrement

    if NombreClientsMax == "0" or NombreClientsMax == "Inconnu":
        ClientsMax = inf
        #On utilise l'infini car si on cherche à vérifier si la limite à été dépassée, le résultat sera toujours 
        
    else: ClientsMax = int(NombreClientsMax)
    # On passe par une variable intérmédiaire car on ne peut modifier la portée d'un paramètre

    HôteConnecté = False
    ServeurVerrouilé = False

    if MotDePasse != "Inconnu":  
        PrésenceMDP = True     
        MDP = MotDePasse

    else:
        PrésenceMDP = False
        MDP = None


    ListeDesClientsConnectés = []
    ListeDesPseudos = []
    ListeDesIpBannies = []

    Nom = {} #Le nom d'utilisateur
    Rôle= {} #Hôte ou admin
    CléPublique = {} #Sa clé de chiffrement RSA
    ModuleDeChiffrement = {} #Son module de chiffrement
    Statut = {} #Si l'utilisateur est connecté (Si il a rentré le mot de passe)
    AdresseIp = {}


    ConnexionSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #On défini les paramêtres du socket

    try: ConnexionSocket.bind((IP, Port))
    except OSError:
    #Si jamais le lancement du serveur échoue (IP Invalide), on affiche un message d'erreur
        tkinter.messagebox.showerror(title="Ouch...", message="It seems that your IP is not valid. Please refer to the help to resolve this issue.")

    else:
        ConnexionSocket.setblocking(0)

        #Démarrage du serveur
        ConnexionSocket.listen()
        print("Server started at " + time.strftime("%H:%M:%S") + " on port " + str(Port))        

        def FonctionServeur():

            global HôteConnecté, ListeDesClientsConnectés, ListeDesPseudos, Nom, Rôle, CléPublique, ModuleDeChiffrement
            global ClientsMax, MDP, PrésenceMDP, Statut, ServeurVerrouilé
            
            while True:

                try: objetClient, CoordonnéesClient = ConnexionSocket.accept()

                except IOError:
                #Si personne n'essaie de se connecter, on ne fait rien
                    pass
                
                else:
                #Connexion d'un client

                    DonnéesDuClient = objetClient.recv(32768)
                    DonnéesDuClient = DonnéesDuClient.decode("utf-8")
                    #On recoit et on convertir les données du client

                    DonnéesDuClient = DonnéesDuClient.split("\n")
                    #On transforme ces données en liste

                    AdresseIp[objetClient] = CoordonnéesClient[0]

                    if DonnéesDuClient[0] not in ListeDesPseudos and ClientsMax >= len(ListeDesClientsConnectés) + 1 and ServeurVerrouilé == False and AdresseIp[objetClient] not in ListeDesIpBannies:

                        objetClient.send(bytes(f"{str(CléPubliqueServeur)}|{str(Module)}|{str(PrésenceMDP)}|{str(len(ListeDesClientsConnectés) + 1)}", "utf-8"))
                        #On envoi au client les informations de chiffremment du serveur

                        Nom[objetClient] = DonnéesDuClient[0]
                        CléPublique[objetClient] = int(DonnéesDuClient[1])
                        ModuleDeChiffrement[objetClient] = int(DonnéesDuClient[2])

                        ListeDesPseudos.append(DonnéesDuClient[0])

                        if PrésenceMDP == False: Statut[objetClient] = "Connecté"

                        else: Statut[objetClient] = "Attente"

                        if HôteConnecté == False:
                        #Si c'est la première connexion, on précise que c'est l'hôte

                            HôteConnecté = True
                            Rôle[objetClient] = "Hôte"
                            Statut[objetClient] = "Connecté" #L'hôte est toujours connecté, pas besoin de mot de passe
                            print(
                                f"[{time.strftime('%H:%M:%S', time.localtime())}] Host {Nom[objetClient]} has just connected")
                            
                        else:
                        #Sinon c'est un client

                            Rôle[objetClient] = "Client"

                            if PrésenceMDP == False:

                                annonce = f"[{time.strftime('%H:%M:%S', time.localtime())}] {Nom[objetClient]} has joined the chat"
                                print(annonce)
                                Envoi("connected", "Annonce")
                                time.sleep(0.3)
                                Envoi(annonce, "Annonce")

                        ListeDesClientsConnectés.append(objetClient)

                    elif DonnéesDuClient[0] in ListeDesPseudos:
                    #Si le nom est déja pris

                        objetClient.send(bytes("False", "utf-8"))
                        time.sleep(0.3) #Le délai évite que les paquets se mélangent
                        objetClient.send(bytes("Your username is already in use on this server, please change it.", "utf-8"))
  
                    elif ClientsMax < len(ListeDesClientsConnectés) + 1:
                    #Si le serveur est complet

                        objetClient.send(bytes("False", "utf-8"))
                        time.sleep(0.3)
                        objetClient.send(bytes("The server has reached its maximum capacity", "utf-8"))

                    elif ServeurVerrouilé:

                        objetClient.send(bytes("False", "utf-8"))
                        time.sleep(0.3)
                        objetClient.send(bytes("The server is locked", "utf-8"))

                    elif AdresseIp[objetClient] in ListeDesIpBannies:

                        objetClient.send(bytes("False", "utf-8"))
                        time.sleep(0.3)
                        objetClient.send(bytes("You have been banned from this server", "utf-8"))


                for client in ListeDesClientsConnectés:
                #On récupere chaque client dans la liste des clients connectés

                    try:
                    #Si un message est envoyé, on le récupere, sinon l'instruction génére une exception

                        if Statut[client] == "Connecté":

                            message = client.recv(32768) #L'argument dans la fonction recv définit combien de caractères on reçoit
                            message = message.decode("utf-8")
                            #On recoit le message et on le décode

                    except BlockingIOError:
                
                        if ListeDesClientsConnectés[0] == client: time.sleep(0.1)

                    except ConnectionResetError:
                    #Si jamais un des clients s'est déconnecté
                        Déconnexion(client)
                    else:
                    #Le serveur a recu un mesage

                            if Statut[client] == "Connecté":

                                message = message.split("-")
                                #Le message comporte un petit entête
                                #Exemple = 564-6646464/65656/4564564654, 564 est içi la longueur totale du message. Cela peut arriver que les très long messages (Fichiers) fassent plus
                                #de 2048 la taille taille du buffer

                                if message[0] == "":
                                #Si le message recu  est vide la connexion a été  perdue
                                    Déconnexion(client)

                                else:
                                #Si le message n'est pas vide
                        
                                    LongeurMessage = int(message[0])

                                    while len(message[1]) < LongeurMessage:
                                    #Tant que le message recu est plus petit que la longueur totale du message

                                        suite = client.recv(32768)
                                        suite = suite.decode("utf-8")

                                        message[1] += suite

                                    message = ChiffrementRSA.déchiffrement(message[1], CléPrivée, Module)
     
                                    MessageListe = message.split("|")
                                    Type = MessageListe[0]
                                    #On récupere le message sous forme de liste afin de déterminer son type

                                    if Type == "Message":

                                            HeureMessage = MessageListe[1]
                                            Contenu = MessageListe[2]

                                            messageFormaté = f"[{HeureMessage}] {Nom[client]} → {Contenu}"
                                            print(messageFormaté)
                                            Envoi(messageFormaté, "Message", client)
                                    
                                    elif Type == "FileTransfer":

                                        file_name = MessageListe[2]
                                        file_size = int(MessageListe[3])
                                        
                                        # Notify the server about the incoming file
                                        Annonce = f"[{HeureCommande}] {Nom[client]} is sending file '{file_name}' ({file_size} bytes)"
                                        print(Annonce)
                                        Envoi(Annonce, "Annonce")
                                        
                                        # Receive file content
                                        received_size = 0
                                        file_content = b""
                                        while received_size < file_size:
                                            chunk = client.recv(4096)  # Adjust chunk size if needed
                                            file_content += chunk
                                            received_size += len(chunk)
                                        
                                        # Save the file
                                        with open(f"Received_{file_name}", "wb") as file:
                                            file.write(file_content)
                                        
                                        print(f"File '{file_name}' received and saved as 'Received_{file_name}'.")
                                        Envoi(f"File '{file_name}' received successfully.", "Message", client)


                                    elif Type == "Commande":

                                        HeureCommande = MessageListe[1]
                                        Commande = MessageListe[2]

                                        CommandeParsée, DeuxièmeArgument = Fonctions.ParserCommande(Commande)

                                        if CommandeParsée == "stop":

                                            if Rôle[client] == "Hôte":
                                                
                                                Envoi(f"[{HeureCommande}] {Nom[client]} has stopped the server", "Annonce")
                                                ArrêtServeur()

                                        elif CommandeParsée == "lock":

                                            if Rôle[client] == "Hôte" or Rôle[client] == "Admin":
                                                
                                                Annonce = f"[{HeureCommande}] {Nom[client]} has locked the server"
                                                Envoi(Annonce, "Annonce")
                                                ServeurVerrouilé = True
