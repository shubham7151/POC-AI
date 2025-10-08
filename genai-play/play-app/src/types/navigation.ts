import { NavigatorScreenParams } from '@react-navigation/native';

export type RootStackParamList = {
  Main: NavigatorScreenParams<BottomTabParamList>;
  AccountDetail: { accountId: string };
  HoldingDetail: { holdingId: string };
  PLAModal: { opportunityId: string };
};

export type BottomTabParamList = {
  Dashboard: undefined;
  Invest: undefined;
  Learn: undefined;
  Profile: undefined;
};

declare global {
  namespace ReactNavigation {
    interface RootParamList extends RootStackParamList {}
  }
}