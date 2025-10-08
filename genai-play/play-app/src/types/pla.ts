export interface LearningOpportunity {
  id: string;
  type: 'cash_management' | 'portfolio_concentration' | 'market_volatility';
  priority: 'high' | 'medium' | 'low';
  triggerCondition: string;
  title: string;
  description: string;
  content: string;
  personalizedData: Record<string, any>;
  isPreloaded: boolean;
  createdAt: string;
  expiresAt?: string;
}

export interface PLAContext {
  currentScreen: string;
  userBehavior: {
    scrollDepth: number;
    timeOnScreen: number;
    interactions: string[];
  };
  portfolioContext: {
    cashBalance: number;
    concentrationRisk: number;
    recentPerformance: number;
  };
  triggerConditions: string[];
}

export interface PLAState {
  isActive: boolean;
  currentOpportunity: LearningOpportunity | null;
  preloadedOpportunities: LearningOpportunity[];
  context: PLAContext;
  isLoading: boolean;
}