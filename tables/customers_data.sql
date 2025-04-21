USE [tech_test]
GO

/****** Object:  Table [stg].[customers_data]    Script Date: 21/04/2025 16:53:39 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [stg].[customers_data](
	[CustomerID] [int] NULL,
	[CustomerName] [varchar](64) NULL,
	[CustomerEmail] [varchar](64) NULL,
	[CustomerLocation] [varchar](64) NULL,
	[HashID] [varchar](64) NULL
) ON [PRIMARY]
GO

