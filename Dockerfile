# Utilise l'image officielle Python
FROM python:3.11

# Installer les locales nécessaires et netcat-openbsd
RUN apt-get update && apt-get install -y locales netcat-openbsd \
    && sed -i '/fr_FR.UTF-8/s/^# //g' /etc/locale.gen \
    && locale-gen

# Définir les variables d'environnement pour la locale
ENV LANG=fr_FR.UTF-8
ENV LANGUAGE=fr_FR:fr
ENV LC_ALL=fr_FR.UTF-8

# Définir le répertoire de travail
WORKDIR /app

# Copier le script wait-for-it.sh dans l'image et le rendre exécutable
COPY wait-for-it.sh /usr/local/bin/wait-for-it.sh
RUN chmod +x /usr/local/bin/wait-for-it.sh

# Copier les dépendances et les installer
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copier le reste du code
COPY . .

# Exposer le port utilisé par Django
EXPOSE 8000

# Commande de démarrage : attendre la DB puis lancer Django
#CMD ["/usr/local/bin/wait-for-it.sh", "db:5432", "--", "python", "manage.py", "runserver", "0.0.0.0:8000"]
ENTRYPOINT ["./entrypoint.sh"]
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]