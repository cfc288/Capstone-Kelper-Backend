# Capstone-Kelper-Backend
Back end for capstone project for Kelper (in flask-python)

# Capstone-Kelper-Frontend
Front end for capstone project for Kelper (in React)


Front End Deployment Link:
https://kelper-frontend-capstone.herokuapp.com/

Back End Deployment Link:
https://kelper-backend-capstone.herokuapp.com/

orriginal git hub repository for front end and back end:
https://github.com/cfc288/Capstone-Project


Kelper is a website designed to help connect companies while assisting in their customer analytics by giving companies a way to track and hold the select public accountable, all the while continuing to grow their businesses and to apply and follow the Pareto Principle (80/20 rule)


Technologies used:
Front End-
React, JSX, Heroku, ReactModal, React useState,

Back End-
Flask, Python, SQL






To run site locally:
Front End:
in terminal 'npm i' to install all associated packages

Back End:
in terminal 'pip3 install -r requirements.txt' to install all associated packaged 



orrignal wireframe images:
https://github.com/cfc288/Capstone-Kelper-Frontend/tree/main/src/pics/attatched%20pictures







Current Content
[x] - More in the about section:
Login/Register functions:
[x] - make login for *admin vs user vs client
[x] - client registration vs employee registration
[x] - sign in message (when pw/email do not match)
Main Index Page:
(page where all incidents are posted)
[x] - have comments be able to be sorted by location, company, client name (alphabetically ascending and descending)
[x] - sort options
name
location
company
Single Client Page(displays all incidents under one client):
[x]-Employee user can add/delete/update any incident report here
Client Page:
(client is the one being reported, the incident report is the report about the client made by the user)
[x] - client page lists all incidents reported by any user
[x] - each incident:
[x] - lists users title/company/location
[x] - has a way to flag incidents for removal (on display one client page)
[x] - flag/report posts for review/deletion
Each incident report:
[x] - has a way for users to flag
Client redemption option:
[x] - clients that have been reported to the website can
message to companies about incidents
[x] - Clients register as a client
[x(on main veiw] - incidents get grouped by business
[x] - usernames are hidden from client
[] - incident reports change to a lighter/greyed out color with a notification on top that incident is under review (for 90 days) but incident report is still legible (this is changed across website, to users and in main index page)
Messages:
[x]-Users can type in user name and send message to another user
[x]-all messages per user are displayed on main page, user (client or employee) can delete a message





******New Stretch Goals
*Admin: [this might need to be its own model as well, i need to look into this further]
[x] - can flag or unflag a review
[x] - ability to change and delete reviews, (client pages?)
[x] - admin has a way to approve/verify/double check
[x] - can change verification


Main page:
*[] - have stars average and then display on index route
*[] - on index page make it just 30 comments per page with the ability to move to 'next page' ( or have more continue to load? ie like fb? react?)
[] - search options
name
location
company
Login/register function
*[] - email verification set up (api?)
*[] - business verification for user
*[] - verify with a work email?
*[] - way to recover password
*[] - extra security? admin needs to verify change?
*[] - google API attached for location pinning to user model(company)
Profiles:
User Page:
(users are the employees/managers making the incident reports about a client)
*[] - users can navigate to their own home/profile page where they can edit their
[] - employee status / business
[] - name
[] - business
[] - edit reviews only they made
[] - can delete individual comments without deleting all of the client
[] - track changes of edit
[] - Ability to message other users
*[] - Admin for verification?
*[] - google maps for location of user/company? (attached to login/register then attaches to review like company/employee information as well)
Clients: (non employee users)
*[] - Client puts in a request to get access to reviews
*[] - (admin or automatic?)
*[]- client gets access to those in a specific location or their name is returned
*[] - Clients first needs to claim reviews made about them to access messaging ability
*[] - Claimed reviews get marked as a green level verification
*[] - reviews get attached to their profile/page after they claim a review
*[] - be able to add stars or (certain item) of choice as review rating method (3/5 stars or 4/5 tomatoes/'karens'? ect)
*[] - option to appeal for each Incident made becomes available once Client/incidents are claimed
*[] - users from companies get emailed/notified and companies have the option to remove the review, write a follow up, delete,
Incidents:
*[] - 3 tier verification
*[] - red verification means only first name, and description of client has been given
*[] - yellow verification means there is a first and last name plus one of the following: legit phone number/email/address
*[] - green means client signed up for a profile for the right to appeal review and has claimed the incident
*[] - if green then will be able to go to one single page where all connected
*[] - if email is sent incident report(s) get flagged and put under investigation
[] - flagged report displays how long incident is under investigation for
*[] - message can be made to go to multiple users
[] - have stars average and then display on main index route
*[] - when flagged a box pops up with the ability to say why and gets sent to admin inbox
*[] - verification status
	[] - blue check mark/something to say client is verified
Admin abilities
*[] - can ban users
*[] - admin gets notified of each flagged incident
*[] - admin is able to track flagged posts
*[] - how many times a review has been flagged
*[] - who has flagged a review and when
*[] - admin is able to assist in "redemption"
*[] - get bugs reported to admin inbox (link on page? auto pop up?)
*[] - find a way to auto flag reports that have too few of details for admin to review
*[] - alerts for users when their reviews have been flagged for rebuttals
*[]-send emails for alerts for


