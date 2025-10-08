export interface User {
  id: string;
  name: string;
  email: string;
}

export interface Account {
  id: string;
  type: 'Investment ISA' | 'Lifetime ISA' | 'Pension' | 'General investment';
  accountNumber: string;
  balance: number;
  cashBalance: number;
  currency: string;
}

export interface Transaction {
  id: string;
  type: 'deposit' | 'withdrawal' | 'investment' | 'dividend';
  amount: number;
  date: string;
  description: string;
  balance: number;
}