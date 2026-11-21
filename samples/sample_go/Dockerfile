# Build the program in the Go image, then run it from a tiny image with nothing else in it
FROM golang:1.25 AS build
WORKDIR /src
COPY go.mod ./
RUN go mod download
COPY . .
RUN CGO_ENABLED=0 go build -o /server .

FROM gcr.io/distroless/static-debian12
COPY --from=build /server /server
EXPOSE 8000
CMD ["/server"]
