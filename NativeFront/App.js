// import React, { Component, Fragment } from 'react';
// import ReactDOM from 'react-dom';
// import { HashRouter as Router, Route, Switch, Redirect } from 'react-router-dom';

// import { Provider as AlertProvider } from 'react-alert';
// import AlertTemplate from 'react-alert-template-basic';

// import Header from './layout/Header';
// import Dashboard from './leads/Dashboard';
// import Alerts from './layout/Alerts';
// import Login from './accounts/Login';
// import Register from './accounts/Register';
// import PrivateRoute from './common/PrivateRoute';

// import { Provider } from 'react-redux';
// import store from '../store';
// import { loadUser } from '../actions/auth';

// Alert Options

import {SafeAreaView, StyleSheet, Text, View, ScrollView } from 'react-native';
import React, {useContext} from "react"
import Contants from 'expo-constants';
import { NavigationContainer } from '@react-navigation/native';
import { createStackNavigator } from '@react-navigation/stack';
import Navigator from './Screens/Navigator';
import { Context, Provider } from "./Screens/globalContext";

// const alertOptions = {
//   timeout: 3000,
//   position: 'top center',
// };

// class App extends Component {
//   componentDidMount() {
//     store.dispatch(loadUser());
//   }


// const myStyles = {
//   title: "Welcome to EcoFoodie!",
//   headerTintColor: "white",
//   headerStyle: {
//     backgroundColor: "purple"
//   }
// }
function App() {

  return (
    <Provider>
    <SafeAreaView style={styles.container}>
      {/* <GooglePlacesInput /> */}
      <NavigationContainer>
        <Navigator />
    </NavigationContainer>
    </SafeAreaView>
    </Provider>
  )



}

export default App;

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: 'white',
    marginTop: Contants.statusBarHeight
  },

  textStyle: {
    fontSize: 25,
  },
});