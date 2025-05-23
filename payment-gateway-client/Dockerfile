FROM php:8.2-apache

WORKDIR /var/www/html

# Install dependencies
RUN apt-get update && apt-get install -y \
    git \
    curl \
    libpng-dev \
    libonig-dev \
    libxml2-dev \
    zip \
    unzip \
    libzip-dev \
    nodejs \
    npm

# Clear cache
RUN apt-get clean && rm -rf /var/lib/apt/lists/*

# Install PHP extensions
RUN docker-php-ext-install pdo_mysql mbstring exif pcntl bcmath gd zip

# Install composer
COPY --from=composer:latest /usr/bin/composer /usr/bin/composer

# Copy existing application directory contents
COPY . .

# Copy .env file (make sure it's in the build context!)
COPY .env.example .env
# Install application dependencies
RUN composer install

# Run migrations (only if the database is set up)
RUN if [ -f .env ] && grep -q 'DB_CONNECTION=' .env; then \
    php artisan migrate --force; \
fi
# Build assets (only if there are frontend assets to build)
RUN if [ -f webpack.mix.js ] || [ -f vite.config.js ] || [ -f tailwind.config.js ]; then \
    npm install && npm run build; \
fi
# Set permissions
RUN chown -R www-data:www-data /var/www/html/storage
RUN chown -R www-data:www-data /var/www/html/database
RUN chmod -R 775 /var/www/html/storage
RUN chmod -R 775 /var/www/html/database

# Enable Apache modules
RUN a2enmod rewrite

# Copy virtual host config
COPY docker/apache.conf /etc/apache2/sites-available/000-default.conf

EXPOSE 80