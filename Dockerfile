FROM nikolaik/python-nodejs:python3.11-nodejs20
LABEL authors="bastianlobe"

# Install Nginx web server
RUN apt-get update && \
    apt-get install -y nginx gettext && \
    rm -rf /var/lib/apt/lists/*

# Create a directory for the Django project
RUN mkdir HelloMeals
COPY requirements.txt /HelloMeals/

WORKDIR /HelloMeals

### Install dependencies ###
# Python
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
# npm
COPY src/frontend/package.json /HelloMeals/src/frontend/
COPY src/frontend/package-lock.json /HelloMeals/src/frontend/
RUN npm --prefix /HelloMeals/src/frontend install

### Copy project files ###
COPY nginx.conf /etc/nginx/sites-available/default
COPY scripts scripts
COPY src src

# Create a directory for static files
RUN mkdir /static

RUN npm --prefix /HelloMeals/src/frontend run build
#Move files to nginx directory, so nginx can access them
RUN mv /HelloMeals/src/frontend/dist/* /usr/share/nginx/html/

# Expose port 6753 for the container
EXPOSE 6753

# Run the boot.sh script when the container starts
ENTRYPOINT ["scripts/boot.sh"]
