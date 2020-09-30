# TESTING

## Method

Testing was carried out manually throughout the development process, when the project was 
feature complete another pass of manual testing was carried out.  
Automated tests were written towards the end as a demonstrative proof of concept.


---------
## Automated Tests

Automated tests have been written to cover the Home, Products, and Contact apps.  
Coverage was used to check the tests covered the most of the major components of these apps.
The Bag, Checkout, Profile apps do not currently have automated tests written for them.

To run the tests simply execute: python3 manage.py test


---------
## Manual Testing

These are most of the manual tests which were performed.

### Home 
##### UX
1. Colours and fonts should look readable and nice
2. Use dev-tools to alter width of screen to check responsive design

##### Functionality
1. Test each link in the Nav Bar
   - At mobile width
   - At desktop width
2. Test each button on homepage
3. Check admin functions on profile widget only show to logged in admins


### Products: List 
##### UX
1. Colours and fonts should look readable and nice
2. Use dev-tools to alter width of screen to check responsive design

##### Functionality
1. Visit the various product categories, check that displayed result set is what is expected
2. Use each sort function, check order is manipulated as expected
3. Up arrow button in bottom right corner: clicking returns screen to top of page


### Products: Details 
##### UX
1. Colours and fonts should look readable and nice
2. Use dev-tools to alter width of screen to check responsive design

##### Functionality
1. Use test items to check templates render correctly
   1. Example item '16oz (454g) Jarred Honey' displays all details correctly:
      - Title
      - Item picture (jar of honey)
      - Description
      - Variety selector list
   2. Url: products/4/
      - Returns user to home page with error "Product has been discontinued"
   3. 'Test Line Discontinued'
      - Only shows two variety items (that aren't discontinued)  
   4. 'No line items':
      - Hides:
        - Variety selector
        - Quantity controls
        - Add to bag button
      - Shows:
        - Error: "Sorry! No product lines available." in red
2. On Variety change
   1. Available stock level display changes when variety changed 
   2. 'Price Per' does as above
   3. Quantity is changed to stock available if above new stock available
   4. Quantity stays the same if value less than new stock available
3. Quantity widget
   1. Subtotal updates when quantity manipulated
   2. Quantity change buttons work, and do not allow Quantity to exceed stock available
4. Admin functions (Edit/Discontinue)
   1. Check can only be seen by logged in superuser
   2. Check edit goes to admin edit page
   3. Check discontinue discontinues the product

##### Functionality: Add to Bag button
1. Add an item, it should add to bag and message window displays this
2. Add item again, it should add to current bag quantity
3. Add different varieties of same product, the bag should the different varieties with their own quanties
4. Use dev tools to edit the form, change quantity min to 0 and value to 0, submit form.  
   You should be redirected back to product details page with error "Can't add item with zero quantity"


### Bag 
##### UX
1. Colours and fonts should look readable and nice
2. Use dev-tools to alter width of screen to check responsive design

##### Functionality
1. Up arrow button in bottom right corner: clicking returns screen to top of page
2. Check item quantity can be changed within limits
   - Update link should change blue and bold
3. Check item can be removed
4. Check fields change to show quantity validation error
   1. Add max quantity of product variety to bag
   2. Go to admin panel, increase reserved stock
   3. Go to Bag page
   4. Quantity should highlight red with red exclamation mark


### Checkout 
##### UX
1. Colours and fonts should look readable and nice
2. Use dev-tools to alter width of screen to check responsive design

##### Functionality
1. User should be sent to bag if item quantity invalid
   1. Add max quantity of product variety to bag
   2. Go to Bag page
   3. On admin panel, increase reserved stock
   4. Try to go to check out
   5. You should be sent back to Bag page with error
2. Go to checkout url with empty bag, you should be sent to products page with error message
3. With items in bag try to make purchases with these cards
   1. 4242 4242 4242 4242
      1. Payment should go through
      2. Order record should be created
      3. User redirects to success page
      4. Confirmation email should be sent to user
   2. 4000 0027 6000 3184
      1. 3D Secure Authorisation popup should appear
         1. Authorise: As above for 4242
         2. Reject or Chancel: Return to page with error displayed under card field
   3. 4000 0082 6000 3178
      1. 3D Secure Authorisation popup should appear
         1. Authorise: Rejected with insufficient funds
         2. Reject or Chancel: Return to page with error displayed under card field
4. Test back up web hook order creation
   1. Open 'stripe_elements.js', go to line 144 and comment out 'form.submit();'
   2. Submit order with 4242 card
   3. Page should stay on blue waiting screen
   4. Look at order records and confirm order was created via web hook
   5. Confirmation email should be sent to user
5. Place order as logged-in user, check that order is added to user's order history
6. Check logged user's delivery details updated if they check the 'Save this delivery information to my profile' checkbox
7. Check Product Line's stock reserved level has been adjusted appropriately


### Contact 
##### UX
1. Colours and fonts should look readable and nice
2. Use dev-tools to alter width of screen to check responsive design

##### Functionality
1. Submit form with all details, message should add to DB and user receive confirm email
2. Dev tools edit page to submit with missing required field, should redirect back to page with error
3. Check unauthed user can submit messages, and receives confirmation email
4. Check logged-in user can submit messages, and receives confirmation email, and their profile is attached to message


### Swarm Report 
##### UX
1. Colours and fonts should look readable and nice
2. Use dev-tools to alter width of screen to check responsive design

##### Functionality
1. Submit form with all details, message should add to DB and user receive confirm email
2. Dev tools edit page to submit with missing required field, should redirect back to page with error
3. Check unauthed user can submit messages, and receives confirmation email
4. Check logged-in user can submit messages, and receives confirmation email, and their profile is attached to message



### Profile 
##### UX
1. Colours and fonts should look readable and nice
2. Use dev-tools to alter width of screen to check responsive design

##### Functionality
1. Check user can save their default information
2. Check empty forms will clear stored details
3. Check order history displays correctly, newest dates first
4. Check clicking on order number takes user to that order's success page, and displays info message that it is an old order


---------
## Issues of Note

### Stripe Payments
Although not an issue per se, the way we were taught Stripe Payments was to have the 
Payment Intent automatically charge the customer's card.  
This caused an issue for my design as I intended to have a final stock check as the order 
was finalised, either by the POST view or through the backup method triggered by the web hook.  
Going via the taught method I would have to issue refunds to the Payment Intent, which was 
not a viable solution from a business perspective due to Stripe's transaction fees not being 
refunded to the business.

After researching and reading Stripe's manual I found I could change the Payment Intent 
to hold capturing the charge until later.  
This allowed me to run additional validation after the payment was authorised, if issues were 
found then the Payment Intent could be cancelled in full without causing charges 
to the customer or transaction fees to the business.

This was set to capture the charge once the order record was generated, but could be
set to capture at a later point, e.g. when the goods are dispatched from the warehouse - 
which a lot of retail companies do.
