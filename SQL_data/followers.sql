INSERT INTO trucks (name, descrip, yelp_link, web_link, twitter_handle)
VALUES ('Naked Chorizo','Naked Chorizo got its name from translating chorizong hubad literally. Chorizong hubad was a Spanish chorizo brought by the Spaniards to the Philippines.' ,'https://www.yelp.com/biz/naked-chorizo-san-francisco', 'http://www.nakedchorizo.com/', 'https://twitter.com/NakedChorizo1' ),
('BOBCHA','Korean Food at its best','https://www.yelp.com/biz/bobcha-south-san-francisco', 'http://www.bobchasf.com/', 'https://twitter.com/bobchasf' ),
('HuLa Truck', 'Pacific Island Flavor with a NorCal Twist', 'https://www.yelp.com/biz/hula-truck-santa-clara','http://www.hulatruck408.com/','https://twitter.com/hulatruck408'),
('El Gondo','Mexican Food Invasion', 'https://www.yelp.com/biz/tacos-el-gondo-south-san-francisco','http://www.tacoselgondo.menu/','https://twitter.com/elgondo'),
('Anzu to You','Hotel Nikkos food truck is out and about in San Francisco','https://www.yelp.com/biz/anzu-to-you-san-francisco','http://www.hotelnikkosf.com/anzu-to-you.aspx','http://twitter.com/HotelNikkoSF'),
('Drums & Crumbs','Serving authentic southern cuisine to the North Bay and San Francisco','https://www.yelp.com/biz/drums-and-crumbs-san-francisco','http://drumsandcrumbs.com/','http://twitter.com/drumsandcrumbs'),
('Cheese Gone Wild','Gourmet mobile food truck specializing in 1/3 lb gourmet burgers, grilled cheese melts, fresh salads and soups','https://www.yelp.com/biz/cheese-gone-wild-south-san-francisco','http://www.cheesegonewild.com/','https://twitter.com/CheeseGoneWild'),
('Lobsta Truck','Bread fresh from New England make our lobster and crab rolls authentic and ready to roll.','https://www.yelp.com/biz/lobsta-truck-san-francisco','http://sf.lobstatruck.com/','http://www.twitter.com/LobstaTruckSF'),
('The Boneyard','Inspired by SF Bay Areas best backyard barbecues and the urge to feast together.','https://www.yelp.com/biz/the-boneyard-san-francisco','http://www.theboneyardtruck.com/','https://twitter.com/BoneyardTruck'),
('The Scotch Bonnet Food Truck','Providing popular and traditional Jamaican food to the masses.','https://www.yelp.com/biz/scotch-bonnet-food-truck-oakland','http://www.scotchbonnet.us/','https://twitter.com/ScotchBonnet510');

INSERT INTO food_categories (cat_id, name)
VALUES ('MEXI','Mexican'),
('KORE','Korean'),
('JAMA','Jamaican'),
('BBQS','BBQ'),
('SOTH','Southern'),
('AMER','American'),
('HAWI','Hawaiian'),
('SEAF','Seafood'),
('FILI','Filipino'),
('SPAN','Spanish'),
('CHIN','Chinese');

INSERT INTO users(email, password, fname, lname, phone, zipcode)
VALUES ('candy@candy.com','candy','Candy','Cane','5105558888', '94501'),
('joe@joe.com','candy','Joe','Cane','5105559999', '94501');


INSERT INTO locations (street_address, city, state, zipcode, longitude, lattitude)
VALUES('491 Bayshore Blvd', 'San Francisco', 'CA', '94124', -122.4061328, 37.7402754),
('23rd St & Treat Ave', 'San Francisco', 'CA', '94124', -122.41312, 37.75417),
('410 Mina Street', 'San Francisco', 'CA', '94103', -122.4062208, 37.78210449);


INSERT INTO schedules (truck_id, location_id, day, start_time, end_time)
VALUES(1,1,'2016-05-12','08:00:00', '16:00:00'),
(1,3,'2016-05-17','08:00:00', '16:00:00'),
(2,3,'2016-05-17','08:00:00', '16:00:00'),
(2,1,'2016-05-13','08:00:00', '16:00:00'),
(3,2,'2016-05-16','08:00:00', '12:00:00'),
(3,3,'2016-05-17','08:00:00', '14:00:00');



INSERT INTO trucks_foods (truck_id,cat_id)
VALUES (1,'SPAN'),
(1,'FILI'),
(2,'KORE'),
(3,'HAWI'),
(4,'MEXI'),
(5,'AMER'),
(6,'AMER'),
(6,'SOTH'),
(7,'AMER'),
(8,'AMER'),
(8,'SEAF'),
(9,'BBQS'),
(9,'AMER'),
(10,'JAMA');


