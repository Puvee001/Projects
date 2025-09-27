USE [dbIceCreamShop]
GO

INSERT INTO [dbo].[tblIceCream_Flavours]
           ([Flavour_Name],[Price])
     VALUES
           		('Chocolate', 38),
				('Vanila', 28),
				('Strawberry', 35),
				('Banana', 37),
				('Rasberry', 165),
				('Mango', 63),
				('Moon Mist', 190),
				('Tutti Frutti', 38),
				('Watermelon', 40),
				('Blue Berry', 121),
				('Passion Fruit', 132),
				('Biscuf', 187),
				('Blue moon', 122),
				('Butterscotch', 85),
				('Bubblegum', 81),
				('Choco chip', 137),
				('Choco chip Cookie dough', 199),
				('Cookies and cream', 175),
				('Cotton Candy', 168),
				('Leche', 166),
				('Mint', 113),
				('Mint Choco chip', 101),
				('Pistachio', 164),
				('Rose', 182),
				('Coconut', 43)

SELECT * FROM [dbo].[tblIceCream_Flavours]