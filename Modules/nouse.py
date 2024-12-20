def FonctionServeur():
        #La fonction qui tourne en boucle tant que le serveur est démarré

            global HôteConnecté, ListeDesClientsConnectés, ListeDesPseudos, Nom, Rôle, CléPublique, ModuleDeChiffrement
            global ClientsMax, MDP, PrésenceMDP, Statut, ServeurVerrouilé
            
            while True:

                try: objetClient, CoordonnéesClient = ConnexionSocket.accept()

                except IOError:
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

                            Rôle[objetClient] = "Client"

                            if PrésenceMDP == False:

                                annonce = f"[{time.strftime('%H:%M:%S', time.localtime())}] {Nom[objetClient]} has joined the chat"
                                print(annonce)
                                Envoi("connected", "Annonce")
                                time.sleep(0.3)
                                Envoi(annonce, "Annonce")

                        ListeDesClientsConnectés.append(objetClient)

                for client in ListeDesClientsConnectés:

                    try:

                        if Statut[client] == "Connecté":

                            message = client.recv(32768) #L'argument dans la fonction recv définit combien de caractères on reçoit
                            message = message.decode("utf-8")

                    except BlockingIOError:
                
                        if ListeDesClientsConnectés[0] == client: time.sleep(0.1)

                    except ConnectionResetError:
                    #Si jamais un des clients s'est déconnecté
                        Déconnexion(client)
                    else:
                    #Le serveur a recu un mesage

                            if Statut[client] == "Connecté":

                                message = message.split("-")

                                if message[0] == "":
                                    Déconnexion(client)

                                else:
                        
                                    LongeurMessage = int(message[0])

                                    while len(message[1]) < LongeurMessage:
                                    #Tant que le message recu est plus petit que la longueur totale du message

                                        suite = client.recv(32768)
                                        suite = suite.decode("utf-8")

                                        message[1] += suite

                                    message = ChiffrementRSA.déchiffrement(message[1], CléPrivée, Module)
     
                                    MessageListe = message.split("|")
                                    Type = MessageListe[0]

                                    if Type == "Message":

                                            HeureMessage = MessageListe[1]
                                            Contenu = MessageListe[2]

                                            messageFormaté = f"[{HeureMessage}] {Nom[client]} → {Contenu}"
                                            print(messageFormaté)
                                            Envoi(messageFormaté, "Message", client)

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

                                        elif CommandeParsée == "unlock":

                                            if Rôle[client] == "Hôte" or Rôle[client] == "Admin":
                                                
                                                Annonce = f"[{HeureCommande}] {Nom[client]} has unlocked the server"
                                                Envoi(Annonce, "Annonce")
                                                ServeurVerrouilé = False

                                        elif CommandeParsée == "ban":

                                            if Rôle[client] == "Hôte" or Rôle[client] == "Admin":
                                            
                                                NomDuBanni = DeuxièmeArgument

                                                Résultat = TrouverClient(NomDuBanni, Nom)

                                                if Résultat == None: 

                                                    Annonce = f'[{time.strftime("%H:%M:%S", time.localtime())}] Unable to find "{NomDuBanni}"'
                                                    print(Annonce)

                                                    messageEnvoi = ChiffrementRSA.chiffrement(Annonce, CléPublique[client], ModuleDeChiffrement[client])
                                                    ChaineMessage = f"{len(messageEnvoi)}-{messageEnvoi}"
                                                    messageEnvoi = ChaineMessage.encode('utf-8')
                                                    client.send(bytes(messageEnvoi))
                                                    #On envoi le message d'échec à l'exécuteur de la commande
