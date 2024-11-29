![TravelHunterLogo](./static/Logo.png)

## Technologies used

[![DJango](https://img.shields.io/badge/DJango-0C4B33?style=for-the-badge&logo=django&logoColor=0C4B33&labelColor=ffffff)](https://www.djangoproject.com/)
[![Postgres](https://img.shields.io/badge/PostgreSQL-31648C?style=for-the-badge&logo=postgresql&logoColor=31648C&labelColor=ffffff)](https://www.postgresql.org/)

## Web Design
[![Canva Design](https://img.shields.io/badge/Web_Design-31648C?style=for-the-badge&logo=canva&logoColor=31648C&labelColor=white)](https://www.canva.com/design/DAFloE_4i28/Vh63LpHFy3p1EVC_CLfFkA/view?utm_content=DAFloE_4i28&utm_campaign=designshare&utm_medium=link&utm_source=publishsharelink)

# Web Prototype App

Web project developed for managing travel agencies and their clients. It is a prototype app developed to manage a DB with the data of the users, products, active travels and benefits offered by the agency.

 The web app implements these main modules:

- __Login__: screen to log in to the app with admin credentials.
  
  ![login screen](./static/login.png "Login Screen")

- __Users Module__: manage user's data in the database.

	![user screen](./static/users.png "Users Screen")
  ![new user screen](./static/user_new.png "New User Screen")
  ![roles screen](./static/roles.png "Roles Screen")
---
- __Products Module__: manage products and all the associated data.

	![products screen](./static/products.png "Products Screen")
  ![new product screen](./static/product_new.png "New Product Screen")
  ![places screen](./static/places.png "Places Screen")
---
- __Travels Module__: manage the current active travels of the agency.
  
	![trips screen](./static/trips.png "Trips Screen")
  ![trip list screen](./static/trip_users.png "Trip List Screen")
---
- __Benefits Module__: manage the benefits the agency offers to its clients.

	![benefits screen](./static/benefits.png "Benefits Screen")
  ![new benefit screen](./static/benefit_new.png "New Benefit Screen")
  ![benefit log screen](./static/benefit_log.png "Benefit Log Screen")
---

All these modules manage their data through CRUD operations. 

There is also an API developed to send and update specific data through the mobile app developed alongside this project.

The mobile app is developed in Flutter and can be found in this [repository](https://github.com/ElyRiven/Prototipo-Movil-Proyecto)

## Database Schema
![DB schema](./static/DB_Diagram.png)
