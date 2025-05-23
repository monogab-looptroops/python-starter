# Test

## Method

Follow the test pyramid: <br>
\* e2e <br>
\*\* module <br>
\*\*\* unit <br>

1. Unit tests: These are fast and you don't have to start any database, queue, device. Those tools might have a fake version.
2. Adapters: Adapters can/need test if they are written by us. Starting the adapters should be easy (for example docker-compose.yml defined) or should have a good description. Test not needed when we trust the adapters/library methods for example: generating an api-client
3. e2e: This is the slowest. If the microservice has api, generated client methods can be called here.

