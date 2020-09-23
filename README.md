# Stonecroft Bees

Stonecroft Bees will be a website for a commercial beekeeping business; which sells bee products, such as honey and beeswax, and beekeeping supplies, such as hives, tools, and books.

The site will be a full featured e-commerce site, allowing both registered and unregistered purchases by customers, and the site admin to administrate products and users, and manage stock levels.

## UX

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
| 26  | Site Owner | Automatically have marked reserved when purchased                 | Prevent shoppers buying more stock than available                                     |
| 27  | Site Owner | Automatically have reserved stocked unmarked when order cancelled | Allow that stock to be re-available for purchase by other shoppers                    |
| 28  | Site Owner | Stock to subtract when order marked as dispatched                 | Have stock levels on system match stock levels in warehouse                           |
| 29  | Site Owner | Get a printable invoice                                           | So I know what items to pick for an order                                             |
|     |            | **_Messaging_**                                                   |                                                                                       |
| 30  | Public     | Report on sightings of bee swarms                                 | Alert local beekeepers of the location of a swarm                                     |
| 31  | Beekeeper  | Get email alerts of swarms reported                               | Collect them and get free bees                                                        |
| 32  | Shopper    | Send enquiries to site owner                                      | To get answers to questions                                                           |

### Wireframes 

For Desktop wireframes see [docs/wireframes/desktop.pdf](docs/wireframes/desktop.pdf)

For Mobile wireframes see [docs/wireframes/mobile.pdf](docs/wireframes/mobile.pdf)


## Features

### Existing Features

#### A secure login system (provided by allauth) to:
- Register for accounts, login/out, handle emails for confirmation and password resets
- User Profiles to:
  - store their contact and delivery information, to prefil forms with for convenience
  - maintain an order history

#### A navbar which provides easy access on any page to:
- Login/Register/View User Profile
- Frequent admin functions
- Shopping cart with a display of the current total
- Search products
- Access product categories
- Access the contact systems

#### A Product Database which:
- Stores details of Products sold such as name, category, etc
- Has Product Lines for different colour varities of products or bulk casings
  - Each line allows it's own price and name, and tracks its own stock levels
- Products list display which displays products filtered by category and allows sorting by various options
- Product details which present the image, name, price etc of the product and its lines to the customers
- Makes use of Django Admin pages to manage creating and editing of products/lines
- Product/Lines soft delete via a '***_discontinued' field, to maintain data integrity and references with order history, etc

#### Stock Keeping:
- Each Product has Product Lines which track the quantity in stock and the amount of stock reserved
- When a customer completes an order stock is reserved on that Line
- The available stock (Quantity - Reserved) is checked at various points to ensure customer can not buy more than is available
  - Product Details: 
    - The available stock is passed to the selector and displayed for the customer
    - This is passed to the quantity selector, which uses it to set its max levels
  - Bag: 
    - Checked when adding to bag, or adjusting current quantity
    - When viewing bag, Javascript highlights the fields which have more selected than available
  - Checkout: 
    - Once as a precheck before the user sees the form, returns them to Bag screen to make adjustments if needed
    - When purchase submitted a final penultimate check is made during order creation (or backup Webhook)
      - This is for the very rare instances that someone has bought the stock between the time the customer enters the checkout and submits the purchase
      - In this case the payment intent is cancelled so the user isn't charged, and the customer is returned to the bag page with error details

#### Bag
- Bag total is visible on every page via a navbar element
- Provides a page for the customer to:
  - view items in their bag
  - alter the quantity of items in the bag
  - remove items from the bag
- Validates that quantity selected is actually available (see Stock Keeping.3)

#### Checkout 
- Uses the Stripe payment system to provide safe and secure checking out
- Allows purchases by both registered and unregistered customers
- Orders are stored in the database
- Uses Stripe Webhooks to create Order record if something goes wrong between the customer purchasing the order and the backend creating the order
- Payment Intents are deferred until Ordered created on DB either via POST backend or Webhook
- Orders have a status:
  - Processing - when order is initially created on DB
  - Pending - set once Webhook has been recieved to confirm payment successfully
  - Picking - order has been sent for picking in warehouse (FOR FUTURE USE)
  - Dispatched - order has been dispatched to customer (FOR FUTURE USE)
  - Cancelled - Order has been cancelled (FOR FUTURE USE)
- Customer recieves email to confirm order

#### Contact
- Provides a contact form for general enquiries
- Provides a contact form for reporting bee swarms
- Both send email receipt to submitter
- Swarms sends email to specified email address (likely an email address group) with details of the swarm
- Messages are stored in the database for future use

### Features Left to Implement

For following User Stories were cut for time, but would be good to implement later:

| ID  | As A/An    | I want to...                                                      | So I can...                                                                           |
| --- | ---------- | ----------------------------------------------------------------- | ------------------------------------------------------------------------------------- |
| 3   | Shopper    | See list of deals, clearance items, etc                           | Take advantage of deals and save money                                                |
| 27  | Site Owner | Automatically have reserved stocked unmarked when order cancelled | Allow that stock to be re-available for purchase by other shoppers                    |
| 28  | Site Owner | Stock to subtract when order marked as dispatched                 | Have stock levels on system match stock levels in warehouse                           |
| 29  | Site Owner | Get a printable invoice                                           | So I know what items to pick for an order                                             |

#### Future Ideas
##### Stock Reservation
As currently implemented the focus was primary a defensive one to prevent customers trying to purchase more stock than available.  
Although this was implemented with the intent of also giving a good User Expirience, there is still room for improvement.

Specifically the final checkout check, which occurs after the customer has already entered their payment information and confirmed the purchase, 
this could be annoying (and concerning) to the customer (though should be rare after the previous checks, and the customer isn't actually charged).

A better system would probably have some sort of soft reservations when a user adds the item to their bag, 
but this would need to make a system to clear or expire those reservations when the user abandons the purchase. 

##### Stock Control / Ordering
The current system is baby steps, it tracks the quantity in the warehouse and updates the amount reserved when purchased.  
But a full system would need to create picking tickets, track when dispatched, and allow the user to cancel their order and return the stock to the available pool.

##### User Profile
There's currently no way for the user to set their name fields, this would be highly useful for a full program.

## Technologies Used

In this section, you should mention all of the languages, frameworks, libraries, and any other tools that you have used to construct this project. For each, provide its name, a link to its official site and a short sentence of why it was used.

- [JQuery](https://jquery.com)
  - The project uses **JQuery** to simplify DOM manipulation.

## Testing

Testing documentation is located in a separate [TESTING.md document](docs/TESTING.md) located in the docs folder.

## Deployment

This section should describe the process you went through to deploy the project to a hosting platform (e.g. GitHub Pages or Heroku).

In particular, you should provide all details of the differences between the deployed version and the development version, if any, including:

- Different values for environment variables (Heroku Config Vars)?
- Different configuration files?
- Separate git branch?

In addition, if it is not obvious, you should also describe how to run your code locally.

## Credits

### Content

- No text resources were sampled from external sources

### Media

- The photos used in this site were obtained from ...
  - swarm.jpg sampled from [Buzz About Bees](https://www.buzzaboutbees.net/swarmingbees.html)
  - bees.jpg from [Undark](https://undark.org/2016/05/24/evolving-a-better-honey-bee-how-wild-bees-resist-the-varroa-mite/)
  - noimage.png taken from Code Institute course materials
  - logo.svg original work by me, Andrew Kenworthy

### Acknowledgements

- I received inspiration for this project, and based the code, from Code Institute's 'Full Stack Frameworks With Django' course material. 
