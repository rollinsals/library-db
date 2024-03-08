# Lending Library Database/App

This was an attempt to implement a library database/app for tracking books and have them lent out to users with them able to review the books. 

Some of the main 'library' pieces are still missing (Checking books in/out of a library branch). This would have been the more interesting pieces but hopefully they'll be added eventually.

API 
## Reader
| Method | Name | Description | Path | Parameters |
| ------ | ---- | ----------- | ---- | ---------- |
| GET | Show | Returns the user's info | ~/user/<id> | - |
| GET | Show Reviews | Returns the reviews created by the user | ~/user/<id>/reviews | - |
| GET | Show Loans | Returns the books currently lent to the user | ~/user/<id>/loans | - |
| POST | Check Out Book | Adds association between the reader and input book | ~/user | book_id, user_id |
| DELETE | Return Book | Removes book from the reader's list | ~/user/<id>/loans | book_id |

## Library
| Method | Name | Description | Path | Parameters |
| ------ | ---- | ----------- | ---- | ---------- |
| GET | Index | Returns list of all library branches | ~/branches | - |
| GET | Show | Returns library branch info | ~/branches/<id> | - |
| GET | List Books | Returns books belonging to a branch | ~/branches/<id>/book_inventory | - |
| ***GET*** | Copies of | Returns number of available copies *(unimplimented)* | - | - |
| ***GET*** | Member List | Lists users under this library *(unimplimented)* | - | - |

## Book
| Method | Name | Description | Path | Parameters |
| ------ | ---- | ----------- | ---- | ---------- |
| GET | Show | Returns the book's info | ~/books/<id> | - |
| GET | Index | Lists all books | ~/books | - |
| POST | Create | Adds new book | ~/books | **Title**, **author_id**, genre, format, publish_year |
| DELETE | Delete | Removes a book | ~/books/<id> | - |
| GET | Libraries Available | Lists library branches with the book | ~/books/<id>/libraries | - |
| GET | List Reviews | Lists reviews of a book | ~/books/<id>/reviews | - |
| GET | Average Rating | Returns average of all reader reviews (0-10) | ~/books/<id>/reviews/avg | - |

## Review
| Method | Name | Description | Path | Parameters |
| ------ | ---- | ----------- | ---- | ---------- |
| GET | Show | Returns a review's info | ~/reviews/<id> | - |
| GET | Index | Returns all reviews | ~/reviews | - |
| POST | Create | Generates a new review | ~/reviews | **reader_id**, **book_id**, review_body, rating |
| PUT | Update | Modifies review text, rating, or both | ~/reviews/<id> | **reader_id**, **book_id**, review_body, rating |
| DELETE | Delete | Removes a user's review | ~/reviews/<id> | - |

#### Retrospective


One of the main things I intended originally was to be able to change the "available copies" of a book from a library list. I didn't really figure out how to access columns in the intermediate tables (of many-to-many relationships). The user to book relationship also had 2 data points (date of check out and due date) I would want to access but again, didn't quite figure it out. The one-to-one could probably be done more properly - it didn't quite feel right. Ideally, it would create a new Reader when a new Profile is created. I'm not positive whether that should be done in the API points or with a SQL trigger. Either way, I'm not entirely satisfied with the current version.

Because some of the more complicated pieces didn't come together, I don't find the existing pieces terribly *interesting* compared to what was covered in the course material. 

The project ended up being a bit more ambitious in scope than I originally thought. The API pieces I did include were not particularly original from the Flask example we completed for the class but trying to piece together how the object back references works definitely required some work. 

I could add in API points for everything still: 
- author entity. still doesn't have any
- user entity points. 
- library members: users associated with each library branch


## Notes
I had to run my Faker seed file a few times to work out some errors so the ids in the Insomnia file match up with my working one. They might need to be adjusted for a new instance of the database.
