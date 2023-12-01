import sys
from multiprocessing import cpu_count

from brute_force import brute_force_enigma
from chiffrer import chiffrer
from dechiffrer import dechiffrer

if __name__ == '__main__':
    # Config pour le 11 novembre
    rotors = "I V IV"
    reflecteur = "B"
    ring = "13 15 11"
    plugboard = "NX EC RV GP SU DK IT FY BL AZ"

    message = "Les troupes britanniques sont entrees a Cuxhaven a quatorze heures le six mai Desormais tout le trafic radio cessera je vous souhaite le meilleur Fermeture pour toujours tout le meilleur au revoir."

    message_chiffrer = chiffrer(rotors, reflecteur, ring, plugboard, message)
    print("Message chiffré: ", message_chiffrer)

    # LESXTROUPESXBRITANNIQUESXSONTXENTREESXAXCUXHAVENXAXQUATORZEXHEURESXLEXSIXXMAIXDESORMAISXTOUTXLEXTRAFICXRADIOXCESSERAXJEXVOUSXSOUHAITEXLEXMEILLEURXFERMETUREXPOURXTOUJOURSXTOUTXLEXMEILLEURXAUXREVOIRX
    message_dechiffrer = dechiffrer(rotors, reflecteur, ring, plugboard, message_chiffrer)
    print("Message déchiffré: ", message_dechiffrer)

    print("\n\n\n")
    print("Brut force")
    print("\n\n\n")

    # # # # # # # # # # # # # # # # # # # #
    #            BRUT FORCE               #
    # # # # # # # # # # # # # # # # # # # #

    # Les Allemands commencaient toujours le premier message de la journée en annonçant le Wetterbericht soit la météo. Dans ce message ça correspond au mot « meteorologie ».
    # La disposition des rotors est la suivante : 19 6 8
    # Les lettres sont branchées de la façon suivante : GH QW TZ RO IP AL SJ DK CN YM

    nb_cpu = cpu_count()
    print("Nombre de cpu: ", nb_cpu)

    message_brut_force_first_mail = "UFLTVDIPVYDQFLDZGEHBNLVVPNCMDTJBSBCISSQAJPWTIMJMRPTOMIKKYKGCJXBNKEQHSUAOMGUJOKLSNABOCSOMYGVLXCJCGVAAYSJFOSISJCAIYFHUJYYJDGGWNCZ"
    message_brut_force_second_mail = "GRWYGBHCZRZKAOQDWJYKQSLNKGINIKUAHAUFKUKGRNVKUWOFTVNCKHDAYWKJBJYVWFFWNVXMLDGXARISRQJQOJGLEAYWNUWVDYUACPBMSJGRSOHAYRLINRHIPCBHJAZO"

    # On protège le code qui lance l'attaque par brut force
    try:
        # On lance une attaque par brut force sur le premier message
        brute_force_enigma(message_brut_force_second_mail,
                           reflector="B",
                           ring="19 6 8",
                           plugboard="GH QW TZ RO IP AL SJ DK CN YM",
                           start_word="meteorologie",
                           mp=True)

    except KeyboardInterrupt:
        print("Interruption manuelle de l'attaque par brut force...")
        sys.exit(1)
