# Presenting *Cypress* via *Salesforce* CRM
The following project shows the basic use of the *Cypress* framework, as an example of testing the correctness of the conversion of a Lead object in the *Salesforce* system. GIF shown below presents the script going from start to end.

![Untitled_ Sep 22, 2022 12_28 AM (1)](https://user-images.githubusercontent.com/80170154/191622027-1374e48f-97a5-417e-abd8-522be143fff6.gif)

## General description of the process
1. Log in to Salesforce account
2. Creating a new Lead type record
3. Opening the page with the details of the new Lead
4. Going through the default convert action
5. Opening list views (accounts, contacts and occasions, respectively) and checking if there are records created by conversion
6. Removing newly created account which results in the removal of the associated contact and opportunity

## Detailed description of the process
### 1. Log in to Salesforce account
The Salesforce Org created on the Trailhead website was used for the visualization. The method ```cy.request ()``` was used to log in with the request method of type **POST**. The most important fields of this request are *pw* that is password and *un* that is username. This allows the script to run correctly as soon as it enters the appropriate url address. Unfortunately, the classic logging in generates problems, such as the script being turned off right after logging in.
### 2. Creating a new Lead type record
This activity is performed in the background using a handwritten function. Its implementation requires the *JSforce* extension, which is an isomorphic JavaScript library using the Salesforce API. In this case, its ability to perform CRUD operations was used. As a result, the *id* of the new record is saved.
### 3. Opening the page with the details of the new Lead
The first visible effect of the script is opening the detail page of the newly created Lead using the previously saved *id*.
### 4. Going through the default convert action
Then the action button "Convert" is clicked and continued by clicking the button with the same label in the new window. Next, the *id* of the newly created account is written down and the window is closed. Between some script transitions, the ```cy.wait ()``` method was used to make sure that all components were completely loaded. Sometimes the script tries to click on a button that has not fully generated yet, causing an error.
### 5. Opening list views (accounts, contacts and occasions, respectively) and checking if there are records created by conversion
In order to check whether new records were actually created as a result of conversion, the script opens another tabs with lists of records. In each of them, it gets to the first link in the first line (record) and checks if these links consist of the appropriate names used when creating a Lead.
### 6. Removing newly created account which results in the removal of the associated contact and opportunity
At the end of the script, the new account record is deleted using a function analogous to creating records. The previously saved *id* of this account is used for this. The system's reaction to account deletion is to remove all derivative records, i.e. contacts and business opportunities. This way, the script leaves no test records behind.

## Important files
- cypress/e2e/CreatingAccountFromLead.cy.js - main file with the above test
- cypress.config.js - *Cypress* configuration file (this is where the logic of these functions is implemented)
- cypress/support/commands.js - function definitions from the ```.config``` file so that they can be used in the main script
- cypress/domain/lead.js - defining the ```Lead``` class corresponding to the object with the same name in *Salesforce*
