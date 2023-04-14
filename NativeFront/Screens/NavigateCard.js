import React, { useContext, useState, useEffect } from 'react'
import { RefreshControl, Alert, FlatList, StyleSheet, Pressable, View, Text, Image, TouchableOpacity, useWindowDimensions, Button, List, ListItem, ScrollView, SafeAreaView } from 'react-native'
import tw from "tailwind-react-native-classnames";
import Logo from '../assets/Images/newlogo.png'
import { TextInput } from 'react-native-paper';
import { Context } from './globalContext';
import { useNavigation } from '@react-navigation/native';
import { setPin } from './MapScreen';
import Geocoder from 'react-native-geocoding';


const Item = ({ item, onPress, backgroundColor, textColor }) => (
  <TouchableOpacity onPress={onPress} style={[styles.item, backgroundColor]}>
    <Text style={[styles.title, textColor]}>{item.header_text}</Text>
    <Text style={[styles.title, textColor]}>{item.body_text}</Text>
    <Text style={[styles.title, textColor]}>{item.city}</Text>
    <Text style={[styles.title, textColor]}>{item.street}</Text>
    <Text style={[styles.title, textColor]}>{item.state}</Text>
    <Text style={[styles.title, textColor]}>{item.country}</Text>
    <Text style={[styles.title, textColor]}>{item.zipcode}</Text>
    <Text style={[styles.title, textColor]}>{item.produceremail}</Text>
  </TouchableOpacity>
);

const wait = (timeout) => {
  return new Promise(resolve => setTimeout(resolve, timeout));
}

function NavigateCard({ route, props }){
  const navigation = useNavigation();
  const {height} = useWindowDimensions()
  const globalContext = useContext(Context)
  const { setIsLoggedIn, domain, userObj, setUserObj} = globalContext;
  const [selectedId, setSelectedId] = useState(null);
  const [producer, setProducer] = useState(false)
  const [listings, setListings] = useState([])
  const [refreshing, setRefreshing] = useState(false);
  Geocoder.init('AIzaSyCqLGPBDseo7DORAv728OqFyiWgGvN1fcQ');

  useEffect(() => {
    fetch(`${domain}/api/auth/posts/`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json'
        },
        })
        .then(res => {
          if (res.ok) {
            return res.json()
          } else {
            throw res.json()
          }
        })
        .then(json => {
            //console.log(json)
            // setListings(json)

            // {json.map(listing => {
            // console.log(listing)
            // })}
            // console.log(json)
            setListings(json)
        })
        .catch(error => {
          console.log(error)
          // console.log(error)
          Alert.alert("An error occured. Unable to gather listings.")
        })
  },[refreshing, listings])
  // console.log("Listings: \n")
  // console.log(listings)
  useEffect(() => {
    fetch(`${domain}/api/auth/producers/${userObj.email}`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json'
      },
      })
      .then(res => {
        if (res.ok) {
          return res.json()
        } else {
          throw res.json()
        }
      })
      .then(json => {
          console.log(json)
          // setListings(json)

          // {json.map(listing => {
          // console.log(listing)
          // })}
          // console.log(json)
          setProducer(true)
      })
      .catch(error => {
      //   console.log('hi')
        console.log(error)
        // Alert.alert("An error occured. Unable to gather producers.")
      })
  },[refreshing, producer])

  const renderItem = ({ item }) => {
    const backgroundColor = item.id === selectedId ? "#6e3b6e" : "#f9c2ff";
    const color = item.id === selectedId ? 'white' : 'black';
    let address = "55 Clark Street";
    return (
      <Item
        item={item}
        onPress={() => {
            setSelectedId(item.id)
            console.log(item)
            address = item.street;
            console.log(address);
            Geocoder.from(address)
            .then(json => {
                var location = json.results[0].geometry.location;
                console.log("new addy: " + location.lat + location.lng);
                setPin(location.lat, location.lng)
            })
            .catch(error => console.warn(error));

        }
        }
        backgroundColor={{ backgroundColor }}
        textColor={{ color }}
      />
    );
  };

  const onRefresh = React.useCallback(() => {
    setRefreshing(true);
    wait(2000).then(() => setRefreshing(false));
  }, []);

  // const RenderArray = () => {
  //   return listings.map(listing => {
  //     console.log(listing.city)
  //     return (
  //       (<View key = {listing.id}>
  //         <Text style={styles.item}>{listing.header_text}</Text>
  //         <Text style={styles.item}>{listing.body_text}</Text>
  //         <Text style={styles.item}>{listing.produceremail}</Text>
  //         <Text style={styles.item}>{listing.date_exp}</Text>
  //         <Text style={styles.item}>{listing.city}{listing.street}{listing.state}{listing.country}{listing.zipcode}</Text>
  //       </View>)
  //     );
  //   })
  // }
  return (
        <SafeAreaView style = {tw`bg-white flex-1`}>
            <Text style = {tw`text-center py-3 text-xl`}> Available Posts </Text>
            <View style = {tw`border-t border-gray-200 flex-shrink`}>
                <View>
                    <ScrollView
                      nestedScrollEnabled={true}
                      refreshControl={
                      <RefreshControl refreshing={refreshing}
                        onRefresh={() => {
                          setRefreshing(true)
                          wait(2000).then(() => setRefreshing(false))
                        }} />
                      }>
                    <View>
                        <Text></Text>
                        <View style = {styles.container}>
                        {/* {console.log("Booooooooooooooooooooo: \n")} */}
                        <FlatList
                        data={listings}
                        renderItem={renderItem}
                        keyExtractor={(item) => item.id}
                        extraData={selectedId}
                        />
                        {/* <RenderArray /> */}
                        </View>
                    </View>
                    </ScrollView>
                </View>
            </View>
        </SafeAreaView>
    )
}

const styles = StyleSheet.create({
    container: {
        padding: 50,
        flex: 1,
      },
      item: {
        padding: 20,
        marginVertical: 8,
        marginHorizontal: 16,
        fontSize: 32,
        // marginTop: 5,
      },
    header : {
        fontWeight : 'bold',
        fontSize : 35,
        marginLeft : 10,
    },
    textbox : {
      height : 200
    },
    subheader : {
        fontWeight : 'bold',
        marginLeft : 10,
        marginBottom : 30,
        color : 'gray'
    },
    inputStyle: {
        backgroundColor: 'white',
        margin : '3%',
        borderColor: '#e8e8e8',
        borderRadius: 5,
        paddingHorizontal: 10,
        marginVertical: 5,
    },
    btn : {
        backgroundColor : '#87CEEB',
        margin : '3%',
        padding: 15,
        marginVertical: 5,
        alignItems: 'center',
        borderRadius: 5,
    },
    altbtn : {
        margin : '3%',
        padding: 15,
        marginVertical: 5,
        alignItems: 'center',
        borderRadius: 5,
    },
    alttxt : {
        color : 'grey',
    },
    txt : {
        color : 'black',
    },
    logo : {
        width : '20%',
        alignSelf : 'flex-start',
        marginTop : -10,
        position : 'absolute'
    }
})

export default NavigateCard