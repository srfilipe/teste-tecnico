USE [tech_test]
GO

/****** Object:  Table [stg].[sales_data]    Script Date: 21/04/2025 16:53:25 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [stg].[sales_data](
	[Date] [date] NOT NULL,
	[ProductID] [int] NOT NULL,
	[ProductName] [nvarchar](200) NULL,
	[QuantitySold] [int] NULL,
	[Price] [decimal](18, 2) NULL,
	[Category] [nvarchar](100) NULL,
	[CustomerID] [int] NOT NULL,
	[HashID] [char](64) NOT NULL,
	[LoadDate] [datetime2](7) NOT NULL
) ON [PRIMARY]
GO

ALTER TABLE [stg].[sales_data] ADD  DEFAULT (sysutcdatetime()) FOR [LoadDate]
GO

