USE [tech_test]
GO

/****** Object:  Table [dw].[FactSales]    Script Date: 21/04/2025 16:54:12 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [dw].[FactSales](
	[SaleKey] [int] IDENTITY(1,1) NOT NULL,
	[Date] [date] NOT NULL,
	[ProductID] [int] NOT NULL,
	[ProductName] [nvarchar](200) NOT NULL,
	[Category] [nvarchar](100) NOT NULL,
	[CustomerID] [int] NOT NULL,
	[QuantitySold] [int] NOT NULL,
	[Price] [decimal](18, 2) NOT NULL,
	[TotalSales] [decimal](18, 2) NOT NULL,
	[HashID] [char](64) NOT NULL,
	[StartDate] [datetime2](7) NOT NULL,
	[EndDate] [datetime2](7) NULL,
	[IsCurrent] [bit] NOT NULL,
PRIMARY KEY CLUSTERED 
(
	[SaleKey] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO

ALTER TABLE [dw].[FactSales] ADD  DEFAULT ((1)) FOR [IsCurrent]
GO

