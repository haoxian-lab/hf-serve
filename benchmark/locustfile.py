from locust import HttpUser, task
from random import choice

tweets = [
    "Nouvelle mise à jour disponible sur iOS ! 📱 #Apple",
    "Le nouvel album de Drake est incroyable 🎧 #Music",
    "Quel temps magnifique aujourd'hui ☀️ #Weather",
    "Je suis tellement excité(e) pour les vacances d'été ! 🌴 #Travel",
    "Le café est mon carburant le matin ☕️ #Coffee",
    "Joyeux anniversaire à mon meilleur ami(e) ! 🎂 #Birthday",
    "Le sport m'aide à me vider la tête 🏋️‍♀️ #Fitness",
    "Je ne peux pas attendre pour voir ce film 🎬 #Movies",
    "La vie est belle, profitez de chaque instant ❤️ #Life",
    "J'adore apprendre de nouvelles choses chaque jour 📚 #Knowledge",
    "Rien ne vaut une bonne soirée avec des amis 👯‍♂️ #Friendship",
    "Je me sens reconnaissant(e) pour tout ce que j'ai 🙏 #Gratitude",
    "La pizza est toujours une bonne idée 🍕 #Food",
    "J'adore découvrir de nouveaux endroits 🗺️ #Adventure",
    "Il n'y a rien de mieux que de se détendre à la maison 🛋️ #Relaxation",
    "La musique est le langage universel 🎶 #Art",
    "J'ai tellement hâte pour le prochain concert ! 🎤 #Concert",
    "La famille est la chose la plus importante 💖 #Family",
    "L'amour est une aventure merveilleuse 💘 #Love",
    "La créativité est la clé du succès 🎨 #Creativity",
]


class HelloWorldUser(HttpUser):
    @task
    def hello_world(self):
        self.client.post(
            "",
            json={"text_data": choice(tweets)},
        )
