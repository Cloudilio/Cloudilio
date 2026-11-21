# Your own Dockerfile

*This page is also on the website: [https://cloudilio.com/docs/dockerfile](https://cloudilio.com/docs/dockerfile)*

## Publish a Go, Ruby, PHP, Java or Rust app with your own Dockerfile

For any language Cloudilio doesn't set up for you, add a Dockerfile to your project. Cloudilio builds it on each publish and runs the image with the same previews, rollbacks, secrets, saved data and domains as every other app. Add a [PostgreSQL or MySQL database](databases.md) or [Redis](redis.md) on the Data page and your app reads `DATABASE_URL` or `REDIS_URL` from its environment, whatever language it's in.

## How Cloudilio picks your Dockerfile

- A project with a `Dockerfile` at its top level that isn't a Python or Node.js project builds with the Dockerfile straight away.
- A Python or Node.js project that also has a Dockerfile is set up by Cloudilio. To build with the Dockerfile instead, open your app's **Advanced settings** and choose **Your Dockerfile** under **Type of app**. Choose **Let Cloudilio set it up instead** to switch back.

## What your image needs

- **Listen on port 8000.** Cloudilio passes it in `PORT`. Your Dockerfile's `CMD` or `ENTRYPOINT` starts the app. An image that listens on its own port, such as 3000 or 8080, still works: when it doesn't answer on 8000, Cloudilio tries the port in its `EXPOSE` line or its output, and sends visitors there.
- **Run as user 1000.** Every app runs as user 1000, whatever `USER` says, so that user must be able to read the app's files. Files you copy in are readable unless you lock them down.
- **Write only to `/app/data` and `/tmp`.** The image is read-only while it runs. `/app/data` is kept across publishes and backed up every day; `/tmp` is cleared on restart.
- **Stay under 5 GB.** The build has 15 minutes and 2 GB of memory, like every build.

## Examples

Go

```
FROM golang:1.25 AS build
WORKDIR /src
COPY go.mod go.sum* ./
RUN go mod download
COPY . .
RUN CGO_ENABLED=0 go build -o /server .

FROM gcr.io/distroless/static-debian12
COPY --from=build /server /server
CMD ["/server"]
```

Ruby (Sinatra or Rails with Puma)

```
FROM ruby:3.4-slim
WORKDIR /app
COPY Gemfile Gemfile.lock ./
RUN bundle install
COPY . .
CMD ["sh", "-c", "bundle exec puma -b tcp://0.0.0.0:$PORT"]
```

PHP

```
FROM php:8.4-cli
WORKDIR /app
COPY . .
CMD ["sh", "-c", "php -S 0.0.0.0:$PORT -t public"]
```

Java (Spring Boot)

```
FROM eclipse-temurin:21-jdk AS build
WORKDIR /src
COPY . .
RUN ./mvnw -q package -DskipTests

FROM eclipse-temurin:21-jre
COPY --from=build /src/target/*.jar /app/app.jar
CMD ["sh", "-c", "java -jar /app/app.jar --server.port=$PORT"]
```

Rust

```
FROM rust:1.90 AS build
WORKDIR /src
COPY . .
RUN cargo build --release

FROM debian:bookworm-slim
COPY --from=build /src/target/release/my-app /usr/local/bin/my-app
CMD ["my-app"]
```

To see one working first, choose the **Go app (Dockerfile)** template on the New app page.

## What a Dockerfile can't do here

- **Use `VOLUME`.** Save files in `/app/data` instead. A volume a base image declares becomes a small folder that's cleared on restart.
- **Use BuildKit features**, such as `RUN --mount` or heredocs (`RUN <<EOF`). Join commands with `&&` instead.
- **Build from an image named with a variable**, an image ID, a registry on the server or a registry on a private address. Write the image's name out, such as `golang:1.25` or `ghcr.io/you/image:1`.
- **Download with `ADD`.** Docker fetches an `ADD` URL outside the build's network limits, so it isn't allowed. Download with `RUN curl -fsSL -o /app/file https://example.com/file` instead. `ADD` still copies and unpacks files from your project.
- **Use `ONBUILD`**, or a base image that has `ONBUILD` steps. Write the steps where they're needed instead.
- **Change the escape character** with an `escape=` line. Continue long lines with a backslash.
- **Get your secrets while building.** Build arguments end up in the image's history, so your app reads secrets from its environment when it runs.
- **Gain privileges.** Apps run with no Linux capabilities, so programs that need them, such as anything that binds to a port below 1024, won't start.

Commands under **Run before each publish**, background workers and scheduled tasks run in your image too. If it has an `ENTRYPOINT`, they're passed to it, as with `docker run`.

## Fix common problems

"Permission denied" when the app starts

The app runs as user 1000, which can't read files only root can read. Make them readable, for example with `RUN chmod -R a+rX /app`.

"Read-only file system"

The app wrote next to its code, or to a folder such as `/var/run`. Point it at `/app/data` or `/tmp`.

The app starts but never answers

Cloudilio already tries the port in `EXPOSE` and in the app's output, so check that the app listens on all addresses (`0.0.0.0`), not `localhost`, and on a port above 1023. Listening on `$PORT`, which is 8000, avoids both problems.

"The Dockerfile can't be built"

The message names the line and what to change. The rules are in **What a Dockerfile can't do here**.
