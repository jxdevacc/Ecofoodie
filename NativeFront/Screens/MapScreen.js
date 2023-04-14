import * as React from 'react';
import {SafeAreaView, StyleSheet, Text, View, ScrollView } from 'react-native';
// import Map from './Map';
import MapView, {Marker} from 'react-native-maps';
import * as Location from "expo-location";

import tw from "tailwind-react-native-classnames";
import { createStackNavigator } from "@react-navigation/stack"
import NavigateCard from '../Screens/NavigateCard';
import DisplayCard from '../Screens/DisplayCard';
import ListingPage from '../Screens/ListingPage';
import PostInfo from '../Screens/PostInfo';
import MapViewDirections from "react-native-maps-directions";

const GOOGLE_MAPS_APIKEY = 'AIzaSyBEMW7hRF6VRYAImlQV7tJyFQq4tPPUWpE'
console.log(GOOGLE_MAPS_APIKEY);

const wait = (timeout) => {
  return new Promise(resolve => setTimeout(resolve, timeout));
}

let targetCoords = {
    lat: 40.6930447,
    long: -73.9874811,
}

let originCoords = {
    lat: 0,
    long: 0,
}


function MapScreen() {
    const coord = targetCoords;
    const Stack = createStackNavigator();
    const [pin, setPin] = React.useState({
        lat: 40.6930447,
        long: -73.9874811,
    });

//    const [marker, setMarker] = React.useState(null);
//    const markerRef = React.useRef(null);

    React.useEffect(() => {
        (async () => {
            let {status} = await Location.requestForegroundPermissionsAsync();
            console.log("checking status");
            if (status !== "granted"){
                console.log("Permission to access location was denied");
                return;
            }

            let location = await Location.getCurrentPositionAsync({});
            console.log("location: " + location.coords.latitude + location.coords.longitude);

            originCoords.lat = location.coords.latitude;
            originCoords.long = location.coords.longitude;

            setPin({
                lat: targetCoords.lat,
                long: targetCoords.long,
            });
        }) ();
    },[]);

    const moveMarker = () => {
        console.log("setting position: ");
        console.log(pin);
        setPin({
            lat: targetCoords.lat,
            long: targetCoords.long,
        });
        console.log("new coords: " + pin.lat + pin.long);
    };

    React.useEffect(() =>  {
        moveMarker();
    }, [coord]);

    return (
        <View style={{flex:1}}>
            <View style={tw`h-1/2`}>
            <MapView style = {{flex: 1}}
                initialRegion={{
                    latitude: 40.6930396,
                    longitude: -73.9875105,
                    latitudeDelta: 0.0922,
                    longitudeDelta: 0.0421,
                }}
                showsUserLocation={true}
            >

            <MapViewDirections
                origin = {originCoords}
                destination = {pin}
                apiKey = {GOOGLE_MAPS_APIKEY}
                strokeWidth = {3}
                strokeColor = "black"
            />

            <Marker
//                ref={markerRef}
                coordinate = {{
                    latitude: pin.lat,
                    longitude: pin.long,
                    //latitude: 40.6930396,
                    //longitude: -73.9875105,
                }}
                pinColor = "red"
                onPress= {moveMarker}
            />
            </MapView>
            </View>
            <View/>
            <Stack.Navigator>
                <Stack.Screen
                    name="NavigateCard"
                    component={NavigateCard}
                    options={{
                        headerShown: false,
                    }}
                />
                <Stack.Screen
                    name="DisplayCard"
                    component={DisplayCard}
                    options={{
                        headerShown: false,
                    }}
                />
            </Stack.Navigator>
            </View>
        )
    }



{/* </View>
    <View>
        <Text>
            Maps
        </Text>
    </View> */}
{/* }; */}

export const setPin = (lat, long) => {
    targetCoords.long = long;
    targetCoords.lat = lat;
    console.log("target coords: " + targetCoords.long + ", " + targetCoords.lat);
}
export default MapScreen


const styles = StyleSheet.create({

}
)
