FROM node:alpine as base

RUN mkdir /app
WORKDIR /app
RUN npm cache clean -f && npm install -g n npm && npm update n npm && apk --no-cache add g++ make python3 && npm install --quiet node-gyp -g

FROM base as build_archimond7450
COPY ./archimond7450.com/frontend/package.json ./
COPY ./archimond7450.com/frontend/package-lock.json ./
RUN npm ci
COPY ./archimond7450.com/frontend/ ./
RUN npm run build

FROM base as build_archiemate
COPY ./archiemate.com/frontend/package.json ./
COPY ./archiemate.com/frontend/package-lock.json ./
RUN npm ci
COPY ./archiemate.com/frontend/ ./
RUN npm run prod

FROM nginx:stable-alpine
COPY --from=build_archimond7450 /app/build /usr/share/nginx/html/archimond7450.com/frontend
COPY --from=build_archiemate /app/build /usr/share/nginx/html/archiemate.com/frontend
CMD ["nginx", "-g", "daemon off;"]

