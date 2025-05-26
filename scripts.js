// script to autowire access token for login to jwt environment variable 
pm.environment.set("JWT", pm.response.json().access_token); 