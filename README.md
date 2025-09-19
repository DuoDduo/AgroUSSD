

# AgroUSSD: Nigerian Agricultural USSD System

### Project Overview

AgroUSSD is a simple USSD-based system designed to help Nigerian farmers access market prices, manage harvests, and connect directly with buyers. It simulates USSD interactions through a console interface, making it accessible to basic mobile phones.

The system promotes fair pricing, reduces middleman exploitation, and helps farmers make informed decisions about their produce.

---

### Key Features

**For Farmers:**

* Register farm details, crops, and location
* Record and manage harvests
* View market prices and compare across locations
* Connect directly with buyers

**For Buyers:**

* Search for farmers by location or product
* Access price and availability information
* Contact farmers directly

**General Features:**

* Menu-based navigation simulating USSD
* Session management for user continuity
* Text-based interface suitable for basic phones
* Input validation and clear feedback messages

---

### Technical Overview

* **Programming Language:** Python 3.8+
* **Interface:** Console-based, simulating USSD menus
* **Data Storage:** JSON/CSV files (file-based persistence)
* **Design:** Object-Oriented Programming with Abstract Base Classes for Users, Products, Marketplace, and USSD Interfaces

---

### Folder Structure

```
AgroUSSD/
├── src/
│   ├── models/           # Farmer, Buyer, Crop, Harvest, and abstract classes
│   ├── services/         # User, Market, Harvest, and Connection services
│   ├── interfaces/       # USSD menu classes and session management
│   ├── utils/            # Helpers, validators, and file handling
│   └── main.py           # Application entry point
│
├── data/                 # JSON files storing users, harvests, market prices, and connections

              
```

### How to Run

1. Ensure Python 3.8+ is installed.


3. Launch the application:

```bash
python main.py
```

4. Navigate the menus to register, check prices, manage harvests, and connect with users.

---

### Why This Matters

* Empowers farmers with market information
* Enables buyers to access fresh produce at fair prices
* Reduces middleman exploitation
* Builds a sustainable, technology-enabled agricultural ecosystem

---

### Team / Authors

* **Blessing James** – Project Lead / Developer


>

---

### License

MIT License

---

