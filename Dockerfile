FROM nikolaik/python-nodejs:python3.11-nodejs20
LABEL authors="bastianlobe"

# Install Nginx web server
RUN apt-get update && \
    apt-get install -y nginx gettext && \
    rm -rf /var/lib/apt/lists/*

# Create a directory for the Django project
RUN mkdir HelloMeals

# Copy the entire current directory to the /HelloMeals directory in the container
COPY . /HelloMeals/

# Set the working directory to /HelloMeals
WORKDIR /HelloMeals
# Upgrade pip
RUN pip install --upgrade pip
# Install Python packages listed in requirements.txt
RUN pip install -r requirements.txt

# Create a directory for static files
RUN mkdir /static

RUN npm --prefix /HelloMeals/src/frontend install

# Copy the Nginx configuration file to the container's /etc/nginx/sites-available directory
COPY nginx.conf /etc/nginx/sites-available/default

# Expose port 6753 for the container
EXPOSE 6753

# Run the boot.sh script when the container starts
ENTRYPOINT ["scripts/boot.sh"]
