FROM node:14

WORKDIR /app
# The .yarnrc file places our node_modules in /node_modules.
COPY package.json .yarnrc ./
COPY docker_entrypoint.sh /entrypoint.sh
RUN yarn && chmod +x /entrypoint.sh
ENV PATH /node_modules/.bin/:$PATH
ENTRYPOINT ["/entrypoint.sh"]
