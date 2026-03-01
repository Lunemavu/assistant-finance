import anthropic

from dotenv import load_dotenv
load_dotenv()
client = anthropic.Anthropic(api_key=os.getenv("API_KEY"))

# Lire le fichier
fichier = open("regles.txt", "r")
contenu = fichier.read()
fichier.close()

print("Fichier chargé ! Tu peux poser des questions sur les règles.")
print("")

historique = []

system = "Tu es un expert en finance et en règles métier. On va t'envoyer des règles et tu vas les analyser, les expliquer et répondre aux questions. Réponds toujours en français de façon claire et simple."

while True:
    question = input("Toi : ")
    
    if question == "quitter":
        print("Au revoir !")
        break
    
    message_complet = "Voici les règles du fichier :\n\n" + contenu + "\n\nQuestion : " + question
    
    historique.append({"role": "user", "content": message_complet})
    
    message = client.messages.create(
        model="claude-opus-4-6",
        max_tokens=1024,
        system=system,
        messages=historique
    )
    
    reponse = message.content[0].text
    historique.append({"role": "assistant", "content": reponse})
    
    print("Claude : " + reponse)
    print("")
