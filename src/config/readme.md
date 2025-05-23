# Config

## Usage
There are two ways to use the configs:
1. Use environment variables and environment files
  In this case you have one or several environment files where you simple list all the variables.

  Example:
  ```
  example__app_version = "v0.0.1"
  ```
  The 'example__' is a prefix you have to use for all the variables and it distingues from any other environment variable. 
  You can modify in the config/SettingsConfigDict.env_prefix
  The 'app' is a pydantic/BaseModel , 'version' is the Field, see in config/AppConfig for this example. 

  The environment variable insert into the dockers overwrite these settings. 

2. Use toml files. 
   This Tom's obvious minimal language, which allows to better structure.
   Example:
   ```
   [app]
   version = "v0.0.1"
   ```  
   It can be overwritten in the same way inserting docker environment variables.

In theory you can use both, but it is a good practice to stick to one way. 

## Priority

Lowest to Highest:
  - default values for the BaseModel classes in config.py
  - overwritten by the toml files
  - overwritten by the .env files
  - overwritten by the environment variables 
  - overwritten by explicit assignment in the code (this can be used for testing) 






