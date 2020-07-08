# Stonecroft Bees

Stonecroft Bees will be a website for a commercial beekeeping business; which sells bee products, such as honey and beeswax, and beekeeping supplies, such as hives, tools, and books.

The site will be a full featured e-commerce site, allowing both registered and unregistered purchases by customers, and the site admin to administrate products and users, and manage stock levels.

## UX

Use this section to provide insight into your UX process, focusing on who this website is for, what it is that they want to achieve and how your project is the best way to help them achieve these things.

In particular, as part of this section we recommend that you provide a list of User Stories, with the following general structure:

- As a user type, I want to perform an action, so that I can achieve a goal.

This section is also where you would share links to any wireframes, mockups, diagrams etc. that you created as part of the design process. These files should themselves either be included as a pdf file in the project itself (in an separate directory), or just hosted elsewhere online and can be in any format that is viewable inside the browser.

### Intended Audience

The site will be intended to be used by customers, both unregistered and registered, to allow them to view products, add products to a shopping basket, and make purchases using Stripe. Registered users will also be able to make a profile to view their previous orders, and store their address and contact information etc to make checking out quicker.

Site Owners will be able to manage user profiles, add product information, and view and manage stock levels, and view and manage outstanding orders.

### User Stories

| ID  | As A/An    | I want to...                                                      | So I can...                                                                           |
| --- | ---------- | ----------------------------------------------------------------- | ------------------------------------------------------------------------------------- |
|     |            | **_Viewing and Navigation_**                                      |                                                                                       |
| 1   | Shopper    | View list of products                                             | Find something to purchase                                                            |
| 2   | Shopper    | View details of product                                           | See Price, Description, Image, and Sizes i/a                                          |
| 3   | Shopper    | See list of deals, clearance items, etc                           | Take advantage of deals and save money                                                |
| 4   | Shopper    | See my cart's total at any time                                   | Avoid spending too much                                                               |
|     |            | **_Registration and User Accounts_**                              |                                                                                       |
| 5   | Reg User   | Register for an account                                           | Save my delivery details and order history                                            |
| 6   | Reg User   | Quickly login/out                                                 | Access my account                                                                     |
| 7   | Reg User   | Request a password reset                                          | receive and email to reset my password in case I forget it                            |
| 8   | Reg User   | Receive an email confirming my registration                       | Verify my account was registered successfully                                         |
| 9   | Reg User   | Access my user profile                                            | View my order history, manage my personal details                                     |
|     |            | **_Sorting and Searching_**                                       |                                                                                       |
| 10  | Shopper    | Sort the list of available products                               | See the products in a list sorted by price, rating, quantity available etc            |
| 11  | Shopper    | Sort a category of products                                       | See the products in a category sorted by name, price, rating, etc                     |
| 12  | Shopper    | Sort multiple categories simultaneously                           | Find the best rated or best priced across broad categories such as 'books' or 'honey' |
| 13  | Shopper    | Search for product                                                | Find a specific item I wish to purchase                                               |
| 14  | Shopper    | View a list of search results                                     | See if the product I want is available to purchase                                    |
|     |            | **_Purchasing and Checkout_**                                     |                                                                                       |
| 15  | Shopper    | Easily select the size and quantity whilst purchasing an item     | Ensure I don't accidentally select the wrong product, quantity, or size               |
| 16  | Shopper    | View items in my basket                                           | See what items are in my basket at a glance to ensure the items are correct           |
| 17  | Shopper    | Adjust the quantity of individual items in my bag                 | Easily adjust the amount of an item I intended to purchase (including removing)       |
| 18  | Shopper    | Easily enter my payment information                               | Checkout quickly, without hassle                                                      |
| 19  | Shopper    | Feel my payment and personal information is secure                | Provide the needed payment and personal information, and feel it is handled safely    |
| 20  | Shopper    | View confirmation of order before completing purchase             | Verify I haven't made any mistakes                                                    |
| 21  | Shopper    | Receive confirmation email after checking out                     | To keep my own record of the purchase                                                 |
|     |            | **_Admin and Store Management_**                                  |                                                                                       |
| 22  | Site Owner | Add a product                                                     | Add new products to my store                                                          |
| 23  | Site Owner | Edit/update a product                                             | Change the price, description, images etc of a product                                |
| 24  | Site Owner | Delete a product                                                  | Remove items that aren't for sale anymore                                             |
|     |            | **_Stock Control_**                                               |                                                                                       |
| 25  | Site Owner | Keep records of available stock levels                            | Manage the level of stock                                                             |
| 24  | Site Owner | Automatically have marked reserved when purchased                 | Prevent shoppers buying more stock than available                                     |
| 25  | Site Owner | Automatically have reserved stocked unmarked when order cancelled | Allow that stock to be re-available for purchase by other shoppers                    |
| 26  | Site Owner | Stock to subtract when order marked as dispatched                 | Have stock levels on system match stock levels in warehouse                           |
| 27  | Site Owner | Get a printable invoice                                           | So I know what items to pick for an order                                             |
|     |            | **_Swarm Alerts_**                                                |                                                                                       |
| 28  | Public     | Report on sightings of bee swarms                                 | Alert local beekeepers of the location of a swarm                                     |
| 29  | Beekeeper  | Get email alerts of swarms reported                               | Collect them and get free bees                                                        |

## Features

In this section, you should go over the different parts of your project, and describe each in a sentence or so.

### Existing Features

- Feature 1 - allows users X to achieve Y, by having them fill out Z
- ...

For some/all of your features, you may choose to reference the specific project files that implement them, although this is entirely optional.

In addition, you may also use this section to discuss plans for additional features to be implemented in the future:

### Features Left to Implement

- Another feature idea

## Technologies Used

In this section, you should mention all of the languages, frameworks, libraries, and any other tools that you have used to construct this project. For each, provide its name, a link to its official site and a short sentence of why it was used.

- [JQuery](https://jquery.com)
  - The project uses **JQuery** to simplify DOM manipulation.

## Testing

In this section, you need to convince the assessor that you have conducted enough testing to legitimately believe that the site works well. Essentially, in this part you will want to go over all of your user stories from the UX section and ensure that they all work as intended, with the project providing an easy and straightforward way for the users to achieve their goals.

Whenever it is feasible, prefer to automate your tests, and if you've done so, provide a brief explanation of your approach, link to the test file(s) and explain how to run them.

For any scenarios that have not been automated, test the user stories manually and provide as much detail as is relevant. A particularly useful form for describing your testing process is via scenarios, such as:

1. Contact form:
   1. Go to the "Contact Us" page
   2. Try to submit the empty form and verify that an error message about the required fields appears
   3. Try to submit the form with an invalid email address and verify that a relevant error message appears
   4. Try to submit the form with all inputs valid and verify that a success message appears.

In addition, you should mention in this section how your project looks and works on different browsers and screen sizes.

You should also mention in this section any interesting bugs or problems you discovered during your testing, even if you haven't addressed them yet.

If this section grows too long, you may want to split it off into a separate file and link to it from here.

## Deployment

This section should describe the process you went through to deploy the project to a hosting platform (e.g. GitHub Pages or Heroku).

In particular, you should provide all details of the differences between the deployed version and the development version, if any, including:

- Different values for environment variables (Heroku Config Vars)?
- Different configuration files?
- Separate git branch?

In addition, if it is not obvious, you should also describe how to run your code locally.

## Credits

### Content

- The text for section Y was copied from the [Wikipedia article Z](https://en.wikipedia.org/wiki/Z)

### Media

- The photos used in this site were obtained from ...

### Acknowledgements

- I received inspiration for this project from X
