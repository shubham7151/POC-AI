export interface Holding {
  id: string;
  symbol: string;
  name: string;
  quantity: number;
  currentPrice: number;
  totalValue: number;
  sector: string;
  percentageOfPortfolio: number;
}

export interface Portfolio {
  accountId: string;
  totalValue: number;
  totalCash: number;
  holdings: Holding[];
  lastUpdated: string;
  performance: {
    daily: number;
    weekly: number;
    monthly: number;
    yearly: number;
  };
}