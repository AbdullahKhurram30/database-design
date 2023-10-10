from faker import Faker
import random as random
from sqlalchemy.orm import sessionmaker
from create import engine, Office, Agent, AgentOffice, Client, House, Buyer, Sale, Commission

# start the session
Session = sessionmaker(bind=engine)
session = Session()

# make a faker object
fake = Faker()

# create some offices
for i in range(100):
    office = Office(name=fake.company(), address=fake.address(), zipcode=fake.zipcode(), phone=fake.phone_number())
    session.add(office)

# create some agents
for i in range(300):
    agent = Agent(name = fake.name(), phone = fake.phone_number(), email = fake.email())
    session.add(agent)

# populate the agent_office table by linking them together
for i in range(300):
    agent_office = AgentOffice(agent_id = i, office_id = fake.random_int(min=1, max=100))
    session.add(agent_office)

# create some clients
for i in range(300):
    client = Client(name = fake.name(), phone = fake.phone_number(), email = fake.email(), address = fake.address())
    session.add(client)

# create some buyers
for i in range(100):
    buyer = Buyer(name = fake.name(), phone = fake.phone_number(), email = fake.email(), address = fake.address())
    session.add(buyer)

session.commit()

# extract all the clients
clients = session.query(Client).all()
# extract all the agents_offices
agent_offices = session.query(AgentOffice).all()
# extract all the buyers
buyers = session.query(Buyer).all()

# create some houses
for i in range(300):
    client = random.choice(clients)
    agent_office = random.choice(agent_offices)
    house = House(seller_id = client.id, bedrooms = fake.random_int(min=1, max=5), bathrooms = fake.random_int(min=1, max=5),
                  listing_price = fake.random_int(min=10000, max=2000000), zipcode = fake.zipcode(), 
                  date_listed = fake.date_time_between(start_date='-1y', end_date='now'),
                  agent_id = agent_office.agent_id, office_id = agent_office.office_id)
    session.add(house)

session.commit()

# extract all the houses
houses = session.query(House).all()

# create some sales
for i in range(100):
    house = random.choice(houses)
    # remove the chosen house from the list as a house can't be sold twice
    houses.remove(house)
    buyer = random.choice(buyers)
    sale = Sale(house_id = house.id, agent_id = house.agent_id, office_id = house.office_id, price = house.listing_price, 
                date_sold = fake.date_time_between(start_date=house.date_listed, end_date='now'), buyer_id = buyer.id)
    session.add(sale)
    # set the house's status to sold
    house.sold = True
    session.add(house)

session.commit()

# extract all the sales
sales = session.query(Sale).all()
# create commissions using sales
for sale in sales:
    commission = Commission(agent_id = sale.agent_id, sale_id = sale.id, amount = sale.commission)
    session.add(commission)

session.commit()
                