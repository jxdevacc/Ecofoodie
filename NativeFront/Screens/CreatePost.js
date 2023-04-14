// import React, {useState} from 'react'
// import {StyleSheet, Text, View, Image, useWindowDimensions, Pressable, Alert} from 'react-native';
// import {TextInput, Button} from 'react-native-paper'
import Logo from '../assets/Images/newlogo.png'
import React, { useContext, useState } from 'react';
import { Alert, StyleSheet, Pressable, View, Text, Image, TouchableOpacity, useWindowDimensions, ScrollView } from 'react-native';
import { TextInput, Checkbox } from 'react-native-paper';
import { Context } from './globalContext';
// import ImagePicker from 'react-native-image-crop-picker';

// import storage from '@react-native-firebase/storage';
// import firestore from '@react-native-firebase/firestore';

function CreatePost({ navigation, route, props }){
    const {height} = useWindowDimensions()
  const globalContext = useContext(Context)
  const { setIsLoggedIn, domain, userObj, setUserObj} = globalContext;
  const [checked, setChecked] = useState(false)
  const [header_text, setHeader] = useState('')
  const [body_text, setBody] = useState('')
  const [city, setCity] = useState('')
  const [street, setStreet] = useState('')
  const [state, setState] = useState('')
  const [country, setCountry] = useState('')
  const [zipcode, setZip] = useState('')
  const [error, setError] = useState("")
  // const [image, setImage] = useState(null)
  // const [uploading, setUploading] = useState(false);
  // const [transferred, setTransferred] = useState(0);
  // const [post, setPost] = useState(null);

  // const takePhotoFromCamera = () => {
  //   ImagePicker.openCamera({
  //     width: 1200,
  //     height: 780,
  //     cropping: true,
  //   }).then((image) => {
  //     console.log(image);
  //     const imageUri = Platform.OS === 'ios' ? image.sourceURL : image.path;
  //     setImage(imageUri);
  //   });
  // };

  // const choosePhotoFromLibrary = () => {
  //   ImagePicker.openPicker({
  //     width: 1200,
  //     height: 780,
  //     cropping: true,
  //   }).then((image) => {
  //     console.log(image);
  //     const imageUri = Platform.OS === 'ios' ? image.sourceURL : image.path;
  //     setImage(imageUri);
  //   });
  // };

  // const submitPost = async () => {
  //   const imageUrl = await uploadImage();
  //   console.log('Image Url: ', imageUrl);
  //   console.log('Post: ', post);

  //   firestore()
  //   .collection('posts')
  //   .add({
  //     userId: user.uid,
  //     post: post,
  //     postImg: imageUrl,
  //     postTime: firestore.Timestamp.fromDate(new Date()),
  //     likes: null,
  //     comments: null,
  //   })
  //   .then(() => {
  //     console.log('Post Added!');
  //     Alert.alert(
  //       'Post published!',
  //       'Your post has been published Successfully!',
  //     );
  //     setPost(null);
  //   })
  //   .catch((error) => {
  //     console.log('Something went wrong with added post to firestore.', error);
  //   });
  // }

  // const uploadImage = async () => {
  //   if( image == null ) {
  //     return null;
  //   }
  //   const uploadUri = image;
  //   let filename = uploadUri.substring(uploadUri.lastIndexOf('/') + 1);

  //   // Add timestamp to File Name
  //   const extension = filename.split('.').pop(); 
  //   const name = filename.split('.').slice(0, -1).join('.');
  //   filename = name + Date.now() + '.' + extension;

  //   setUploading(true);
  //   setTransferred(0);

  //   const storageRef = storage().ref(`photos/${filename}`);
  //   const task = storageRef.putFile(uploadUri);

  //   // Set transferred state
  //   task.on('state_changed', (taskSnapshot) => {
  //     console.log(
  //       `${taskSnapshot.bytesTransferred} transferred out of ${taskSnapshot.totalBytes}`,
  //     );

  //     setTransferred(
  //       Math.round(taskSnapshot.bytesTransferred / taskSnapshot.totalBytes) *
  //         100,
  //     );
  //   });

  //   try {
  //     await task;

  //     const url = await storageRef.getDownloadURL();

  //     setUploading(false);
  //     setImage(null);

  //     // Alert.alert(
  //     //   'Image uploaded!',
  //     //   'Your image has been uploaded to the Firebase Cloud Storage Successfully!',
  //     // );
  //     return url;

  //   } catch (e) {
  //     console.log(e);
  //     return null;
  //   }

  // };

  function handleLogin() {
    const date = new Date();
    date.setHours(date.getHours() +2);
    console.log('DATEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE')
    console.log(date)
    console.log(date.getTime())
    console.log(date.getFullYear())
    console.log(date.getMonth())
    console.log(date.getDate())
    console.log(date.getHours())
    console.log(date.getMinutes())
    console.log(date.getSeconds())
    console.log(date.getMilliseconds())
    // console.log(date);
    // console.log(header_text);
    // console.log(body_text);
    // console.log(userObj.email);
    // console.log(city);
    // console.log(street);
    // console.log(state);
    // console.log(zipcode);
    // console.log(country);
    setError("")
    console.log(checked)
    let body = JSON.stringify({
      'header_text': header_text,
      'body_text': body_text,
      'produceremail': userObj.email,
      //make a field called refrigerated if refrigerated
      'date_exp': date, //current date plus 2 hours would actually be custom based on what food it is
      'city': city,
      'street': street,
      'state': state,
      'country': country,
      'zipcode': zipcode,
      'group_directed': checked,
    })

    fetch(`${domain}/api/auth/posts/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body:body
      })
      .then(res => {
        if (res.ok) {
          return res.json()
        } else {
          throw res.json()
        }
      })
      .then(json => {
        Alert.alert("Post Created!")
        navigation.navigate("ListingPage")
      })
      .catch(error => {
        console.log(error)
        Alert.alert("An error occured. Unable to make post.")
      })

  }
  return (
    <View>
    <ScrollView>
    <View>
        <Text style = {styles.header}>
            Create Your Listing!
        </Text>
        <TextInput style = {styles.inputStyle}
            label = "Title"
            value = {header_text}
            onChangeText={text => setHeader(text)}
        />
        <TextInput style = {[styles.inputStyle, styles.textbox]}
            label = "Description"
            value = {body_text}
            multiline = {true}
            onChangeText={text => setBody(text)}
        />
        <TextInput style = {styles.inputStyle}
            label = "City"
            value = {city}
            onChangeText={text => setCity(text)}
        />
        <TextInput style = {styles.inputStyle}
            label = "State"
            value = {state}
            onChangeText={text => setState(text)}
        />
        <TextInput style = {styles.inputStyle}
            label = "Street"
            value = {street}
            onChangeText={text => setStreet(text)}
        />
        <TextInput style = {styles.inputStyle}
            label = "Country"
            value = {country}
            onChangeText={text => setCountry(text)}
        />
        <TextInput style = {styles.inputStyle}
        label = "Zip Code"
        value = {zipcode}
        onChangeText={text => setZip(text)}
        />
        {/* <View style={{flexDirection: 'row'}}>
        <Text>Make Group Private?</Text>
        <Checkbox
        status ={checked ? 'checked' : 'unchecked'}
        onPress={()=>setChecked(!checked)}/>
        </View> */}
        <Text> Please take photos of the food</Text> 

        {/* link to camera and take images and store them in firebase */}
    </View>
    <Pressable style = {styles.btn} onPress = {() => handleLogin()}>
    <Text style = {styles.txt}>
        Post
    </Text>
    </Pressable>
    <Pressable style = {styles.altbtn} onPress = {() => navigation.navigate("ListingPage")}>
    <Text style = {styles.alttxt}>
        I changed my mind
        <Text style = {{color: 'blue'}}> Go back</Text>
    </Text>
    </Pressable>
    </ScrollView>
    </View>
  )

}

const styles = StyleSheet.create({
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
export default CreatePost
