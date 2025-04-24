FROM node:20-alpine AS build
WORKDIR /tmp
COPY client/package.json client/package-lock.json ./
RUN npm install
COPY client/ ./
RUN npm run build

FROM python:3.12-alpine
WORKDIR /srv/erates
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
COPY --from=build /tmp/dist ./public/static
COPY public/templates public/templates
COPY app app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0"]