from faker import Faker
import random as random
from sqlalchemy.orm import sessionmaker
from create import Base, Office, Agent, AgentOffice, Client, House, Buyer, Sale, Commission
from sqlalchemy import create_engine
import os

# Create the database engine
test_engine = create_engine('sqlite:///test.db')
Base.metadata.create_all(test_engine)
# create a session
Session = sessionmaker(bind = test_engine)
session = Session()
fake = Faker()

def test_office_creation():
    # make a office
    office = Office(name=fake.company(), address=fake.address(), zipcode=fake.zipcode(), phone=fake.phone_number())
    # add it to the database
    session.add(office)
    session.commit()
    # query all offices
    offices = session.query(Office).all()
    # check that you only have one office
    assert len(offices) ==  1
    # check the office has the right name
    assert offices[0].name == office.name
    # check the office has the right address
    assert offices[0].address == office.address
    # check the office has the right zipcode
    assert offices[0].zipcode == office.zipcode
    # check the office has the right phone number
    assert offices[0].phone == office.phone
    # remove office from the database
    session.delete(office)

def test_agent_creation():
    # create an Agent
    agent = Agent(name=fake.name(), phone=fake.phone_number(), email=fake.email())
    # add it to the database
    session.add(agent)
    session.commit()
    # query all agents
    agents = session.query(Agent).all()
    # check that you only have one agent
    assert len(agents) ==  1
    # check the agent has the right name
    assert agents[0].name == agent.name
    # check the agent has the right phone number
    assert agents[0].phone == agent.phone
    # check the agent has the right email
    assert agents[0].email == agent.email
    # remove the agent from the database
    session.delete(agent)

def test_office_agent_relation():
    # make an office, an agent, and one relationship between them
    office = Office(name=fake.company(), address=fake.address(), zipcode=fake.zipcode(), phone=fake.phone_number())
    agent = Agent(name=fake.name(), phone=fake.phone_number(), email=fake.email())
    session.add_all([office, agent])
    session.commit()
    # query all the agents and offices
    agents = session.query(Agent).all()
    offices = session.query(Office).all()
    agent_office = AgentOffice(agent_id=agent.id, office_id=office.id)
    # add the agent_office to the database
    session.add(agent_office)
    session.commit()
    # query all agent_office relationships
    agent_offices = session.query(AgentOffice).all()
    # check you only have one of each
    assert len(agents) ==  1
    assert len(offices) ==  1
    assert len(agent_offices) ==  1
    # check the relationship has the right agent_id
    assert agent_offices[0].agent_id == agent.id
    # check the relationship has the right office_id
    assert agent_offices[0].office_id == office.id
    # check that the relationship is consistent in the database
    assert agent_offices[0].agent_id == agents[0].id
    assert agent_offices[0].office_id == offices[0].id
    # remove them all from the database
    session.delete(office)
    session.delete(agent)
    session.delete(agent_office)

def test_client_creation():
    # make a client
    client = Client(name=fake.name(), phone=fake.phone_number(), email=fake.email(), address=fake.address())
    # add it to the database
    session.add(client)
    session.commit()
    # query all clients
    clients = session.query(Client).all()
    # check that you only have one client
    assert len(clients) ==  1
    # check the client has the right name
    assert clients[0].name == client.name
    # check the client has the right phone number
    assert clients[0].phone == client.phone
    # check the client has the right email
    assert clients[0].email == client.email
    # check the client has the right address
    assert clients[0].address == client.address
    # remove client from the database
    session.delete(client)

def test_house_creation():
    # make a client, agent, office
    client = Client(name=fake.name(), phone=fake.phone_number(), email=fake.email(), address=fake.address())
    agent = Agent(name=fake.name(), phone=fake.phone_number(), email=fake.email())
    office = Office(name=fake.company(), address=fake.address(), zipcode=fake.zipcode(), phone=fake.phone_number())
    # add these to the database
    session.add_all([client, agent, office])
    session.commit()
    # query all the agents, offices and clients
    agents = session.query(Agent).all()
    offices = session.query(Office).all()
    clients = session.query(Client).all()
    agent_office = AgentOffice(agent_id=agent.id, office_id=office.id)
    # add the agent_office to the database
    session.add(agent_office)
    session.commit()
    # query all agent_office relationships
    agent_offices = session.query(AgentOffice).all()
    # make a house
    house = House(seller_id=client.id, bedrooms=random.randint(1,5),
                  bathrooms=random.randint(1,5), listing_price=random.randint(10000,1000000),
                  zipcode = fake.zipcode(), date_listed=fake.date_time_between(start_date='-1y', end_date='now'),
                  agent_id=agent.id, office_id=agent_office.office_id)
    # add it to the database
    session.add(house)
    session.commit()
    # query all houses
    houses = session.query(House).all()
    # check that you only have one house
    assert len(houses) ==  1
    # check the house has the right seller_id
    assert houses[0].seller_id == client.id
    # check the house has the right bedrooms
    assert houses[0].bedrooms == house.bedrooms
    # check the house has the right bathrooms
    assert houses[0].bathrooms == house.bathrooms
    # check the house has the right listing_price
    assert houses[0].listing_price == house.listing_price
    # check the house has the right zipcode
    assert houses[0].zipcode == house.zipcode
    # check the house has the right date_listed
    assert houses[0].date_listed == house.date_listed
    # check the house has the right agent_id
    assert houses[0].agent_id == agent.id
    # check the house has the right office_id
    assert houses[0].office_id == agent_office.office_id
    # remove them all from the database
    session.delete(client)
    session.delete(agent)
    session.delete(office)
    session.delete(agent_office)
    session.delete(house)

def test_buyer_creation():
    # make a buyer
    buyer = Buyer(name=fake.name(), phone=fake.phone_number(), email=fake.email(), address=fake.address())
    # add it to the database
    session.add(buyer)
    session.commit()
    # query all buyers
    buyers = session.query(Buyer).all()
    # check that you only have one buyer
    assert len(buyers) ==  1
    # check the buyer has the right name
    assert buyers[0].name == buyer.name
    # check the buyer has the right phone number
    assert buyers[0].phone == buyer.phone
    # check the buyer has the right email
    assert buyers[0].email == buyer.email
    # check the buyer has the right address
    assert buyers[0].address == buyer.address
    # remove buyer from the database
    session.delete(buyer)

def test_sale_creation():
    # make a client, agent, office
    client = Client(name=fake.name(), phone=fake.phone_number(), email=fake.email(), address=fake.address())
    agent = Agent(name=fake.name(), phone=fake.phone_number(), email=fake.email())
    office = Office(name=fake.company(), address=fake.address(), zipcode=fake.zipcode(), phone=fake.phone_number())
    # add these to the database
    session.add_all([client, agent, office])
    session.commit()
    # query all the agents, offices and clients
    agents = session.query(Agent).all()
    offices = session.query(Office).all()
    clients = session.query(Client).all()
    agent_office = AgentOffice(agent_id=agent.id, office_id=office.id)
    # add the agent_office to the database
    session.add(agent_office)
    session.commit()
    # query all agent_office relationships
    agent_offices = session.query(AgentOffice).all()
    # make a house
    house = House(seller_id=client.id, bedrooms=random.randint(1,5),
                  bathrooms=random.randint(1,5), listing_price=random.randint(10000,1000000),
                  zipcode = fake.zipcode(), date_listed=fake.date_time_between(start_date='-1y', end_date='now'),
                  agent_id=agent.id, office_id=agent_office.office_id)
    # add it to the database
    session.add(house)
    session.commit()
    # query all houses
    houses = session.query(House).all()
    # make a buyer
    buyer = Buyer(name=fake.name(), phone=fake.phone_number(), email=fake.email(), address=fake.address())
    # add it to the database
    session.add(buyer)
    session.commit()
    # query all buyers
    buyers = session.query(Buyer).all()
    # make a sale
    sale = Sale(house_id=house.id, agent_id=house.agent_id,
                office_id=house.office_id, price=house.listing_price,
                date_sold=fake.date_time_between(start_date=house.date_listed, end_date='now'),
                buyer_id=buyer.id)
    # add it to the database
    session.add(sale)
    session.commit()
    # query all sales
    sales = session.query(Sale).all()
    # check that you only have one sale
    assert len(sales) ==  1
    # check the sale has the right house_id
    assert sales[0].house_id == house.id
    # check the sale has the right agent_id
    assert sales[0].agent_id == house.agent_id
    # check the sale has the right office_id
    assert sales[0].office_id == house.office_id
    # check the sale has the right price
    assert sales[0].price == house.listing_price
    # check the sale has the right date_sold
    assert sales[0].date_sold == sale.date_sold
    # check the sale has the right buyer_id
    assert sales[0].buyer_id == buyer.id
    # remove them all from the database
    session.delete(client)
    session.delete(agent)
    session.delete(office)
    session.delete(agent_office)
    session.delete(house)
    session.delete(buyer)
    session.delete(sale)

def test_commission_creation():
    # make a client, agent, office
    client = Client(name=fake.name(), phone=fake.phone_number(), email=fake.email(), address=fake.address())
    agent = Agent(name=fake.name(), phone=fake.phone_number(), email=fake.email())
    office = Office(name=fake.company(), address=fake.address(), zipcode=fake.zipcode(), phone=fake.phone_number())
    # add these to the database
    session.add_all([client, agent, office])
    session.commit()
    # query all the agents, offices and clients
    agents = session.query(Agent).all()
    offices = session.query(Office).all()
    clients = session.query(Client).all()
    agent_office = AgentOffice(agent_id=agent.id, office_id=office.id)
    # add the agent_office to the database
    session.add(agent_office)
    session.commit()
    # query all agent_office relationships
    agent_offices = session.query(AgentOffice).all()
    # make a house
    house = House(seller_id=client.id, bedrooms=random.randint(1,5),
                  bathrooms=random.randint(1,5), listing_price=random.randint(10000,1000000),
                  zipcode = fake.zipcode(), date_listed=fake.date_time_between(start_date='-1y', end_date='now'),
                  agent_id=agent.id, office_id=agent_office.office_id)
    # add it to the database
    session.add(house)
    session.commit()
    # query all houses
    houses = session.query(House).all()
    # make a buyer
    buyer = Buyer(name=fake.name(), phone=fake.phone_number(), email=fake.email(), address=fake.address())
    # add it to the database
    session.add(buyer)
    session.commit()
    # query all buyers
    buyers = session.query(Buyer).all()
    # make a sale
    sale = Sale(house_id=house.id, agent_id=house.agent_id,
                office_id=house.office_id, price=house.listing_price,
                date_sold=fake.date_time_between(start_date=house.date_listed, end_date='now'),
                buyer_id=buyer.id)
    # add it to the database
    session.add(sale)
    session.commit()
    # query all sales
    sales = session.query(Sale).all()
    # make the commission object
    commission = Commission(agent_id=sale.agent_id, sale_id=sale.id, 
                            amount=sale.commission)
    # add it to the database
    session.add(commission)
    session.commit()
    # query all commissions
    commissions = session.query(Commission).all()
    # check that you only have one commission
    assert len(commissions) ==  1
    # check the commission has the right agent_id
    assert commissions[0].agent_id == sale.agent_id
    # check the commission has the right sale_id
    assert commissions[0].sale_id == sale.id
    # check the commission has the right amount
    assert commissions[0].amount == sale.commission
    # remove them all from the database
    session.delete(client)
    session.delete(agent)
    session.delete(office)
    session.delete(agent_office)
    session.delete(house)
    session.delete(buyer)
    session.delete(sale)
    session.delete(commission)

def test_commission_calculation():
    # we don't need to add these to the database as the objective is checking the calculations
    # make a house for below 100000
    house = House(seller_id=1, bedrooms=random.randint(1,5),
                    bathrooms=random.randint(1,5), listing_price=70000,
                    zipcode = fake.zipcode(), date_listed=fake.date_time_between(start_date='-1y', end_date='now'),
                    agent_id=1, office_id=1)
    # make a sale
    sale = Sale(house_id=house.id, agent_id=house.agent_id,
                office_id=house.office_id, price=house.listing_price,
                date_sold=fake.date_time_between(start_date=house.date_listed, end_date='now'),
                buyer_id=1)
    # make the commission object
    commission = Commission(agent_id=sale.agent_id, sale_id=sale.id,
                            amount=sale.commission)
    # check the commission amount is correct
    assert commission.amount == 7000
    # make a house between 100000 and 200000
    house_2 = House(seller_id=2, bedrooms=random.randint(1,5),
                    bathrooms=random.randint(1,5), listing_price=170000,
                    zipcode = fake.zipcode(), date_listed=fake.date_time_between(start_date='-1y', end_date='now'),
                    agent_id=2, office_id=2)
    # make a sale
    sale_2 = Sale(house_id=house_2.id, agent_id=house_2.agent_id,
                office_id=house_2.office_id, price=house_2.listing_price,
                date_sold=fake.date_time_between(start_date=house_2.date_listed, end_date='now'),
                buyer_id=2)
    # make the commission object
    commission_2 = Commission(agent_id=sale_2.agent_id, sale_id=sale_2.id,
                            amount=sale_2.commission)
    # check the commission amount is correct
    assert commission_2.amount == 12750
    # make a house between 200000 and 500000
    house_3 = House(seller_id=3, bedrooms=random.randint(1,5),
                    bathrooms=random.randint(1,5), listing_price=400000,
                    zipcode = fake.zipcode(), date_listed=fake.date_time_between(start_date='-1y', end_date='now'),
                    agent_id=3, office_id=3)
    # make a sale
    sale_3 = Sale(house_id=house_3.id, agent_id=house_3.agent_id,
                office_id=house_3.office_id, price=house_3.listing_price,
                date_sold=fake.date_time_between(start_date=house_3.date_listed, end_date='now'),
                buyer_id=3)
    # make the commission object
    commission_3 = Commission(agent_id=sale_3.agent_id, sale_id=sale_3.id,
                            amount=sale_3.commission)
    # check the commission amount is correct
    assert commission_3.amount == 24000
    # make a house between 500000 and 1000000
    house_4 = House(seller_id=4, bedrooms=random.randint(1,5),
                    bathrooms=random.randint(1,5), listing_price=700000,
                    zipcode = fake.zipcode(), date_listed=fake.date_time_between(start_date='-1y', end_date='now'),
                    agent_id=4, office_id=4)
    # make a sale
    sale_4 = Sale(house_id=house_4.id, agent_id=house_4.agent_id,
                office_id=house_4.office_id, price=house_4.listing_price,
                date_sold=fake.date_time_between(start_date=house_4.date_listed, end_date='now'),
                buyer_id=4)
    # make the commission object
    commission_4 = Commission(agent_id=sale_4.agent_id, sale_id=sale_4.id,
                            amount=sale_4.commission)
    # check the commission amount is correct
    assert commission_4.amount == 35000
    # make a house above 10000000
    house_5 = House(seller_id=5, bedrooms=random.randint(1,5),
                    bathrooms=random.randint(1,5), listing_price=1500000,
                    zipcode = fake.zipcode(), date_listed=fake.date_time_between(start_date='-1y', end_date='now'),
                    agent_id=5, office_id=5)
    # make a sale
    sale_5 = Sale(house_id=house_5.id, agent_id=house_5.agent_id,
                office_id=house_5.office_id, price=house_5.listing_price,
                date_sold=fake.date_time_between(start_date=house_5.date_listed, end_date='now'),
                buyer_id=5)
    # make the commission object
    commission_5 = Commission(agent_id=sale_5.agent_id, sale_id=sale_5.id,
                            amount=sale_5.commission)
    # check the commission amount is correct
    assert commission_5.amount == 60000

def destroy_testing_database():
    # drop all tables
    Base.metadata.drop_all(test_engine)
    session.close()
    # remove file from directory
    os.remove('test.db')



if __name__ == '__main__':
    print('Running tests...')
    print('Testing office creation')
    test_office_creation()
    print('Test passed (1/9)')
    print('Testing agent creation')
    test_agent_creation()
    print('Test passed (2/9)')
    print('Testing office-agent relation')
    test_office_agent_relation()
    print('Test passed (3/9)')
    print('Testing client creation')
    test_client_creation()
    print('Test passed (4/9)')
    print('Testing house creation')
    test_house_creation()
    print('Test passed (5/9)')
    print('Testing buyer creation')
    test_buyer_creation()
    print('Test passed (6/9)')
    print('Testing sale creation')
    test_sale_creation()
    print('Test passed (7/9)')
    print('Testing commission creation')
    test_commission_creation()
    print('Test passed (8/9)')
    print('Testing commission calculation')
    test_commission_calculation()
    print('Test passed (9/9)')
    print('All tests passed')
    print('Destroying testing database')
    destroy_testing_database()
    print('Testing database destroyed')