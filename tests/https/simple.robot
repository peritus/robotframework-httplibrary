*** Settings ***

Resource        variables.txt
Library         HttpLibrary.HTTP
Test Setup      Create HTTP Context  ${HOST}    https

*** Test Cases ***

Simple GET on self-signed Mockserver
    GET      /200

Full-URL GET with full url on self-signed mock server
    GET      https://${HOST}/200

Full-URL GET to https://encrypted.google.com/
    GET      https://encrypted.google.com/

Simple GET to https://encrypted.google.com/
    Create HTTP Context  encrypted.google.com   https
    GET      /
