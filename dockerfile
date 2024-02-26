# Use the official Kong image as a base
FROM kong:latest

# Install dependencies for building Perl
USER root
RUN apt-get update && apt-get install -y \
    build-essential \
    wget \
    libreadline-dev

# Define Perl version
ARG PERL_VERSION=5.34.0

# Download, compile, and install Perl
WORKDIR /usr/src/perl
RUN wget https://www.cpan.org/src/5.0/perl-${PERL_VERSION}.tar.gz \
    && tar -xzf perl-${PERL_VERSION}.tar.gz --strip-components=1 \
    && ./Configure -des -Dprefix=/usr/local \
    && make \
    && make test \
    && make install

# Clean up
RUN apt-get remove --purge -y build-essential wget \
    && apt-get autoremove -y \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* /usr/src/perl*

# Switch back to the kong user
USER kong

# Continue with your Kong setup...
