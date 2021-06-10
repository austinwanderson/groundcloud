# GroundCloud Take Home Assignment

## Deliverable 
- Simple Django app that shows utilization of a Django Rest Framework
- Ability to utilize core/built-in functionality of Django and (third party library) Django Rest Framework
- 1-2 Django ORM Models - names / attributes of applicants chosing, at least one model should relate to another
- database doesn’t matter, default django db (SQLite) is ok
- DjangoRestFramework views for the django models (standard/stock api actions are enough)
- No need to create a webpage screen - no front end - just code review
Review process:
- Set up Github repo and invite dev team members
- Team is looking for the ability for you to create and implement functional code that  leverages built in functionality of Django and DRF
- interactive code review process after merging your submission to simulate interaction model with the team

## Outcome

- Simple Django app built upon Django Rest Framework.
- PostGres and PostGIS used as a database.
- 3 ORM Models: Company, Driver, Truck
- Each 'Driver' has a FK attribute 'company_id'
- Each 'Truck' has a FK attribute 'driver_id'
- Ability to create, update, and delete an ORM model based on PK
- Ability to list all of a specified ORM model.
- Created view to use PostGIS to return the truck closest to a given lat,lng coordinate.

### Tests
-Tested using HTTPie (pip install httpie)

~~~
//Create a company
http --json POST http://127.0.0.1:8000/company/create name="Amazon"

//Create a driver
http --json POST http://127.0.0.1:8000/driver/create name="Jeff Bezos" company_id=1

//Create a truck
http --json POST http://127.0.0.1:8000/truck/create current_driver=1 current_location="POINT(36.16645743895505 -115.23731350660487)"

//Update a company
http PUT http://127.0.0.1:8000/company/1/ name="FedEx"

//Update a driver
http://127.0.0.1:8000/driver/1/ name="Not Jeff Bezos" company_id=1

//Update a truck
http PUT http://127.0.0.1:8000/truck/3/ current_driver=1 current_location="POINT(36.16682744 -115.2354351351)"

//Delete a company
http DELETE http://127.0.0.1:8000/company/1/

//Delete a driver
http DELETE http://127.0.0.1:8000/driver/1/

//Delete a truck
http DELETE http://127.0.0.1:8000/truck/1/

//List trucks, drivers, companies
http GET http://127.0.0.1:8000/trucks/
http GET http://127.0.0.1:8000/drivers/
http GET http://127.0.0.1:8000/companies/

//Get truck closest to lat,lng coordinate
http GET http://127.0.0.1:8000/truck/closest lat==36.1742452 lng==-115.25345267356

//output
{
    "current_driver": null,
    "current_location": {
        "coordinates": [
            36.16645744,
            -115.23723431
        ],
        "type": "Point"
    },
    "distance": 1840.83171382,
    "id": 3
}

~~~