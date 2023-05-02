# AWSToDoList
This project is a to-do list application to be hosted on AWS on utilzing and EC2 instance for hosting, 
an API gateway to filter traffic between the application and the backend. AWS Lambda functions are utilized to access data within the database, which
is a DynamoDB. 


- The Main Application
  Login and Registration
  ![image](https://user-images.githubusercontent.com/97745329/235690336-38bafc00-914b-4f03-bbfb-6d80e4e81d76.png)
  ![image](https://user-images.githubusercontent.com/97745329/235690548-491bc173-3108-4ee2-b0af-ee60f8c742e4.png)

   - The login and registration screens are made using bootstrap 5 to make them more modern and responsive. Users have the ability to create accounts and login via
     the main application which on a button press, sends the data to an HTTP endpoint on the Gateway, which then passes it on to the Lambda Functions for
     processing. 
   - Failures and successful operations are displayed to the user with like so: (successful registration message)
      ![image](https://user-images.githubusercontent.com/97745329/235691424-43edaf1d-c9d7-46d6-9095-b52405629f1e.png)
      
   Home Page
   ![image](https://user-images.githubusercontent.com/97745329/235691780-e7110b16-ac8b-46f8-9d16-247a730e6bb0.png)
   - Users are a main homepage with a jumbotron banner containing their name, and a logout button
   - Each individual task is represented on their own div container with corresponding modals for their update and deleting functions:
      - ![image](https://user-images.githubusercontent.com/97745329/235692276-9c119e1b-9d81-4500-897a-585c0f54807c.png)
      - ![image](https://user-images.githubusercontent.com/97745329/235692411-323ee3cd-3187-4804-9027-190419305063.png)
   - Users can add new tasks by selecting the Create button which will open a modal for creating new tasks:
     - ![image](https://user-images.githubusercontent.com/97745329/235692653-37a973d3-7719-4835-a064-ba227edc072f.png)
     
- Database
  - The web application is built using a DynamoDb NoSQL database for its flexabiltiy and affordability. It consists of two tables: a User accoun table, where passwords
    and emails are stored. Passwords are hashed for tranist then encrypted using a Symmetric AWS KMS key for storage within the database. The tasks table links user 
    accounts with their data using a primary key (email) and a sort key (task name). The database is backed up using AWS backups for protection. 
       - ![image](https://user-images.githubusercontent.com/97745329/235693470-5443f9c0-d1c2-48fb-b18c-7166436b21df.png)
- Lambdas
  - The web app hosted on the EC2 communicates to the backend with Python Lambda functions as a middle layer, the is one for each action: Login, Registration, Create,
    Update, and Delete. Lambda functions were selected as they did not always need to be running like the main application, so a FaaS could save on money and reduce
    overall responsibiltiy of the application. 
- API Gateway
  - Similar to the Lambdas, there is an HTTP endpoint for each function. The gateway acts as a layer between the Lambdas and the application and can be updated later
    for better security and traffic monitoring. 
      - ![image](https://user-images.githubusercontent.com/97745329/235694734-939d3506-b280-4b3d-816b-9d27d29d7de6.png)


       
       



