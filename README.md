## Installation des dependances
----------------------------
Veuillez suivre ces étapes, pour installer l'application :

1. Clonez le repository sur la machine en local.
    ``` Liens repo
    https://github.com/marytraore02/Chat-with-multiple-pdf-llm-rag.git
    ```
2. Creer un environnement virtuel avec la version de python 3.9
    ``` 
        python3.9 -m venv venv
    ```

2. Activer l'environnemnet python 3.9
    ``` 
        source venv/bin/activate
    ```

2. Installez tout les dépendances requises en exécutant la commande suivante :

   ```
    pip install -r requirements.txt
   ```

3. Obtenez une clé API auprès d'OpenAI et ajoutez-la au fichier `.env` dans le répertoire du projet.
    accessible sur https://platform.openai.com/api-keys

```commandline
    OPENAI_API_KEY=your_secrit_api_key
```


## Usage
Pour utiliser l'application, procédez comme suit :

1. Assurez-vous d'avoir installé les dépendances requises et ajouté la clé API OpenAI au fichier « .env ».

2. Exécutez le fichier « app.py » à l'aide de la CLI Streamlit. Exécutez la commande suivante :
   ```
   streamlit run app.py
   ```

3. L'application se lancera dans votre navigateur Web par défaut, affichant l'interface utilisateur.

4. Chargez plusieurs documents PDF dans l'application en suivant les instructions fournies.
