# API Layer for Microservice

This API layer exposes functionality of microservice. It includes models for data exchange, routers to connect service methods to the API, and optional authorization.

Besides, it includes:
- **Swagger interface** (default in FastAPI)

- **Jython client code generation** This is saved into the client/jython folder every time the microservice starts
- **Exception handling** for logging FastAPI `HttpException` to the console

# remarks
Using a service model for communication instead of a separate model can be acceptable depending on the context. However, consider these potential downsides:

- You may expose unnecessary fields to the client.
- Changes in service models can unintentionally alter the communication layer.
 