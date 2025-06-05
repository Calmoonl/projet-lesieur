# Utilise l'image officielle Python
FROM python:3.11

# Installer les locales n�cessaires
RUN apt-get update && apt-get install -y locales \
    && sed -i '/fr_FR.UTF-8/s/^# //g' /etc/locale.gen \
    && locale-gen

# D�finir les variables d'environnement pour la locale
ENV LANG=fr_FR.UTF-8
ENV LANGUAGE=fr_FR:fr
ENV LC_ALL=fr_FR.UTF-8

# D�finir le r�pertoire de travail
WORKDIR /app

# Copier les d�pendances et les installer
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copier le reste du code
COPY . .

# Exposer le port utilis� par Django
EXPOSE 8000

# Commande de d�marrage
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
